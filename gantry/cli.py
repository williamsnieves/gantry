from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
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
PROFILES = ("lean", "standard")
# Accepted and installed as `standard`: it never did anything else.
RETIRED_PROFILES = {"strict": "standard"}

# Skills live once in distribution/shared and are rendered at install time. The
# shared catalogue gets compact descriptions: specialist agents read a skill by
# explicit path when a change needs it, so nothing competes for implicit
# discovery or sits in context unused. A runtime with native skill discovery
# receives only the entry-point skills, with their full description.
ENTRYPOINT_SKILLS = ("harness-start", "harness-run", "harness-ship", "harness-onboard", "harness-evaluate")
COMPACT_DESCRIPTION = (
    "Portable engineering capability `{name}`. Use when the harness or a "
    "specialist agent explicitly requires this named capability."
)
NATIVE_SKILL_DIRS = {"claude": ".claude/skills"}

# What `gantry inspect` found in the project: its stack and the commands that check it.
PROJECT_FILE = ".harness/project.yaml"

# Which model each tier of gate runs on. Written once and then the user's: an install never overwrites it.
MODELS_FILE = ".harness/models.yaml"
MODELS_TEMPLATE = """# Which model each gate runs on, per runtime. Yours to edit; agents cannot.
#
# The router gives every gate a tier from its job and the change's risk:
#   fast      runs the project's checks and reports them (Validator outside the DESIGN lane)
#   standard  reviews code against known rules (code reviews, QA, Detail Analyst outside the DESIGN lane)
#   deep      judges risk, design or the change as a whole (Security, Architecture, Reviewer; every reviewer in the DESIGN lane)
#
# An empty value means the session's own model, which is how every gate runs until you fill one in.
# On Claude Code the values are the model names its agent launcher accepts, for example:
#   fast: haiku
#   standard: sonnet
{sections}"""

# Runtimes whose command hooks the harness can register. The guard denies agent
# edits to harness files and quality configuration, and pull-request creation
# before the Final Pre-PR Gate passes. See distribution/core/.harness/bin/hook.py.
HOOK_MARKER = ".harness/bin/hook.py"
HOOK_SETTINGS = {"claude": ".claude/settings.json"}
# Runtimes whose specialists write their own report, which only a hook can confine to that file.
AGENT_DIRS = {"claude": ".claude/agents"}
HOOK_MATCHERS = ("Edit|Write|MultiEdit|NotebookEdit", "Bash", "Agent|Task")
HOOK_DISCLOSURE = """Hooks registered in {path} (skip with --no-hooks):
  - deny agent edits to harness files and to routing state written by route.py
  - deny agent edits to existing lint, type, test and CI configuration (not in the lean profile)
  - deny `gh pr create` until `route.py ready` passes, and commands using --no-verify (not in the lean profile)
  - deny launching a gate after the review stopped at a stage that did not pass (not in the lean profile)
  - ask you to confirm when the agent records your approval of a design with `spec.py approve`
  - deny `git commit` and `git push` while the change adds a secret
  - deny `gh pr merge` until `release.py check` passes (not in the lean profile)
  - launch each gate on the model .harness/models.yaml gives its tier, when you have filled one in
  They apply to the agent only; you can still make these changes yourself."""

# What tells `gantry init` that a project already uses an agent tool, and the tool's command when it does not.
RUNTIME_NAMES = {"claude": "Claude Code", "codex": "Codex", "cursor": "Cursor", "opencode": "OpenCode", "omp": "Oh My Pi"}
RUNTIME_SIGNS = {"claude": (".claude", "CLAUDE.md"), "codex": (".codex",), "cursor": (".cursor", ".cursorrules"),
                 "opencode": (".opencode", "opencode.json"), "omp": (".omp",)}
RUNTIME_COMMANDS = {"claude": ("claude",), "codex": ("codex",), "cursor": ("cursor-agent", "cursor"),
                    "opencode": ("opencode",), "omp": ("omp",)}
FRONTEND = {"react", "next", "vue", "svelte", "angular"}
BACKEND = {"express", "fastify", "nestjs", "hono", "prisma", "drizzle", "typeorm", "fastapi", "django", "flask", "sqlalchemy"}
PROFILE_MEANING = {
    "lean": "the hooks deny only edits to the harness and committing a secret",
    "standard": "the hooks also deny weakening a check, skipping a review stage, and a pull request before the review passes",
}

# Set by --verbose: print one line per file instead of a count per group.
VERBOSE = False

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
    for p in sorted(root.rglob("*")):
        # Bytecode a local run left beside the scripts is not part of the harness.
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc":
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

def planned(src: Path, content: str | None) -> bytes:
    """The bytes an install writes for one shipped file."""
    return content.encode("utf-8") if content is not None else src.read_bytes()

def conflict(dst: Path, managed: dict | None, new_hash: str, force: bool) -> str | None:
    """Why an install must not overwrite `dst`, or None. A file that already has the shipped content is never a conflict."""
    if force or not dst.exists():
        return None
    current = sha256(dst)
    if current == new_hash:
        return None
    if managed is None:
        return "exists and was not installed by the harness"
    if current != managed.get("sha256"):
        return "was edited after the harness installed it"
    return None

def managed_copy(src: Path, dst: Path, project: Path, state: dict, *, force: bool, dry_run: bool, label: str, content: str | None = None):
    key = rel(project, dst)
    data = planned(src, content)
    new_hash = hashlib.sha256(data).hexdigest()
    why = conflict(dst, state["managed_files"].get(key), new_hash, force)
    if why:
        raise SystemExit(f"Refusing to overwrite {key}: it {why}.\nUse --force only after reviewing it.")

    change = "new" if not dst.exists() else "unchanged" if sha256(dst) == new_hash else "updated"
    state.setdefault("_written", set()).add(key)
    state.setdefault("_report", {}).setdefault(label, {"new": 0, "updated": 0, "unchanged": 0})[change] += 1
    if VERBOSE:
        print(f"{'[DRY-RUN] ' if dry_run else ''}install {label}: {key} ({change})")
    if dry_run:
        return

    if change != "unchanged":
        dst.parent.mkdir(parents=True, exist_ok=True)
        if content is None:
            shutil.copy2(src, dst)
        else:
            dst.write_bytes(data)
    state["managed_files"][key] = {
        "sha256": new_hash,
        "owner": label,
    }

def skills_root() -> Path:
    return distribution_root() / "shared/skills/.agents/skills"

def skill_files(dst_root: Path, *, compact: bool, label: str, only: tuple[str, ...] | None = None):
    src_root = skills_root()
    for src in iter_files(src_root):
        relative = src.relative_to(src_root)
        if only is not None and relative.parts[0] not in only:
            continue
        content = None
        if len(relative.parts) == 2 and relative.name == "SKILL.md":
            content = render_skill(src.read_text(encoding="utf-8"), relative.parts[0], compact=compact)
        yield src, dst_root / relative, label, content

def shared_files(project: Path):
    """Every file the shared installation ships, as (source, destination, owner, rendered content or None)."""
    core = distribution_root() / "core/.harness"
    for src in iter_files(core):
        yield src, project / ".harness" / src.relative_to(core), "shared-core", None
    yield from skill_files(project / ".agents/skills", compact=True, label="shared-skills")

def runtime_files(runtime: str, project: Path, hooks: bool):
    """Every file one runtime overlay ships. Without hooks its specialists are installed without write access."""
    overlay = distribution_root() / "runtimes" / runtime
    agents_dir = overlay / AGENT_DIRS[runtime] if runtime in AGENT_DIRS else None
    for src in iter_files(overlay):
        content = None
        if not hooks and agents_dir and src.parent == agents_dir:
            content = read_only_agent(src.read_text(encoding="utf-8"))
        yield src, project / src.relative_to(overlay), f"runtime:{runtime}", content
    if runtime in NATIVE_SKILL_DIRS:
        yield from skill_files(project / NATIVE_SKILL_DIRS[runtime], compact=False, label=f"runtime:{runtime}", only=ENTRYPOINT_SKILLS)

def planned_files(project: Path, runtimes: list[str], hooks: bool):
    yield from shared_files(project)
    for runtime in runtimes:
        yield from runtime_files(runtime, project, hooks)

def conflicts(project: Path, state: dict, runtimes: list[str], hooks: bool) -> list[str]:
    """Every file an install would refuse to overwrite, found before anything is written."""
    found = []
    for src, dst, _, content in planned_files(project, runtimes, hooks):
        key = rel(project, dst)
        why = conflict(dst, (state.get("managed_files") or {}).get(key), hashlib.sha256(planned(src, content)).hexdigest(), False)
        if why:
            found.append(f"{key}: {why}")
    return found

def pending(project: Path, state: dict, runtimes: list[str], hooks: bool) -> int:
    """How many installed files differ from what this version ships: what `gantry upgrade` would write."""
    managed = state.get("managed_files") or {}
    return sum(1 for src, dst, _, content in planned_files(project, runtimes, hooks)
               if managed.get(rel(project, dst), {}).get("sha256") != hashlib.sha256(planned(src, content)).hexdigest())

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
    if settings != before or VERBOSE:
        print(HOOK_DISCLOSURE.format(path=HOOK_SETTINGS[runtime]))
    else:
        print(f"hooks: already registered in {HOOK_SETTINGS[runtime]}")

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

def write_harness_config(project: Path, runtimes: list[str], scope: str, profile: str, *, dry_run: bool, receipts: bool = False, mutation: bool = False):
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
            "receipts": receipts,
            "mutation": mutation,
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
    for src, dst, label, content in shared_files(project):
        managed_copy(src, dst, project, state, force=force, dry_run=dry_run, label=label, content=content)
    merge_agents_block(project, dry_run=dry_run)
    if not dry_run:
        state["shared_installed"] = True

def read_only_agent(text: str) -> str:
    """Agent definition without write access, for installs where no hook limits what it may write."""
    text = re.sub(r"^(tools: .*?), Write$", r"\1", text, count=1, flags=re.M)
    return re.sub(r"^permissionMode: acceptEdits$", "permissionMode: plan", text, count=1, flags=re.M)

def install_runtime(runtime: str, project: Path, state: dict, *, force: bool, dry_run: bool, hooks: bool = True):
    for src, dst, label, content in runtime_files(runtime, project, hooks):
        managed_copy(src, dst, project, state, force=force, dry_run=dry_run, label=label, content=content)
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

def saved_config(project: Path) -> tuple[str | None, str | None]:
    """(scope, profile) of the current installation, so a reinstall keeps what the person chose."""
    path = project / ".harness/harness.config.yaml"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    found = [re.search(rf"[\"']?{key}[\"']?\s*:\s*[\"']?([\w-]+)", text) for key in ("scope_profile", "delivery_profile")]
    scope, profile = (m.group(1) if m else None for m in found)
    profile = RETIRED_PROFILES.get(profile, profile)
    return (scope if scope in SCOPES else None), (profile if profile in PROFILES else None)

def saved_option(project: Path, name: str) -> bool:
    """Whether an opt-in of this installation is on (`pre_pr.<name>` in the harness config)."""
    path = project / ".harness/harness.config.yaml"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    return bool(re.search(rf"^\s*[\"']?{name}[\"']?\s*:\s*true\b", text, re.M))

def saved_receipts(project: Path) -> bool:
    return saved_option(project, "receipts")

def hooks_registered(project: Path, runtime: str) -> bool:
    path = project / HOOK_SETTINGS[runtime]
    return path.is_file() and HOOK_MARKER in path.read_text(encoding="utf-8", errors="replace")

def print_report(state: dict, dry_run: bool):
    for label, counts in state.pop("_report", {}).items():
        changed = ", ".join(f"{n} {kind}" for kind, n in counts.items() if n and kind != "unchanged") or "unchanged"
        print(f"{'[DRY-RUN] ' if dry_run else ''}{label + ':':18} {sum(counts.values()):4} files ({changed})")

def cmd_install(args):
    project = ensure_project(args.project)
    runtimes = parse_runtimes(args.runtime)
    if not runtimes:
        raise SystemExit("Select at least one runtime with --runtime, or run `gantry init` to be asked.")

    state = load_state(project)
    state.setdefault("managed_files", {})
    state.setdefault("runtimes", [])
    saved_scope, saved_profile = saved_config(project)
    scope = args.scope or saved_scope or "mixed"
    profile = args.profile or saved_profile or "standard"
    receipts = saved_receipts(project) if getattr(args, "receipts", None) is None else args.receipts
    mutation = saved_option(project, "mutation") if getattr(args, "mutation", None) is None else args.mutation

    # Look before writing: a refusal halfway would leave files the install state does not know about.
    if not args.force:
        found = conflicts(project, state, runtimes, not args.no_hooks)
        if found:
            print(f"{len(found)} file(s) would be overwritten:")
            for line in found:
                print(f"  {line}")
            raise SystemExit("Nothing was changed. Review them, then rerun with --force to replace them with the harness's version.")

    install_shared(project, state, force=args.force, dry_run=args.dry_run)
    for runtime in runtimes:
        install_runtime(runtime, project, state, force=args.force, dry_run=args.dry_run, hooks=not args.no_hooks)
    print_report(state, args.dry_run)

    prune_stale(project, state, runtimes, force=args.force, dry_run=args.dry_run)

    final_runtimes = sorted(set(state["runtimes"]) | set(runtimes), key=RUNTIMES.index)
    write_harness_config(
        project, final_runtimes, scope, profile, dry_run=args.dry_run, receipts=receipts, mutation=mutation
    )

    models = project / MODELS_FILE
    if models.exists():
        print(f"keep: {MODELS_FILE}")
    else:
        print(f"{'[DRY-RUN] ' if args.dry_run else ''}write: {MODELS_FILE}")
        if not args.dry_run:
            sections = "".join(f'{r}:\n  fast: ""\n  standard: ""\n  deep: ""\n' for r in final_runtimes)
            models.write_text(MODELS_TEMPLATE.format(sections=sections), encoding="utf-8")

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
    print(f"Installed runtimes: {', '.join(final_runtimes)}  (scope {scope}, profile {profile})")
    print_entrypoints(final_runtimes)
    if mutation:
        print("Mutation testing is on: `python3 .harness/bin/mutate.py` changes each line a change adds and runs "
              + (f"`{description['checks']['test']['command']}`" if "test" in description["checks"] else "the project's tests")
              + " against it.\nThe review runs it; what the tests did not notice becomes a condition at the Final Pre-PR Gate.")
    if receipts:
        print("Review receipts are on: `route.py ready` writes one per reviewed change under .harness/receipts/. Commit it with the\n"
              "change and make CI run `python3 .harness/bin/route.py verify --base origin/<default branch>` on pull requests.")
    if not args.dry_run:
        print("Check the installation at any time with `gantry doctor`.")


def suggest_runtimes(project: Path, state: dict) -> list[tuple[str, str]]:
    """The agent tools this project most likely uses, each with the reason, strongest evidence first."""
    installed = [(r, "already installed") for r in state.get("runtimes") or []]
    if installed:
        return installed
    in_project = [(r, f"found {next(s for s in RUNTIME_SIGNS[r] if (project / s).exists())}")
                  for r in RUNTIMES if any((project / s).exists() for s in RUNTIME_SIGNS[r])]
    if in_project:
        return in_project
    return [(r, f"`{next(c for c in RUNTIME_COMMANDS[r] if shutil.which(c))}` is on your PATH")
            for r in RUNTIMES if any(shutil.which(c) for c in RUNTIME_COMMANDS[r])]

def suggest_scope(description: dict) -> str:
    frameworks = set(description.get("frameworks") or [])
    front, back = bool(frameworks & FRONTEND), bool(frameworks & BACKEND)
    return "fullstack" if front and back else "frontend" if front else "backend" if back else "mixed"

def interactive() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()

def ask(question: str, default: str) -> str:
    try:
        answer = input(f"{question} [{default}]: ").strip()
    except EOFError:
        answer = ""
    return answer or default

def ask_choice(question: str, choices: tuple[str, ...], default: str) -> str:
    while True:
        answer = ask(question, default).lower()
        if answer in choices:
            return answer
        print(f"  choose one of: {', '.join(choices)}")

def ask_yes(question: str, default: bool = True) -> bool:
    answer = ask(question, "Y/n" if default else "y/N").lower()
    return default if answer in ("y/n",) else answer.startswith("y")

def cmd_init(args):
    """Guided install: propose what the project shows, ask only what no flag answered."""
    project = ensure_project(args.project)
    state = load_state(project)
    description = detect.detect(project)
    saved_scope, saved_profile = saved_config(project)
    found = suggest_runtimes(project, state)
    runtimes = parse_runtimes(args.runtime) if args.runtime else [r for r, _ in found]
    scope = args.scope or saved_scope or suggest_scope(description)
    profile = args.profile or saved_profile or "standard"
    hooks = not args.no_hooks
    receipts = saved_receipts(project) if args.receipts is None else args.receipts
    mutation = saved_option(project, "mutation") if args.mutation is None else args.mutation
    proposal = f"--runtime {','.join(runtimes) or '<tool>'} --scope {scope} --profile {profile}"

    if args.yes or (args.runtime and not interactive()):
        if not runtimes:
            raise SystemExit(f"No agent tool was found in this project or on your PATH. Name one: gantry init --runtime <{'|'.join(RUNTIMES)}>")
    elif not interactive():
        raise SystemExit(f"This is not a terminal, so nothing can be asked. Accept the proposal with:\n  gantry init --yes {proposal}")
    else:
        print(f"Gantry {VERSION} setup for {project}\n")
        print("\n".join(detect.summary(description)[:4]))
        if not args.runtime:
            reasons = dict(found)
            print("\nWhich agent tools do you use in this project? Comma separated, or `all`.")
            for r in RUNTIMES:
                print(f"  {r:9} {RUNTIME_NAMES[r]:12} {reasons.get(r, '')}".rstrip())
            while True:
                try:
                    runtimes = parse_runtimes(ask("Tools", ",".join(runtimes) or "claude"))
                except SystemExit as error:
                    print(f"  {error}")
                    continue
                if runtimes:
                    break
        if not args.scope:
            print("\nWhat does the project cover? This is context for routing; it never hides a reviewer a change needs.")
            scope = ask_choice(f"Scope ({', '.join(SCOPES)})", SCOPES, scope)
        if not args.profile:
            print("\nHow much should the hooks refuse? The Final Pre-PR Gate is the same in every profile.")
            for name in PROFILES:
                print(f"  {name:9} {PROFILE_MEANING[name]}")
            profile = ask_choice("Profile", PROFILES, profile)
        hookable = [r for r in runtimes if r in HOOK_SETTINGS]
        if hookable and hooks:
            print(f"\nGuard hooks can be registered in {', '.join(HOOK_SETTINGS[r] for r in hookable)}. They stop the agent, not you;")
            print("without them the same rules are only checked at the Final Pre-PR Gate.")
            hooks = ask_yes("Register the hooks?")
        if args.receipts is None:
            print("\nShould CI be able to check that what is merged is what was reviewed? The final gate then writes a small receipt")
            print("per change, which you commit with it, and `route.py verify` fails a pull request whose content has none.")
            receipts = ask_yes("Keep review receipts?", default=receipts)
        if args.mutation is None:
            print("\nShould the review check that the tests would notice if the new lines were wrong? It changes each added line")
            print("(`>=` to `>`, `&&` to `||`) and runs your tests against it: about a dozen extra test runs per review.")
            mutation = ask_yes("Turn mutation testing on?", default=mutation)
        hook_note = f", hooks {'on' if hooks else 'off'}" if hookable else "; none of these tools has hooks, so the rules are checked at the Final Pre-PR Gate"
        print(f"\nInstall for {', '.join(runtimes)} with scope {scope}, profile {profile}{hook_note}{', review receipts on' if receipts else ''}{', mutation testing on' if mutation else ''}.")
        if not ask_yes("Go ahead?"):
            print("Nothing was changed.")
            return
        print()

    cmd_install(argparse.Namespace(project=str(project), runtime=",".join(runtimes), scope=scope, profile=profile,
                                   force=args.force, dry_run=args.dry_run, no_hooks=not hooks, receipts=receipts, mutation=mutation))

def cmd_upgrade(args):
    """Reinstall what is installed with this version of Gantry, keeping the runtimes, scope, profile and hook choice."""
    project = ensure_project(args.project)
    state = load_state(project)
    runtimes = list(state.get("runtimes") or [])
    if not runtimes:
        raise SystemExit("The harness is not installed in this project; run `gantry init`.")
    scope, profile = saved_config(project)
    no_hooks = any(r in HOOK_SETTINGS and not hooks_registered(project, r) for r in runtimes)
    print(f"Gantry {state.get('harness_version') or 'unknown'} -> {VERSION} for {', '.join(runtimes)}"
          f"{' (hooks stay off; turn them on with `gantry install`)' if no_hooks else ''}")
    cmd_install(argparse.Namespace(project=str(project), runtime=",".join(runtimes), scope=scope, profile=profile,
                                   force=args.force, dry_run=args.dry_run, no_hooks=no_hooks, receipts=None, mutation=None))


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
        print(f"  {r:8} -> {mark}harness-onboard once, then {mark}harness-start for each piece of work ({mark}harness-run reviews it, {mark}harness-ship releases it)")

def cmd_plan(args):
    args.dry_run = True
    cmd_install(args)

def cmd_status(args):
    project = ensure_project(args.project)
    state = load_state(project)
    scope, profile = saved_config(project)
    print(f"Harness version: {state.get('harness_version') or 'not installed'}")
    print("Installed runtimes:", ", ".join(state.get("runtimes") or []) or "none")
    if scope or profile:
        print(f"Scope: {scope}  Profile: {profile}")
    for runtime in state.get("runtimes") or []:
        if runtime in HOOK_SETTINGS:
            print(f"Hooks ({runtime}): {'registered' if hooks_registered(project, runtime) else 'not registered'}")
    print("Managed files:", len(state.get("managed_files") or {}))
    cfg = project / ".harness/harness.config.yaml"
    if cfg.exists():
        print("Config:", cfg)
    if state.get("runtimes"):
        print_entrypoints(state["runtimes"])

def script(project: Path, name: str, *arguments: str, stdin: str = "") -> tuple[int, str]:
    """Run one of the installed harness scripts the way an agent would: with `python3` from the PATH."""
    try:
        proc = subprocess.run(["python3", str(project / ".harness/bin" / name), *arguments], cwd=project, input=stdin,
                              capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as error:
        return 1, str(error)
    return proc.returncode, (proc.stdout + proc.stderr).strip()

def models_by_runtime(project: Path) -> dict[str, dict[str, str]]:
    """{runtime: {tier: model}} for every tier the project filled in."""
    path = project / MODELS_FILE
    found, section = {}, None
    for line in (path.read_text(encoding="utf-8") if path.is_file() else "").splitlines():
        line = line.split("#", 1)[0].rstrip()
        header = re.fullmatch(r"([\w-]+):", line)
        entry = re.fullmatch(r"\s+(\w+):\s*[\"']?([^\"'\s]*)[\"']?", line)
        if header:
            section = header.group(1)
        elif entry and section and entry.group(2):
            found.setdefault(section, {})[entry.group(1)] = entry.group(2)
    return found

def cmd_doctor(args):
    project = ensure_project(args.project)
    state = load_state(project)
    errors, warnings, notes = [], [], []   # each item: (what is wrong, how to fix it or None)
    runtimes = state.get("runtimes") or []

    if not state.get("harness_version"):
        errors.append(("Harness install state is missing.", "gantry init"))

    # Check managed files still exist and hashes match.
    modified = []
    for key, meta in (state.get("managed_files") or {}).items():
        p = project / key
        if not p.exists():
            errors.append((f"Missing managed file: {key}", "gantry upgrade"))
        elif sha256(p) != meta.get("sha256"):
            modified.append(key)
    for key in modified[:5]:
        warnings.append((f"Locally modified managed file: {key}", None))
    if modified:
        more = f"and {len(modified) - 5} more; " if len(modified) > 5 else ""
        warnings.append((f"{more}an upgrade refuses to replace edited files",
                         "review them, then `gantry upgrade --force` to take the harness's version"))

    # Core invariants.
    required = [
        ".harness/core/routing/ROUTING-POLICY.md",
        ".harness/bin/route.py",
        ".harness/bin/hook.py",
        ".harness/bin/scan.py",
        ".harness/bin/release.py",
        ".harness/bin/mutate.py",
        ".harness/core/pre-pr/FINAL-PRE-PR-GATE.md",
        ".harness/agents/reviewer/AGENT.md",
        ".harness/evals/end-to-end/E2E-ORACLE.md",
        ".agents/skills/harness-run/SKILL.md",
    ]
    for key in required:
        if not (project / key).exists():
            errors.append((f"Missing core artifact: {key}", "gantry upgrade"))

    runtime_checks = {
        "claude": [".claude/agents/reviewer.md", ".claude/skills/harness-run/SKILL.md"],
        "codex": [".codex/agents/reviewer.toml"],
        "cursor": [".cursor/agents/reviewer.md", ".cursor/rules/00-portable-harness.mdc"],
        "opencode": [".opencode/agents/reviewer.md", ".opencode/commands/harness-run.md"],
        "omp": [".omp/agents/reviewer.md", ".omp/commands/harness-run.md", ".omp/RULES.md"],
    }
    for runtime in runtimes:
        for key in runtime_checks[runtime]:
            if not (project / key).exists():
                errors.append((f"{runtime}: missing {key}", "gantry upgrade"))

    hooks_on = True
    for runtime in runtimes:
        if runtime in HOOK_SETTINGS and not hooks_registered(project, runtime):
            hooks_on = False
            warnings.append((f"{runtime}: guard hooks are not registered in {HOOK_SETTINGS[runtime]}; gates are advisory only.",
                             f"gantry install --runtime {runtime}"))

    agents_md = (project / "AGENTS.md").read_text(encoding="utf-8") if (project / "AGENTS.md").exists() else ""
    if START not in agents_md:
        if find_block_markers(agents_md):
            warnings.append(("AGENTS.md still has the pre-rename harness block.", "gantry upgrade"))
        else:
            warnings.append(("Managed AGENTS.md harness block is missing.", "gantry upgrade"))

    if runtimes:
        # Is this what the installed CLI ships? Files edited locally are reported above, not here.
        behind = pending(project, state, runtimes, hooks_on)
        if behind or state.get("harness_version") != VERSION:
            warnings.append((f"The installation is {state.get('harness_version')}; this CLI is {VERSION} and ships {behind} file(s) that differ.",
                             "`gantry upgrade --dry-run` to see what changes, `gantry upgrade` to apply it"))

        # Do the scripts run here, the way an agent will run them?
        if not shutil.which("python3"):
            errors.append(("`python3` is not on the PATH; the router, the scan and the hooks are run with it.", "install Python 3.10 or later"))
        else:
            code, out = script(project, "route.py", "guardrails")
            if code != 0:
                errors.append((f"`python3 .harness/bin/route.py` does not run: {out.splitlines()[-1] if out else 'no output'}",
                               "the harness needs Python 3.10 or later as `python3`"))
            for runtime in runtimes:
                if runtime in HOOK_SETTINGS and hooks_on:
                    code, out = script(project, "hook.py", runtime, stdin="{}")
                    if code != 0:
                        errors.append((f"{runtime}: the guard hook does not run: {out.splitlines()[-1] if out else 'no output'}", "gantry upgrade"))

        # The router tells one change from another through git.
        try:
            inside = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=project, capture_output=True, text=True).returncode == 0
        except OSError:
            inside = False
        if not inside:
            warnings.append(("This is not a git repository; the router cannot tell what a change contains, so every review covers nothing.", "git init"))
        elif subprocess.run(["git", "check-ignore", "-q", ".harness/runtime/x"], cwd=project).returncode != 0:
            warnings.append((".harness/runtime/ (routing plan, gate reports, approvals) is not ignored by git; it is local review state "
                             "and every branch writes the same files.", "gantry upgrade, which installs .harness/.gitignore"))

        # Receipts are only worth committing if something checks them.
        if saved_receipts(project):
            ci = [f for d in (".github/workflows", ".circleci") if (project / d).is_dir() for f in (project / d).rglob("*") if f.is_file()]
            ci += [project / name for name in (".gitlab-ci.yml", "Jenkinsfile", "azure-pipelines.yml") if (project / name).is_file()]
            if not any("route.py verify" in f.read_text(encoding="utf-8", errors="replace") for f in ci):
                warnings.append(("Review receipts are on, but no CI file runs `route.py verify`, so nothing checks them.",
                                 "run `python3 .harness/bin/route.py verify --base origin/<default branch>` on pull requests, "
                                 "with the full history fetched; or turn them off with `gantry install --runtime <tool> --no-receipts`"))

        if saved_option(project, "mutation") and not re.search(
                r"^  test:", (project / PROJECT_FILE).read_text(encoding="utf-8") if (project / PROJECT_FILE).is_file() else "", re.M):
            warnings.append(("Mutation testing is on, but no test command is recorded, so it cannot run.",
                             f"add it under `checks:` in {PROJECT_FILE}; or turn it off with `gantry install --runtime <tool> --no-mutation`"))

        # What the Validator will run.
        described = project / PROJECT_FILE
        if not described.is_file():
            warnings.append((f"{PROJECT_FILE} is missing; the Validator has to rediscover the check commands on every run.", "gantry inspect --write"))
        else:
            text = described.read_text(encoding="utf-8")
            absent = [check for check in ("test", "lint", "typecheck") if not re.search(rf"^  {check}:", text, re.M)]
            if absent and re.search(r'^kind:\s*"?brownfield', text, re.M):
                warnings.append((f"No command recorded for: {', '.join(absent)}. The Validator cannot run what is not listed.",
                                 f"add it under `checks:` in {PROJECT_FILE}, or `gantry inspect --write` after adding the tooling"))

        # What reviewers read first.
        if not (project / "docs/conventions.md").is_file():
            notes.append(("docs/conventions.md is not written yet; reviewers have no project conventions to judge against.",
                          "run the harness-onboard skill in your agent"))
        elif shutil.which("python3"):
            code, out = script(project, "conventions.py", "check")
            if code != 0:
                warnings.append(("docs/conventions.md does not pass its check: " + "; ".join(line.strip() for line in out.splitlines()[1:4]),
                                 "python3 .harness/bin/conventions.py check"))

        # Which model runs the gates.
        mapped = models_by_runtime(project)
        if not (project / MODELS_FILE).is_file():
            warnings.append((f"{MODELS_FILE} is missing.", "gantry upgrade"))
        for runtime, tiers in mapped.items():
            unknown = [tier for tier in tiers if tier not in ("fast", "standard", "deep")]
            if runtime not in RUNTIMES or unknown:
                warnings.append((f"{MODELS_FILE}: unknown {'runtime ' + runtime if runtime not in RUNTIMES else 'tier ' + ', '.join(unknown)}; it is ignored.",
                                 "runtimes are " + ", ".join(RUNTIMES) + "; tiers are fast, standard, deep"))
        for runtime in runtimes:
            tiers = {tier: model for tier, model in mapped.get(runtime, {}).items() if tier in ("fast", "standard", "deep")}
            if not tiers:
                notes.append((f"{runtime}: every gate runs on the session's model.",
                              f"to spend less on low-risk gates, map tiers to models in {MODELS_FILE}"))
            else:
                enforced = "the hook launches each gate on it" if runtime in HOOK_SETTINGS and hooks_on else "nothing enforces it; the lead agent is told which model to launch"
                notes.append((f"{runtime}: gates run on {', '.join(f'{tier}={model}' for tier, model in tiers.items())}; {enforced}.", None))

    if errors:
        print("DOCTOR: FAIL")
    elif warnings:
        print("DOCTOR: PASS WITH WARNINGS")
    else:
        print("DOCTOR: PASS")

    for label, items in (("ERROR", errors), ("WARN ", warnings), ("NOTE ", notes)):
        for what, fix in items:
            print(f"{label}: {what}")
            if fix:
                print(f"       fix: {fix}")
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
            write_harness_config(project, remaining, scope, profile, dry_run=False, receipts=saved_receipts(project), mutation=saved_option(project, "mutation"))
            save_state(project, state)
        elif args.purge_shared:
            sp = state_path(project)
            if sp.exists():
                sp.unlink()
            for owned in (PROJECT_FILE, MODELS_FILE):
                if (project / owned).exists():
                    (project / owned).unlink()
        else:
            save_state(project, state)

    print("Remaining runtimes:", ", ".join(remaining) or "none")

def build_parser():
    p = argparse.ArgumentParser(prog="gantry", description="Gantry harness installer")
    p.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = p.add_subparsers(dest="command", required=True)

    def common_install(sp, *, runtime_required: bool):
        sp.add_argument("--project", default=".")
        sp.add_argument("--runtime", required=runtime_required, help="claude,codex,cursor,opencode,omp or all")
        sp.add_argument("--scope", choices=SCOPES, help="default: what is installed, else mixed")
        sp.add_argument("--profile", choices=PROFILES, type=lambda value: RETIRED_PROFILES.get(value, value),
                        help="default: what is installed, else standard")
        sp.add_argument("--force", action="store_true", help="replace files that were edited or that the harness does not own")
        sp.add_argument("--dry-run", action="store_true")
        sp.add_argument("--no-hooks", action="store_true", help="do not register the harness guard hooks")
        sp.add_argument("--verbose", action="store_true", help="print every file")
        sp.add_argument("--receipts", action=argparse.BooleanOptionalAction, default=None,
                        help="keep a receipt per reviewed change so CI can verify it; default: what is installed, else off")

        sp.add_argument("--mutation", action=argparse.BooleanOptionalAction, default=None,
                        help="mutate the lines a change adds and run the tests against them; default: what is installed, else off")

    init = sub.add_parser("init", help="Guided install: proposes the tools, scope and profile it finds, and asks")
    common_install(init, runtime_required=False)
    init.add_argument("--yes", action="store_true", help="accept the proposal without being asked")
    init.set_defaults(func=cmd_init)

    ins = sub.add_parser("install", help="Install one or more runtime adapters, without questions")
    common_install(ins, runtime_required=True)
    ins.set_defaults(func=cmd_install)

    plan = sub.add_parser("plan", help="Show what install would change")
    common_install(plan, runtime_required=True)
    plan.set_defaults(func=cmd_plan)

    up = sub.add_parser("upgrade", help="Bring the installation to this version, keeping its runtimes, scope, profile and hooks")
    up.add_argument("--project", default=".")
    up.add_argument("--force", action="store_true", help="replace files that were edited locally")
    up.add_argument("--dry-run", action="store_true")
    up.add_argument("--verbose", action="store_true", help="print every file")
    up.set_defaults(func=cmd_upgrade)

    st = sub.add_parser("status", help="Show installed harness/runtime state")
    st.add_argument("--project", default=".")
    st.set_defaults(func=cmd_status)

    dr = sub.add_parser("doctor", help="Check the installation and say how to fix what is wrong")
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

def main(argv: list[str] | None = None):
    global VERBOSE
    parser = build_parser()
    args = parser.parse_args(argv)
    VERBOSE = bool(getattr(args, "verbose", False))
    args.func(args)

if __name__ == "__main__":
    main()
