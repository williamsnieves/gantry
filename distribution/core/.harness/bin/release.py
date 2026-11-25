#!/usr/bin/env python3
"""The release gate, and the record of what happened after shipping.

    python3 .harness/bin/release.py check --runtime claude
    python3 .harness/bin/release.py record --outcome SHIPPED --change "#42 severity filter"
    python3 .harness/bin/release.py record --outcome INCIDENT --change "#42" \\
        --note "filtered list showed other tenants" --missed SECURITY

`check` runs before the change is merged or deployed. It adds to the Final
Pre-PR Gate what only matters when shipping: a change that moves data, schema
or infrastructure has a written rollout (order, how to verify it, how to undo
it), and a change users will notice is in the changelog when the project keeps
one. It decides nothing about the code; the review did that.

`record` appends one line to docs/releases.md. A rollback or an incident is the
evidence that something got past the review: `--missed` names the risk nobody
declared, so the record says where the harness has to get better.

Standard library only.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import route  # noqa: E402
import spec  # noqa: E402

OUTCOMES = {
    "SHIPPED": "it is in production and was verified there",
    "ROLLED_BACK": "it was shipped and then undone",
    "INCIDENT": "it caused a problem in production",
}
RELEASES_FILE = "docs/releases.md"
HEADER = (
    "# Releases\n\n"
    "What happened to each change after it shipped. Written by `.harness/bin/release.py record`.\n"
    "A rollback or an incident names the risk the review did not see.\n\n"
    "| Date | Change | Outcome | What happened | Risk nobody declared |\n"
    "|---|---|---|---|---|\n"
)
CHANGELOGS = ("CHANGELOG.md", "CHANGELOG", "CHANGES.md", "HISTORY.md")
USER_VISIBLE = ("BEHAVIORAL", "USER_IMPACT", "COMPATIBILITY")
MIN_ROLLOUT_WORDS = 20


def rollout_problem(root: Path, plan: dict) -> str | None:
    """A change that needs a rollout has one written in its specification."""
    why = route.needs_rollout(plan.get("work_mode", ""), plan.get("risk_triggers") or [])
    if not why:
        return None
    sources = [s for s in plan.get("accepted_behavior_sources") or [] if (root / s).is_file()]
    ask = ("say in what order it is deployed, how it is verified in production and how it is undone, "
           "in a `## Rollout` section of the specification")
    if not sources:
        return f"{why}, and there is no specification to hold its rollout; {ask}, then pass it to `route.py plan --behavior-source`"
    for source in sources:
        text = spec.sections((root / source).read_text(encoding="utf-8", errors="replace")).get("Rollout", "")
        if len(text.split()) >= MIN_ROLLOUT_WORDS:
            return None
    return f"{why}, and {', '.join(sources)} has no `## Rollout` section of at least {MIN_ROLLOUT_WORDS} words; {ask}"


def status(root: Path, runtime: str) -> tuple[str, list[str], list[str]]:
    """Return (status, blockers, conditions) for the release gate."""
    review, blockers, conditions = route.readiness(root, runtime)
    if review == "PRE_PR_BLOCKED":
        return "RELEASE_BLOCKED", ["the Final Pre-PR Gate does not pass: " + blocker for blocker in blockers], conditions
    plan = route.parse((route.state_dir(root, runtime) / "routing-plan.yaml").read_text(encoding="utf-8"))
    blockers, conditions = [], ["from the review: " + condition for condition in conditions]
    problem = rollout_problem(root, plan)
    if problem:
        blockers.append(problem)
    changelog = next((name for name in CHANGELOGS if (root / name).is_file()), None)
    dimensions = {t.get("dimension") for t in plan.get("risk_triggers") or []}
    if changelog and dimensions & set(USER_VISIBLE) and changelog not in route.change_identity(root)[1]:
        conditions.append(f"the project keeps {changelog} and this change is visible to users, but the change does not touch it")
    if blockers:
        return "RELEASE_BLOCKED", blockers, conditions
    return ("RELEASE_READY_WITH_CONDITIONS" if conditions else "RELEASE_READY"), [], conditions


def cmd_check(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    result, blockers, conditions = status(root, args.runtime)
    print(result)
    for blocker in blockers:
        print(f"  blocker: {blocker}")
    for condition in conditions:
        print(f"  condition: {condition}")
    if result != "RELEASE_BLOCKED":
        print("  next: put the conditions in the pull request; after it ships, verify it as the rollout says and run "
              "`python3 .harness/bin/release.py record --outcome <SHIPPED|ROLLED_BACK|INCIDENT> --change \"<reference>\"`")
    return 1 if result == "RELEASE_BLOCKED" else 0


def cell(text: str) -> str:
    return re.sub(r"\s+", " ", text).replace("|", "/").strip()


def cmd_record(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    outcome = args.outcome.upper()
    if outcome not in OUTCOMES:
        raise route.RouteError(f"unknown outcome {args.outcome!r}. Known: {', '.join(OUTCOMES)}")
    note = cell(args.note or "")
    if outcome != "SHIPPED" and not note:
        raise route.RouteError(f"{outcome} needs --note: what happened, in one sentence")
    missed = []
    for raw in args.missed or []:
        dimension = raw.strip().upper()
        if dimension not in route.TRIGGERS:
            raise route.RouteError(f"unknown risk {raw!r}. Known: {', '.join(route.TRIGGERS)}")
        missed.append(dimension)
    if missed and outcome == "SHIPPED":
        raise route.RouteError("--missed is for a rollback or an incident")
    path = root / RELEASES_FILE
    text = path.read_text(encoding="utf-8") if path.is_file() else HEADER
    if not text.endswith("\n"):
        text += "\n"
    text += f"| {date.today().isoformat()} | {cell(args.change)} | {outcome} | {note or 'verified in production'} | {', '.join(missed)} |\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"recorded in {RELEASES_FILE}: {outcome}, {cell(args.change)}")
    if outcome != "SHIPPED":
        print("  next: reproduce it with a failing test, then fix it as REMEDIATION work with the harness-start skill"
              + ("" if missed else "; if a risk trigger should have been declared for the original change, record it with --missed"))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="release.py", description="Release gate and release record.")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Before merging or deploying: is the change ready to ship?")
    check.add_argument("--runtime", required=True, choices=route.RUNTIMES)
    check.add_argument("--project", default=".")
    check.set_defaults(func=cmd_check)
    record = sub.add_parser("record", help="After shipping: write down what happened")
    record.add_argument("--outcome", required=True, help=" | ".join(OUTCOMES))
    record.add_argument("--change", required=True, help="pull request, version or short name of what shipped")
    record.add_argument("--note", help="what happened; required unless the outcome is SHIPPED")
    record.add_argument("--missed", action="append", help="repeatable: the risk trigger nobody declared for this change")
    record.add_argument("--project", default=".")
    record.set_defaults(func=cmd_record)
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except route.RouteError as error:
        print(f"release.py: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
