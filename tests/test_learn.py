"""Rules a project learned from what went wrong, applied by the router. Run: python3 tests/test_learn.py"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "distribution/core/.harness/bin"
sys.path.insert(0, str(BIN))
import route  # noqa: E402


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args], cwd=cwd, check=True, capture_output=True)


def run(tool, *args, cwd, expect=0):
    proc = subprocess.run([sys.executable, str(BIN / tool), *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == expect, (args, proc.returncode, proc.stdout, proc.stderr)
    return proc.stdout + proc.stderr


assert route.rule_matches("apps/api/", "apps/api/src/a.ts") and not route.rule_matches("apps/api/", "apps/web/a.ts")
assert route.rule_matches("src/*.sql", "src/a.sql") and route.rule_matches("src/pay.ts", "src/pay.ts") and not route.rule_matches("src/pay.ts", "src/pay.tsx")

with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp).resolve()
    (project / "apps/api/src/incidents").mkdir(parents=True)
    (project / "apps/api/src/incidents/list.ts").write_text("export const a = 1;\n")
    (project / "apps/web").mkdir()
    (project / "apps/web/page.tsx").write_text("export const b = 1;\n")
    git(project, "init", "-q", "-b", "main")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "base")

    # Nothing happened yet: nothing to propose, nothing learned.
    assert "NOTHING TO PROPOSE" in run("learn.py", "propose", cwd=project)
    assert "NO RULES" in run("learn.py", "list", cwd=project)

    # An incident that names the risk nobody declared is what a rule is proposed from; a shipped change is not.
    run("release.py", "record", "--outcome", "SHIPPED", "--change", "#41 sorting", cwd=project)
    out = run("release.py", "record", "--outcome", "INCIDENT", "--change", "#42 severity filter",
              "--note", "the filtered list showed incidents of other tenants", "--missed", "SECURITY", cwd=project)
    assert "learn.py propose" in out, out
    out = run("learn.py", "propose", cwd=project)
    assert "LEARN: 1 PROPOSAL(S)" in out and "nobody declared SECURITY" in out, out
    assert 'learn.py add --trigger SECURITY --path <folder or file it happened in> --because "the filtered list showed incidents of other tenants" --from "#42 severity filter"' in out, out

    # A person decides where it applies. A rule for everything, an unknown risk, or no reason is refused.
    add = ("learn.py", "add", "--trigger", "SECURITY", "--from", "#42 severity filter")
    run(*add, "--path", "*", "--because", "every query keeps the tenant filter", cwd=project, expect=2)
    run(*add, "--path", "apps/api/src/incidents/", "--because", "careful", cwd=project, expect=2)
    run("learn.py", "add", "--trigger", "RISKY", "--path", "apps/", "--because", "every query keeps the tenant filter", cwd=project, expect=2)
    assert not (project / "docs/learned.md").exists()
    out = run(*add, "--path", "apps/api/src/incidents/", "--because", "a filtered list showed other tenants: every query keeps the tenant filter", cwd=project)
    assert "learned L-1: a change touching apps/api/src/incidents/ is routed with SECURITY" in out, out
    assert route.learned_rules(project) == [{"id": "L-1", "paths": ["apps/api/src/incidents/"], "trigger": "SECURITY",
                                             "because": "a filtered list showed other tenants: every query keeps the tenant filter",
                                             "source": "#42 severity filter"}]
    assert "NOTHING TO PROPOSE" in run("learn.py", "propose", cwd=project)  # the incident is covered now
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "learned")
    git(project, "checkout", "-q", "-b", "feature")

    plan = ("route.py", "plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND")
    # A change elsewhere is not touched by the rule.
    (project / "apps/web/page.tsx").write_text("export const b = 2;\n")
    out = run(*plan, cwd=project)
    assert "learned rule" not in out and "REQUIRED        security" not in out, out
    # A change where it happened is routed to the gate that judges that risk, with the lesson as its evidence.
    (project / "apps/api/src/incidents/list.ts").write_text("export const a = 2;\n")
    out = run(*plan, cwd=project)
    assert "REQUIRED        security" in out and "Lane: DESIGN" in out, out
    written = (project / ".harness/runtime/claude/routing-plan.yaml").read_text()
    assert "learned rule L-1, this project was caught here before: a filtered list showed other tenants: every query keeps the tenant filter (apps/api/src/incidents/list.ts)" in written, written
    # When the agent already declared the risk, the trigger stays one and gains the lesson.
    out = run(*plan, "--trigger", "SECURITY=changes the tenant predicate", cwd=project)
    written = (project / ".harness/runtime/claude/routing-plan.yaml").read_text()
    assert written.count('dimension: "SECURITY"') == 1 and "changes the tenant predicate; learned rule L-1" in written, written
    # It can be dismissed like any detected signal, with a reason that is recorded.
    out = run(*plan, "--dismiss", "SECURITY=only a comment changed", cwd=project)
    assert "REQUIRED        security" not in out, out

    # The rules decide how changes are judged: an agent does not edit them, and a change that does is flagged for a person.
    assert route.protection("docs/learned.md")[0] == "quality-config"
    run("learn.py", "add", "--trigger", "PERFORMANCE", "--path", "apps/web/page.tsx", "--path", "legacy/",
        "--because", "the page loaded every incident at once", cwd=project)
    assert [r["id"] for r in route.learned_rules(project)] == ["L-1", "L-2"]
    out = run("learn.py", "list", cwd=project)
    assert "L-2: apps/web/page.tsx, legacy/ -> PERFORMANCE" in out and "stale" not in out, out
    # A rule whose code is gone is pointed out, and removed by a person.
    run("learn.py", "add", "--trigger", "MIGRATION", "--path", "old-service/", "--because", "the backfill ran before the schema change", cwd=project)
    out = run("learn.py", "list", cwd=project)
    assert "L-3: old-service/ -> MIGRATION" in out and "stale: no file of the project matches" in out and "learn.py remove L-3" in out, out
    assert "removed L-3" in run("learn.py", "remove", "l-3", cwd=project)
    run("learn.py", "remove", "L-9", cwd=project, expect=2)
    assert [r["id"] for r in route.learned_rules(project)] == ["L-1", "L-2"]
    # Rows edited by hand into something that is not a rule are ignored, not obeyed.
    with (project / "docs/learned.md").open("a") as file:
        file.write("| L-7 | `apps/` | EVERYTHING | nope nope nope nope | |\n| note | x | SECURITY | y | |\n")
    assert [r["id"] for r in route.learned_rules(project)] == ["L-1", "L-2"]

# The hook asks the person before a rule is added or removed.
sys.path.insert(0, str(BIN))
import hook  # noqa: E402
ask = lambda command: hook.confirm({"tool_name": "Bash", "tool_input": {"command": command}})
assert "rules this project learned" in ask('python3 .harness/bin/learn.py add --trigger SECURITY --path a/ --because "x y z w"')
assert ask("python3 .harness/bin/learn.py remove L-1") and ask("python3 .harness/bin/learn.py list") is None and ask("python3 .harness/bin/learn.py propose") is None

print("LEARN TESTS: PASS")
