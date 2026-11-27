"""The project's own checks, run once and tied to the version of the change. Run: python3 tests/test_check.py"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "distribution/core/.harness/bin"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(ROOT))
import check  # noqa: E402

from gantry import detect  # noqa: E402


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args], cwd=cwd, check=True, capture_output=True)


def run(tool, *args, cwd, expect=0):
    proc = subprocess.run([sys.executable, str(BIN / tool), *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == expect, (args, proc.returncode, proc.stdout, proc.stderr)
    return proc.stdout


def tree(files):
    root = Path(tempfile.mkdtemp(prefix="gantry-check-"))
    for name, text in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(text)
    return root


# Detection: a format command is recorded only when it checks; a script that rewrites files is not one.
found = lambda files: detect.detect(tree(files))["checks"].get("format", {}).get("command")
assert found({"package.json": json.dumps({"scripts": {"format": "prettier --write .", "format:check": "prettier --check ."}})}) == "npm run format:check"
assert found({"package.json": json.dumps({"scripts": {"format": "prettier --write ."}})}) is None
assert found({"pyproject.toml": "[project]\ndependencies = ['black']\n"}) == "black --check ."
assert found({"pyproject.toml": "[tool.ruff]\n[tool.ruff.format]\nquote-style = 'single'\n", "uv.lock": ""}) == "uv run ruff format --check ."
assert found({"pyproject.toml": "[tool.ruff]\nline-length = 100\n"}) is None
assert found({"Cargo.toml": "[package]\n"}) == "cargo fmt --check"
assert found({"Makefile": "fmt-check:\n\ttrue\n"}) == "make fmt-check"
described = detect.render(detect.detect(tree({"Cargo.toml": "[package]\n"})))
assert list(check.commands(tree({".harness/project.yaml": described}))) == ["format", "lint", "test", "build"], described

py = sys.executable
with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp).resolve()
    (project / "src").mkdir()
    (project / "tests").mkdir()
    (project / ".harness").mkdir()
    (project / ".harness/.gitignore").write_text("runtime/\n")
    (project / ".gitignore").write_text("__pycache__/\n")  # as a real project has: what a test run leaves is not the change
    (project / ".harness/harness.config.yaml").write_text("pre_pr:\n  mutation: false\n")
    (project / "tools").mkdir()
    # Stand-ins for a linter and a formatter: fail when the code holds a marker.
    (project / "tools/lint.py").write_text("import pathlib, sys\nbad = 'TODO' in pathlib.Path('src/pricing.py').read_text()\nprint('src/pricing.py: TODO left in code' if bad else 'clean')\nsys.exit(bad)\n")
    (project / ".harness/project.yaml").write_text(
        "kind: \"brownfield\"\nnotes: []\nchecks:\n"
        f"  test:\n    command: \"{py} -B -m unittest discover -s tests -q\"\n    source: \"x\"\n"
        f"  lint:\n    command: \"{py} tools/lint.py\"\n    source: \"x\"\n"
        f"  build:\n    command: '{py} -c pass'\n    source: \"x\"\n")
    (project / "src/__init__.py").write_text("")
    (project / "src/pricing.py").write_text("def shipping(total):\n    return 5\n")
    (project / "tests/test_pricing.py").write_text(
        "import unittest\nfrom src.pricing import *\n\nclass Pricing(unittest.TestCase):\n    def test_shipping(self):\n        self.assertEqual(shipping(10), 5)\n")
    git(project, "init", "-q", "-b", "main")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "base")
    git(project, "checkout", "-q", "-b", "feature")

    assert list(check.commands(project)) == ["lint", "test", "build"]  # fastest kinds first, whatever the file's order
    assert run("check.py", "status", cwd=project, expect=1).startswith("CHECKS: NOT RUN")

    # A change that breaks the linter and a test: every check is run, and one run says everything that is wrong.
    (project / "src/pricing.py").write_text("def shipping(total):\n    return 6  # TODO\n")
    out = run("check.py", cwd=project, expect=1)
    assert "check: lint       FAIL (exit 1)" in out and "    src/pricing.py: TODO left in code" in out, out
    assert "check: test       FAIL (exit 1)" in out and "AssertionError: 6 != 5" in out, out
    assert "check: build      PASS" in out and "check: typecheck  NOT CONFIGURED" in out, out
    assert "CHECKS: FAIL (failed: lint, test; passed: build)" in out and "fix the code, not the check" in out, out
    assert run("check.py", "status", cwd=project, expect=1) == out  # read again, nothing run

    # The final gate blocks on a check that fails on the version being reviewed, whatever the gates said.
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

    out = review("PRE_PR_BLOCKED")
    assert "the project's `lint` check fails on this version of the change" in out and "the project's `test` check fails" in out, out

    # Fixing one and rerunning only it keeps the others' results for the same version... which an edit has made stale.
    (project / "src/pricing.py").write_text("def shipping(total):\n    return 6\n")
    assert run("check.py", "status", cwd=project, expect=1).startswith("CHECKS: STALE")
    out = run("check.py", "--only", "lint", cwd=project)
    assert "CHECKS: INCOMPLETE (passed: lint; not run: test, build)" in out, out
    assert "check: lint" in run("check.py", "status", cwd=project, expect=1)  # incomplete is not a pass
    out = run("check.py", "--only", "test,build", cwd=project, expect=1)
    assert "CHECKS: FAIL (failed: test; passed: lint, build)" in out, out  # lint kept from the run on this same version

    # All green: the gate passes and says under quality that the checks ran.
    (project / "tests/test_pricing.py").write_text((project / "tests/test_pricing.py").read_text().replace("(shipping(10), 5)", "(shipping(10), 6)"))
    out = run("check.py", cwd=project)
    assert out.splitlines()[-1] == "CHECKS: PASS (passed: lint, test, build)", out
    assert run("check.py", "status", cwd=project) == out
    out = review("PRE_PR_PASS")
    assert "pillar: quality: validator PASS, backend-code-review PASS, detail-analyst PASS, reviewer PASS, checks run by check.py: lint, test, build passed" in out, out
    saved = json.loads((project / ".harness/runtime/checks.json").read_text())

    # The Validator's rejection is what a check says. With every listed check passing on this version it is refused,
    # and the defect it saw by reading goes on as a trigger for the gate that owns that risk.
    def validator(decision, *extra, expect=0):
        proc = subprocess.run([py, str(BIN / "route.py"), "gate", "--runtime", "claude", "--agent", "validator", "--decision", decision,
                               "--report", ".harness/runtime/claude/artifacts/validator-report.md", *extra], cwd=project, capture_output=True, text=True)
        assert proc.returncode == expect, (decision, proc.returncode, proc.stdout, proc.stderr)
        return proc.stdout + proc.stderr

    out = validator("CHANGES_REQUIRED", expect=2)
    assert "CHANGES_REQUIRED was not recorded" in out and '--decision PASS --trigger "<DIMENSION>=<what it saw>"' in out, out
    out = validator("PASS", "--trigger", "SECURITY=the filter drops the tenant condition")
    assert "next: validator reported a risk the plan does not cover" in out, out
    validator("BLOCKED")  # a check that could not be run is still the Validator's to say
    run("route.py", "gate", "--runtime", "claude", "--agent", "backend-code-review", "--decision", "CHANGES_REQUIRED",
        "--report", ".harness/runtime/claude/artifacts/backend-code-review-report.md", cwd=project)  # only the Validator is held to the checks
    # One check not run on this version, or one failing, and the rejection is the Validator's again.
    (project / ".harness/runtime/checks.json").write_text(json.dumps({**saved, "checks": {k: v for k, v in saved["checks"].items() if k != "build"}}))
    validator("CHANGES_REQUIRED")
    (project / ".harness/runtime/checks.json").write_text(json.dumps(saved))

    # A result is for the commands the project has now: change a command and its result no longer counts.
    text = (project / ".harness/project.yaml").read_text()
    (project / ".harness/project.yaml").write_text(text.replace("tools/lint.py", "tools/lint.py --strict"))
    assert run("check.py", "status", cwd=project, expect=1).startswith("CHECKS: STALE")
    (project / ".harness/project.yaml").write_text(text)

    # Never run and never asked for: the gate does not require it. Unknown names and a command that cannot start are said.
    (project / ".harness/runtime/checks.json").unlink()
    assert "checks run by" not in review("PRE_PR_PASS")
    proc = subprocess.run([py, str(BIN / "check.py"), "--only", "types"], cwd=project, capture_output=True, text=True)
    assert proc.returncode == 2 and "no check named types; the project has: lint, test, build" in proc.stderr, proc
    (project / ".harness/project.yaml").write_text("checks:\n  lint:\n    command: \"no-such-tool-xyz --check\"\n")
    out = run("check.py", cwd=project, expect=1)
    assert "check: lint       FAIL (did not start)" in out and "without a shell" in out, out
    (project / ".harness/project.yaml").write_text(f"checks:\n  test:\n    command: \"{py} -c 'import time; time.sleep(5)'\"\n")
    assert "check: test       FAIL (timed out)" in run("check.py", "--timeout", "0.5", cwd=project, expect=1)
    (project / ".harness/project.yaml").write_text("checks: {}\n")
    assert run("check.py", cwd=project).startswith("CHECKS: NOTHING TO RUN")

print("CHECK TESTS: PASS")
