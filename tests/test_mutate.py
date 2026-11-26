"""Mutation testing of the lines a change adds. Run: python3 tests/test_mutate.py"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "distribution/core/.harness/bin"
sys.path.insert(0, str(BIN))
import mutate  # noqa: E402


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args], cwd=cwd, check=True, capture_output=True)


def run(tool, *args, cwd, expect=0):
    proc = subprocess.run([sys.executable, str(BIN / tool), *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == expect, (args, proc.returncode, proc.stdout, proc.stderr)
    return proc.stdout


# One small change per operator; strings, imports, types, arrows and generics are left alone.
changes = lambda line: {(m["was"], m["now"]) for m in mutate.mutants_of(line)}
assert changes("  return total >= 100") == {(">=", ">")}
assert changes("if (a === b && !done) {") == {("===", "!=="), ("&&", "||"), ("!", "")}
assert changes("    if not ready or count < limit:") == {("not", ""), ("or", "and"), ("<", "<=")}
assert changes("const total = price * quantity + shipping;") == {("*", "/"), ("+", "-")}
assert changes("return { active: true };") == {("true", "false")}
for untouched in ('const message = "a >= b && true";', "import { a } from './a';", "const f = (x: Map<string, number>) => x;",
                  "export type Level = 'a' | 'b';", "// if (a >= b)", "const n = -1;", "items.map((item) => item.id)"):
    assert mutate.mutants_of(untouched) == [], (untouched, mutate.mutants_of(untouched))

with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp).resolve()
    (project / "src").mkdir()
    (project / "tests").mkdir()
    (project / ".harness").mkdir()
    (project / ".harness/.gitignore").write_text("runtime/\n")
    (project / ".harness/harness.config.yaml").write_text("pre_pr:\n  mutation: true\n")
    (project / ".harness/project.yaml").write_text(f'checks:\n  test:\n    command: "{sys.executable} -m unittest discover -s tests -q"\n    source: "test"\n')
    (project / "src/__init__.py").write_text("")
    (project / "src/pricing.py").write_text("def shipping(total):\n    return 5\n")
    (project / "tests/test_pricing.py").write_text(
        "import unittest\nfrom src.pricing import *\n\nclass Pricing(unittest.TestCase):\n    def test_shipping(self):\n        self.assertEqual(shipping(10), 5)\n")
    git(project, "init", "-q", "-b", "main")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "base")
    git(project, "checkout", "-q", "-b", "feature")
    # The rule: a discount from a total of 100. The tests try 99 and 101, so they execute the line and miss its boundary.
    with (project / "src/pricing.py").open("a") as file:
        file.write("\n\ndef qualifies_for_discount(total):\n    return total >= 100\n")
    with (project / "tests/test_pricing.py").open("a") as file:
        file.write("\n    def test_discount(self):\n        self.assertFalse(qualifies_for_discount(99))\n        self.assertTrue(qualifies_for_discount(101))\n")
    source = (project / "src/pricing.py").read_text()

    (project / ".harness/harness.config.yaml").write_text("pre_pr:\n  mutation: false\n")
    assert "MUTATION: OFF" in run("mutate.py", cwd=project)  # nothing runs unless the project asked
    assert not (project / ".harness/runtime/mutation.json").exists()
    git(project, "checkout", "-q", ".harness/harness.config.yaml")

    out = run("mutate.py", cwd=project)
    assert out.splitlines()[0] == "MUTATION: SURVIVORS (0 of 1 mutants killed)", out
    assert "  survived: src/pricing.py:6 `>=` changed to `>`" in out and "add the test that fails on that change" in out, out
    assert (project / "src/pricing.py").read_text() == source and not (project / ".harness/runtime/mutation-backup.json").exists()

    # The final gate carries it as a condition, and says so under quality.
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

    out = review("PRE_PR_PASS_WITH_CONDITIONS")
    assert "condition: the tests pass with src/pricing.py:6 `>=` changed to `>`; add the test that fails on it" in out, out
    assert "reviewer PASS, mutation: 0 of 1 changes to the added lines were caught by the tests" in out, out

    # The test for exactly 100 kills it. The result belonged to the earlier version, so the gate asks for a new run.
    with (project / "tests/test_pricing.py").open("a") as file:
        file.write("        self.assertTrue(qualifies_for_discount(100))\n")
    assert "mutation testing is on and was not run for this version of the change" in review("PRE_PR_PASS_WITH_CONDITIONS")
    assert run("mutate.py", cwd=project).splitlines()[0] == "MUTATION: PASS (1 of 1 mutants killed)"
    out = review("PRE_PR_PASS")
    assert "mutation: 1 of 1 changes to the added lines were caught by the tests" in out, out

    # A run that was killed halfway leaves a mutant in the code: the gate blocks, and the next run or `restore` puts it back.
    (project / ".harness/runtime/mutation-backup.json").write_text(json.dumps({"path": "src/pricing.py", "content": source}))
    (project / "src/pricing.py").write_text(source.replace(">=", ">"))
    assert "left a deliberate change in the code" in review("PRE_PR_BLOCKED")
    assert "restored src/pricing.py" in run("mutate.py", "restore", cwd=project)
    assert (project / "src/pricing.py").read_text() == source
    assert "nothing to restore" in run("mutate.py", "restore", cwd=project)
    review("PRE_PR_PASS")

    # Bounded: the limit is said, never hidden. Tests that fail before any mutation judge nothing.
    with (project / "src/pricing.py").open("a") as file:
        file.write("\n\ndef band(total):\n    if total >= 500 and total < 1000:\n        return 2\n    return 1 if total > 0 else 0\n")
    out = run("mutate.py", "--max", "2", cwd=project)
    assert "not run (limit of 2 mutants" in out and "of 2 mutants killed" in out, out
    out = run("route.py", "ready", "--runtime", "claude", cwd=project, expect=1)  # the edit made the gates stale; the count is still said
    out = review("PRE_PR_PASS_WITH_CONDITIONS" if "survived:" in run("mutate.py", "--max", "2", cwd=project) else "PRE_PR_PASS")
    assert " not run" in out.split("pillar: quality")[1].splitlines()[0], out
    with (project / "tests/test_pricing.py").open("a") as file:
        file.write("        self.assertTrue(False)\n")
    out = run("mutate.py", cwd=project, expect=1)
    assert "MUTATION: NOT RUN" in out and "does not pass on the change as it is" in out, out
    assert "mutation testing could not run: the tests do not pass before any mutation" in review("PRE_PR_PASS_WITH_CONDITIONS")
    # A change with no runtime logic has nothing to mutate, and the gate asks for nothing.
    git(project, "checkout", "-q", ".")
    git(project, "clean", "-fdq")
    (project / "README.md").write_text("# notes\n")
    assert "NOTHING TO MUTATE" in run("mutate.py", cwd=project)
    out = review("PRE_PR_PASS")
    assert "mutation: nothing to mutate" in out, out

print("MUTATION TESTS: PASS")
