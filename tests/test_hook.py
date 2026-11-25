"""Tests for the pre-tool-use guard. Run: python3 tests/test_hook.py"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
                   cwd=cwd, check=True, capture_output=True)


def gantry(*args):
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    proc = subprocess.run([sys.executable, "-m", "gantry", *args], capture_output=True, text=True, env=env)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp).resolve()
    (project / "src").mkdir()
    (project / "src/app.ts").write_text("export const a = 1;\n")
    (project / "eslint.config.js").write_text("export default [];\n")
    (project / ".github/workflows").mkdir(parents=True)
    (project / ".github/workflows/ci.yml").write_text("name: CI\n")
    out = gantry("install", "--runtime", "claude", "--project", str(project))
    assert "Hooks registered in .claude/settings.json" in out
    git(project, "init", "-q", "-b", "main")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "base")
    git(project, "checkout", "-q", "-b", "feature")
    (project / "src/app.ts").write_text("export const a = 2;\n")

    def hook(tool, cwd=project, raw=None, **tool_input):
        payload = raw if raw is not None else json.dumps(
            {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input, "cwd": str(cwd)})
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
        proc = subprocess.run([sys.executable, str(project / ".harness/bin/hook.py"), "claude"],
                              input=payload, capture_output=True, text=True, env=env)
        assert proc.returncode == 0, proc.stderr
        if not proc.stdout.strip():
            return None, proc.stderr
        output = json.loads(proc.stdout)["hookSpecificOutput"]
        assert output["hookEventName"] == "PreToolUse" and output["permissionDecision"] == "deny"
        return output["permissionDecisionReason"], proc.stderr

    def denied(tool, **tool_input):
        reason, _ = hook(tool, **tool_input)
        assert reason and reason.startswith("Gantry: "), (tool, tool_input, reason)
        assert "ask the user" in reason
        return reason

    def allowed(tool, **tool_input):
        reason, _ = hook(tool, **tool_input)
        assert reason is None, (tool, tool_input, reason)

    # Ordinary work is untouched.
    allowed("Edit", file_path=str(project / "src/app.ts"))
    allowed("Write", file_path="src/new.ts")
    allowed("Write", file_path=str(project / ".harness/runtime/claude/artifacts/notes.md"))

    # A specialist may write its own report and nothing else; nobody else may write that report.
    def as_agent(agent, path, tool="Write"):
        payload = json.dumps({"hook_event_name": "PreToolUse", "tool_name": tool, "agent_type": agent,
                              "tool_input": {"file_path": str(project / path)}, "cwd": str(project)})
        return hook(tool, raw=payload)[0]

    qa_report = ".harness/runtime/claude/artifacts/qa-report.md"
    assert as_agent("qa", qa_report) is None
    for path in ("src/app.ts", ".harness/runtime/claude/artifacts/security-report.md", "notes.md"):
        reason = as_agent("qa", path)
        assert reason and "qa reviews the change and does not edit files" in reason and qa_report in reason, (path, reason)
    assert "does not edit files" in as_agent("reviewer", "src/app.ts", tool="Edit")
    for writer in (None, "general-purpose", "security"):
        reason = as_agent(writer, qa_report)
        assert reason and ("written only by the qa agent" in reason or "does not edit files" in reason), (writer, reason)
    assert "written only by the qa agent" in denied("Write", file_path=str(project / qa_report))
    # An agent that is not a harness specialist follows the ordinary rules.
    assert as_agent("general-purpose", "src/app.ts") is None
    allowed("Edit", file_path="/somewhere/else/eslint.config.js")
    allowed("Bash", command="npm test && git commit -m 'x' && git push")
    allowed("Read", file_path=str(project / ".harness/bin/route.py"))

    # The harness's own files, installed files and generated routing state.
    for path in (".harness/bin/route.py", ".harness/core/routing/ROUTING-POLICY.md", ".claude/settings.json",
                 ".harness/harness.config.yaml", ".harness/project.yaml", ".claude/agents/qa.md", ".agents/skills/harness-run/SKILL.md",
                 ".harness/runtime/claude/routing-plan.yaml", ".harness/runtime/claude/gates.json"):
        denied("Edit", file_path=str(project / path))
    denied("Write", file_path=".harness/runtime/claude/gates.json")  # even when it does not exist yet

    # Existing quality configuration cannot be weakened; new configuration can be created.
    assert "fix the code it reports on" in denied("Edit", file_path=str(project / "eslint.config.js"))
    denied("MultiEdit", file_path=".github/workflows/ci.yml")
    allowed("Write", file_path="vitest.config.ts")
    allowed("Write", file_path=".github/workflows/release.yml")

    # Skipping checks, and opening a pull request before the gates pass.
    assert "--no-verify" in denied("Bash", command="git commit --no-verify -m wip")
    reason = denied("Bash", command="git push -u origin feature && gh pr create --fill")
    assert "PRE_PR_BLOCKED" in reason and "no routing plan" in reason
    allowed("Bash", command="gh pr view 12 && gh pr list")

    route = [sys.executable, str(project / ".harness/bin/route.py")]
    subprocess.run([*route, "plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND",
                    "--trigger", "BEHAVIORAL=x"], cwd=project, check=True, capture_output=True)
    assert "qa: required gate has no recorded result" in denied("Bash", command="gh pr create --title x --body y")
    reports = project / ".harness/runtime/claude/artifacts"
    reports.mkdir(parents=True, exist_ok=True)
    for agent in ("validator", "backend-code-review", "qa", "detail-analyst", "reviewer"):
        (reports / f"{agent}-report.md").write_text("ok\n")
        subprocess.run([*route, "gate", "--runtime", "claude", "--agent", agent, "--decision", "PASS",
                        "--report", f".harness/runtime/claude/artifacts/{agent}-report.md"], cwd=project, check=True, capture_output=True)
    allowed("Bash", command="gh pr create --title x --body y")
    (project / "src/app.ts").write_text("export const a = 3;\n")  # a post-gate edit makes readiness stale
    assert "edited after the routing plan" in denied("Bash", command="gh pr create --fill")

    # The lean profile keeps only the protection of the harness itself.
    gantry("install", "--runtime", "claude", "--profile", "lean", "--project", str(project))
    allowed("Edit", file_path="eslint.config.js")
    allowed("Bash", command="git commit --no-verify -m wip")
    allowed("Bash", command="gh pr create --fill")
    denied("Edit", file_path=".harness/bin/hook.py")

    # A malformed event never blocks work.
    reason, stderr = hook("Edit", raw="not json")
    assert reason is None and "internal error, allowing the action" in stderr

    # Uninstalling removes the settings file the harness created.
    gantry("uninstall", "--purge-shared", "--project", str(project))
    assert not (project / ".claude/settings.json").exists()

print("HOOK TESTS: PASS")
