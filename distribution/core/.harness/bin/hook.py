#!/usr/bin/env python3
"""Pre-tool-use guard for agent runtimes that support command hooks.

Reads the hook event as JSON on stdin and denies four things:

1. Edits to the harness's own files, and to routing state that only
   route.py may write. A specialist agent may write one file, its own
   report, and nobody else may write that report.
2. Edits to existing quality configuration (lint, types, tests, CI), so a
   failing check is fixed in the code rather than by weakening the check.
3. `gh pr create` before the Final Pre-PR Gate passes for the current change,
   and commands that pass `--no-verify`.
4. Launching a gate after the review stopped at a stage that did not pass.
5. `git commit` and `git push` while the change adds a secret (see scan.py).

It also turns `spec.py approve` into a question for the person: approving a
design is their decision, so the agent's command waits for their confirmation.

Rules 2, 3 and 4 are off when the delivery profile is `lean`.

A hook is a first barrier, not a boundary: a shell command can still write a
file. `route.py ready` reports any quality configuration the change touched,
however it was edited. If this script fails internally it allows the action
and says so on stderr, so a bug here never blocks work.

    python3 .harness/bin/hook.py <runtime>     # event JSON on stdin
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import route  # noqa: E402

EDIT_TOOLS = ("Edit", "Write", "MultiEdit", "NotebookEdit")
PR_CREATE = re.compile(r"(^|[\s;&|(])gh\s+pr\s+create\b")
NO_VERIFY = re.compile(r"(^|\s)--no-verify\b")
COMMIT_OR_PUSH = re.compile(r"(^|[\s;&|(])git\s+(?:-\S+\s+\S+\s+)*(commit|push)\b")
APPROVE = re.compile(r"\bspec\.py[\"']?\s+approve\b")
SUBAGENT_TOOLS = ("Agent", "Task")
REPORT = re.compile(r"\.harness/runtime/([a-z]+)/artifacts/([a-z-]+)-report\.md")
ASK_USER = "If the change is really needed, stop and ask the user to make it or to approve it; do not work around this."


def profile(root: Path) -> str:
    try:
        text = (root / ".harness/harness.config.yaml").read_text(encoding="utf-8")
    except OSError:
        return "standard"
    match = re.search(r"^\s*delivery_profile:\s*['\"]?(\w+)", text, re.M)
    return match.group(1) if match else "standard"


def managed_files(root: Path) -> set[str]:
    try:
        state = json.loads((root / ".harness/install-state.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return set(state.get("managed_files") or {})


def relative(root: Path, raw: str) -> str | None:
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None  # outside the project


def confirm(event: dict) -> str | None:
    """Return the question to put to the person before the tool call runs, or None."""
    if event.get("tool_name") != "Bash" or event.get("agent_type") in route.AGENTS:
        return None
    if APPROVE.search(str((event.get("tool_input") or {}).get("command") or "")):
        return ("Gantry: this records that you approved the specification as it is written now. "
                "Confirm only if you have read it and agree with its design.")
    return None


def decide(event: dict, root: Path, runtime: str) -> str | None:
    """Return the reason to deny the tool call, or None to allow it."""
    tool = event.get("tool_name")
    tool_input = event.get("tool_input") or {}
    enforcing = profile(root) != "lean"

    if tool in EDIT_TOOLS:
        raw = tool_input.get("file_path") or tool_input.get("notebook_path")
        path = relative(root, raw) if raw else None
        if not path:
            return None
        agent = event.get("agent_type")
        if agent in route.AGENTS:
            own = f".harness/runtime/{runtime}/artifacts/{agent}-report.md"
            if path == own:
                return None
            return (
                f"Gantry: {agent} reviews the change and does not edit files. The only file it may write is its report, {own}. "
                f"Put what you found in the report; the lead decides what happens next."
            )
        report = REPORT.fullmatch(path)
        if report and report.group(1) == runtime and report.group(2) in route.AGENTS:
            return (
                f"Gantry: {path} is written only by the {report.group(2)} agent, so a report is exactly what the reviewer said. "
                f"Launch {report.group(2)} again if the report is missing or wrong. {ASK_USER}"
            )
        protected = route.protection(path)
        if protected is None and path in managed_files(root):
            protected = ("harness", "it was installed by the harness")
        if protected is None:
            return None
        kind, why = protected
        if kind == "harness":
            return f"Gantry: {path} cannot be edited by the agent because {why}. {ASK_USER}"
        if enforcing and (root / path).exists():
            return (
                f"Gantry: {path} cannot be edited by the agent because {why}. "
                f"If a check fails, fix the code it reports on. {ASK_USER}"
            )
        return None

    if tool == "Bash" and event.get("agent_type") in route.AGENTS and APPROVE.search(str(tool_input.get("command") or "")):
        return f"Gantry: approving a specification is the user's decision, not a reviewer's. {ASK_USER}"

    if tool in SUBAGENT_TOOLS and enforcing:
        gate = tool_input.get("subagent_type")
        kind, rejecting, later = route.next_step(root, runtime)
        if kind == "STOP" and gate in later:
            return (
                f"Gantry: the review stopped because {', '.join(rejecting)} did not pass, and {gate} would judge a change "
                f"that has to be edited anyway. Run `python3 .harness/bin/route.py ready --runtime {runtime}` and report "
                f"the blockers; once the change is fixed, `route.py plan` starts the review again. "
                f"If this version needs {gate}'s opinion regardless, stop and ask the user to launch it; do not work around this."
            )
        return None

    if tool == "Bash" and COMMIT_OR_PUSH.search(str(tool_input.get("command") or "")):
        secrets = route.scan_change(root, route.change_identity(root)[1])["secret"]
        if secrets:
            return (
                f"Gantry: the change adds what looks like a secret ({route.scan.summary(secrets)}), and a commit or a push "
                f"would spread it. Remove it from the file and read it from the environment instead. "
                f"If it is not a real secret, stop and ask the user; do not work around this."
            )

    if tool == "Bash" and enforcing:
        command = str(tool_input.get("command") or "")
        if NO_VERIFY.search(command):
            return f"Gantry: --no-verify skips the project's commit and push checks. Run the command without it and fix what the checks report. {ASK_USER}"
        if PR_CREATE.search(command):
            status, blockers, _ = route.readiness(root, runtime)
            if status == "PRE_PR_BLOCKED":
                listed = "; ".join(blockers)
                return (
                    f"Gantry: a pull request can be created only after the Final Pre-PR Gate passes for the current change. "
                    f"`python3 .harness/bin/route.py ready --runtime {runtime}` reports PRE_PR_BLOCKED: {listed}. "
                    f"Resolve these with the harness-run skill, or ask the user to create the pull request themselves."
                )
    return None


def main() -> int:
    runtime = sys.argv[1] if len(sys.argv) > 1 else "claude"
    try:
        event = json.load(sys.stdin)
        root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or ".")
        reason = decide(event, root, runtime)
    except Exception as error:  # fail open: a bug in the guard must not block work
        print(f"gantry hook: internal error, allowing the action ({error!r})", file=sys.stderr)
        return 0
    question = None
    if not reason:
        try:
            question = confirm(event)
        except Exception as error:
            print(f"gantry hook: internal error, allowing the action ({error!r})", file=sys.stderr)
    if question:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": question,
            }
        }))
    if reason:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
