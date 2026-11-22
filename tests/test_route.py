"""Tests for the deterministic router. Run: python3 tests/test_route.py"""
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "distribution/core/.harness/bin/route.py"
SCENARIOS = ROOT / "distribution/core/.harness/evals/end-to-end/scenarios"
sys.path.insert(0, str(ROOT / "evals"))
import scoring  # noqa: E402

spec = importlib.util.spec_from_file_location("route", ROUTE)
route = importlib.util.module_from_spec(spec)
spec.loader.exec_module(route)


def run(*args, cwd=None, expect=0):
    proc = subprocess.run([sys.executable, str(ROUTE), *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == expect, (args, proc.returncode, proc.stdout, proc.stderr)
    return proc


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
                   cwd=cwd, check=True, capture_output=True)


# The router and the scorer agree on the vocabulary.
assert set(route.AGENTS) == set(scoring.AGENTS)
assert tuple(route.WORK_MODES) == scoring.WORK_MODES
assert route.APPLICABILITY == scoring.APPLICABILITY

# Given each scenario's own classification, the rules reproduce its oracle.
checked = 0
for scenario_file in sorted(SCENARIOS.glob("*.yaml")):
    data = yaml.safe_load(scenario_file.read_text())
    if not (data.get("input") or {}).get("work_mode") or not (data.get("input") or {}).get("scopes"):
        continue
    oracle = scoring.load_oracle(scenario_file)
    if not oracle["routing"]:
        continue
    triggers = [{"dimension": d, "evidence": "from scenario"} for d in oracle["risk_triggers"]]
    decisions = route.route(oracle["work_mode"], oracle["scopes"], triggers)
    plan = {key: [] for key in scoring.TEMPLATE_KEYS}
    plan.update(work_mode=oracle["work_mode"], scopes=oracle["scopes"], risk_triggers=triggers,
                agents=[{"agent": a, "applicability": decisions[a][0], "reason": decisions[a][1]} for a in route.AGENTS])
    score = scoring.score_plan(plan, oracle)
    assert score["passed"], (scenario_file.name, score["failure"], score["agents"])
    checked += 1
assert checked >= 6, checked

# Size never suppresses Security; an unqualified architecture trigger covers every layer in scope.
decisions = route.route("IMPLEMENTATION", ["BACKEND"], [{"dimension": "SECURITY", "evidence": "x"}])
assert decisions["security"][0] == "REQUIRED" and decisions["frontend-code-review"][0] == "NOT_APPLICABLE"
both = route.route("IMPLEMENTATION", ["BACKEND", "FRONTEND"], [{"dimension": "ARCHITECTURE", "evidence": "x"}])
assert both["backend-architecture-review"][0] == both["frontend-architecture-review"][0] == "REQUIRED"
one = route.route("IMPLEMENTATION", ["BACKEND", "FRONTEND"], [{"dimension": "ARCHITECTURE", "evidence": "x", "layer": "frontend"}])
assert one["frontend-architecture-review"][0] == "REQUIRED" and one["backend-architecture-review"][0] == "NOT_TRIGGERED"
docs = route.route("IMPLEMENTATION", ["DOCUMENTATION"], [])
assert all(state != "REQUIRED" for state, _, _ in docs.values()), docs

# The plan format round-trips, and any YAML parser reads the same thing.
sample = {"a": "text: with `colon: inside` and \"quotes\"", "b": [], "c": {}, "d": ["x", "y"], "n": 3, "t": True, "z": None,
          "items": [{"k": "v", "deps": ["p", "q"], "empty": []}, {"k": "w", "nested": {"deep": "é"}}]}
text = "\n".join(route.emit(sample)) + "\n"
assert route.parse(text) == sample
assert yaml.safe_load(text) == sample

with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp)
    git(project, "init", "-q")
    (project / "src").mkdir()
    (project / "src/app.ts").write_text("export const a = 1;\n")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "base")
    (project / "src/app.ts").write_text("export const a = 2;\n")
    plan_file = project / ".harness/runtime/claude/routing-plan.yaml"

    out = run("plan", "--runtime", "claude", "--work-mode", "implementation", "--scope", "backend",
              "--trigger", "BEHAVIORAL=value of `a: number` changed", "--trigger", "SECURITY=tenant predicate relaxed",
              cwd=project).stdout
    assert "REQUIRED        security" in out
    plan = yaml.safe_load(plan_file.read_text())  # free text with a colon stays valid YAML
    assert plan == route.parse(plan_file.read_text())
    assert not scoring.validate_plan(plan), scoring.validate_plan(plan)
    assert plan["change_identity"]["type"] == "working-tree" and plan["change_identity"]["changed_files"] == 1
    required = [e["agent"] for e in plan["agents"] if e["applicability"] == "REQUIRED"]
    assert required == ["validator", "backend-code-review", "qa", "security", "detail-analyst", "reviewer"], required
    by_agent = {e["agent"]: e for e in plan["agents"]}
    assert by_agent["security"]["minimal_dependencies"] == ["validator"]
    assert by_agent["reviewer"]["minimal_dependencies"] == required[:-1]
    assert by_agent["qa"]["expected_output"] == "qa-report.md"
    run("check", str(plan_file))

    # Same input, same plan; a different change, a different identity. The plan file itself does not count.
    first = plan_file.read_text()
    run("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND",
        "--trigger", "BEHAVIORAL=value of `a: number` changed", "--trigger", "SECURITY=tenant predicate relaxed", cwd=project)
    assert plan_file.read_text() == first
    (project / "src/app.ts").write_text("export const a = 3;\n")
    run("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND", "--trigger", "BEHAVIORAL=x", cwd=project)
    assert yaml.safe_load(plan_file.read_text())["change_identity"]["value"] != plan["change_identity"]["value"]

    # A hand-edited plan fails the check.
    edited = plan_file.read_text().replace('applicability: "REQUIRED"', 'applicability: "NOT_TRIGGERED"', 1)
    plan_file.write_text(edited)
    assert "edited by hand" in run("check", str(plan_file), expect=1).stdout
    plan_file.write_text("work_mode: IMPLEMENTATION\nrequired_gates:\n  - validator\n")
    assert "not a plan generated by route.py" in run("check", str(plan_file), expect=1).stdout
    run("check", str(project / "missing.yaml"), expect=1)

    # A migration file in the change adds the MIGRATION trigger even if the classification omits it.
    (project / "prisma/migrations/0002").mkdir(parents=True)
    (project / "prisma/migrations/0002/migration.sql").write_text("ALTER TABLE x ADD COLUMN y INT;\n")
    out = run("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND", "--trigger", "BEHAVIORAL=x", cwd=project).stdout
    assert "Added from the changed files: MIGRATION" in out
    plan = yaml.safe_load(plan_file.read_text())
    assert {"MIGRATION": "detected", "BEHAVIORAL": "declared"} == {t["dimension"]: t["source"] for t in plan["risk_triggers"]}
    states = {e["agent"]: e["applicability"] for e in plan["agents"]}
    assert states["infrastructure"] == states["backend-architecture-review"] == "REQUIRED"
    run("check", str(plan_file))
    # ...unless it is dismissed with a recorded reason.
    run("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND", "--trigger", "BEHAVIORAL=x",
        "--dismiss", "MIGRATION=seed data for a test database only", cwd=project)
    plan = yaml.safe_load(plan_file.read_text())
    assert plan["dismissed_signals"] == [{"dimension": "MIGRATION", "reason": "seed data for a test database only"}]
    assert {e["agent"]: e["applicability"] for e in plan["agents"]}["infrastructure"] == "NOT_TRIGGERED"
    run("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND",
        "--dismiss", "INFRASTRUCTURE=nothing to dismiss", cwd=project, expect=2)

    # Bad input is rejected with a message that says what to do.
    for bad in (["--work-mode", "CODING", "--scope", "BACKEND"],
                ["--work-mode", "IMPLEMENTATION", "--scope", "SERVER"],
                ["--work-mode", "IMPLEMENTATION"],
                ["--work-mode", "IMPLEMENTATION", "--scope", "BACKEND", "--trigger", "SECURITY"],
                ["--work-mode", "IMPLEMENTATION", "--scope", "BACKEND", "--trigger", "RISKY=x"],
                ["--work-mode", "IMPLEMENTATION", "--scope", "BACKEND", "--trigger", "ARCHITECTURE@mobile=x"]):
        assert run("plan", "--runtime", "claude", *bad, cwd=project, expect=2).stderr.startswith("route.py: ")

# Works outside a git repository.
with tempfile.TemporaryDirectory() as tmp:
    run("plan", "--runtime", "opencode", "--work-mode", "ARCHITECTURE_ONLY", "--scope", "SOFTWARE_ARCHITECTURE",
        "--trigger", "ARCHITECTURE=new event architecture", cwd=tmp)
    plan = yaml.safe_load((Path(tmp) / ".harness/runtime/opencode/routing-plan.yaml").read_text())
    assert plan["change_identity"] == {"type": "unversioned", "value": "none", "changed_files": 0}

assert "SECURITY:" in run("vocabulary").stdout
print("ROUTER TESTS: PASS")
