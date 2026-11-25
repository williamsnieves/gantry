"""The release gate and the release record. Run: python3 tests/test_release.py"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "distribution/core/.harness/bin"

SPEC = """# Split incident titles

## Problem
Titles longer than the column are truncated silently.

## Behavior
- AC-1: A title of 300 characters is stored whole.

## Out of scope
Changing how titles are displayed.

## Design
Widen the column in place. Rejected: a second column, which doubles every write. Undo by narrowing the column after checking no row exceeds the old width.

## Slices
1. Migration and repository change (AC-1)

## Open questions
None.
"""
ROLLOUT = """
## Rollout
Deploy the migration before the application, because the old code still writes short titles safely. Verify with a 300 character title in staging and then in production. Undo by deploying the previous application version and then the down migration.
"""


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args], cwd=cwd, check=True, capture_output=True)


def run(tool, *args, cwd, expect=0):
    proc = subprocess.run([sys.executable, str(BIN / tool), *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == expect, (args, proc.returncode, proc.stdout, proc.stderr)
    return proc.stdout + proc.stderr


with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp).resolve()
    (project / "src").mkdir()
    (project / "src/app.ts").write_text("export const a = 1;\n")
    (project / "CHANGELOG.md").write_text("# Changelog\n")
    git(project, "init", "-q", "-b", "main")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "base")
    git(project, "checkout", "-q", "-b", "feature")
    (project / "src/app.ts").write_text("export const a = 2;\n")
    (project / "docs/specs").mkdir(parents=True)
    spec = project / "docs/specs/titles.md"
    spec.write_text(SPEC)
    reports = project / ".harness/runtime/claude/artifacts"
    reports.mkdir(parents=True)

    def review(*triggers):
        """Plan the change and pass every gate the plan requires."""
        out = run("route.py", "plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND",
                  "--behavior-source", "docs/specs/titles.md", *[a for t in triggers for a in ("--trigger", f"{t}=x")], cwd=project)
        for line in out.splitlines():
            if line.strip().startswith("REQUIRED"):
                agent = line.split()[1]
                (reports / f"{agent}-report.md").write_text("ok\n")
                run("route.py", "gate", "--runtime", "claude", "--agent", agent, "--decision", "PASS",
                    "--report", f".harness/runtime/claude/artifacts/{agent}-report.md", cwd=project)

    def check(expect):
        out = run("release.py", "check", "--runtime", "claude", cwd=project, expect=1 if expect == "RELEASE_BLOCKED" else 0)
        assert out.splitlines()[0] == expect, out
        return out

    # Nothing ships before the review passes.
    assert "the Final Pre-PR Gate does not pass: no routing plan" in check("RELEASE_BLOCKED")

    # A change users will notice, in a project that keeps a changelog.
    review("BEHAVIORAL")
    out = run("route.py", "ready", "--runtime", "claude", cwd=project)
    assert out.startswith("PRE_PR_PASS") and "next: before the change is merged or deployed, run `python3 .harness/bin/release.py check" in out, out
    out = check("RELEASE_READY_WITH_CONDITIONS")
    assert "the project keeps CHANGELOG.md and this change is visible to users" in out and "release.py record" in out, out
    (project / "CHANGELOG.md").write_text("# Changelog\n- Titles are stored whole.\n")
    review("BEHAVIORAL")
    check("RELEASE_READY")

    # A change that moves data needs its rollout written down; the lane says so before anything is built.
    out = run("route.py", "lane", "--work-mode", "IMPLEMENTATION", "--trigger", "MIGRATION=widen the title column", cwd=project)
    assert "--lane DESIGN --rollout" in out and "rollout: the specification needs a `## Rollout` section" in out, out
    assert "rollout:" not in run("route.py", "lane", "--work-mode", "IMPLEMENTATION", "--trigger", "BEHAVIORAL=x", cwd=project)
    assert "## Rollout" in run("spec.py", "check", "docs/specs/titles.md", "--lane", "DESIGN", "--rollout", cwd=project, expect=1)
    review("MIGRATION")
    out = check("RELEASE_BLOCKED")
    assert "trigger MIGRATION means this change has to be rolled out" in out and "has no `## Rollout` section" in out, out
    assert "from the review: lane DESIGN but no person approved" in out, out
    spec.write_text(SPEC + "\n## Rollout\nDeploy it carefully.\n")
    review("MIGRATION")
    check("RELEASE_BLOCKED")
    spec.write_text(SPEC + ROLLOUT)
    run("spec.py", "check", "docs/specs/titles.md", "--lane", "DESIGN", "--rollout", cwd=project)
    review("MIGRATION")
    assert "has no `## Rollout`" not in check("RELEASE_READY_WITH_CONDITIONS")

    # With hooks, `gh pr merge` waits for the release gate; the lean profile does not.
    def hook(command):
        payload = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(project)})
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
        proc = subprocess.run([sys.executable, str(BIN / "hook.py"), "claude"], input=payload, capture_output=True, text=True, env=env)
        assert proc.returncode == 0 and not proc.stderr, proc.stderr
        return json.loads(proc.stdout)["hookSpecificOutput"]["permissionDecisionReason"] if proc.stdout.strip() else None

    assert hook("gh pr merge 12 --squash") is None
    spec.write_text(SPEC)
    review("MIGRATION")
    reason = hook("gh pr merge 12 --squash")
    assert reason and "RELEASE_BLOCKED" in reason and "ask the user" in reason, reason
    assert hook("gh pr view 12") is None
    (project / ".harness/harness.config.yaml").write_text("delivery_profile: lean\n")
    assert hook("gh pr merge 12 --squash") is None

    # The record of what happened after shipping.
    releases = project / "docs/releases.md"
    out = run("release.py", "record", "--outcome", "shipped", "--change", "#42 title width", cwd=project)
    assert "recorded in docs/releases.md: SHIPPED" in out and "next:" not in out, out
    run("release.py", "record", "--outcome", "INCIDENT", "--change", "#42", cwd=project, expect=2)
    run("release.py", "record", "--outcome", "SHIPPED", "--change", "#43", "--missed", "SECURITY", cwd=project, expect=2)
    run("release.py", "record", "--outcome", "INCIDENT", "--change", "#42", "--note", "x", "--missed", "RISKY", cwd=project, expect=2)
    run("release.py", "record", "--outcome", "EXPLODED", "--change", "#42", "--note", "x", cwd=project, expect=2)
    out = run("release.py", "record", "--outcome", "INCIDENT", "--change", "#42 | title width",
              "--note", "long titles\nwere cut for one tenant", "--missed", "data_integrity", cwd=project)
    assert "next: reproduce it with a failing test" in out and "--missed" not in out, out
    out = run("release.py", "record", "--outcome", "ROLLED_BACK", "--change", "#44", "--note", "migration locked the table", cwd=project)
    assert "record it with --missed" in out, out
    lines = releases.read_text().splitlines()
    assert lines[0] == "# Releases" and len([l for l in lines if l.startswith("| 20")]) == 3, lines
    assert lines[-2].endswith("| #42 / title width | INCIDENT | long titles were cut for one tenant | DATA_INTEGRITY |"), lines[-2]
    assert lines[-1].endswith("| #44 | ROLLED_BACK | migration locked the table |  |"), lines[-1]

print("RELEASE TESTS: PASS")
