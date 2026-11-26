#!/usr/bin/env python3
"""What this project learned from changes that went wrong, as rules the router applies.

    python3 .harness/bin/learn.py propose
    python3 .harness/bin/learn.py add --trigger SECURITY --path apps/api/src/incidents/ \\
        --because "a filtered list showed other tenants: every query keeps the tenant filter" --from "#42"
    python3 .harness/bin/learn.py list
    python3 .harness/bin/learn.py remove L-2

A rule says: when a change touches these paths, add this risk trigger, because
of this. `route.py plan` applies it like any signal it detects from the change,
so the gate that judges that risk is routed and receives the lesson as the
trigger's evidence. Nothing else is loaded into anyone's context.

`propose` reads docs/releases.md for rollbacks and incidents that named a risk
nobody declared and that no rule covers yet. It proposes; a person decides
where the lesson applies and adds the rule. Rules live in docs/learned.md, a
table the project owns: review it in pull requests, edit it by hand, delete
what stopped being true. `list` marks rules whose paths no longer exist.

Standard library only.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import release  # noqa: E402
import route  # noqa: E402

HEADER = (
    "# Learned rules\n\n"
    "What this project learned from changes that went wrong. When a change touches the paths of a rule,\n"
    "`.harness/bin/route.py plan` adds its risk, so the gate that judges it is routed and reads the lesson.\n"
    "Added with `.harness/bin/learn.py add`; edit or delete rows freely. A path ending in `/` is a folder; `*` matches within a name.\n\n"
    "| Id | When a change touches | Add the risk | Because | Learned from |\n"
    "|---|---|---|---|---|\n"
)
MANY = 25


def incidents(root: Path) -> list[dict]:
    """Rollbacks and incidents in docs/releases.md that named a risk nobody declared."""
    path = root / release.RELEASES_FILE
    found = []
    for line in (path.read_text(encoding="utf-8") if path.is_file() else "").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[2] in ("ROLLED_BACK", "INCIDENT") and cells[4]:
            missed = [d.strip() for d in cells[4].split(",") if d.strip() in route.TRIGGERS]
            if missed:
                found.append({"date": cells[0], "change": cells[1], "outcome": cells[2], "note": cells[3], "missed": missed})
    return found


def cmd_propose(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    rules = route.learned_rules(root)
    open_ones = []
    for incident in incidents(root):
        for dimension in incident["missed"]:
            if not any(rule["trigger"] == dimension and incident["change"] in rule["source"] for rule in rules):
                open_ones.append((incident, dimension))
    if not open_ones:
        print("LEARN: NOTHING TO PROPOSE (every rollback or incident that named a missed risk has a rule, or there is none)")
        return 0
    print(f"LEARN: {len(open_ones)} PROPOSAL(S)")
    for incident, dimension in open_ones:
        print(f"  {incident['date']} {incident['change']} ({incident['outcome']}): {incident['note']}")
        print(f"    nobody declared {dimension}. If a change to the same code should always be reviewed for it, the person decides where:")
        print(f"    python3 .harness/bin/learn.py add --trigger {dimension} --path <folder or file it happened in> "
              f"--because \"{incident['note']}\" --from \"{incident['change']}\"")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    dimension = args.trigger.strip().upper()
    if dimension not in route.TRIGGERS:
        raise route.RouteError(f"unknown risk {args.trigger!r}. Known: {', '.join(route.TRIGGERS)}")
    paths = [p.strip().lstrip("./") for p in args.path if p.strip()]
    if not paths:
        raise route.RouteError("--path is required: the folder or file the lesson applies to")
    for pattern in paths:
        if pattern in ("*", "**", "/") or re.fullmatch(r"[*/.]*", pattern):
            raise route.RouteError(f"--path {pattern!r} matches everything; a rule for every change is a convention, write it in docs/conventions.md")
    because = release.cell(args.because)
    if len(because.split()) < 4:
        raise route.RouteError("--because needs a sentence: what went wrong and what to check, for the reviewer who will read it")
    rules = route.learned_rules(root)
    number = max([int(rule["id"][2:]) for rule in rules] or [0]) + 1
    path = root / route.LEARNED_FILE
    text = path.read_text(encoding="utf-8") if path.is_file() else HEADER
    if not text.endswith("\n"):
        text += "\n"
    text += f"| L-{number} | {', '.join(f'`{p}`' for p in paths)} | {dimension} | {because} | {release.cell(args.source or '')} |\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"learned L-{number}: a change touching {', '.join(paths)} is routed with {dimension}")
    if len(rules) + 1 > MANY:
        print(f"  note: {len(rules) + 1} rules; run `learn.py list` and delete the ones that stopped being true")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    path = root / route.LEARNED_FILE
    wanted = args.id.strip().upper()
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    kept = [line for line in lines if not re.match(rf"\|\s*{re.escape(wanted)}\s*\|", line)]
    if len(kept) == len(lines):
        raise route.RouteError(f"no rule {wanted} in {route.LEARNED_FILE}")
    path.write_text("\n".join(kept) + "\n", encoding="utf-8")
    print(f"removed {wanted}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    rules = route.learned_rules(root)
    if not rules:
        print(f"LEARN: NO RULES ({route.LEARNED_FILE} is empty or missing)")
        return 0
    tracked = (route.git(root, "ls-files") or "").splitlines()
    print(f"LEARN: {len(rules)} RULE(S)")
    for rule in rules:
        stale = bool(tracked) and not any(route.rule_matches(pattern, file) for pattern in rule["paths"] for file in tracked)
        print(f"  {rule['id']}: {', '.join(rule['paths'])} -> {rule['trigger']}: {rule['because']}"
              + (f" (from {rule['source']})" if rule["source"] else ""))
        if stale:
            print(f"    stale: no file of the project matches its paths any more; `learn.py remove {rule['id']}` or correct the path")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="learn.py", description="Rules this project learned, applied by the router.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, func, text in (("propose", cmd_propose, "Rollbacks and incidents that no rule covers yet"),
                             ("list", cmd_list, "The rules, and the ones whose paths no longer exist")):
        command = sub.add_parser(name, help=text)
        command.add_argument("--project", default=".")
        command.set_defaults(func=func)
    add = sub.add_parser("add", help="Add a rule; a person decides this")
    add.add_argument("--trigger", required=True, help="the risk to add: " + ", ".join(route.TRIGGERS))
    add.add_argument("--path", action="append", required=True, help="repeatable: folder (ending in /), file or pattern")
    add.add_argument("--because", required=True, help="what went wrong and what to check")
    add.add_argument("--from", dest="source", help="the change it was learned from, as written in docs/releases.md")
    add.add_argument("--project", default=".")
    add.set_defaults(func=cmd_add)
    remove = sub.add_parser("remove", help="Delete a rule that stopped being true")
    remove.add_argument("id")
    remove.add_argument("--project", default=".")
    remove.set_defaults(func=cmd_remove)
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except route.RouteError as error:
        print(f"learn.py: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
