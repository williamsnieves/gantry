"""Refactoring with pinned tests. Run: python3 tests/test_refactor.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "distribution/core/.harness/bin"
sys.path.insert(0, str(BIN))
import refactor  # noqa: E402


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args], cwd=cwd, check=True, capture_output=True)


def run(tool, *args, cwd, expect=0):
    proc = subprocess.run([sys.executable, str(BIN / tool), *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == expect, (args, proc.returncode, proc.stdout, proc.stderr)
    return proc.stdout


for path in ("src/a.test.ts", "tests/unit/a.py", "pkg/a_test.go", "app/__tests__/a.tsx", "test_a.py", "src/OrderTest.php", "src/__snapshots__/a.snap"):
    assert refactor.TEST.search(path), path
for path in ("src/a.ts", "src/contest.py", "src/latest/a.go", "src/testing.ts"):
    assert not refactor.TEST.search(path), path

py = sys.executable
OLD = "def price(total, member):\n    if member:\n        if total >= 100:\n            return total * 0.8\n        return total * 0.9\n    return total\n"
NEW = "def price(total, member):\n    return total * discount(total, member)\n\n\ndef discount(total, member):\n    if not member:\n        return 1\n    return 0.8 if total >= 100 else 0.9\n"
TESTS = "import unittest\nfrom src.pricing import price\n\nclass Pricing(unittest.TestCase):\n    def test_guest(self):\n        self.assertEqual(price(50, False), 50)\n"
MORE = "import unittest\nfrom src.pricing import price\n\nclass Member(unittest.TestCase):\n    def test_member(self):\n        self.assertEqual(price(100, True), 80)\n        self.assertEqual(price(50, True), 45)\n"

with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp).resolve()
    for directory in ("src", "tests", ".harness"):
        (project / directory).mkdir()
    (project / ".gitignore").write_text("__pycache__/\n")
    (project / ".harness/.gitignore").write_text("runtime/\n")
    (project / ".harness/harness.config.yaml").write_text("pre_pr:\n  mutation: false\n")
    (project / ".harness/project.yaml").write_text(f'checks:\n  test:\n    command: "{py} -m unittest discover -s tests -q"\n')
    (project / "src/__init__.py").write_text("")
    (project / "src/pricing.py").write_text(OLD)
    (project / "tests/test_pricing.py").write_text(TESTS)
    git(project, "init", "-q", "-b", "main")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "base")
    git(project, "checkout", "-q", "-b", "refactor/pricing")

    assert run("refactor.py", "status", cwd=project, expect=1).startswith("REFACTOR: NOT PINNED")

    # Too late: once the code is changed, passing tests say nothing about the code as it was.
    (project / "src/pricing.py").write_text(NEW)
    out = run("refactor.py", "pin", cwd=project, expect=1)
    assert "REFACTOR: NOT PINNED (code is already changed: src/pricing.py)" in out and "git stash" in out, out
    (project / "src/pricing.py").write_text(OLD)

    # A test that describes the current behaviour must pass on it before it can be the fixed point.
    (project / "tests/test_member.py").write_text(MORE.replace("80)", "75)"))
    out = run("refactor.py", "pin", cwd=project, expect=1)
    assert "does not pass on the code as it is" in out and "AssertionError" in out and "fix the test, not the code" in out, out
    (project / "tests/test_member.py").write_text(MORE)
    out = run("refactor.py", "pin", cwd=project)
    assert "REFACTOR: PINNED (2 test files pass on the code as it is, 1 of them written for this change)" in out, out

    # The refactoring, with the tests left alone.
    (project / "src/pricing.py").write_text(NEW)
    assert run("refactor.py", "status", cwd=project).startswith("REFACTOR: HELD (2 pinned test files are unchanged)")

    reports = project / ".harness/runtime/claude/artifacts"
    reports.mkdir(parents=True)

    def review(expect):
        run("route.py", "plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND", cwd=project)
        for agent in ("validator", "backend-code-review", "detail-analyst", "reviewer"):
            (reports / f"{agent}-report.md").write_text(f"# {agent}\n")
            run("route.py", "gate", "--runtime", "claude", "--agent", agent, "--decision", "PASS",
                "--report", f".harness/runtime/claude/artifacts/{agent}-report.md", cwd=project)
        out = run("route.py", "ready", "--runtime", "claude", cwd=project, expect=0 if expect != "PRE_PR_BLOCKED" else 1)
        assert out.splitlines()[0] == expect, out
        return out

    # Pinned but the tests were not run on this version: a condition, not a pass.
    out = review("PRE_PR_PASS_WITH_CONDITIONS")
    assert "the tests pinned before this refactoring were not run on this version" in out, out
    run("check.py", cwd=project)
    out = review("PRE_PR_PASS")
    assert "refactoring: 2 of 2 test files pinned before the change are unchanged" in out, out

    # Editing or removing a pinned test, or adding one after the fact, is said; the first two are conditions for a person.
    (project / "tests/test_member.py").write_text(MORE.replace("45)", "45.0)"))
    (project / "tests/test_pricing.py").unlink()
    (project / "tests/test_late.py").write_text(TESTS)
    out = run("refactor.py", "status", cwd=project, expect=1)
    assert "REFACTOR: TESTS CHANGED (2 of 2 pinned test files)" in out and "  edited: tests/test_member.py" in out, out
    assert "  removed: tests/test_pricing.py" in out and "added after the pin: tests/test_late.py" in out, out
    run("check.py", cwd=project)
    out = review("PRE_PR_PASS_WITH_CONDITIONS")
    assert "changed tests that were pinned before it started" in out and "tests/test_member.py (edited), tests/test_pricing.py (removed)" in out, out

    # A pin belongs to its branch and starting point; another change is not judged by it. `clear` withdraws it.
    git(project, "stash", "-q", "-u")
    git(project, "checkout", "-q", "-b", "feature/other", "main")
    assert run("refactor.py", "status", cwd=project, expect=1).startswith("REFACTOR: NOT PINNED")
    git(project, "checkout", "-q", "refactor/pricing")
    assert "pinned test files" in run("refactor.py", "status", cwd=project, expect=1)  # recognised again on its own branch
    assert "pin removed" in run("refactor.py", "clear", cwd=project) and "nothing was pinned" in run("refactor.py", "clear", cwd=project)

    # Nothing to pin against: no test command, or no tests.
    (project / ".harness/project.yaml").write_text("checks: {}\n")
    assert "no test command" in run("refactor.py", "pin", cwd=project, expect=1)

print("REFACTOR TESTS: PASS")
