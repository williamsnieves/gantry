#!/usr/bin/env python3
"""Deterministic router for the harness.

The agent classifies the change (work mode, scopes, risk triggers with
evidence). This tool turns that classification into the routing plan: which
specialist gates are REQUIRED, which are not, and why. Same classification in,
same plan out.

    python3 .harness/bin/route.py vocabulary
    python3 .harness/bin/route.py plan --runtime claude --work-mode IMPLEMENTATION \\
        --scope BACKEND --trigger "SECURITY=tenant predicate relaxed for support staff"
    python3 .harness/bin/route.py check .harness/runtime/claude/routing-plan.yaml
    python3 .harness/bin/route.py gate --runtime claude --agent qa --decision PASS --report <file>
    python3 .harness/bin/route.py ready --runtime claude

Standard library only, so it runs in any project with Python 3.9+.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PLAN_VERSION = "2.0.0"
CONTRACT_VERSION = "1.0.0"

RUNTIMES = ("claude", "codex", "cursor", "opencode", "omp")
AGENTS = (
    "validator",
    "backend-code-review",
    "backend-architecture-review",
    "frontend-code-review",
    "frontend-architecture-review",
    "qa",
    "performance",
    "security",
    "infrastructure",
    "detail-analyst",
    "reviewer",
)
SPECIALISTS = AGENTS[1:9]
APPLICABILITY = ("REQUIRED", "CONDITIONAL", "NOT_APPLICABLE", "NOT_TRIGGERED", "ALREADY_SATISFIED", "BLOCKED")

WORK_MODES = {
    "DISCOVERY": "Understanding an existing system or requirement. No implementation gates.",
    "ARCHITECTURE_ONLY": "Requirements or architecture work with no implementation.",
    "IMPLEMENTATION": "Production code, configuration or tests are being changed.",
    "REVIEW_ONLY": "Reviewing existing implementation without modifying it.",
    "REMEDIATION": "Fixing known findings, including adding missing test evidence.",
    "MIGRATION": "Schema, platform or architecture migration where old and new states coexist.",
    "RELEASE_ONLY": "Deployment, release or configuration work with no new application behavior.",
}
SCOPES = {
    "DOCUMENTATION": "Documentation only.",
    "REQUIREMENTS": "Requirements or acceptance criteria.",
    "SOFTWARE_ARCHITECTURE": "System-level choices: boundaries, data ownership, events, topology.",
    "BACKEND": "Domain or application behavior, HTTP/API implementation, persistence, server-side authorization.",
    "FRONTEND": "UI behavior, hooks and state, frontend adapters, browser interactions.",
    "FULL_STACK": "One accepted behavior crosses frontend and backend. Not merely because the repository has both.",
    "DATA": "Data model or data ownership.",
    "DATABASE": "Schema, constraints, indexes, queries at the database level.",
    "API_CONTRACT": "A request or response shape other components depend on.",
    "EVENTING": "Events, queues, asynchronous messaging.",
    "SECURITY": "The change is itself security work.",
    "PERFORMANCE": "The change is itself performance work.",
    "INFRASTRUCTURE": "IaC, cloud or PaaS, Kubernetes, runtime configuration, IAM or network.",
    "CI_CD": "Build, test or deploy workflow mechanics.",
    "DEPLOYMENT": "How and where the system is deployed.",
    "MIGRATION": "Old and new states coexist, or staged compatibility matters.",
    "OBSERVABILITY": "Logging, metrics, tracing, alerting.",
    "TEST_ONLY": "Production behavior is unchanged; only tests or evidence are modified.",
    "CONFIGURATION": "Application configuration.",
    "DEPENDENCY": "Third-party dependency added, removed or upgraded.",
}
TRIGGERS = {
    "BEHAVIORAL": (
        "new user or business behavior; changed validation; changed state transition; error or recovery behavior; "
        "multi-step workflow; browser-only interaction; changed test evidence for existing behavior",
        "QA",
    ),
    "ARCHITECTURE": (
        "new module or service boundary; new port or adapter abstraction; new shared or global state ownership; "
        "new transaction owner; new event architecture; new deployment topology; new compatibility seam",
        "the Architecture Review of the affected layer",
    ),
    "SECURITY": (
        "authn or authz; multi-tenancy; privilege; public entry point; sensitive or personal data; secret; webhook; "
        "file upload or download; user-generated HTML; redirect or callback; third-party script or provider; "
        "IAM or network; analytics or privacy",
        "Security",
    ),
    "DATA_INTEGRITY": (
        "database write semantics; financial or destructive operation; idempotency; concurrency; lost-update risk; "
        "schema constraint; data ownership",
        "QA",
    ),
    "MIGRATION": (
        "schema migration; dual read or write; backfill; compatibility facade; old and new version coexistence; "
        "platform migration",
        "Backend Architecture Review, QA and Infrastructure",
    ),
    "PERFORMANCE": (
        "accepted latency, throughput, Core Web Vitals, bundle or memory target; measured regression; "
        "large data growth; load or capacity requirement; known performance-sensitive path. "
        "Not merely because the code contains a loop",
        "Performance",
    ),
    "INFRASTRUCTURE": (
        "IaC; CI/CD; cloud runtime; Kubernetes; new environment variable or secret; deployment strategy; "
        "health or readiness; backup or recovery; autoscaling",
        "Infrastructure",
    ),
    "COMPATIBILITY": (
        "public API change; event or schema version; mixed-version deployment; client and server rollout order; "
        "backward compatibility",
        "QA",
    ),
    "USER_IMPACT": (
        "critical path; revenue or entitlement; destructive action; authentication; accessibility-critical interaction",
        "QA",
    ),
    "OPERABILITY": (
        "background job; queue or worker; reconciliation; alerting; runbook; startup or shutdown",
        "nothing by itself; Infrastructure becomes conditional",
    ),
}
LAYERS = ("backend", "frontend")

# Signals read from the changed files. They are added to the plan even when the
# classification omits them, so a small diff cannot hide them; each can only be
# dropped with an explicit, recorded --dismiss.
PATH_SIGNALS = (
    ("MIGRATION", "schema or migration file changed",
     lambda p: "/migrations/" in f"/{p}" or p.endswith((".sql", "schema.prisma")) or "/alembic/" in f"/{p}"),
    ("INFRASTRUCTURE", "CI/CD, container or infrastructure file changed",
     lambda p: p.startswith(".github/workflows/") or p.endswith((".tf", ".tfvars"))
     or Path(p).name in ("Dockerfile", "docker-compose.yml", "docker-compose.yaml", ".gitlab-ci.yml", "Jenkinsfile")
     or p.startswith(("k8s/", "kubernetes/", "helm/", "terraform/", "infra/"))),
)

GATE_DECISIONS = ("PASS", "PASS_WITH_CONDITIONS", "CHANGES_REQUIRED", "BLOCKED")
PASSING = ("PASS", "PASS_WITH_CONDITIONS")

# Files that define how the project's work is judged. The harness's own files are
# always protected from agent edits; quality configuration is protected unless the
# delivery profile is lean.
HARNESS_PROTECTED = (".harness/core/", ".harness/bin/", ".harness/agents/", ".harness/evals/")
HARNESS_PROTECTED_FILES = (".harness/harness.config.yaml", ".harness/install-state.json", ".claude/settings.json")
GENERATED_STATE = ("routing-plan.yaml", "gates.json")
QUALITY_CONFIG_NAMES = (
    ".eslintignore", ".prettierignore", "biome.json", "biome.jsonc", "ruff.toml", ".ruff.toml", ".flake8",
    "mypy.ini", ".pylintrc", "tox.ini", "pytest.ini", ".pre-commit-config.yaml", ".gitlab-ci.yml", "Jenkinsfile",
    ".golangci.yml", ".golangci.yaml", ".rubocop.yml", "lefthook.yml", ".editorconfig",
)
QUALITY_CONFIG_PREFIXES = (
    "eslint.config.", ".eslintrc", ".prettierrc", "prettier.config.", "tsconfig", "jest.config.", "vitest.config.",
    "playwright.config.", "cypress.config.", "stylelint.config.", ".stylelintrc",
)
QUALITY_CONFIG_DIRS = (".github/workflows/", ".husky/", ".circleci/")


def protection(path: str) -> tuple[str, str] | None:
    """Return (kind, why) if a project-relative path is protected, else None."""
    path = path.replace("\\", "/")
    if path.startswith("./"):
        path = path[2:]
    name = path.rsplit("/", 1)[-1]
    if path.startswith(HARNESS_PROTECTED) or path in HARNESS_PROTECTED_FILES:
        return "harness", "it is part of the harness that judges this work"
    if path.startswith(".harness/runtime/") and name in GENERATED_STATE:
        return "harness", "it is written only by .harness/bin/route.py"
    if name in QUALITY_CONFIG_NAMES or name.startswith(QUALITY_CONFIG_PREFIXES) or path.startswith(QUALITY_CONFIG_DIRS):
        return "quality-config", "it configures the checks (lint, types, tests, CI) that judge this work"
    return None


IMPLEMENTING = ("IMPLEMENTATION", "REMEDIATION", "MIGRATION", "RELEASE_ONLY")
NO_CODE = ("DISCOVERY", "ARCHITECTURE_ONLY")
BACKEND_SIDE = ("BACKEND", "FULL_STACK", "DATABASE", "DATA", "EVENTING", "MIGRATION", "SOFTWARE_ARCHITECTURE")
FRONTEND_SIDE = ("FRONTEND", "FULL_STACK")
QA_TRIGGERS = ("BEHAVIORAL", "DATA_INTEGRITY", "MIGRATION", "COMPATIBILITY", "USER_IMPACT")
INFRA_SCOPES = ("INFRASTRUCTURE", "CI_CD", "DEPLOYMENT")


class RouteError(Exception):
    pass


# --------------------------------------------------------------------------- routing rules


def route(work_mode: str, scopes: list[str], triggers: list[dict]) -> dict[str, tuple[str, str, str]]:
    """Return {agent: (applicability, reason, trigger_source)}."""
    scope_set = set(scopes)
    dims = {t["dimension"] for t in triggers}
    implementing = work_mode in IMPLEMENTING
    no_code = work_mode in NO_CODE
    review_only = work_mode == "REVIEW_ONLY"
    test_only = "TEST_ONLY" in scope_set
    docs_only = scope_set <= {"DOCUMENTATION", "REQUIREMENTS"}
    backend = bool(scope_set & {"BACKEND", "FULL_STACK"})
    frontend = bool(scope_set & set(FRONTEND_SIDE))
    backend_side = bool(scope_set & set(BACKEND_SIDE))

    def layers_of(dimension: str) -> set[str]:
        """Layers a trigger applies to; an unqualified trigger applies to every layer in scope."""
        found: set[str] = set()
        for trigger in triggers:
            if trigger["dimension"] == dimension:
                found |= {trigger["layer"]} if trigger.get("layer") else set(LAYERS)
        return found

    out: dict[str, tuple[str, str, str]] = {}

    # Validator
    if no_code:
        out["validator"] = ("NOT_APPLICABLE", f"{work_mode} work has no implementation to check mechanically.", "")
    elif docs_only:
        out["validator"] = ("NOT_TRIGGERED", "Documentation-only change.", "")
    elif review_only:
        out["validator"] = ("CONDITIONAL", "Review of existing code; run only if mechanical evidence is requested.", "REVIEW_ONLY")
    else:
        out["validator"] = ("REQUIRED", "Implementation, tests or configuration changed; mechanical checks run first.", work_mode)

    # Code reviews
    for agent, in_scope, label in (
        ("backend-code-review", backend, "backend"),
        ("frontend-code-review", frontend, "frontend"),
    ):
        if not in_scope:
            out[agent] = ("NOT_APPLICABLE", f"No {label} scope in this change.", "")
        elif no_code:
            out[agent] = ("NOT_APPLICABLE", f"{work_mode} work has no {label} implementation to review.", "")
        elif test_only:
            out[agent] = ("NOT_TRIGGERED", f"Test-only change; {label} production behavior is unchanged.", "")
        elif docs_only:
            out[agent] = ("NOT_TRIGGERED", "Documentation-only change.", "")
        elif review_only:
            out[agent] = ("CONDITIONAL", f"Review-only work; run if a {label} code review was requested.", "REVIEW_ONLY")
        else:
            out[agent] = ("REQUIRED", f"{label.capitalize()} production behavior changed.", label.upper())

    # Architecture reviews
    architecture_layers = layers_of("ARCHITECTURE")
    for agent, in_scope, layer in (
        ("backend-architecture-review", backend_side, "backend"),
        ("frontend-architecture-review", frontend, "frontend"),
    ):
        if not in_scope:
            out[agent] = ("NOT_APPLICABLE", f"No {layer} scope in this change.", "")
        elif layer == "backend" and "MIGRATION" in dims and not no_code:
            out[agent] = ("REQUIRED", "Migration seam: compatibility and data ownership need architecture review.", "MIGRATION")
        elif layer in architecture_layers:
            if no_code:
                out[agent] = ("CONDITIONAL", "Design work; validate with architecture skills, review once implemented.", "ARCHITECTURE")
            else:
                out[agent] = ("REQUIRED", f"Architecture trigger on the {layer} layer.", "ARCHITECTURE")
        elif layer == "backend" and "DATA_INTEGRITY" in dims and not no_code:
            out[agent] = ("CONDITIONAL", "Data-integrity risk; required only if transaction or data ownership changed.", "DATA_INTEGRITY")
        else:
            out[agent] = ("NOT_TRIGGERED", f"No architecture trigger on the {layer} layer.", "")

    # QA
    qa_dims = sorted(dims & set(QA_TRIGGERS))
    if no_code:
        out["qa"] = ("NOT_APPLICABLE", f"{work_mode} work has no implemented behavior to test.", "")
    elif review_only:
        out["qa"] = ("CONDITIONAL", "Review-only work; run if test-evidence review was requested.", "REVIEW_ONLY")
    elif test_only:
        out["qa"] = ("REQUIRED", "Test evidence changed; QA judges whether it is sufficient and meaningful.", "TEST_ONLY")
    elif qa_dims:
        out["qa"] = ("REQUIRED", "Accepted behavior or its risk profile changed.", "+".join(qa_dims))
    else:
        out["qa"] = ("NOT_TRIGGERED", "No behavioral, data-integrity, migration, compatibility or user-impact trigger.", "")

    # Performance
    if "PERFORMANCE" in dims:
        state = "CONDITIONAL" if no_code else "REQUIRED"
        out["performance"] = (state, "Performance trigger declared.", "PERFORMANCE")
    else:
        out["performance"] = ("NOT_TRIGGERED", "No performance target, measured regression, or performance-sensitive path.", "")

    # Security
    if "SECURITY" in dims:
        state = "CONDITIONAL" if work_mode == "DISCOVERY" else "REQUIRED"
        out["security"] = (state, "Security trigger declared; change size does not reduce this.", "SECURITY")
    else:
        out["security"] = ("NOT_TRIGGERED", "No trust-boundary, authorization, tenancy, secret or sensitive-data trigger.", "")

    # Infrastructure
    infra_sources = sorted((dims & {"INFRASTRUCTURE", "MIGRATION"}) | (scope_set & set(INFRA_SCOPES)))
    if infra_sources:
        state = "CONDITIONAL" if no_code else "REQUIRED"
        out["infrastructure"] = (state, "Infrastructure, CI/CD, deployment or migration-rollout concern.", "+".join(infra_sources))
    elif "OPERABILITY" in dims:
        out["infrastructure"] = ("CONDITIONAL", "Operability concern; required only if runtime or deployment changes.", "OPERABILITY")
    else:
        out["infrastructure"] = ("NOT_TRIGGERED", "No infrastructure, CI/CD, deployment or migration trigger.", "")

    # Detail Analyst and Reviewer
    if implementing and not test_only and not docs_only:
        out["detail-analyst"] = ("REQUIRED", "Cross-artifact completeness before Reviewer.", "PRE_PR_READINESS")
    else:
        out["detail-analyst"] = ("CONDITIONAL", "Run only if spec, test or documentation propagation is in question.", "")
    if implementing and not docs_only:
        out["reviewer"] = ("REQUIRED", "Integrates gate results before the Final Pre-PR Gate.", "PRE_PR_READINESS")
    elif no_code:
        out["reviewer"] = ("NOT_TRIGGERED", f"{work_mode} work is not moving toward a pull request.", "")
    else:
        out["reviewer"] = ("CONDITIONAL", "Run if the work is moving toward the pre-PR path.", "")
    return out


def dependencies(states: dict[str, str]) -> dict[str, list[str]]:
    """Minimum ordering: Validator, then specialists, then Detail Analyst, then Reviewer."""
    required = [a for a in AGENTS if states[a] == "REQUIRED"]
    specialists = [a for a in required if a in SPECIALISTS]
    deps: dict[str, list[str]] = {a: [] for a in AGENTS}
    for agent in specialists:
        deps[agent] = ["validator"] if "validator" in required else []
    deps["detail-analyst"] = specialists or (["validator"] if "validator" in required else [])
    deps["reviewer"] = [a for a in required if a != "reviewer"]
    return deps


# --------------------------------------------------------------------------- change identity


def git(root: Path, *arguments: str) -> str | None:
    try:
        proc = subprocess.run(["git", *arguments], cwd=root, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return proc.stdout if proc.returncode == 0 else None


def is_harness_path(path: str) -> bool:
    return path.startswith(".harness/runtime/")


def base_commit(root: Path) -> str | None:
    """Where the change starts: the fork point from the default branch, else HEAD."""
    head = (git(root, "rev-parse", "HEAD") or "").strip()
    if not head:
        return None
    for ref in ("origin/HEAD", "origin/main", "origin/master", "main", "master"):
        fork = (git(root, "merge-base", "HEAD", ref) or "").strip()
        if fork and fork != head:
            return fork
    return head


def change_identity(root: Path) -> tuple[dict, list[str]]:
    """Identify the change by a digest of the content of every file it touches.

    The change is everything that differs from the base commit, committed or
    not, plus untracked files. Committing the same content does not change the
    identity; editing any file does.
    """
    status = git(root, "status", "--porcelain", "--untracked-files=all")
    if status is None:
        return {"type": "unversioned", "value": "none"}, []
    paths = {
        line[3:].split(" -> ")[-1].strip().strip('"')
        for line in status.splitlines() if line[:2] == "??"
    }
    base = base_commit(root)
    if base:
        paths |= set((git(root, "diff", "--name-only", base) or "").split("\n"))
    else:  # no commits yet: everything staged is the change
        paths |= set((git(root, "diff", "--name-only", "--cached") or "").split("\n"))
    paths = sorted(p for p in paths if p and not is_harness_path(p))
    if not paths:
        return {"type": "clean", "value": base or "none"}, []
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.encode() + b"\0")
        file = root / path
        digest.update(file.read_bytes() if file.is_file() else b"<deleted>")
        digest.update(b"\0")
    return {"type": "content", "value": "sha256:" + digest.hexdigest()[:16]}, paths


def detect_signals(paths: list[str]) -> list[dict]:
    signals = []
    for dimension, description, matches in PATH_SIGNALS:
        hits = [p for p in paths if matches(p)]
        if hits:
            shown = ", ".join(hits[:3]) + (f" and {len(hits) - 3} more" if len(hits) > 3 else "")
            signals.append({"dimension": dimension, "evidence": f"{description}: {shown}"})
    return signals


# --------------------------------------------------------------------------- plan file format
# Block-style YAML in which every scalar is a JSON literal. Any YAML parser
# reads it; this module reads it back without one.


def emit(value: object, indent: int = 0) -> list[str]:
    pad = "  " * indent
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{pad}{key}:")
                lines += emit(item, indent + 1)
            else:
                lines.append(f"{pad}{key}: {json.dumps(item, ensure_ascii=False)}")
        return lines
    lines = []
    for item in value:  # list
        if isinstance(item, dict) and item:
            body = emit(item, indent + 1)
            lines.append(f"{pad}- {body[0].lstrip()}")
            lines += body[1:]
        else:
            lines.append(f"{pad}- {json.dumps(item, ensure_ascii=False)}")
    return lines


def parse(text: str) -> dict:
    lines = [line.rstrip("\n") for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    position = 0

    def depth(line: str) -> int:
        spaces = len(line) - len(line.lstrip(" "))
        if spaces % 2:
            raise RouteError(f"unexpected indentation: {line!r}")
        return spaces // 2

    def scalar(raw: str) -> object:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise RouteError(f"value is not a JSON literal: {raw!r}") from None

    def key_value(body: str) -> tuple[str, str]:
        key, separator, rest = body.partition(":")
        if not separator or not key or " " in key:
            raise RouteError(f"expected `key: value`: {body!r}")
        return key, rest.strip()

    def block(level: int) -> object:
        nonlocal position
        if lines[position].lstrip().startswith("- "):
            items = []
            while position < len(lines) and depth(lines[position]) == level and lines[position].lstrip().startswith("- "):
                body = lines[position].lstrip()[2:]
                if body.startswith(("{", "[", '"')) or body in ("null", "true", "false") or body[:1].isdigit() or body[:1] == "-":
                    items.append(scalar(body))
                    position += 1
                else:  # mapping item: rewrite the first line as a nested key
                    lines[position] = "  " * (level + 1) + body
                    items.append(block(level + 1))
            return items
        mapping: dict = {}
        while position < len(lines) and depth(lines[position]) == level and not lines[position].lstrip().startswith("- "):
            key, rest = key_value(lines[position].strip())
            position += 1
            if rest:
                mapping[key] = scalar(rest)
            elif position < len(lines) and depth(lines[position]) > level:
                mapping[key] = block(level + 1)
            else:
                raise RouteError(f"key {key!r} has no value")
        return mapping

    if not lines:
        raise RouteError("plan is empty")
    result = block(0)
    if position != len(lines) or not isinstance(result, dict):
        raise RouteError(f"could not read the plan near: {lines[min(position, len(lines) - 1)]!r}")
    return result


def digest_of(plan: dict) -> str:
    body = {key: value for key, value in plan.items() if key != "plan_digest"}
    return "sha256:" + hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:32]


# --------------------------------------------------------------------------- commands


def parse_trigger(raw: str) -> dict:
    head, separator, evidence = raw.partition("=")
    dimension, _, layer = head.strip().partition("@")
    dimension, layer, evidence = dimension.strip().upper(), layer.strip().lower(), evidence.strip()
    if dimension not in TRIGGERS:
        raise RouteError(f"unknown trigger dimension {dimension!r}. Known: {', '.join(TRIGGERS)}")
    if layer and layer not in LAYERS:
        raise RouteError(f"unknown layer {layer!r} in {raw!r}. Known: {', '.join(LAYERS)}")
    if not separator or not evidence:
        raise RouteError(f"trigger {dimension} needs evidence: --trigger \"{dimension}=what in the change causes it\"")
    trigger = {"dimension": dimension, "evidence": evidence, "source": "declared"}
    if layer:
        trigger["layer"] = layer
    return trigger


def build_plan(args: argparse.Namespace, root: Path) -> dict:
    work_mode = args.work_mode.upper()
    if work_mode not in WORK_MODES:
        raise RouteError(f"unknown work mode {work_mode!r}. Known: {', '.join(WORK_MODES)}")
    scopes = []
    for scope in args.scope or []:
        scope = scope.upper()
        if scope not in SCOPES:
            raise RouteError(f"unknown scope {scope!r}. Known: {', '.join(SCOPES)}")
        if scope not in scopes:
            scopes.append(scope)
    if not scopes:
        raise RouteError("at least one --scope is required")
    triggers = [parse_trigger(raw) for raw in args.trigger or []]

    dismissed = []
    for raw in args.dismiss or []:
        dimension, separator, reason = raw.partition("=")
        dimension = dimension.strip().upper()
        if dimension not in TRIGGERS or not separator or not reason.strip():
            raise RouteError(f"--dismiss needs a known dimension and a reason: --dismiss \"MIGRATION=why it does not apply\"")
        dismissed.append({"dimension": dimension, "reason": reason.strip()})

    identity, paths = change_identity(root)
    declared = {t["dimension"] for t in triggers}
    dismissed_dims = {d["dimension"] for d in dismissed}
    for signal in detect_signals(paths):
        if signal["dimension"] not in declared and signal["dimension"] not in dismissed_dims and work_mode not in NO_CODE:
            triggers.append({**signal, "source": "detected"})
    unused = sorted(dismissed_dims - {s["dimension"] for s in detect_signals(paths)})
    if unused:
        raise RouteError(f"--dismiss given for {', '.join(unused)}, but nothing in the changed files signals it")

    decisions = route(work_mode, scopes, triggers)
    states = {agent: decisions[agent][0] for agent in AGENTS}
    deps = dependencies(states)
    plan = {
        "routing_plan_version": PLAN_VERSION,
        "harness_contract_version": CONTRACT_VERSION,
        "generated_by": "route.py",
        "change_identity": {**identity, "changed_files": len(paths)},
        "work_mode": work_mode,
        "scopes": scopes,
        "risk_triggers": triggers,
        "dismissed_signals": dismissed,
        "accepted_behavior_sources": list(args.behavior_source or []),
        "existing_gate_results": [],
        "agents": [
            {
                "agent": agent,
                "applicability": decisions[agent][0],
                "reason": decisions[agent][1],
                "trigger_source": decisions[agent][2],
                "required_inputs": [],
                "expected_output": f"{agent}-report.md",
                "minimal_dependencies": deps[agent] if decisions[agent][0] == "REQUIRED" else [],
            }
            for agent in AGENTS
        ],
        "new_dynamic_triggers": [],
        "deferred_questions": [],
        "notes": list(args.note or []),
    }
    plan["plan_digest"] = digest_of(plan)
    return plan


def validate(plan: dict) -> list[str]:
    problems = []
    if plan.get("plan_digest") != digest_of(plan):
        problems.append("plan_digest does not match the content: the plan was edited by hand. Regenerate it with `route.py plan`.")
    if plan.get("work_mode") not in WORK_MODES:
        problems.append(f"unknown work_mode {plan.get('work_mode')!r}")
    for scope in plan.get("scopes") or []:
        if scope not in SCOPES:
            problems.append(f"unknown scope {scope!r}")
    triggers = plan.get("risk_triggers") or []
    for trigger in triggers:
        if not isinstance(trigger, dict) or trigger.get("dimension") not in TRIGGERS or not trigger.get("evidence"):
            problems.append(f"malformed risk trigger: {trigger!r}")
    agents = plan.get("agents") or []
    listed = [entry.get("agent") for entry in agents if isinstance(entry, dict)]
    if listed != list(AGENTS):
        problems.append("agents must list every harness agent exactly once, in order")
    elif not problems:
        expected = route(plan["work_mode"], plan["scopes"], triggers)
        for entry in agents:
            if entry.get("applicability") != expected[entry["agent"]][0]:
                problems.append(
                    f"{entry['agent']} is {entry.get('applicability')} but the routing rules give {expected[entry['agent']][0]}"
                )
    return problems


def cmd_vocabulary(_: argparse.Namespace) -> int:
    print("WORK MODES (choose one)")
    for name, text in WORK_MODES.items():
        print(f"  {name}: {text}")
    print("\nSCOPES (choose every one that applies)")
    for name, text in SCOPES.items():
        print(f"  {name}: {text}")
    print("\nRISK TRIGGERS (declare each one the change causes, with evidence from the change)")
    for name, (signals, activates) in TRIGGERS.items():
        print(f"  {name}: {signals}. Activates {activates}.")
    print("\nChange size is not a trigger. A one-line change to an authorization check is a SECURITY trigger.")
    print("Qualify ARCHITECTURE with a layer when only one is affected: --trigger \"ARCHITECTURE@backend=...\"")
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    plan = build_plan(args, root)
    out = Path(args.out) if args.out else root / ".harness/runtime" / args.runtime / "routing-plan.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(emit(plan)) + "\n", encoding="utf-8")
    try:
        shown = out.relative_to(root)
    except ValueError:
        shown = out
    print(f"Routing plan written to {shown}")
    print(f"Change identity: {plan['change_identity']['type']} {plan['change_identity']['value']}")
    for trigger in plan["risk_triggers"]:
        if trigger["source"] == "detected":
            print(f"Added from the changed files: {trigger['dimension']} ({trigger['evidence']})")
    for entry in plan["agents"]:
        print(f"  {entry['applicability']:15} {entry['agent']:30} {entry['reason']}")
    return 0


def state_dir(root: Path, runtime: str) -> Path:
    return root / ".harness/runtime" / runtime


def load_gates(root: Path, runtime: str) -> dict:
    path = state_dir(root, runtime) / "gates.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("gates", {})
    except (json.JSONDecodeError, AttributeError):
        raise RouteError(f"{path} is not readable; it is written only by `route.py gate`") from None


def save_gates(root: Path, runtime: str, gates: dict) -> None:
    path = state_dir(root, runtime) / "gates.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"gates": gates}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def cmd_gate(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    identity, _ = change_identity(root)
    gates = load_gates(root, args.runtime)
    if args.carry_forward:
        previous = gates.get(args.agent)
        if not previous or previous["decision"] not in PASSING:
            raise RouteError(f"{args.agent} has no passing result to carry forward; run the gate instead")
        if args.decision or args.report or args.condition:
            raise RouteError("--carry-forward keeps the recorded decision; do not combine it with --decision, --report or --condition")
        if previous["change_identity"] == identity["value"]:
            print(f"{args.agent}: already recorded for the current change")
            return 0
        previous.setdefault("carried_forward", []).append({"from": previous["change_identity"], "reason": args.carry_forward})
        previous["change_identity"] = identity["value"]
        save_gates(root, args.runtime, gates)
        print(f"{args.agent}: {previous['decision']} carried forward to {identity['value']}")
        return 0
    if not args.decision:
        raise RouteError(f"--decision is required. Known: {', '.join(GATE_DECISIONS)}")
    if not args.report:
        raise RouteError("--report is required: a gate result without its report is not evidence")
    report = (root / args.report) if not Path(args.report).is_absolute() else Path(args.report)
    if not report.is_file() or not report.read_text(encoding="utf-8", errors="replace").strip():
        raise RouteError(f"report {args.report} does not exist or is empty")
    conditions = [c.strip() for c in args.condition or [] if c.strip()]
    if args.decision == "PASS_WITH_CONDITIONS" and not conditions:
        raise RouteError("PASS_WITH_CONDITIONS needs at least one --condition")
    if args.decision == "PASS" and conditions:
        raise RouteError("PASS takes no --condition; use PASS_WITH_CONDITIONS")
    try:
        shown = report.resolve().relative_to(root).as_posix()
    except ValueError:
        shown = str(report)
    gates[args.agent] = {
        "decision": args.decision,
        "change_identity": identity["value"],
        "report": shown,
        "report_sha256": hashlib.sha256(report.read_bytes()).hexdigest()[:16],
        "conditions": conditions,
    }
    save_gates(root, args.runtime, gates)
    print(f"{args.agent}: {args.decision} recorded for {identity['value']}")
    return 0


def readiness(root: Path, runtime: str) -> tuple[str, list[str], list[str]]:
    """Return (status, blockers, conditions) for the Final Pre-PR Gate.

    Precedence: a changes-required or blocked gate, then a missing or stale
    required gate, then conditions, then pass. Nothing is averaged.
    """
    plan_path = state_dir(root, runtime) / "routing-plan.yaml"
    if not plan_path.exists():
        return "PRE_PR_BLOCKED", ["no routing plan; run `route.py plan` for this change"], []
    try:
        plan = parse(plan_path.read_text(encoding="utf-8"))
    except RouteError as error:
        return "PRE_PR_BLOCKED", [f"routing plan was not generated by route.py ({error})"], []
    problems = validate(plan)
    if problems:
        return "PRE_PR_BLOCKED", [f"routing plan is invalid: {problem}" for problem in problems], []
    identity, paths = change_identity(root)
    if plan["change_identity"]["value"] != identity["value"]:
        return "PRE_PR_BLOCKED", [
            "the change was edited after the routing plan was written; rerun `route.py plan`, then rerun the gates "
            "the edit invalidates and carry the others forward with `route.py gate --carry-forward`"
        ], []
    gates = load_gates(root, runtime)
    blockers, missing, conditions = [], [], []
    for entry in plan["agents"]:
        if entry["applicability"] != "REQUIRED":
            continue
        agent, result = entry["agent"], gates.get(entry["agent"])
        if result is None:
            missing.append(f"{agent}: required gate has no recorded result")
        elif result["change_identity"] != identity["value"]:
            missing.append(f"{agent}: result is stale, it was recorded for an earlier version of the change")
        elif result["decision"] not in PASSING:
            blockers.append(f"{agent}: {result['decision']} (see {result['report']})")
        else:
            report = root / result["report"]
            if not report.is_file() or hashlib.sha256(report.read_bytes()).hexdigest()[:16] != result["report_sha256"]:
                missing.append(f"{agent}: report {result['report']} is missing or was changed after the result was recorded")
            conditions += [f"{agent}: {condition}" for condition in result["conditions"]]
            conditions += [f"{agent}: carried forward ({c['reason']})" for c in result.get("carried_forward", [])]
    judged = sorted(p for p in paths if (protection(p) or ("", ""))[0] == "quality-config")
    if judged:
        conditions.append("the change edits the checks that judge it; a person must review: " + ", ".join(judged))
    if blockers or missing:
        return "PRE_PR_BLOCKED", blockers + missing, conditions
    return ("PRE_PR_PASS_WITH_CONDITIONS" if conditions else "PRE_PR_PASS"), [], conditions


def cmd_ready(args: argparse.Namespace) -> int:
    status, blockers, conditions = readiness(Path(args.project).resolve(), args.runtime)
    print(status)
    for blocker in blockers:
        print(f"  blocker: {blocker}")
    for condition in conditions:
        print(f"  condition: {condition}")
    return 1 if status == "PRE_PR_BLOCKED" else 0


def cmd_check(args: argparse.Namespace) -> int:
    path = Path(args.plan)
    if not path.exists():
        print(f"ROUTING PLAN: FAIL\n  {path} does not exist")
        return 1
    try:
        plan = parse(path.read_text(encoding="utf-8"))
    except RouteError as error:
        print(f"ROUTING PLAN: FAIL\n  not a plan generated by route.py ({error})")
        return 1
    problems = validate(plan)
    if problems:
        print("ROUTING PLAN: FAIL")
        for problem in problems:
            print(f"  {problem}")
        return 1
    required = [entry["agent"] for entry in plan["agents"] if entry["applicability"] == "REQUIRED"]
    print(f"ROUTING PLAN: PASS ({len(required)} required gates: {', '.join(required) or 'none'})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="route.py", description="Deterministic router for the harness.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("vocabulary", help="List work modes, scopes and risk triggers").set_defaults(func=cmd_vocabulary)

    plan = sub.add_parser("plan", help="Write the routing plan for the current change")
    plan.add_argument("--runtime", required=True, choices=RUNTIMES)
    plan.add_argument("--work-mode", required=True)
    plan.add_argument("--scope", action="append", help="repeatable")
    plan.add_argument("--trigger", action="append", help='repeatable: "DIMENSION=evidence" or "DIMENSION@layer=evidence"')
    plan.add_argument("--dismiss", action="append", help='repeatable: "DIMENSION=reason" to drop a signal detected from the changed files')
    plan.add_argument("--behavior-source", action="append", help="repeatable: file that defines the accepted behavior")
    plan.add_argument("--note", action="append")
    plan.add_argument("--project", default=".")
    plan.add_argument("--out")
    plan.set_defaults(func=cmd_plan)

    check = sub.add_parser("check", help="Validate a routing plan")
    check.add_argument("plan")
    check.set_defaults(func=cmd_check)

    gate = sub.add_parser("gate", help="Record a gate result for the current change")
    gate.add_argument("--runtime", required=True, choices=RUNTIMES)
    gate.add_argument("--agent", required=True, choices=AGENTS)
    gate.add_argument("--decision", choices=GATE_DECISIONS)
    gate.add_argument("--report", help="the specialist's report file")
    gate.add_argument("--condition", action="append", help="repeatable; required for PASS_WITH_CONDITIONS")
    gate.add_argument("--carry-forward", metavar="REASON",
                      help="keep a passing result after an edit that does not invalidate it, with the reason")
    gate.add_argument("--project", default=".")
    gate.set_defaults(func=cmd_gate)

    ready = sub.add_parser("ready", help="Final Pre-PR Gate: is every required gate passed for the current change?")
    ready.add_argument("--runtime", required=True, choices=RUNTIMES)
    ready.add_argument("--project", default=".")
    ready.set_defaults(func=cmd_ready)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except RouteError as error:
        print(f"route.py: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
