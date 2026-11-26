#!/usr/bin/env python3
"""Mutation testing of the lines a change adds: would the project's tests notice if they were wrong?

    python3 .harness/bin/mutate.py [--project .] [--max 12] [--budget 600]
    python3 .harness/bin/mutate.py restore

Each added line of runtime code gets small deliberate changes, one at a time
(`>=` to `>`, `&&` to `||`, `true` to `false`, `+` to `-`, a negation removed).
The project's own test command, from `.harness/project.yaml`, is run against
each. A mutant the tests fail on is killed. A mutant the tests pass on
survived: no test would notice that change, because none runs the line or none
checks what it decides. Survivors become a condition at the Final Pre-PR Gate;
they do not block it, because a mutant can be equivalent to the original and
only a person or QA can tell.

It is off unless the project turned it on (`gantry install --mutation`), and
bounded: at most `--max` mutants, spread over the added lines, within
`--budget` seconds. The file being mutated is saved first and put back after
every run; `restore` puts it back if a run was killed halfway, and the final
gate blocks while a mutant is still in the code.

Standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import route  # noqa: E402
import scan  # noqa: E402

RESULT_FILE = ".harness/runtime/mutation.json"
BACKUP_FILE = ".harness/runtime/mutation-backup.json"

# (what it tests, pattern, replacement). Comparison and arithmetic operators are matched only between spaces,
# which is how formatted code writes them and how generics, arrows and signs are not written.
OPERATORS = (
    ("boundary", re.compile(r" >= "), " > "),
    ("boundary", re.compile(r" <= "), " < "),
    ("boundary", re.compile(r"(?<![=\-]) > (?!=)"), " >= "),
    ("boundary", re.compile(r" < (?!=)"), " <= "),
    ("equality", re.compile(r"==="), "!=="),
    ("equality", re.compile(r"!=="), "==="),
    ("equality", re.compile(r"(?<![=!<>]) == (?!=)"), " != "),
    ("equality", re.compile(r" != (?!=)"), " == "),
    ("logic", re.compile(r" && "), " || "),
    ("logic", re.compile(r" \|\| "), " && "),
    ("logic", re.compile(r" and "), " or "),
    ("logic", re.compile(r" or "), " and "),
    ("negation", re.compile(r"(?<![=!\w)\]])!(?=[\w(])"), ""),
    ("negation", re.compile(r"\bnot (?!in\b)"), ""),
    ("constant", re.compile(r"\btrue\b"), "false"),
    ("constant", re.compile(r"\bfalse\b"), "true"),
    ("constant", re.compile(r"\bTrue\b"), "False"),
    ("constant", re.compile(r"\bFalse\b"), "True"),
    ("arithmetic", re.compile(r" \+ "), " - "),
    ("arithmetic", re.compile(r"(?<![=(,:]) - "), " + "),
    ("arithmetic", re.compile(r" \* "), " / "),
)
NOT_LOGIC = re.compile(r"^\s*(?:import\b|from\b.*\bimport\b|export\s+(?:type|interface|\*|\{)|type\s|interface\s|@|//|#|\*|/\*|package\b|use\b)")
STRING = re.compile(r"""(["'`])(?:\\.|(?!\1).)*\1""")


def masked(text: str) -> str:
    """The line with the inside of its string literals blanked, so an operator in a message is not mutated."""
    return STRING.sub(lambda m: m.group(1) + " " * (len(m.group(0)) - 2) + m.group(1), text)


def mutants_of(text: str) -> list[dict]:
    """Every single change the operators make to one line: {kind, was, now, text}. One per operator pattern."""
    if NOT_LOGIC.search(text):
        return []
    visible, found = masked(text), []
    for kind, pattern, replacement in OPERATORS:
        match = pattern.search(visible)
        if match:
            found.append({"kind": kind, "was": match.group(0).strip() or match.group(0), "now": replacement.strip(),
                          "text": text[:match.start()] + replacement + text[match.end():]})
    return found


def candidates(root: Path, paths: list[str], base: str | None) -> list[dict]:
    """Mutants of the added lines of runtime code, ordered so a bounded run covers as many lines as it can."""
    per_line = []
    for path, number, text in scan.added_lines(root, paths, base):
        if path.endswith(scan.CODE) and not scan.NOT_RUNTIME.search(path) and len(text) <= 400:
            found = [{"path": path, "line": number, **mutant} for mutant in mutants_of(text)]
            if found:
                per_line.append(found)
    ordered, depth = [], 0
    while any(len(found) > depth for found in per_line):  # the first mutant of every line, then the second, ...
        ordered += [found[depth] for found in per_line if len(found) > depth]
        depth += 1
    return ordered


def enabled(root: Path) -> bool:
    try:
        text = (root / ".harness/harness.config.yaml").read_text(encoding="utf-8")
    except OSError:
        return False
    return bool(re.search(r"^\s*[\"']?mutation[\"']?\s*:\s*true\b", text, re.M))


def test_command(root: Path) -> str | None:
    """The test command the project recorded. It is not an argument: the agent being judged does not choose it."""
    try:
        text = (root / ".harness/project.yaml").read_text(encoding="utf-8")
    except OSError:
        return None
    match = re.search(r"^  test:\s*\n\s+command:\s*(.+)$", text, re.M)
    if not match:
        return None
    raw = match.group(1).strip()
    try:
        return json.loads(raw) if raw.startswith('"') else raw.strip("'")
    except json.JSONDecodeError:
        return raw.strip('"')


def run_tests(root: Path, command: str, limit: float) -> str:
    """`pass`, `fail` or `timeout` for one run of the project's tests."""
    try:
        # No Python bytecode is written: a mutant of the same size, written within the same second as the last one,
        # would otherwise be run from the cache of the previous version and be judged for code that is not there.
        proc = subprocess.run(shlex.split(command), cwd=root, capture_output=True, timeout=limit,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    except subprocess.TimeoutExpired:
        return "timeout"
    except OSError:
        return "fail"
    return "pass" if proc.returncode == 0 else "fail"


def restore(root: Path) -> str | None:
    """Put back a file a killed run left mutated. Returns its path, or None when there was nothing to undo."""
    backup = root / BACKUP_FILE
    if not backup.is_file():
        return None
    saved = json.loads(backup.read_text(encoding="utf-8"))
    (root / saved["path"]).write_text(saved["content"], encoding="utf-8")
    backup.unlink()
    return saved["path"]


def load_result(root: Path) -> dict | None:
    try:
        return json.loads((root / RESULT_FILE).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def describe(mutant: dict) -> str:
    return f"{mutant['path']}:{mutant['line']} `{mutant['was']}` changed to `{mutant['now'] or 'nothing'}`"


def cmd_run(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    undone = restore(root)
    if undone:
        print(f"restored {undone}: an earlier run was stopped while it was mutated")
    if not enabled(root):
        print("MUTATION: OFF (turn it on with `gantry install --runtime <tool> --mutation`)")
        return 0
    identity, paths = route.change_identity(root)
    found = candidates(root, paths, route.base_commit(root))
    result = {"change": identity["value"], "mutants": 0, "killed": 0, "survived": [], "not_run": len(found), "command": None}
    command = test_command(root)

    def finish(headline: str, code: int = 0) -> int:
        # Identified again at the end: running the tests may leave files behind, and they are part of what is reviewed.
        result["change"] = route.change_identity(root)[0]["value"]
        (root / RESULT_FILE).parent.mkdir(parents=True, exist_ok=True)
        (root / RESULT_FILE).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(headline)
        for mutant in result["survived"]:
            print(f"  survived: {describe(mutant)}")
        if result["survived"]:
            print("  next: for each survivor, add the test that fails on that change, or say in the pull request why the change "
                  "makes no difference; then run this again")
        return code

    if not found:
        return finish("MUTATION: NOTHING TO MUTATE (the change adds no line of runtime code an operator applies to)")
    if not command:
        result["error"] = "no test command"
        return finish("MUTATION: NOT RUN (no test command under `checks:` in .harness/project.yaml)", 1)
    result["command"] = command
    (root / BACKUP_FILE).parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    if run_tests(root, command, args.budget) != "pass":
        result["error"] = "the tests do not pass before any mutation"
        return finish(f"MUTATION: NOT RUN (`{command}` does not pass on the change as it is; mutants are judged against passing tests)", 1)
    baseline = time.monotonic() - started
    limit = max(30.0, baseline * 3)

    def stop(*_):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)

    for mutant in found[:args.max]:
        if time.monotonic() - started + baseline > args.budget:
            break
        file = root / mutant["path"]
        original = file.read_text(encoding="utf-8")
        lines = original.split("\n")
        if mutant["line"] > len(lines):
            continue
        lines[mutant["line"] - 1] = mutant["text"]
        (root / BACKUP_FILE).write_text(json.dumps({"path": mutant["path"], "content": original}), encoding="utf-8")
        try:
            file.write_text("\n".join(lines), encoding="utf-8")
            outcome = run_tests(root, command, limit)
        finally:
            restore(root)
        result["mutants"] += 1
        result["not_run"] -= 1
        if outcome == "pass":
            result["survived"].append({key: mutant[key] for key in ("path", "line", "kind", "was", "now")})
        else:
            result["killed"] += 1
    left = f", {result['not_run']} not run (limit of {args.max} mutants or {args.budget} s)" if result["not_run"] else ""
    counts = f"{result['killed']} of {result['mutants']} mutants killed{left}"
    return finish(f"MUTATION: {'SURVIVORS' if result['survived'] else 'PASS'} ({counts})")


def cmd_restore(args: argparse.Namespace) -> int:
    undone = restore(Path(args.project).resolve())
    print(f"restored {undone}" if undone else "nothing to restore")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mutate.py", description="Mutation testing of the lines the current change adds.")
    parser.add_argument("command", nargs="?", choices=("run", "restore"), default="run")
    parser.add_argument("--project", default=".")
    parser.add_argument("--max", type=int, default=12, help="at most this many mutants (default 12)")
    parser.add_argument("--budget", type=float, default=600, help="stop starting new mutants after this many seconds (default 600)")
    args = parser.parse_args(argv)
    try:
        return cmd_restore(args) if args.command == "restore" else cmd_run(args)
    except KeyboardInterrupt:
        restore(Path(args.project).resolve())
        print("mutate.py: stopped; the mutated file was put back", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
