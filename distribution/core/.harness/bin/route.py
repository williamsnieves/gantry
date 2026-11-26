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
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scan  # noqa: E402

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
        "the change alters how the system decides who may do what: authentication or authorization logic, "
        "a tenant-isolation rule, a privilege or role; or it opens something new: a public entry point, a webhook, "
        "file upload or download, a redirect or callback, a third-party script or provider, rendering of "
        "user-generated HTML, IAM or network exposure; or it newly stores, logs or sends sensitive or personal "
        "data or a secret. Not merely because the code runs behind authentication or reads tenant-scoped data: "
        "a validated parameter added to an existing protected endpoint, with its access rules unchanged, is not a trigger",
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

# How much is settled before building. The lane follows the triggers, not the size of the work.
LANES = {
    "NONE": "Nothing is being built.",
    "DIRECT": "Build it, then review it. No specification is needed.",
    "SPEC": "Write the acceptance criteria and the slices before building.",
    "DESIGN": "Write the specification with its design, and have the user approve it before building.",
}
DESIGN_TRIGGERS = ("ARCHITECTURE", "SECURITY", "DATA_INTEGRITY", "MIGRATION", "COMPATIBILITY")
NOT_BUILDING = ("DISCOVERY", "REVIEW_ONLY")
# How capable a model each gate needs. The tier follows the gate's job and the lane, so it follows the risk:
# nothing is saved on a change in the DESIGN lane or on the gates that judge security, architecture and the whole.
TIERS = {
    "fast": "runs the project's checks and reports them",
    "standard": "reviews code against known rules",
    "deep": "judges risk, design or the change as a whole",
}
DEEP_AGENTS = ("security", "backend-architecture-review", "frontend-architecture-review", "reviewer")
# Which model each tier runs on, per runtime. The user's file; empty means the session's own model.
MODELS_FILE = ".harness/models.yaml"

# Changes that cannot simply be merged: something has to happen in order, be verified and be undoable.
ROLLOUT_TRIGGERS = ("MIGRATION", "INFRASTRUCTURE", "DATA_INTEGRITY")
ROLLOUT_MODES = ("MIGRATION", "RELEASE_ONLY")

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
HARNESS_PROTECTED = (".harness/core/", ".harness/bin/", ".harness/agents/", ".harness/evals/", ".harness/receipts/")
HARNESS_PROTECTED_FILES = (".harness/harness.config.yaml", ".harness/project.yaml", ".harness/models.yaml", ".harness/install-state.json",
                           ".harness/runtime/approvals.json", ".claude/settings.json")
# Written by `spec.py approve`: which specifications a person approved, by content.
APPROVALS_FILE = ".harness/runtime/approvals.json"
# Written by `route.py ready` when the project keeps review receipts: one small file per reviewed change, named after
# the change's digest and committed with it, so `route.py verify` can tell in CI that what is merged is what was reviewed.
RECEIPTS_DIR = ".harness/receipts/"
READY = ("PRE_PR_PASS", "PRE_PR_PASS_WITH_CONDITIONS")

# Every guardrail, by the phase it acts in: (phase, what it guarantees, what enforces it on every runtime,
# what a runtime with command hooks adds). `route.py guardrails` prints this table.
GUARDRAILS = (
    ("any", "the harness's files and routing state are not edited by the agent",
     "the final gate rejects a routing plan or a report that was changed by hand", "the edit is denied"),
    ("specify", "how much is settled before building follows the risk, not the size",
     "`route.py lane`; `route.py plan` computes the lane again from the change itself", ""),
    ("specify", "a specification has its criteria, and each criterion is delivered by a slice",
     "`spec.py check`", ""),
    ("specify", "a design is approved by a person",
     "the final gate carries a condition until `spec.py approve` was run on the current text",
     "`spec.py approve` asks the person to confirm; a reviewing agent cannot run it"),
    ("build", "a failing check is fixed in the code, not by weakening the check",
     "the final gate carries a condition naming any lint, type, test or CI configuration the change edits",
     "the edit and `--no-verify` are denied (not in the lean profile)"),
    ("build", "a secret does not leave in the change",
     "`scan.py` reads every added line; the final gate blocks on a credential in a provider's format or a private key, "
     "and carries a condition for anything that may be one", "`git commit` and `git push` are denied while one is there"),
    ("build", "code that needs a security reviewer gets one",
     "a risky pattern in the added lines adds the SECURITY trigger to the routing plan, which routes the Security gate", ""),
    ("review", "a reviewer reports and does not fix; a report is what the reviewer wrote",
     "the final gate rejects a report changed after its result was recorded",
     "a reviewer can write only its own report, and nobody else can write it"),
    ("review", "each gate runs on the model its job and the change's risk call for, when the project maps tiers to models",
     "`route.py plan` records a tier per gate and `next:` names the model to launch", "the gate is launched on that model whatever was asked"),
    ("review", "the review stops at the first stage that does not pass",
     "`route.py next`; the final gate stays blocked", "launching a later gate is denied (not in the lean profile)"),
    ("review", "a risk a gate sees outside its own scope is not lost under its pass",
     "`route.py gate --trigger` records it; the router asks for the plan to be rerun with it, "
     "and the final gate carries a condition while no routed gate has judged it", ""),
    ("review", "a result counts only for the version of the change it judged",
     "results are tied to a digest of the change; an edit makes them stale", ""),
    ("release", "a pull request is opened only after every required gate passed",
     "`route.py ready` exits non-zero", "`gh pr create` is denied (not in the lean profile)"),
    ("release", "what is merged is the version that was reviewed, when the project keeps review receipts",
     "`route.py ready` writes a receipt named after the change's digest, committed with the change; "
     "`route.py verify`, run in CI, fails when the pull request's content has none", ""),
    ("release", "a change that moves data, schema or infrastructure ships with a written rollout: order, verification, undo",
     "`release.py check` blocks without a `## Rollout` section in the specification",
     "`gh pr merge` is denied while it blocks (not in the lean profile)"),
    ("release", "a change users will notice is in the changelog, when the project keeps one",
     "`release.py check` carries a condition", ""),
    ("operate", "what happened after shipping is written down, and a failure names the risk nobody declared",
     "`release.py record` appends to docs/releases.md; nothing forces it to be run", ""),
)
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
    return path.startswith((".harness/runtime/", RECEIPTS_DIR))


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


def change_identity(root: Path, base: str | None = None) -> tuple[dict, list[str]]:
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
    base = base or base_commit(root)
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


def scan_change(root: Path, paths: list[str]) -> dict[str, list[dict]]:
    """What scan.py finds in the lines the change adds. A failure of the scan is reported, never hidden."""
    try:
        return scan.findings(root, paths, base_commit(root))
    except Exception as error:  # the scan must not take the router down with it
        return {"secret": [], "allowed": [], "risky": [],
                "suspect": [{"what": f"the security scan could not run ({error!r})", "path": "scan.py", "line": 0}]}


def detect_signals(paths: list[str], root: Path | None = None) -> list[dict]:
    """Triggers the change itself shows: from the paths it touches and, with `root`, from the lines it adds."""
    signals = []
    risky = scan_change(root, paths)["risky"] if root else []
    if risky:
        signals.append({"dimension": "SECURITY", "evidence": "the security scan found " + scan.summary(risky)})
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


def lane(work_mode: str, triggers: list[dict]) -> tuple[str, str]:
    """Return (lane, why). Decided before any code exists, from the same vocabulary as the routing plan."""
    dimensions = [trigger["dimension"] for trigger in triggers]
    if work_mode in NOT_BUILDING:
        return "NONE", f"{work_mode} work changes nothing"
    design = [d for d in dimensions if d in DESIGN_TRIGGERS]
    if work_mode in ("MIGRATION", "ARCHITECTURE_ONLY"):
        return "DESIGN", f"{work_mode} work"
    if design:
        return "DESIGN", "trigger " + ", ".join(dict.fromkeys(design)) + ": a wrong choice here is expensive to undo"
    if dimensions:
        return "SPEC", "trigger " + ", ".join(dict.fromkeys(dimensions)) + ": the accepted behavior has to be written down to be tested"
    return "DIRECT", "no risk trigger: behavior, data and interfaces stay as they are"


def tier(agent: str, lane_name: str) -> str:
    """The model tier a gate runs on for a change in this lane."""
    if agent in DEEP_AGENTS:
        return "deep"
    if agent == "validator":
        return "standard" if lane_name == "DESIGN" else "fast"
    return "deep" if lane_name == "DESIGN" else "standard"


def configured_models(root: Path, runtime: str) -> dict[str, str]:
    """{tier: model} from the project's models file for this runtime; tiers left empty are absent."""
    try:
        text = (root / MODELS_FILE).read_text(encoding="utf-8")
    except OSError:
        return {}
    models, section = {}, None
    for line in text.splitlines():
        line = line.split("#", 1)[0].rstrip()
        header = re.fullmatch(r"([\w-]+):", line)
        entry = re.fullmatch(r"\s+(\w+):\s*[\"']?([^\"'\s]*)[\"']?", line)
        if header:
            section = header.group(1)
        elif entry and section == runtime and entry.group(1) in TIERS and entry.group(2):
            models[entry.group(1)] = entry.group(2)
    return models


def gate_models(root: Path, runtime: str) -> dict[str, str]:
    """{agent: model} for the required gates of the current plan whose tier has a model configured."""
    models = configured_models(root, runtime)
    if not models:
        return {}
    try:
        plan = parse((state_dir(root, runtime) / "routing-plan.yaml").read_text(encoding="utf-8"))
    except (OSError, RouteError):
        return {}
    return {e["agent"]: models[e["model_tier"]] for e in plan.get("agents", [])
            if e.get("applicability") == "REQUIRED" and e.get("model_tier") in models}


def needs_rollout(work_mode: str, triggers: list[dict]) -> str | None:
    """Why this change needs a written rollout, or None."""
    if work_mode in ROLLOUT_MODES:
        return f"{work_mode} work has to be rolled out"
    dimensions = [t.get("dimension") for t in triggers if isinstance(t, dict) and t.get("dimension") in ROLLOUT_TRIGGERS]
    if dimensions and work_mode not in NO_CODE + NOT_BUILDING:
        return "trigger " + ", ".join(dict.fromkeys(dimensions)) + " means this change has to be rolled out"
    return None


def cmd_lane(args: argparse.Namespace) -> int:
    work_mode = args.work_mode.upper()
    if work_mode not in WORK_MODES:
        raise RouteError(f"unknown work mode {work_mode!r}. Known: {', '.join(WORK_MODES)}")
    triggers = [parse_trigger(raw) for raw in args.trigger or []]
    name, why = lane(work_mode, triggers)
    print(f"lane: {name}")
    print(f"why: {why}")
    print(f"next: {LANES[name]}")
    if name in ("SPEC", "DESIGN"):
        rollout = " --rollout" if needs_rollout(work_mode, triggers) else ""
        print(f"spec: write docs/specs/<short-name>.md, then run `python3 .harness/bin/spec.py check docs/specs/<short-name>.md --lane {name}{rollout}`")
        if rollout:
            print("rollout: the specification needs a `## Rollout` section: the order it is deployed in, how it is verified "
                  "in production and how it is undone")
    return 0


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
    detected = detect_signals(paths, root)
    for signal in detected:
        if signal["dimension"] not in declared and signal["dimension"] not in dismissed_dims and work_mode not in NO_CODE:
            triggers.append({**signal, "source": "detected"})
    unused = sorted(dismissed_dims - {s["dimension"] for s in detected})
    if unused:
        raise RouteError(f"--dismiss given for {', '.join(unused)}, but nothing in the changed files signals it")

    decisions = route(work_mode, scopes, triggers)
    lane_name = lane(work_mode, triggers)[0]
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
        "lane": lane_name,
        "dismissed_signals": dismissed,
        "accepted_behavior_sources": list(args.behavior_source or []),
        "existing_gate_results": [],
        "agents": [
            {
                "agent": agent,
                "applicability": decisions[agent][0],
                "reason": decisions[agent][1],
                "trigger_source": decisions[agent][2],
                "model_tier": tier(agent, lane_name),
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
    if not problems and plan.get("lane") != lane(plan["work_mode"], triggers)[0]:
        problems.append(f"lane is {plan.get('lane')!r} but the work mode and triggers give {lane(plan['work_mode'], triggers)[0]}")
    agents = plan.get("agents") or []
    listed = [entry.get("agent") for entry in agents if isinstance(entry, dict)]
    if listed != list(AGENTS):
        problems.append("agents must list every harness agent exactly once, in order")
    elif not problems:
        expected = route(plan["work_mode"], plan["scopes"], triggers)
        for entry in agents:
            if entry.get("model_tier") != tier(entry["agent"], plan.get("lane", "")):
                problems.append(f"{entry['agent']} has model tier {entry.get('model_tier')!r} but the lane gives "
                                f"{tier(entry['agent'], plan.get('lane', ''))}")
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
    print(f"Lane: {plan['lane']}")
    scanned = scan_change(root, change_identity(root)[1])
    for kind, label in (("secret", "Secret in the change, the final gate will block"), ("suspect", "Possible credential")):
        if scanned[kind]:
            print(f"{label}: {scan.summary(scanned[kind])}")
    unspecified = missing_specification(plan, root)
    if unspecified:
        print(f"Note: {unspecified}")
    for trigger in plan["risk_triggers"]:
        if trigger["source"] == "detected":
            print(f"Added from the changed files: {trigger['dimension']} ({trigger['evidence']})")
    models = configured_models(root, args.runtime)
    for entry in plan["agents"]:
        on = ""
        if entry["applicability"] == "REQUIRED":
            on = f" [{entry['model_tier']}" + (f": {models[entry['model_tier']]}]" if entry["model_tier"] in models else "]")
        print(f"  {entry['applicability']:15} {entry['agent']:30} {entry['reason']}{on}")
    if not args.out:
        print(describe_next(root, args.runtime))
    return 0


def approved(root: Path, source: str) -> bool:
    """Whether a person approved this file as it is now."""
    try:
        recorded = json.loads((root / APPROVALS_FILE).read_text(encoding="utf-8")).get(Path(source).as_posix(), {})
        return recorded.get("sha256") == hashlib.sha256((root / source).read_bytes()).hexdigest()
    except (OSError, json.JSONDecodeError, AttributeError):
        return False


def missing_specification(plan: dict, root: Path) -> str | None:
    """A SPEC or DESIGN change is expected to name the file that says what it should do, and a design to be approved."""
    if plan.get("lane") not in ("SPEC", "DESIGN") or plan.get("work_mode") in NO_CODE:
        return None
    sources = plan.get("accepted_behavior_sources") or []
    existing = [source for source in sources if (root / source).is_file()]
    if not existing:
        given = f"none of {', '.join(sources)} exists" if sources else "no --behavior-source was given"
        return (f"lane {plan['lane']} but {given}: the accepted behavior was not written down before building, "
                "so the gates judged the change against the request alone")
    if plan["lane"] == "DESIGN" and not any(approved(root, source) for source in existing):
        return (f"lane DESIGN but no person approved {', '.join(existing)} as it is now; a person must read the design, "
                f"then run `python3 .harness/bin/spec.py approve {existing[0]}`")
    return None


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


def next_step(root: Path, runtime: str) -> tuple[str, list[str], list[str]]:
    """What to do after the results recorded so far: ("RUN", agents, []), ("STOP", rejecting, not run) or ("READY", [], []).

    Gates run in stages: Validator, the specialists, Detail Analyst, Reviewer.
    A stage that ends with a gate demanding changes stops the review, because
    the later stages would judge a change that has to be edited anyway.
    """
    plan_path = state_dir(root, runtime) / "routing-plan.yaml"
    if not plan_path.exists():
        return "READY", [], []
    try:
        plan = parse(plan_path.read_text(encoding="utf-8"))
    except RouteError:
        return "READY", [], []
    required = [e["agent"] for e in plan.get("agents", []) if e.get("applicability") == "REQUIRED"]
    identity, _ = change_identity(root)
    gates = load_gates(root, runtime)
    current = {a: r["decision"] for a, r in gates.items() if r.get("change_identity") == identity["value"]}
    groups = [
        [a for a in required if a == "validator"],
        [a for a in required if a in SPECIALISTS],
        [a for a in required if a == "detail-analyst"],
        [a for a in required if a == "reviewer"],
    ]
    stages = [group for group in groups if group]
    for index, stage in enumerate(stages):
        pending = [a for a in stage if a not in current]
        if pending:
            return "RUN", pending, []
        rejecting = [a for a in stage if current[a] not in PASSING]
        if rejecting:
            later = [a for group in stages[index + 1:] for a in group if a not in current]
            return "STOP", rejecting, later
    return "READY", [], []


def unrouted_triggers(root: Path, runtime: str) -> list[tuple[str, dict]]:
    """Triggers a gate reported for the current change that the routing plan does not include: (agent, trigger)."""
    try:
        plan = parse((state_dir(root, runtime) / "routing-plan.yaml").read_text(encoding="utf-8"))
    except (OSError, RouteError):
        return []
    planned = {t.get("dimension") for t in plan.get("risk_triggers") or [] if isinstance(t, dict)}
    identity = change_identity(root)[0]["value"]
    return [(agent, trigger) for agent, result in sorted(load_gates(root, runtime).items())
            if result.get("change_identity") == identity
            for trigger in result.get("reported_triggers", []) if trigger["dimension"] not in planned]


def describe_next(root: Path, runtime: str) -> str:
    reported = unrouted_triggers(root, runtime)
    if reported:
        flags = " ".join(f'--trigger "{t["dimension"]}={t["evidence"]}"' for _, t in reported)
        return (f"next: {', '.join(dict.fromkeys(a for a, _ in reported))} reported a risk the plan does not cover. "
                f"Rerun `route.py plan` with the same arguments plus {flags}, then run the gates it adds.")
    kind, agents, skipped = next_step(root, runtime)
    if kind == "RUN":
        models = gate_models(root, runtime)
        chosen = [f"{agent}={models[agent]}" for agent in agents if agent in models]
        return "next: run " + ", ".join(agents) + ("\nmodels: launch " + ", ".join(chosen) if chosen else "")
    if kind == "STOP":
        text = "next: stop. " + ", ".join(agents) + " did not pass"
        if skipped:
            text += "; do not run " + ", ".join(skipped) + " until the change is fixed"
        return text + f". Run `route.py ready --runtime {runtime}` and report the blockers."
    return f"next: run `route.py ready --runtime {runtime}`"


def cmd_gate(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    identity, _ = change_identity(root)
    gates = load_gates(root, args.runtime)
    if args.carry_forward:
        previous = gates.get(args.agent)
        if not previous or previous["decision"] not in PASSING:
            raise RouteError(f"{args.agent} has no passing result to carry forward; run the gate instead")
        if args.decision or args.report or args.condition or args.trigger:
            raise RouteError("--carry-forward keeps the recorded decision; do not combine it with --decision, --report, --condition or --trigger")
        if previous["change_identity"] == identity["value"]:
            print(f"{args.agent}: already recorded for the current change")
            return 0
        previous.setdefault("carried_forward", []).append({"from": previous["change_identity"], "reason": args.carry_forward})
        previous["change_identity"] = identity["value"]
        save_gates(root, args.runtime, gates)
        print(f"{args.agent}: {previous['decision']} carried forward to {identity['value']}")
        print(describe_next(root, args.runtime))
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
    reported = [{"dimension": t["dimension"], "evidence": t["evidence"]} for t in map(parse_trigger, args.trigger or [])]
    if reported:
        gates[args.agent]["reported_triggers"] = reported
    save_gates(root, args.runtime, gates)
    print(f"{args.agent}: {args.decision} recorded for {identity['value']}")
    print(describe_next(root, args.runtime))
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
    kind, rejecting, skipped = next_step(root, runtime)
    blockers, missing, conditions = [], [], []
    for entry in plan["agents"]:
        if entry["applicability"] != "REQUIRED":
            continue
        agent, result = entry["agent"], gates.get(entry["agent"])
        if kind == "STOP" and agent in skipped:
            missing.append(f"{agent}: not run, the review stopped when {', '.join(rejecting)} did not pass")
        elif result is None:
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
    unspecified = missing_specification(plan, root)
    if unspecified:
        conditions.append(unspecified)
    scanned = scan_change(root, paths)
    if scanned["secret"]:
        blockers.append("the change adds what looks like a secret: " + scan.summary(scanned["secret"]) +
                        "; remove it, and rotate it if it was ever real")
    if scanned["allowed"]:
        conditions.append(f"marked `{scan.ALLOW}`, a person must confirm it is not a real secret: " + scan.summary(scanned["allowed"]))
    if scanned["suspect"]:
        conditions.append("possible credential, a person must look: " + scan.summary(scanned["suspect"]))
    for agent, trigger in unrouted_triggers(root, runtime):
        conditions.append(f"{agent} reported a {trigger['dimension']} risk that no routed gate judged: {trigger['evidence']}; "
                          "a person must judge it, or rerun `route.py plan` with that trigger")
    if blockers or missing:
        return "PRE_PR_BLOCKED", blockers + missing, conditions
    return ("PRE_PR_PASS_WITH_CONDITIONS" if conditions else "PRE_PR_PASS"), [], conditions


def receipts_enabled(root: Path) -> bool:
    try:
        text = (root / ".harness/harness.config.yaml").read_text(encoding="utf-8")
    except OSError:
        return False
    return bool(re.search(r"^\s*[\"']?receipts[\"']?\s*:\s*true\b", text, re.M))


def receipt_file(identity: dict) -> str:
    return RECEIPTS_DIR + identity["value"].split(":", 1)[-1] + ".json"


def write_receipt(root: Path, runtime: str, status: str, conditions: list[str]) -> str | None:
    """Record that this exact content passed the Final Pre-PR Gate. Same review in, same file out."""
    identity, _ = change_identity(root)
    if identity["type"] != "content":
        return None
    plan = parse((state_dir(root, runtime) / "routing-plan.yaml").read_text(encoding="utf-8"))
    gates = load_gates(root, runtime)
    target = receipt_file(identity)
    base = base_commit(root)
    folder = root / RECEIPTS_DIR
    folder.mkdir(parents=True, exist_ok=True)
    # A receipt this change added for an earlier version of itself no longer describes anything.
    for old in folder.glob("*.json"):
        name = RECEIPTS_DIR + old.name
        if name != target and (not base or git(root, "cat-file", "-e", f"{base}:{name}") is None):
            old.unlink()
    receipt = {
        "change": identity["value"],
        "status": status,
        "conditions": conditions,
        "runtime": runtime,
        "work_mode": plan.get("work_mode"),
        "lane": plan.get("lane"),
        "risk_triggers": sorted({t.get("dimension") for t in plan.get("risk_triggers") or []}),
        "gates": {e["agent"]: gates[e["agent"]]["decision"] for e in plan["agents"]
                  if e["applicability"] == "REQUIRED" and e["agent"] in gates},
    }
    (root / target).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return target


def cmd_verify(args: argparse.Namespace) -> int:
    """For CI: does the content of this change have a receipt of a review that passed?"""
    root = Path(args.project).resolve()

    def fail(*lines: str) -> int:
        print("REVIEW RECEIPT: FAIL")
        for line in lines:
            print(f"  {line}")
        return 1

    if git(root, "rev-parse", "--git-dir") is None:
        return fail("this is not a git repository, so there is no change to identify")
    if (git(root, "rev-parse", "--is-shallow-repository") or "").strip() == "true":
        return fail("the checkout is shallow, so where the change starts cannot be found; fetch the full history "
                    "(`fetch-depth: 0` in actions/checkout)")
    base = None
    if args.base:
        base = (git(root, "merge-base", "HEAD", args.base) or "").strip()
        if not base:
            return fail(f"cannot find where this change leaves {args.base}; fetch that branch first")
    identity, paths = change_identity(root, base)
    if identity["type"] != "content":
        print("REVIEW RECEIPT: NOTHING TO VERIFY (no change against the base)")
        return 0
    target = receipt_file(identity)
    try:
        receipt = json.loads((root / target).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        hint = ("" if receipts_enabled(root) else
                "; receipts are off in this project, turn them on with `gantry install --runtime <tool> --receipts`")
        return fail(f"no receipt for this version of the change ({identity['value']}, {len(paths)} files): {target} is missing",
                    "it was not reviewed, or it was edited after the review; run the harness-run skill and commit the receipt "
                    "`route.py ready` writes" + hint)
    if not isinstance(receipt, dict) or receipt.get("change") != identity["value"] or receipt.get("status") not in READY:
        return fail(f"{target} does not record a passed review of this change")
    print(f"REVIEW RECEIPT: PASS ({receipt['status']}, {len(paths)} files, gates: {', '.join(receipt.get('gates') or {}) or 'none'})")
    for condition in receipt.get("conditions") or []:
        print(f"  condition: {condition}")
    return 0


def cmd_ready(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    status, blockers, conditions = readiness(root, args.runtime)
    print(status)
    for blocker in blockers:
        print(f"  blocker: {blocker}")
    for condition in conditions:
        print(f"  condition: {condition}")
    if status != "PRE_PR_BLOCKED":
        print(f"  next: before the change is merged or deployed, run `python3 .harness/bin/release.py check --runtime {args.runtime}`")
        written = write_receipt(root, args.runtime, status, conditions) if receipts_enabled(root) else None
        if written:
            print(f"  receipt: {written}; commit it with the change, CI checks it with `route.py verify`")
    return 1 if status == "PRE_PR_BLOCKED" else 0


def cmd_guardrails(_: argparse.Namespace) -> int:
    phase = None
    for name, what, everywhere, with_hooks in GUARDRAILS:
        if name != phase:
            print(f"{name.upper()}")
            phase = name
        print(f"  {what}")
        print(f"    every runtime: {everywhere}")
        if with_hooks:
            print(f"    with hooks: {with_hooks}")
    return 0


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

    sub.add_parser("guardrails", help="List what the harness guarantees in each phase and what enforces it").set_defaults(func=cmd_guardrails)

    before = sub.add_parser("lane", help="Before building: how much has to be settled first")
    before.add_argument("--work-mode", required=True)
    before.add_argument("--trigger", action="append", help='repeatable: "DIMENSION=what in the request causes it"')
    before.set_defaults(func=cmd_lane)

    check = sub.add_parser("check", help="Validate a routing plan")
    check.add_argument("plan")
    check.set_defaults(func=cmd_check)

    gate = sub.add_parser("gate", help="Record a gate result for the current change")
    gate.add_argument("--runtime", required=True, choices=RUNTIMES)
    gate.add_argument("--agent", required=True, choices=AGENTS)
    gate.add_argument("--decision", choices=GATE_DECISIONS)
    gate.add_argument("--report", help="the specialist's report file")
    gate.add_argument("--condition", action="append", help="repeatable; required for PASS_WITH_CONDITIONS")
    gate.add_argument("--trigger", action="append",
                      help='repeatable: "DIMENSION=what the gate saw", for a risk outside this gate\'s own scope')
    gate.add_argument("--carry-forward", metavar="REASON",
                      help="keep a passing result after an edit that does not invalidate it, with the reason")
    gate.add_argument("--project", default=".")
    gate.set_defaults(func=cmd_gate)

    ready = sub.add_parser("ready", help="Final Pre-PR Gate: is every required gate passed for the current change?")
    ready.add_argument("--runtime", required=True, choices=RUNTIMES)
    ready.add_argument("--project", default=".")
    ready.set_defaults(func=cmd_ready)

    verify = sub.add_parser("verify", help="In CI: fail unless this exact change has a receipt of a passed review")
    verify.add_argument("--base", help="the branch the change will be merged into, e.g. origin/main; default: the default branch")
    verify.add_argument("--project", default=".")
    verify.set_defaults(func=cmd_verify)

    following = sub.add_parser("next", help="Which gates to run now, given the results recorded so far")
    following.add_argument("--runtime", required=True, choices=RUNTIMES)
    following.add_argument("--project", default=".")
    following.set_defaults(func=lambda a: print(describe_next(Path(a.project).resolve(), a.runtime)) or 0)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except RouteError as error:
        print(f"route.py: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
