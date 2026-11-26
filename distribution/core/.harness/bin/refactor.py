#!/usr/bin/env python3
"""Refactoring with a fixed point: the tests that passed before the code was touched are the tests that judge it after.

    python3 .harness/bin/refactor.py pin       before changing any code
    python3 .harness/bin/refactor.py status    at any time
    python3 .harness/bin/refactor.py clear     this change is not a refactoring after all

A refactoring changes how code is built and not what it does. The only
evidence of that is a set of tests that passed on the old code and pass,
unchanged, on the new. `pin` records that set: it refuses when runtime code is
already changed, runs the project's test command, and saves a digest of every
test file. Tests written to cover code that had none go in before the pin, so
they are proven against the old behaviour too.

From then on the Final Pre-PR Gate carries a condition for every pinned test
that was edited or removed, and for a version on which the tests were not run.
It does not block: moving a module changes an import in its test, and only a
person can say the test still checks the same thing.

Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check  # noqa: E402
import route  # noqa: E402
import scan  # noqa: E402

PIN_FILE = ".harness/runtime/refactor.json"
TEST = re.compile(r"(?:^|/)(?:tests?|__tests__|specs?|e2e|fixtures?|mocks?|__mocks__|__snapshots__)/"
                  r"|(?:\.|_)(?:test|spec)\.[a-z]+$|(?:^|/)(?:test_[^/]*\.py|conftest\.py)$|_test\.go$|Tests?\.(?:java|kt|cs|php)$|\.snap$")


def digest(file: Path) -> str:
    return hashlib.sha256(file.read_bytes()).hexdigest()[:16]


def test_files(root: Path) -> dict[str, str]:
    """{path: digest} of every test file git knows or would add."""
    listed = route.git(root, "ls-files", "-co", "--exclude-standard") or ""
    return {path: digest(root / path) for path in sorted(set(listed.splitlines()))
            if TEST.search(path) and not route.is_harness_path(path) and (root / path).is_file()}


def branch(root: Path) -> str:
    return (route.git(root, "rev-parse", "--abbrev-ref", "HEAD") or "").strip()


def load_pin(root: Path) -> dict | None:
    """The pin of the change being worked on. One made on another branch, or from another starting point, is not this change's."""
    try:
        pin = json.loads((root / PIN_FILE).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(pin, dict) or pin.get("branch") != branch(root) or pin.get("base") != route.base_commit(root):
        return None
    return pin


def state(root: Path) -> dict | None:
    """What happened to the pinned tests since the pin: {pinned, edited, removed, added}. None when nothing is pinned."""
    pin = load_pin(root)
    if not pin:
        return None
    now = test_files(root)
    return {"pinned": len(pin["tests"]),
            "edited": sorted(path for path, was in pin["tests"].items() if path in now and now[path] != was),
            "removed": sorted(path for path in pin["tests"] if path not in now),
            "added": sorted(path for path in now if path not in pin["tests"])}


def cmd_pin(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    if route.base_commit(root) is None:
        print("refactor.py: this needs a git repository with a commit: the pin is tied to where the change starts", file=sys.stderr)
        return 2
    _, paths = route.change_identity(root)
    touched = [path for path in paths if path.endswith(scan.CODE) and not TEST.search(path)]
    if touched:
        shown = ", ".join(touched[:5]) + (f" and {len(touched) - 5} more" if len(touched) > 5 else "")
        print(f"REFACTOR: NOT PINNED (code is already changed: {shown})")
        print("  next: the pin proves the tests pass on the code as it was. Set those edits aside (`git stash`), pin, and bring them back.")
        return 1
    command = check.commands(root).get("test")
    if not command:
        print("REFACTOR: NOT PINNED (no test command under `checks:` in .harness/project.yaml)")
        return 1
    tests = test_files(root)
    if not tests:
        print("REFACTOR: NOT PINNED (no test file found; write the tests that describe what the code does today, then pin)")
        return 1
    print(f"running the tests: `{command}`", file=sys.stderr, flush=True)
    result = check.run(root, command, args.timeout)
    if result["status"] != "pass":
        print(f"REFACTOR: NOT PINNED (`{command}` does not pass on the code as it is)")
        print("\n".join("    " + line for line in result["output"].splitlines()))
        print("  next: a test written to describe the current behaviour must pass before the code changes; fix the test, not the code")
        return 1
    pin = {"branch": branch(root), "base": route.base_commit(root), "command": command, "tests": test_files(root)}
    (root / PIN_FILE).parent.mkdir(parents=True, exist_ok=True)
    (root / PIN_FILE).write_text(json.dumps(pin, indent=1) + "\n", encoding="utf-8")
    new = [path for path in paths if path in pin["tests"]]
    print(f"REFACTOR: PINNED ({len(pin['tests'])} test files pass on the code as it is" + (f", {len(new)} of them written for this change" if new else "") + ")")
    print("  next: one refactoring at a time; after each, `python3 .harness/bin/check.py --only test`. Leave the pinned tests as they are.")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    found = state(root)
    if found is None:
        print("REFACTOR: NOT PINNED (run `python3 .harness/bin/refactor.py pin` before changing code)")
        return 1
    changed = found["edited"] + found["removed"]
    if not changed:
        print(f"REFACTOR: HELD ({found['pinned']} pinned test files are unchanged)")
    else:
        print(f"REFACTOR: TESTS CHANGED ({len(changed)} of {found['pinned']} pinned test files)")
        for path in found["edited"]:
            print(f"  edited: {path}")
        for path in found["removed"]:
            print(f"  removed: {path}")
        print("  next: put them back, or say in the pull request why each still checks the same behaviour; a person confirms it")
    for path in found["added"]:
        print(f"  added after the pin: {path} (it never ran against the old code, so it does not show the behaviour was kept)")
    return 1 if changed else 0


def cmd_clear(args: argparse.Namespace) -> int:
    file = Path(args.project).resolve() / PIN_FILE
    existed = file.is_file()
    if existed:
        file.unlink()
    print("pin removed" if existed else "nothing was pinned")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="refactor.py", description="Pin the tests before a refactoring and see that they were kept.")
    parser.add_argument("command", choices=("pin", "status", "clear"))
    parser.add_argument("--project", default=".")
    parser.add_argument("--timeout", type=float, default=900, help="seconds the test command may take (default 900)")
    args = parser.parse_args(argv)
    return {"pin": cmd_pin, "status": cmd_status, "clear": cmd_clear}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
