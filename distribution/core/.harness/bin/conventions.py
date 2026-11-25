#!/usr/bin/env python3
"""Check `docs/conventions.md`, the project's own description of how it is built.

    python3 .harness/bin/conventions.py check [--project .]

The file is written by the harness-onboard skill and owned by the project. This
checks what can be checked without judgement: the headings are there, the file
is short enough to be read on every run, and every file it cites exists.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PATH = "docs/conventions.md"
HEADINGS = ("Structure", "Patterns", "Tests", "Do not", "Open questions")
MAX_WORDS = 600
# A backticked token that looks like a project path: has a slash or a file extension, no spaces.
CITED = re.compile(r"`([A-Za-z0-9_.@()\[\]/-]+)`")
LOOKS_LIKE_PATH = re.compile(r"/|\.[A-Za-z0-9]{1,5}$")


def cited_paths(text: str) -> list[str]:
    out = []
    for token in CITED.findall(text):
        token = re.sub(r":\d+(-\d+)?$", "", token)
        if LOOKS_LIKE_PATH.search(token) and not token.startswith(("http", "@", "-", ".")) and "*" not in token:
            out.append(token)
    return list(dict.fromkeys(out))


def problems(root: Path) -> list[str]:
    path = root / PATH
    if not path.is_file():
        return [f"{PATH} does not exist; run the harness-onboard skill"]
    text = path.read_text(encoding="utf-8", errors="replace")
    found = re.findall(r"^## +(.+?)\s*$", text, re.M)
    out = [f"missing section: ## {heading}" for heading in HEADINGS if heading not in found]
    words = len(text.split())
    if words > MAX_WORDS:
        out.append(f"{words} words; keep it under {MAX_WORDS} so it can be read on every run")
    body = re.sub(r"^#.*$", "", text, flags=re.M).strip()
    if not body:
        out.append("the sections are empty")
    for cited in cited_paths(text):
        # A bare file name cannot be located without guessing; only paths are checked.
        if "/" in cited and not (root / cited).exists():
            out.append(f"cites `{cited}`, which does not exist")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="conventions.py")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help=f"Validate {PATH}")
    check.add_argument("--project", default=".")
    args = parser.parse_args(argv)
    found = problems(Path(args.project).resolve())
    if found:
        print("CONVENTIONS: FAIL")
        for problem in found:
            print(f"  {problem}")
        return 1
    print("CONVENTIONS: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
