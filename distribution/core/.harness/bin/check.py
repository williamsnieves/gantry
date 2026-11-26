#!/usr/bin/env python3
"""Run the project's own checks (format, lint, types, tests, build) and say which pass. No model is involved.

    python3 .harness/bin/check.py [--project .] [--only lint,test] [--timeout 900]
    python3 .harness/bin/check.py status

The commands are the ones recorded under `checks:` in `.harness/project.yaml`.
They are not arguments: whoever is being judged does not choose what judges
it. Each one is run once, the fastest kinds first, and all of them are run
even when one fails, so one run says everything that is wrong.

The result is saved with the digest of the change it was run on. `status`
prints it again without running anything while the change is still the same,
so the person, the agent that built the change and the Validator read one
result instead of each running the commands again. An edit makes it stale.
The Final Pre-PR Gate blocks on a check that failed on the current version.

Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import route  # noqa: E402

RESULT_FILE = ".harness/runtime/checks.json"
# Fastest first: a formatting or lint failure is known in seconds, before the tests and the build are paid for.
ORDER = ("format", "lint", "typecheck", "test", "build")
TAIL_LINES = 25
TAIL_CHARS = 4000
CHECK = re.compile(r"^  [\"']?([\w.-]+)[\"']?:\s*$")
COMMAND = re.compile(r"^    command:\s*(.+?)\s*$")


def commands(root: Path) -> dict[str, str]:
    """{check name: command} from `.harness/project.yaml`, in the order they are run."""
    try:
        lines = (root / ".harness/project.yaml").read_text(encoding="utf-8").splitlines()
    except OSError:
        return {}
    found, inside, name = {}, False, None
    for line in lines:
        if not line.startswith((" ", "#")) and line.strip():
            inside, name = line.rstrip() == "checks:", None
        elif inside and CHECK.match(line):
            name = CHECK.match(line).group(1)
        elif inside and name and COMMAND.match(line):
            raw = COMMAND.match(line).group(1)
            try:
                value = json.loads(raw) if raw.startswith('"') else raw.strip("'")
            except json.JSONDecodeError:
                value = raw.strip('"')
            if isinstance(value, str) and value.strip():
                found[name] = value.strip()
    return {name: found[name] for name in [*[n for n in ORDER if n in found], *[n for n in found if n not in ORDER]]}


def tail(text: str) -> str:
    """The end of a command's output: where a failing tool says what failed."""
    return "\n".join(text.strip().splitlines()[-TAIL_LINES:])[-TAIL_CHARS:]


def run(root: Path, command: str, limit: float) -> dict:
    """One check: {status: pass|fail|timeout|error, exit, seconds, output}."""
    started = time.monotonic()
    try:
        proc = subprocess.run(shlex.split(command), cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True, errors="replace", timeout=limit)
        status, code, output = ("pass" if proc.returncode == 0 else "fail"), proc.returncode, proc.stdout
    except subprocess.TimeoutExpired as error:
        output = error.stdout.decode("utf-8", "replace") if isinstance(error.stdout, bytes) else (error.stdout or "")
        status, code = "timeout", None
    except (OSError, ValueError) as error:
        status, code = "error", None
        output = f"could not start it: {error}. A command is run without a shell; put a pipeline or `&&` in a script and call the script."
    return {"command": command, "status": status, "exit": code, "seconds": round(time.monotonic() - started, 1),
            "output": "" if status == "pass" else tail(output)}


def load_result(root: Path) -> dict | None:
    try:
        result = json.loads((root / RESULT_FILE).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return result if isinstance(result, dict) and isinstance(result.get("checks"), dict) else None


def current(root: Path, identity: dict | None = None) -> dict | None:
    """The saved result, when it was run on this version of the change and with the commands the project has now."""
    result = load_result(root)
    identity = identity or route.change_identity(root)[0]
    if not result or result.get("change") != identity["value"]:
        return None
    configured = commands(root)
    result["checks"] = {name: check for name, check in result["checks"].items() if configured.get(name) == check.get("command")}
    return result


def headline(result: dict, configured: dict[str, str]) -> str:
    checks = result["checks"]
    failed = [name for name, check in checks.items() if check["status"] != "pass"]
    passed = [name for name, check in checks.items() if check["status"] == "pass"]
    left = [name for name in configured if name not in checks]
    parts = ([f"failed: {', '.join(failed)}"] if failed else []) + ([f"passed: {', '.join(passed)}"] if passed else []) + \
            ([f"not run: {', '.join(left)}"] if left else [])
    return f"CHECKS: {'FAIL' if failed else 'PASS' if not left else 'INCOMPLETE'} ({'; '.join(parts)})"


def report(result: dict, configured: dict[str, str]) -> int:
    for name, check in result["checks"].items():
        detail = {"pass": "PASS", "fail": f"FAIL (exit {check['exit']})", "timeout": "FAIL (timed out)",
                  "error": "FAIL (did not start)"}[check["status"]]
        print(f"check: {name:<10} {detail}  `{check['command']}`  {check['seconds']} s")
        if check["status"] != "pass" and check["output"]:
            print("\n".join("    " + line for line in check["output"].splitlines()))
    for name in ("test", "lint", "typecheck"):
        if name not in configured:
            print(f"check: {name:<10} NOT CONFIGURED (no command under `checks:` in .harness/project.yaml)")
    print(headline(result, configured))
    failed = any(check["status"] != "pass" for check in result["checks"].values())
    if failed:
        print("  next: fix the code, not the check, and run this again; `--only <name>` reruns one")
    return 1 if failed else 0


def cmd_run(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    configured = commands(root)
    if not configured:
        print("CHECKS: NOTHING TO RUN (no command under `checks:` in .harness/project.yaml; "
              "`gantry inspect --write` detects them, or write them there yourself)")
        return 0
    wanted = [name.strip() for name in (args.only or "").split(",") if name.strip()]
    unknown = [name for name in wanted if name not in configured]
    if unknown:
        print(f"check.py: no check named {', '.join(unknown)}; the project has: {', '.join(configured)}", file=sys.stderr)
        return 2
    ran = {}
    for name in wanted or configured:
        print(f"running {name}: `{configured[name]}`", file=sys.stderr, flush=True)
        ran[name] = run(root, configured[name], args.timeout)
    # Identified after the run: a check may leave files behind, and they are part of what is reviewed.
    identity = route.change_identity(root)[0]
    earlier = current(root, identity) if wanted else None   # a rerun of one check keeps the others of this same version
    checks = {**(earlier["checks"] if earlier else {}), **ran}
    result = {"change": identity["value"], "checks": {name: checks[name] for name in configured if name in checks}}
    (root / RESULT_FILE).parent.mkdir(parents=True, exist_ok=True)
    (root / RESULT_FILE).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return report(result, configured)


def cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    configured = commands(root)
    if not load_result(root):
        print("CHECKS: NOT RUN (run `python3 .harness/bin/check.py`)")
        return 1
    result = current(root)
    if not result or not result["checks"]:
        print("CHECKS: STALE (the change or the commands were edited since they ran; run `python3 .harness/bin/check.py`)")
        return 1
    code = report(result, configured)
    return code or (0 if all(name in result["checks"] for name in configured) else 1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check.py", description="Run the project's own checks and record which pass.")
    parser.add_argument("command", nargs="?", choices=("run", "status"), default="run")
    parser.add_argument("--project", default=".")
    parser.add_argument("--only", help="comma-separated check names to run; the others keep their result for this version")
    parser.add_argument("--timeout", type=float, default=900, help="seconds one check may take (default 900)")
    args = parser.parse_args(argv)
    return cmd_status(args) if args.command == "status" else cmd_run(args)


if __name__ == "__main__":
    sys.exit(main())
