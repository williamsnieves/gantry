#!/usr/bin/env python3
"""Check a specification written before building.

    python3 .harness/bin/spec.py check docs/specs/<name>.md [--lane SPEC|DESIGN]
    python3 .harness/bin/spec.py approve docs/specs/<name>.md      # a person's decision

A specification is short and has fixed headings. This checks what needs no
judgement: the headings are there, every acceptance criterion has an id, every
criterion is delivered by a slice, and a DESIGN-lane change has its design.
Whether the criteria are the right ones is for the user and the reviewers.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HEADINGS = ("Problem", "Behavior", "Out of scope", "Slices", "Open questions")
MAX_WORDS = 800
APPROVALS_FILE = ".harness/runtime/approvals.json"
CRITERION = re.compile(r"^\s*[-*]\s+\**(AC-\d+)\**\s*[:.]\s*(\S.*)$", re.M)
REFERENCE = re.compile(r"\bAC-\d+\b")
NOTHING = re.compile(r"^(none|n/a|nothing|-)?\.?$", re.I)


def sections(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    parts = re.split(r"^## +(.+?)\s*$", text, flags=re.M)
    for name, body in zip(parts[1::2], parts[2::2]):
        out[name.strip()] = body.strip()
    return out


def problems(path: Path, lane: str) -> tuple[list[str], list[str]]:
    """Return (problems, notes). Problems fail the check; notes are for the reader."""
    if not path.is_file():
        return [f"{path} does not exist"], []
    text = path.read_text(encoding="utf-8", errors="replace")
    found = sections(text)
    required = HEADINGS + (("Design",) if lane == "DESIGN" else ())
    out = [f"missing section: ## {heading}" for heading in required if heading not in found]
    out += [f"section is empty: ## {heading}" for heading in ("Problem", "Behavior", "Slices") if heading in found and not found[heading]]
    if lane == "DESIGN" and "Design" in found and len(found["Design"].split()) < 20:
        out.append("## Design is too short to judge: say what was chosen, what was rejected and how to undo it")
    words = len(text.split())
    if words > MAX_WORDS:
        out.append(f"{words} words; keep it under {MAX_WORDS}. A longer change is more than one specification")
    criteria = CRITERION.findall(found.get("Behavior", ""))
    ids = [identifier for identifier, _ in criteria]
    if "Behavior" in found and found["Behavior"] and not ids:
        out.append("## Behavior has no acceptance criteria; write each as `- AC-1: <what can be observed>`")
    out += [f"{identifier} appears more than once" for identifier in sorted({i for i in ids if ids.count(i) > 1})]
    sliced = REFERENCE.findall(found.get("Slices", ""))
    out += [f"{identifier} is not delivered by any slice" for identifier in ids if identifier not in sliced]
    out += [f"## Slices refers to {identifier}, which is not a criterion" for identifier in sorted(set(sliced) - set(ids))]
    notes = []
    questions = found.get("Open questions", "")
    if questions and not NOTHING.match(questions):
        count = len(re.findall(r"^\s*[-*\d]", questions, re.M)) or 1
        notes.append(f"{count} open question(s): settle them with the user before building what depends on them")
    return out, notes


def approve(spec: str, lane: str, root: Path) -> int:
    """Record that a person approved the specification as it is now. An edit afterwards voids the approval."""
    try:
        relative = (root / spec).resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        print(f"SPEC: NOT APPROVED\n  {spec} is outside the project")
        return 1
    path = root / relative
    found, _ = problems(path, lane)
    if found:
        print("SPEC: NOT APPROVED\n  it does not pass the check:")
        for line in found:
            print(f"    {line}")
        return 1
    record = root / APPROVALS_FILE
    try:
        approvals = json.loads(record.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        approvals = {}
    approvals[relative] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "lane": lane}
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(json.dumps(approvals, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"SPEC: APPROVED ({relative})\n  editing the specification voids the approval")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="spec.py")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Validate a specification")
    check.add_argument("spec")
    check.add_argument("--lane", choices=("SPEC", "DESIGN"), default="SPEC")
    approval = sub.add_parser("approve", help="Record a person's approval of a specification as it is now")
    approval.add_argument("spec")
    approval.add_argument("--lane", choices=("SPEC", "DESIGN"), default="DESIGN")
    approval.add_argument("--project", default=".")
    args = parser.parse_args(argv)
    if args.command == "approve":
        return approve(args.spec, args.lane, Path(args.project))
    found, notes = problems(Path(args.spec), args.lane)
    print("SPEC: FAIL" if found else "SPEC: PASS")
    for line in found:
        print(f"  {line}")
    for line in notes:
        print(f"  note: {line}")
    if not found and args.lane == "DESIGN":
        print(f"  next: show the specification to the user and wait for their approval before building; "
              f"once they approve, run `python3 .harness/bin/spec.py approve {args.spec}`")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
