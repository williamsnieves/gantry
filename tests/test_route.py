"""Tests for the deterministic router. Run: python3 tests/test_route.py"""
import hashlib
import importlib.util
import json
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
    assert plan["change_identity"]["type"] == "content" and plan["change_identity"]["changed_files"] == 1
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

# The Final Pre-PR Gate is computed from recorded gate results, for the current change only.
with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp)
    git(project, "init", "-q", "-b", "main")
    (project / "src").mkdir()
    (project / "src/app.ts").write_text("export const a = 1;\n")
    (project / "eslint.config.js").write_text("export default [];\n")
    (project / "docs/specs").mkdir(parents=True)
    (project / "docs/specs/change.md").write_text("# Change\n")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "base")
    git(project, "checkout", "-q", "-b", "feature")
    (project / "src/app.ts").write_text("export const a = 2;\n")
    reports = project / ".harness/runtime/claude/artifacts"
    reports.mkdir(parents=True)

    def ready(expect):
        out = run("ready", "--runtime", "claude", cwd=project, expect=0 if expect != "PRE_PR_BLOCKED" else 1).stdout
        assert out.splitlines()[0] == expect, out
        return out

    def gate(agent, decision, *extra, expect=0):
        (reports / f"{agent}-report.md").write_text(f"# {agent}\n{decision}\n")
        return run("gate", "--runtime", "claude", "--agent", agent, "--decision", decision,
                   "--report", f".harness/runtime/claude/artifacts/{agent}-report.md", *extra, cwd=project, expect=expect)

    def plan(*sources):
        sources = sources or ("docs/specs/change.md",)
        return run("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND", "--trigger", "BEHAVIORAL=x",
                   *[a for source in sources for a in ("--behavior-source", source)], cwd=project).stdout

    assert "no routing plan" in ready("PRE_PR_BLOCKED")
    plan()
    required = ["validator", "backend-code-review", "qa", "detail-analyst", "reviewer"]
    out = ready("PRE_PR_BLOCKED")
    assert all(f"{agent}: required gate has no recorded result" in out for agent in required), out

    # The router names the stage to run next and stops the review at the first stage that does not pass.
    following = lambda: run("next", "--runtime", "claude", cwd=project).stdout.strip()
    assert following() == "next: run validator", following()
    out = gate("validator", "CHANGES_REQUIRED").stdout
    assert "next: stop. validator did not pass; do not run backend-code-review, qa, detail-analyst, reviewer" in out, out
    out = ready("PRE_PR_BLOCKED")
    assert "validator: CHANGES_REQUIRED" in out and "qa: not run, the review stopped when validator did not pass" in out, out
    assert "next: run backend-code-review, qa" in gate("validator", "PASS").stdout
    # A stage is finished before it stops: the specialists were launched together.
    assert "next: run qa" in gate("backend-code-review", "BLOCKED").stdout
    out = gate("qa", "PASS").stdout
    assert "next: stop. backend-code-review did not pass; do not run detail-analyst, reviewer" in out, out
    assert "next: run detail-analyst" in gate("backend-code-review", "PASS").stdout
    assert "next: run reviewer" in gate("detail-analyst", "PASS").stdout
    assert "next: run `route.py ready --runtime claude`" in gate("reviewer", "PASS").stdout
    (project / ".harness/runtime/claude/gates.json").unlink()

    # Missing evidence is not a pass; a gate result needs a real report and valid arguments.
    run("gate", "--runtime", "claude", "--agent", "qa", "--decision", "PASS", cwd=project, expect=2)
    run("gate", "--runtime", "claude", "--agent", "qa", "--decision", "PASS", "--report", "nope.md", cwd=project, expect=2)
    gate("qa", "PASS_WITH_CONDITIONS", expect=2)
    gate("qa", "PASS", "--condition", "x", expect=2)

    for agent in required[:-1]:
        gate(agent, "PASS")
    assert "reviewer: required gate has no recorded result" in ready("PRE_PR_BLOCKED")
    assert "pillar:" not in ready("PRE_PR_BLOCKED")
    gate("reviewer", "PASS")
    assert "pillar: quality: validator PASS, backend-code-review PASS, qa PASS, detail-analyst PASS, reviewer PASS" in ready("PRE_PR_PASS")

    # A change in the SPEC or DESIGN lane that names no specification passes, with a condition that says so.
    plan_file = project / ".harness/runtime/claude/routing-plan.yaml"
    specified = plan_file.read_text()
    assert 'lane: "SPEC"' in specified and "Lane: SPEC" in plan() and "Note:" not in plan()
    run("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND", "--trigger", "BEHAVIORAL=x", cwd=project)
    assert "lane SPEC but no --behavior-source was given" in ready("PRE_PR_PASS_WITH_CONDITIONS")
    assert "Note: lane SPEC but none of docs/specs/nope.md exists" in plan("docs/specs/nope.md")
    assert "none of docs/specs/nope.md exists" in ready("PRE_PR_PASS_WITH_CONDITIONS")
    # The lane is part of the plan: editing it by hand invalidates the plan.
    plan_file.write_text(specified.replace('lane: "SPEC"', 'lane: "DIRECT"'))
    assert "routing plan is invalid" in ready("PRE_PR_BLOCKED")
    plan_file.write_text(specified)
    ready("PRE_PR_PASS")

    # A design counts as approved only while the text a person approved is unchanged.
    def design(*sources):
        return run("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND", "--trigger", "DATA_INTEGRITY=x",
                   *[a for source in sources for a in ("--behavior-source", source)], cwd=project).stdout

    assert "Lane: DESIGN" in design("docs/specs/change.md") and "no person approved docs/specs/change.md" in design("docs/specs/change.md")
    for agent in required:
        gate(agent, "PASS")
    assert "spec.py approve docs/specs/change.md" in ready("PRE_PR_PASS_WITH_CONDITIONS")
    approvals = project / ".harness/runtime/approvals.json"
    approvals.write_text(json.dumps({"docs/specs/change.md": {"sha256": hashlib.sha256(b"# Change\n").hexdigest()}}))
    ready("PRE_PR_PASS")
    approvals.write_text(json.dumps({"docs/specs/change.md": {"sha256": "0" * 64}}))
    assert "no person approved" in ready("PRE_PR_PASS_WITH_CONDITIONS")
    approvals.unlink()
    plan()
    for agent in required:
        gate(agent, "PASS")
    ready("PRE_PR_PASS")

    # A risk a gate reports outside its own scope survives its pass: the router asks for it to be routed,
    # and the final gate carries a condition until the plan covers it.
    out = gate("validator", "PASS", "--trigger", "SECURITY=severity filter drops the tenant predicate").stdout
    assert 'next: validator reported a risk the plan does not cover' in out and '--trigger "SECURITY=severity filter drops' in out, out
    out = ready("PRE_PR_PASS_WITH_CONDITIONS")
    assert "validator reported a SECURITY risk that no routed gate judged: severity filter drops the tenant predicate" in out, out
    gate("validator", "PASS", "--trigger", "BEHAVIORAL=already in the plan")
    ready("PRE_PR_PASS")
    gate("validator", "PASS", "--trigger", "RISKY=x", expect=2)
    gate("validator", "PASS")

    # One blocker is not averaged away by four passes.
    gate("qa", "CHANGES_REQUIRED")
    assert "qa: CHANGES_REQUIRED" in ready("PRE_PR_BLOCKED")
    gate("qa", "PASS_WITH_CONDITIONS", "--condition", "add a test for the empty title")
    assert "condition: qa: add a test for the empty title" in ready("PRE_PR_PASS_WITH_CONDITIONS")
    gate("qa", "PASS")

    # Tampering with a report after it was recorded invalidates that gate.
    (reports / "qa-report.md").write_text("rewritten\n")
    assert "qa: report" in ready("PRE_PR_BLOCKED")
    gate("qa", "PASS")
    ready("PRE_PR_PASS")

    # Committing the same content keeps the identity, so readiness survives the commit.
    git(project, "add", "src")
    git(project, "commit", "-q", "-m", "change")
    ready("PRE_PR_PASS")

    # Any edit after the gates makes readiness stale.
    (project / "src/app.ts").write_text("export const a = 3;\n")
    assert "edited after the routing plan" in ready("PRE_PR_BLOCKED")
    plan()
    assert ready("PRE_PR_BLOCKED").count("result is stale") == 5
    # Rerun the invalidated gates, carry the others forward with a reason.
    for agent in ("validator", "backend-code-review", "qa"):
        gate(agent, "PASS")
    run("gate", "--runtime", "claude", "--agent", "detail-analyst", "--carry-forward", "no spec or doc touched", cwd=project)
    run("gate", "--runtime", "claude", "--agent", "reviewer", "--carry-forward", "x", "--decision", "PASS", cwd=project, expect=2)
    gate("reviewer", "PASS")
    assert "detail-analyst: carried forward (no spec or doc touched)" in ready("PRE_PR_PASS_WITH_CONDITIONS")

    # A change that edits the checks that judge it always carries a condition for a person.
    (project / "eslint.config.js").write_text("export default [{ rules: {} }];\n")
    plan()
    for agent in required:
        gate(agent, "PASS")
    assert "a person must review: eslint.config.js" in ready("PRE_PR_PASS_WITH_CONDITIONS")

# Review receipts: what CI can check about a pull request is that its content is the content that was reviewed.
with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp)
    git(project, "init", "-q", "-b", "main")
    (project / "src").mkdir()
    (project / "src/app.ts").write_text("export const a = 1;\n")
    (project / ".harness").mkdir()
    (project / ".harness/.gitignore").write_text("runtime/\n")
    (project / ".harness/harness.config.yaml").write_text("pre_pr:\n  receipts: false\n")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "base")
    git(project, "checkout", "-q", "-b", "feature")
    verify = lambda *extra, expect=0: run("verify", *extra, cwd=project, expect=expect).stdout
    assert "NOTHING TO VERIFY" in verify()
    (project / "src/app.ts").write_text("export const a = 2;\n")
    reports = project / ".harness/runtime/claude/artifacts"
    reports.mkdir(parents=True)

    def review():
        run("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND", cwd=project)
        for agent in ("validator", "backend-code-review", "detail-analyst", "reviewer"):
            (reports / f"{agent}-report.md").write_text(f"# {agent}\n")
            run("gate", "--runtime", "claude", "--agent", agent, "--decision", "PASS",
                "--report", f".harness/runtime/claude/artifacts/{agent}-report.md", cwd=project)
        return run("ready", "--runtime", "claude", cwd=project).stdout

    receipts = lambda: sorted(p.name for p in (project / ".harness/receipts").glob("*.json"))
    # Off unless the project asked for them: nothing is written, and CI says how to turn them on.
    assert "receipt:" not in review() and not (project / ".harness/receipts").exists()
    out = verify(expect=1)
    assert "REVIEW RECEIPT: FAIL" in out and "no receipt for this version of the change" in out and "--receipts" in out, out
    (project / ".harness/harness.config.yaml").write_text("pre_pr:\n  receipts: true\n")
    git(project, "commit", "-q", "-am", "turn receipts on")  # as an install on the default branch would have
    out = review()
    assert "receipt: .harness/receipts/" in out and len(receipts()) == 1, out
    first = receipts()[0]
    written = json.loads((project / ".harness/receipts" / first).read_text())
    assert written["status"] == "PRE_PR_PASS" and written["gates"]["reviewer"] == "PASS" and written["lane"] == "DIRECT", written
    assert written["change"] == "sha256:" + first[:-5]
    # The gate says, pillar by pillar, who judged the change; a pillar nobody judged is said, not left out.
    assert "  pillar: quality: validator PASS, backend-code-review PASS, detail-analyst PASS, reviewer PASS" in out, out
    assert "  pillar: security: added lines scanned for secrets and risky patterns; no specialist gate ran, no SECURITY trigger" in out, out
    assert "  pillar: scalability: no specialist gate ran, no PERFORMANCE or INFRASTRUCTURE trigger was declared or detected" in out, out
    assert len(written["pillars"]) == 4 and written["pillars"][2].startswith("performance: added lines scanned for queries in loops and unbounded reads; no specialist gate ran"), written
    # The receipt is not part of the change it describes: writing and committing it leaves the review valid.
    assert review().splitlines()[0] == "PRE_PR_PASS" and receipts() == [first]
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "change")
    out = verify("--base", "main")
    assert out.startswith("REVIEW RECEIPT: PASS (PRE_PR_PASS, 2 files, gates: validator, backend-code-review, detail-analyst, reviewer)"), out
    assert "  pillar: performance: added lines scanned" in out, out
    # An edit after the review is a version nobody reviewed, committed or not.
    (project / "src/app.ts").write_text("export const a = 3;\n")
    assert "edited after the review" in verify("--base", "main", expect=1)
    # Reviewing it again replaces this change's receipt; one that came from the base branch stays.
    git(project, "commit", "-q", "-am", "edit")
    git(project, "checkout", "-q", "main")
    (project / ".harness/receipts").mkdir()
    (project / ".harness/receipts/0000000000000000.json").write_text("{}\n")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "an earlier change, merged")
    git(project, "checkout", "-q", "feature")
    git(project, "merge", "-q", "main", "-m", "merge main")
    out = review()
    assert receipts() == sorted(["0000000000000000.json", receipts()[-1]]) and first not in receipts(), (receipts(), first)
    assert "REVIEW RECEIPT: PASS" in verify("--base", "main")
    # A receipt written by hand for another outcome, an unknown base, and a shallow checkout do not pass.
    mine = project / ".harness/receipts" / receipts()[-1]
    mine.write_text(mine.read_text().replace("PRE_PR_PASS", "PRE_PR_BLOCKED"))
    assert "does not record a passed review" in verify("--base", "main", expect=1)
    assert "cannot find where this change leaves origin/nope" in verify("--base", "origin/nope", expect=1)
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "all")
    shallow = Path(tmp + "-shallow")
    subprocess.run(["git", "clone", "-q", "--depth", "1", "file://" + str(project), str(shallow)], check=True, capture_output=True)
    assert "the checkout is shallow" in run("verify", cwd=shallow, expect=1).stdout
    import shutil
    shutil.rmtree(shallow)
assert route.protection(".harness/receipts/abc.json")[0] == "harness"

# Protected paths.
for path, kind in ((".harness/core/routing/ROUTING-POLICY.md", "harness"), (".harness/bin/route.py", "harness"),
                   ("./.claude/settings.json", "harness"), (".harness/runtime/claude/routing-plan.yaml", "harness"),
                   (".harness/runtime/opencode/gates.json", "harness"), ("eslint.config.js", "quality-config"),
                   ("apps/web/tsconfig.json", "quality-config"), (".github/workflows/ci.yml", "quality-config"),
                   ("apps/api/vitest.config.ts", "quality-config"), (".prettierrc.json", "quality-config")):
    assert (route.protection(path) or ("",))[0] == kind, path
for path in ("src/app.ts", ".harness/runtime/claude/artifacts/qa-report.md", "package.json", "docs/eslint.md",
             "apps/api/src/config.ts", ".claude/agents/qa.md"):
    assert route.protection(path) is None, path

# Works outside a git repository.
with tempfile.TemporaryDirectory() as tmp:
    run("plan", "--runtime", "opencode", "--work-mode", "ARCHITECTURE_ONLY", "--scope", "SOFTWARE_ARCHITECTURE",
        "--trigger", "ARCHITECTURE=new event architecture", cwd=tmp)
    plan = yaml.safe_load((Path(tmp) / ".harness/runtime/opencode/routing-plan.yaml").read_text())
    assert plan["change_identity"] == {"type": "unversioned", "value": "none", "changed_files": 0}

assert "SECURITY:" in run("vocabulary").stdout

# The guardrail table in the README is the one the router prints.
table = run("guardrails").stdout.strip()
assert all(phase in table for phase in ("ANY", "SPECIFY", "BUILD", "REVIEW", "RELEASE", "OPERATE")), table
assert table in (ROOT / "README.md").read_text(encoding="utf-8"), "README guardrail table differs from `route.py guardrails`"

# The lane is decided before any code exists, from the triggers and never from the size of the work.
def lane_of(mode, *triggers):
    arguments = [a for trigger in triggers for a in ("--trigger", f"{trigger}=evidence")]
    return run("lane", "--work-mode", mode, *arguments).stdout.splitlines()[0]

assert lane_of("IMPLEMENTATION") == "lane: DIRECT"
assert lane_of("REMEDIATION") == "lane: DIRECT"
assert lane_of("IMPLEMENTATION", "BEHAVIORAL") == "lane: SPEC"
assert lane_of("IMPLEMENTATION", "USER_IMPACT", "PERFORMANCE") == "lane: SPEC"
assert lane_of("IMPLEMENTATION", "BEHAVIORAL", "SECURITY") == "lane: DESIGN"
assert lane_of("IMPLEMENTATION", "DATA_INTEGRITY") == "lane: DESIGN"
assert lane_of("MIGRATION") == "lane: DESIGN"
assert lane_of("REVIEW_ONLY", "SECURITY") == "lane: NONE"

# The model tier follows the gate's job and the lane: nothing is saved on a risky change or on the gates that judge risk.
for agent in route.AGENTS:
    assert route.tier(agent, "DESIGN") == ("standard" if agent == "validator" else "deep"), agent
    assert route.tier(agent, "DIRECT") == route.tier(agent, "SPEC"), agent
assert route.tier("validator", "SPEC") == "fast" and route.tier("qa", "SPEC") == "standard"
assert all(route.tier(agent, "DIRECT") == "deep" for agent in route.DEEP_AGENTS)
assert set(route.DEEP_AGENTS) <= set(route.AGENTS)

with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp)
    plan_args = ("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND")
    out = run(*plan_args, "--trigger", "BEHAVIORAL=x", cwd=project).stdout
    # With no models file every gate runs on the session's model, and the plan still records the tier.
    assert "validator" in out and "[fast]" in out and "[deep]" in out and "models:" not in out, out
    plan_file = project / ".harness/runtime/claude/routing-plan.yaml"
    written = yaml.safe_load(plan_file.read_text())
    tiers = {e["agent"]: e["model_tier"] for e in written["agents"]}
    assert tiers["validator"] == "fast" and tiers["qa"] == "standard" and tiers["reviewer"] == "deep", tiers
    plan_file.write_text(plan_file.read_text().replace('model_tier: "deep"', 'model_tier: "fast"'))
    assert "ROUTING PLAN: FAIL" in run("check", str(plan_file), expect=1).stdout  # a tier edited by hand invalidates the plan
    # The project's file maps tiers to models for its runtime; an empty value and another runtime's section change nothing.
    (project / ".harness/models.yaml").write_text(
        "# comment\nclaude:\n  fast: haiku   # cheap\n  standard: \"sonnet\"\n  deep: \"\"\nopencode:\n  deep: other/model\n  fast: x\n")
    assert route.configured_models(project, "claude") == {"fast": "haiku", "standard": "sonnet"}
    assert route.configured_models(project, "opencode") == {"deep": "other/model", "fast": "x"}
    assert route.configured_models(project, "cursor") == {}
    out = run(*plan_args, "--trigger", "BEHAVIORAL=x", cwd=project).stdout
    assert "[fast: haiku]" in out and "[standard: sonnet]" in out and "[deep]" in out, out
    assert out.rstrip().endswith("next: run validator\nmodels: launch validator=haiku"), out
    assert route.gate_models(project, "claude") == {"validator": "haiku", "backend-code-review": "sonnet", "qa": "sonnet",
                                                    "detail-analyst": "sonnet"}, route.gate_models(project, "claude")
    # The same gates on a change in the DESIGN lane move up a tier.
    out = run(*plan_args, "--trigger", "DATA_INTEGRITY=x", cwd=project).stdout
    assert "[standard: sonnet]" in out and "[fast" not in out and out.count("[deep]") >= 3, out
    assert route.gate_models(project, "claude") == {"validator": "sonnet"}, route.gate_models(project, "claude")
assert "spec.py check" in run("lane", "--work-mode", "IMPLEMENTATION", "--trigger", "BEHAVIORAL=x").stdout
assert "spec.py" not in run("lane", "--work-mode", "IMPLEMENTATION").stdout
run("lane", "--work-mode", "IMPLEMENTATION", "--trigger", "BEHAVIORAL", expect=2)  # a trigger needs evidence
run("lane", "--work-mode", "NOPE", expect=2)
print("ROUTER TESTS: PASS")
