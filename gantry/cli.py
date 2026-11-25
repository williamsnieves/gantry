from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except Exception:
    yaml = None

from gantry import detect

VERSION = "1.0.0"
START = "<!-- GANTRY:START -->"
END = "<!-- GANTRY:END -->"
# Markers written by installs made before the rename. They are still recognised
# so an existing block is replaced or removed instead of duplicated.
LEGACY_MARKERS = (("<!-- LOOP-ENGINEERING-HARNESS:START -->", "<!-- LOOP-ENGINEERING-HARNESS:END -->"),)
RUNTIMES = ("claude", "codex", "cursor", "opencode", "omp")
ALIASES = {
    "claude-code": "claude",
    "oh-my-pi": "omp",
    "ohmypi": "omp",
    "open-code": "opencode",
}
SCOPES = ("fullstack", "backend", "frontend", "architecture", "infrastructure", "mixed")
PROFILES = ("lean", "standard", "strict")

# Skills live once in distribution/shared and are rendered at install time. The
# shared catalogue gets compact descriptions: specialist agents read a skill by
# explicit path when a change needs it, so nothing competes for implicit
# discovery or sits in context unused. A runtime with native skill discovery
# receives only the entry-point skills, with their full description.
ENTRYPOINT_SKILLS = ("harness-start", "harness-run", "harness-onboard", "harness-evaluate")
COMPACT_DESCRIPTION = (
    "Portable engineering capability `{name}`. Use when the harness or a "
    "specialist agent explicitly requires this named capability."
)
NATIVE_SKILL_DIRS = {"claude": ".claude/skills"}

# What `gantry inspect` found in the project: its stack and the commands that check it.
PROJECT_FILE = ".harness/project.yaml"

# Runtimes whose command hooks the harness can register. The guard denies agent
# edits to harness files and quality configuration, and pull-request creation
# before the Final Pre-PR Gate passes. See distribution/core/.harness/bin/hook.py.
HOOK_MARKER = ".harness/bin/hook.py"
HOOK_SETTINGS = {"claude": ".claude/settings.json"}
# Runtimes whose specialists write their own report, which only a hook can confine to that file.
AGENT_DIRS = {"claude": ".claude/agents"}
HOOK_MATCHERS = ("Edit|Write|MultiEdit|NotebookEdit", "Bash")
HOOK_DISCLOSURE = """Hooks registered in {path} (skip with --no-hooks):
  - deny agent edits to harness files and to routing state written by route.py
  - deny agent edits to existing lint, type, test and CI configuration (not in the lean profile)
  - deny `gh pr create` until `route.py ready` passes, and commands using --no-verify (not in the lean profile)
  They apply to the agent only; you can still make these changes yourself."""

def package_root() -> Path:
    return Path(__file__).resolve().parents[1]

def distribution_root() -> Path:
    return package_root() / "distribution"

def template_root() -> Path:
    return package_root() / "templates"

def normalize_runtime(value: str) -> str:
    v = value.strip().lower()
    return ALIASES.get(v, v)

def parse_runtimes(raw: str) -> list[str]:
    if not raw:
        return []
    vals = [normalize_runtime(v) for v in raw.split(",") if v.strip()]
    if "all" in vals:
        vals = list(RUNTIMES)
    bad = [v for v in vals if v not in RUNTIMES]
    if bad:
        raise SystemExit(f"Unsupported runtime(s): {', '.join(bad)}")
    # stable de-dupe
    out = []
    for v in vals:
        if v not in out:
            out.append(v)
    return out

def ensure_project(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    if not p.exists() or not p.is_dir():
        raise SystemExit(f"Project directory does not exist: {p}")
    return p

def iter_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.is_file():
            yield p

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def state_path(project: Path) -> Path:
    return project / ".harness/install-state.json"

def load_state(project: Path) -> dict:
    p = state_path(project)
    if not p.exists():
        return {
            "harness_version": None,
            "runtimes": [],
            "managed_files": {},
            "shared_installed": False,
        }
    return json.loads(p.read_text(encoding="utf-8"))

def save_state(project: Path, state: dict) -> None:
    p = state_path(project)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def rel(project: Path, path: Path) -> str:
    return path.relative_to(project).as_posix()

def render_skill(text: str, name: str, *, compact: bool) -> str:
    """Return SKILL.md text, swapping the frontmatter description when compact."""
    if not compact or name in ENTRYPOINT_SKILLS:
        return text
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise SystemExit(f"Skill {name} has no frontmatter; cannot render it.")
    frontmatter, body = text[4:].split("\n---\n", 1)
    out, skipping, replaced = [], False, False
    for line in frontmatter.split("\n"):
        if line.startswith("description:"):
            out.append("description: " + COMPACT_DESCRIPTION.format(name=name))
            skipping, replaced = True, True
            continue
        if skipping and (line.startswith((" ", "\t")) or line == ""):
            continue
        skipping = False
        out.append(line)
    if not replaced:
        raise SystemExit(f"Skill {name} has no description; cannot render it.")
    return "---\n" + "\n".join(out) + "\n---\n" + body

def managed_copy(src: Path, dst: Path, project: Path, state: dict, *, force: bool, dry_run: bool, label: str, content: str | None = None):
    key = rel(project, dst)
    managed = state["managed_files"].get(key)

    if dst.exists():
        if managed:
            current_hash = sha256(dst)
            previous_hash = managed.get("sha256")
            if current_hash != previous_hash and not force:
                raise SystemExit(
                    f"Refusing to overwrite locally modified harness file: {dst}\n"
                    f"Use --force only after reviewing the local changes."
                )
        elif not force:
            raise SystemExit(
                f"Refusing to overwrite existing unmanaged file: {dst}\n"
                f"Use --force only if the harness should own this path."
            )

    state.setdefault("_written", set()).add(key)
    print(f"{'[DRY-RUN] ' if dry_run else ''}install {label}: {key}")
    if dry_run:
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    if content is None:
        shutil.copy2(src, dst)
    else:
        dst.write_text(content, encoding="utf-8")
    state["managed_files"][key] = {
        "sha256": sha256(dst),
        "owner": label,
    }

def managed_tree(src_root: Path, dst_root: Path, project: Path, state: dict, *, force: bool, dry_run: bool, label: str):
    for src in iter_files(src_root):
        target = dst_root / src.relative_to(src_root)
        managed_copy(src, target, project, state, force=force, dry_run=dry_run, label=label)

def skills_root() -> Path:
    return distribution_root() / "shared/skills/.agents/skills"

def install_skills(dst_root: Path, project: Path, state: dict, *, compact: bool, force: bool, dry_run: bool, label: str, only: tuple[str, ...] | None = None):
    src_root = skills_root()
    for src in iter_files(src_root):
        relative = src.relative_to(src_root)
        if only is not None and relative.parts[0] not in only:
            continue
        content = None
        if len(relative.parts) == 2 and relative.name == "SKILL.md":
            content = render_skill(src.read_text(encoding="utf-8"), relative.parts[0], compact=compact)
        managed_copy(src, dst_root / relative, project, state, force=force, dry_run=dry_run, label=label, content=content)

def find_block_markers(text: str) -> tuple[str, str] | None:
    for start, end in ((START, END), *LEGACY_MARKERS):
        if start in text and end in text:
            return start, end
    return None

def hook_command(runtime: str) -> str:
    return f'python3 "$CLAUDE_PROJECT_DIR/{HOOK_MARKER}" {runtime}'

def without_harness_hooks(settings: dict) -> dict:
    """Drop the harness's own PreToolUse entries, leaving everything else untouched."""
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict) or not isinstance(hooks.get("PreToolUse"), list):
        return settings
    kept = []
    for entry in hooks["PreToolUse"]:
        commands = [h for h in (entry.get("hooks") or []) if HOOK_MARKER not in str(h.get("command", ""))] if isinstance(entry, dict) else None
        if commands is None:
            kept.append(entry)
        elif commands:
            kept.append({**entry, "hooks": commands})
    if kept:
        hooks["PreToolUse"] = kept
    else:
        del hooks["PreToolUse"]
    if not hooks:
        del settings["hooks"]
    return settings

def load_settings(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Cannot register hooks: {path} is not valid JSON ({exc}). Fix it or install with --no-hooks.")
    if not isinstance(data, dict):
        raise SystemExit(f"Cannot register hooks: {path} is not a JSON object. Fix it or install with --no-hooks.")
    return data

def write_settings(path: Path, settings: dict, *, dry_run: bool, verb: str):
    print(f"{'[DRY-RUN] ' if dry_run else ''}{verb} hooks: {path.name}")
    if dry_run:
        return
    if settings:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    elif path.exists():
        path.unlink()

def install_hooks(runtime: str, project: Path, *, dry_run: bool):
    path = project / HOOK_SETTINGS[runtime]
    before = load_settings(path)
    settings = without_harness_hooks(json.loads(json.dumps(before)))
    entries = settings.setdefault("hooks", {}).setdefault("PreToolUse", [])
    for matcher in HOOK_MATCHERS:
        entries.append({"matcher": matcher, "hooks": [{"type": "command", "command": hook_command(runtime)}]})
    if settings != before:
        write_settings(path, settings, dry_run=dry_run, verb="register")
    print(HOOK_DISCLOSURE.format(path=HOOK_SETTINGS[runtime]))

def remove_hooks(runtime: str, project: Path, *, dry_run: bool):
    path = project / HOOK_SETTINGS[runtime]
    if not path.exists():
        return
    try:
        before = load_settings(path)
    except SystemExit:
        print(f"skip unreadable settings file: {HOOK_SETTINGS[runtime]}")
        return
    settings = without_harness_hooks(json.loads(json.dumps(before)))
    if settings != before:
        write_settings(path, settings, dry_run=dry_run, verb="remove")

def merge_agents_block(project: Path, *, dry_run: bool):
    block = (template_root() / "AGENTS.block.md").read_text(encoding="utf-8").strip()
    path = project / "AGENTS.md"
    old = path.read_text(encoding="utf-8") if path.exists() else ""

    markers = find_block_markers(old)
    if markers:
        pattern = re.compile(re.escape(markers[0]) + r".*?" + re.escape(markers[1]), re.S)
        new = pattern.sub(lambda _: block, old)
    else:
        new = old.rstrip() + ("\n\n" if old.strip() else "") + block + "\n"

    if new == old:
        return
    print(f"{'[DRY-RUN] ' if dry_run else ''}merge managed block: AGENTS.md")
    if not dry_run:
        path.write_text(new, encoding="utf-8")

def remove_agents_block(project: Path, *, dry_run: bool):
    path = project / "AGENTS.md"
    if not path.exists():
        return
    old = path.read_text(encoding="utf-8")
    markers = find_block_markers(old)
    if not markers:
        return
    pattern = re.compile(r"\n?" + re.escape(markers[0]) + r".*?" + re.escape(markers[1]) + r"\n?", re.S)
    new = pattern.sub("\n", old).strip()
    if new:
        new += "\n"
    print(f"{'[DRY-RUN] ' if dry_run else ''}remove managed block: AGENTS.md")
    if not dry_run:
        if new:
            path.write_text(new, encoding="utf-8")
        else:
            path.unlink()

def write_harness_config(project: Path, runtimes: list[str], scope: str, profile: str, *, dry_run: bool):
    config_path = project / ".harness/harness.config.yaml"
    config = {
        "harness_version": VERSION,
        "project": {
            "scope_profile": scope,
            "delivery_profile": profile,
        },
        "routing": {
            "scope_profile_is_advisory": True,
            "risk_triggers_override_scope_profile": True,
            "dynamic_routing": True,
        },
        "execution": {
            "default_review_mode": "parallel_when_safe",
            "review_agents_read_only": True,
            "stable_snapshot_per_wave": True,
            "minimal_rereview": True,
        },
        "pre_pr": {
            "enabled": True,
            "allow_pass_with_conditions": True,
        },
        "installed_runtimes": runtimes,
    }
    text = (
        yaml.safe_dump(config, sort_keys=False, allow_unicode=True)
        if yaml else
        json.dumps(config, indent=2)
    )
    print(f"{'[DRY-RUN] ' if dry_run else ''}write: .harness/harness.config.yaml")
    if not dry_run:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(text, encoding="utf-8")

def install_shared(project: Path, state: dict, *, force: bool, dry_run: bool):
    droot = distribution_root()
    managed_tree(
        droot / "core/.harness",
        project / ".harness",
        project, state,
        force=force, dry_run=dry_run, label="shared-core",
    )
    install_skills(
        project / ".agents/skills", project, state,
        compact=True, force=force, dry_run=dry_run, label="shared-skills",
    )
    merge_agents_block(project, dry_run=dry_run)
    if not dry_run:
        state["shared_installed"] = True

def read_only_agent(text: str) -> str:
    """Agent definition without write access, for installs where no hook limits what it may write."""
    text = re.sub(r"^(tools: .*?), Write$", r"\1", text, count=1, flags=re.M)
    return re.sub(r"^permissionMode: acceptEdits$", "permissionMode: plan", text, count=1, flags=re.M)

def install_runtime(runtime: str, project: Path, state: dict, *, force: bool, dry_run: bool, hooks: bool = True):
    overlay = distribution_root() / "runtimes" / runtime
    agents_dir = overlay / AGENT_DIRS[runtime] if runtime in AGENT_DIRS else None
    for src in iter_files(overlay):
        content = None
        if not hooks and agents_dir and src.parent == agents_dir:
            content = read_only_agent(src.read_text(encoding="utf-8"))
        managed_copy(src, project / src.relative_to(overlay), project, state,
                     force=force, dry_run=dry_run, label=f"runtime:{runtime}", content=content)
    if runtime in NATIVE_SKILL_DIRS:
        install_skills(
            project / NATIVE_SKILL_DIRS[runtime], project, state,
            compact=False, force=force, dry_run=dry_run, label=f"runtime:{runtime}", only=ENTRYPOINT_SKILLS,
        )
    if runtime in HOOK_SETTINGS:
        if hooks:
            install_hooks(runtime, project, dry_run=dry_run)
        else:
            remove_hooks(runtime, project, dry_run=dry_run)
    if not dry_run and runtime not in state["runtimes"]:
        state["runtimes"].append(runtime)

def prune_stale(project: Path, state: dict, runtimes: list[str], *, force: bool, dry_run: bool):
    """Remove files an earlier version installed that this version no longer ships."""
    written = state.pop("_written", set())
    owners = {"shared-core", "shared-skills", *(f"runtime:{r}" for r in runtimes)}
    for key, meta in list(state["managed_files"].items()):
        if meta.get("owner") in owners and key not in written:
            if remove_managed_file(project, key, meta, force=force, dry_run=dry_run) and not dry_run:
                state["managed_files"].pop(key, None)

def cmd_install(args):
    project = ensure_project(args.project)
    runtimes = parse_runtimes(args.runtime)
    if not runtimes:
        raise SystemExit("Select at least one runtime with --runtime.")

    state = load_state(project)
    state.setdefault("managed_files", {})
    state.setdefault("runtimes", [])

    install_shared(project, state, force=args.force, dry_run=args.dry_run)
    for runtime in runtimes:
        install_runtime(runtime, project, state, force=args.force, dry_run=args.dry_run, hooks=not args.no_hooks)

    prune_stale(project, state, runtimes, force=args.force, dry_run=args.dry_run)

    final_runtimes = sorted(set(state["runtimes"]) | set(runtimes), key=RUNTIMES.index)
    write_harness_config(
        project, final_runtimes, args.scope, args.profile, dry_run=args.dry_run
    )

    description = detect.detect(project)
    described = project / PROJECT_FILE
    if described.exists():
        print(f"keep: {PROJECT_FILE} (refresh with `gantry inspect --write`)")
    else:
        print(f"{'[DRY-RUN] ' if args.dry_run else ''}write: {PROJECT_FILE}")
        if not args.dry_run:
            described.write_text(detect.render(description), encoding="utf-8")

    if not args.dry_run:
        state["harness_version"] = VERSION
        state["runtimes"] = final_runtimes
        save_state(project, state)

    print()
    print("\n".join(detect.summary(description)))
    print()
    print("Installed runtimes:", ", ".join(final_runtimes))
    print_entrypoints(final_runtimes)


def cmd_inspect(args):
    project = ensure_project(args.project)
    description = detect.detect(project)
    if args.json:
        print(json.dumps(description, indent=2))
    else:
        print("\n".join(detect.summary(description)))
    if args.write:
        if not (project / ".harness").is_dir():
            raise SystemExit("The harness is not installed in this project; run `gantry install` first.")
        (project / PROJECT_FILE).write_text(detect.render(description), encoding="utf-8")
        print(f"write: {PROJECT_FILE}")

def print_entrypoints(runtimes):
    prefix = {"codex": "$"}
    print("Commands:")
    for r in runtimes:
        mark = prefix.get(r, "/")
        print(f"  {r:8} -> {mark}harness-onboard once, then {mark}harness-start for each piece of work ({mark}harness-run reviews it)")

def cmd_plan(args):
    args.dry_run = True
    cmd_install(args)

def cmd_status(args):
    project = ensure_project(args.project)
    state = load_state(project)
    print(f"Harness version: {state.get('harness_version') or 'not installed'}")
    print("Installed runtimes:", ", ".join(state.get("runtimes") or []) or "none")
    print("Managed files:", len(state.get("managed_files") or {}))
    cfg = project / ".harness/harness.config.yaml"
    if cfg.exists():
        print("Config:", cfg)
    if state.get("runtimes"):
        print_entrypoints(state["runtimes"])

def cmd_doctor(args):
    project = ensure_project(args.project)
    state = load_state(project)
    errors = []
    warnings = []

    if not state.get("harness_version"):
        errors.append("Harness install state is missing.")

    # Check managed files still exist and hashes match.
    for key, meta in (state.get("managed_files") or {}).items():
        p = project / key
        if not p.exists():
            errors.append(f"Missing managed file: {key}")
            continue
        if sha256(p) != meta.get("sha256"):
            warnings.append(f"Locally modified managed file: {key}")

    # Core invariants.
    required = [
        ".harness/core/routing/ROUTING-POLICY.md",
        ".harness/bin/route.py",
        ".harness/bin/hook.py",
        ".harness/core/pre-pr/FINAL-PRE-PR-GATE.md",
        ".harness/agents/reviewer/AGENT.md",
        ".harness/evals/end-to-end/E2E-ORACLE.md",
        ".agents/skills/harness-run/SKILL.md",
    ]
    for key in required:
        if not (project / key).exists():
            errors.append(f"Missing core artifact: {key}")

    runtime_checks = {
        "claude": [".claude/agents/reviewer.md", ".claude/skills/harness-run/SKILL.md"],
        "codex": [".codex/agents/reviewer.toml"],
        "cursor": [".cursor/agents/reviewer.md", ".cursor/rules/00-portable-harness.mdc"],
        "opencode": [".opencode/agents/reviewer.md", ".opencode/commands/harness-run.md"],
        "omp": [".omp/agents/reviewer.md", ".omp/commands/harness-run.md", ".omp/RULES.md"],
    }
    for runtime in state.get("runtimes") or []:
        for key in runtime_checks[runtime]:
            if not (project / key).exists():
                errors.append(f"{runtime}: missing {key}")

    for runtime in state.get("runtimes") or []:
        if runtime in HOOK_SETTINGS:
            settings_file = project / HOOK_SETTINGS[runtime]
            registered = settings_file.exists() and HOOK_MARKER in settings_file.read_text(encoding="utf-8")
            if not registered:
                warnings.append(f"{runtime}: guard hooks are not registered in {HOOK_SETTINGS[runtime]}; gates are advisory only.")

    agents_md = (project / "AGENTS.md").read_text(encoding="utf-8") if (project / "AGENTS.md").exists() else ""
    if START not in agents_md:
        if find_block_markers(agents_md):
            warnings.append("AGENTS.md still has the pre-rename harness block; run `gantry install` to update it.")
        else:
            warnings.append("Managed AGENTS.md harness block is missing.")

    if errors:
        print("DOCTOR: FAIL")
    elif warnings:
        print("DOCTOR: PASS WITH WARNINGS")
    else:
        print("DOCTOR: PASS")

    for e in errors:
        print("ERROR:", e)
    for w in warnings:
        print("WARN :", w)
    raise SystemExit(1 if errors else 0)

def remove_managed_file(project: Path, key: str, meta: dict, *, force: bool, dry_run: bool):
    p = project / key
    if not p.exists():
        return True
    current = sha256(p)
    if current != meta.get("sha256") and not force:
        print(f"skip locally modified file: {key}")
        return False
    print(f"{'[DRY-RUN] ' if dry_run else ''}remove: {key}")
    if not dry_run:
        p.unlink()
        # clean empty dirs upward but never remove project root
        parent = p.parent
        while parent != project and parent.exists():
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent
    return True

def cmd_uninstall(args):
    project = ensure_project(args.project)
    state = load_state(project)
    installed = list(state.get("runtimes") or [])
    if not installed and not state.get("shared_installed"):
        print("Harness is not installed.")
        return

    runtimes = parse_runtimes(args.runtime) if args.runtime else installed
    if args.runtime and "all" in args.runtime.lower():
        runtimes = installed

    managed = dict(state.get("managed_files") or {})
    remove_keys = []
    for key, meta in managed.items():
        owner = meta.get("owner", "")
        if owner.startswith("runtime:") and owner.split(":", 1)[1] in runtimes:
            remove_keys.append(key)

    for key in remove_keys:
        if remove_managed_file(project, key, managed[key], force=args.force, dry_run=args.dry_run):
            if not args.dry_run:
                state["managed_files"].pop(key, None)

    for runtime in runtimes:
        if runtime in HOOK_SETTINGS:
            remove_hooks(runtime, project, dry_run=args.dry_run)

    remaining = [r for r in installed if r not in runtimes]

    if args.purge_shared and not remaining:
        for key, meta in list(state.get("managed_files", {}).items()):
            if meta.get("owner", "").startswith("shared-"):
                if remove_managed_file(project, key, meta, force=args.force, dry_run=args.dry_run):
                    if not args.dry_run:
                        state["managed_files"].pop(key, None)
        remove_agents_block(project, dry_run=args.dry_run)
        if not args.dry_run:
            state["shared_installed"] = False

    if not args.dry_run:
        state["runtimes"] = remaining
        if remaining:
            save_state(project, state)
            # Update config with existing scope/profile when possible.
            cfg = project / ".harness/harness.config.yaml"
            scope, profile = "mixed", "standard"
            if cfg.exists() and yaml:
                try:
                    data = yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}
                    scope = data.get("project", {}).get("scope_profile", scope)
                    profile = data.get("project", {}).get("delivery_profile", profile)
                except Exception:
                    pass
            write_harness_config(project, remaining, scope, profile, dry_run=False)
            save_state(project, state)
        elif args.purge_shared:
            sp = state_path(project)
            if sp.exists():
                sp.unlink()
            if (project / PROJECT_FILE).exists():
                (project / PROJECT_FILE).unlink()
        else:
            save_state(project, state)

    print("Remaining runtimes:", ", ".join(remaining) or "none")

def build_parser():
    p = argparse.ArgumentParser(prog="gantry", description="Gantry harness installer")
    p.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = p.add_subparsers(dest="command", required=True)

    def common_install(sp):
        sp.add_argument("--project", default=".")
        sp.add_argument("--runtime", required=True, help="claude,codex,cursor,opencode,omp or all")
        sp.add_argument("--scope", choices=SCOPES, default="mixed")
        sp.add_argument("--profile", choices=PROFILES, default="standard")
        sp.add_argument("--force", action="store_true")
        sp.add_argument("--dry-run", action="store_true")
        sp.add_argument("--no-hooks", action="store_true", help="do not register the harness guard hooks")

    ins = sub.add_parser("install", help="Install one or more runtime adapters")
    common_install(ins)
    ins.set_defaults(func=cmd_install)

    init = sub.add_parser("init", help="Alias for install")
    common_install(init)
    init.set_defaults(func=cmd_install)

    plan = sub.add_parser("plan", help="Show what install would change")
    common_install(plan)
    plan.set_defaults(func=cmd_plan)

    st = sub.add_parser("status", help="Show installed harness/runtime state")
    st.add_argument("--project", default=".")
    st.set_defaults(func=cmd_status)

    dr = sub.add_parser("doctor", help="Validate the installed harness")
    dr.add_argument("--project", default=".")
    dr.set_defaults(func=cmd_doctor)

    insp = sub.add_parser("inspect", help="Describe the project: new or existing, stack, and check commands")
    insp.add_argument("--project", default=".")
    insp.add_argument("--json", action="store_true")
    insp.add_argument("--write", action="store_true", help=f"save the result to {PROJECT_FILE}")
    insp.set_defaults(func=cmd_inspect)

    un = sub.add_parser("uninstall", help="Remove selected runtime overlays")
    un.add_argument("--project", default=".")
    un.add_argument("--runtime", help="runtime list; defaults to all installed")
    un.add_argument("--purge-shared", action="store_true", help="remove shared core/skills when no runtimes remain")
    un.add_argument("--force", action="store_true")
    un.add_argument("--dry-run", action="store_true")
    un.set_defaults(func=cmd_uninstall)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
