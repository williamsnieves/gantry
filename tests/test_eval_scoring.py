"""Unit tests for evals/scoring.py. Run: python3 tests/test_eval_scoring.py"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))
import scoring  # noqa: E402

SCENARIOS = ROOT / "distribution/core/.harness/evals/end-to-end/scenarios"
CASES = ROOT / "evals/cases"


def oracle(name):
    return scoring.load_oracle(next(SCENARIOS.glob(f"*-{name}.yaml")))


def plan(work_mode, states, **extra):
    base = {key: [] for key in scoring.TEMPLATE_KEYS}
    base.update(routing_plan_version="1.0.0", harness_contract_version="1.0.0",
                change_identity={"type": "working-tree", "value": "x"}, work_mode=work_mode)
    base["agents"] = [
        {"agent": a, "applicability": states.get(a, "NOT_TRIGGERED"), "reason": "because"} for a in scoring.AGENTS
    ]
    base.update(extra)
    return base


SMALL_FRONTEND = {a: "REQUIRED" for a in ("validator", "frontend-code-review", "qa", "detail-analyst", "reviewer")}

# Every case maps to an oracle that loads, and every oracle agent is known.
case_ids = sorted(p.name for p in CASES.iterdir() if (p / "case.yaml").exists())
assert len(case_ids) == 6, case_ids
for case_id in case_ids:
    case = yaml.safe_load((CASES / case_id / "case.yaml").read_text())
    assert case["request"].strip()
    loaded = oracle(case["scenario"])
    assert loaded["routing"] and loaded["work_mode"] in scoring.WORK_MODES, case_id

# architecture-only uses a different oracle shape and is still normalised.
arch = oracle("architecture-only")["routing"]
assert arch["validator"] == "NOT_APPLICABLE" and arch["backend-code-review"] == "NOT_APPLICABLE"
assert arch["reviewer"] == "NOT_TRIGGERED"

# A correct plan passes.
good = scoring.score_plan(plan("IMPLEMENTATION", SMALL_FRONTEND, scopes=["FRONTEND"], risk_triggers=["BEHAVIORAL"]),
                          oracle("small-frontend"))
assert good["passed"] and good["schema_valid"] and good["required_recall"] == 1.0, good
assert good["scopes"]["recall"] == 1.0 and good["state_agreement"] == 1.0

# Triggers written as mappings (the shape agents actually produce) are read by dimension.
mapped = scoring.score_plan(
    plan("IMPLEMENTATION", SMALL_FRONTEND, scopes=["frontend"],
         risk_triggers=[{"dimension": "BEHAVIORAL", "trigger": "changed validation"}, {"dimension": "SECURITY"}]),
    oracle("small-frontend"))
assert mapped["risk_triggers"] == {"shape": "mapping", "missing": [], "extra": ["SECURITY"], "recall": 1.0}, mapped["risk_triggers"]
assert mapped["scopes"]["shape"] == "name" and mapped["scopes"]["recall"] == 1.0
assert good["risk_triggers"]["shape"] == "name"

# NOT_APPLICABLE and NOT_TRIGGERED are interchangeable for an inactive gate.
swapped = scoring.score_plan(plan("IMPLEMENTATION", {**SMALL_FRONTEND, "security": "NOT_APPLICABLE"}),
                             oracle("small-frontend"))
assert swapped["passed"] and swapped["state_agreement"] == 1.0

# Dropping a required gate is the safety failure.
missed = scoring.score_plan(plan("IMPLEMENTATION", {**SMALL_FRONTEND, "qa": "NOT_TRIGGERED"}), oracle("small-frontend"))
assert not missed["passed"] and missed["missed_required"] == ["qa"] and missed["required_recall"] == 0.8

# Size must not suppress Security.
tiny = {a: "REQUIRED" for a in ("validator", "backend-code-review", "qa", "detail-analyst", "reviewer")}
no_security = scoring.score_plan(plan("IMPLEMENTATION", tiny), oracle("tiny-multitenant-auth"))
assert no_security["missed_required"] == ["security"]
# ...and a CONDITIONAL oracle entry accepts any state.
with_security = {**tiny, "security": "REQUIRED"}
for state in ("REQUIRED", "CONDITIONAL", "NOT_TRIGGERED"):
    scored = scoring.score_plan(plan("IMPLEMENTATION", {**with_security, "backend-architecture-review": state}),
                                oracle("tiny-multitenant-auth"))
    assert scored["passed"], state

# Activating a gate the oracle keeps off is over-routing.
over = scoring.score_plan(plan("IMPLEMENTATION", {**SMALL_FRONTEND, "performance": "REQUIRED"}), oracle("small-frontend"))
assert not over["passed"] and over["unnecessary"] == ["performance"] and over["required_recall"] == 1.0

# Wrong work mode fails even with the right gates.
wrong_mode = scoring.score_plan(plan("REVIEW_ONLY", SMALL_FRONTEND), oracle("small-frontend"))
assert not wrong_mode["passed"] and not wrong_mode["work_mode"]["match"]

# A plan in another shape (as seen in real runs) is unscorable, not silently passed.
freeform = {"work_mode": "IMPLEMENTATION", "required_gates": ["validator", "qa"], "optional_gates": ["detail-analyst"]}
unscorable = scoring.score_plan(freeform, oracle("small-frontend"))
assert not unscorable["scorable"] and not unscorable["passed"] and not unscorable["schema_valid"]
assert "missing key: agents" in unscorable["schema_problems"]

# Schema problems are reported without blocking scoring.
partial = plan("IMPLEMENTATION", SMALL_FRONTEND)
del partial["notes"]
partial["agents"] = [e for e in partial["agents"] if e["agent"] != "infrastructure"]
partial["agents"][0]["reason"] = ""
scored = scoring.score_plan(partial, oracle("small-frontend"))
assert scored["passed"] and not scored["schema_valid"]
assert {"missing key: notes", "agent 'infrastructure' is not classified", "agent 'validator' has no reason"} <= set(scored["schema_problems"])
assert scored["agents"]["infrastructure"]["actual"] == scoring.OMITTED
for junk in (None, [], "text"):
    assert scoring.validate_plan(junk) == ["plan is not a YAML mapping"]

# Consistency counts distinct routing decisions across trials.
same = scoring.consistency([good, swapped])
assert same == {"trials": 2, "distinct_decisions": 1, "agreement": 1.0}, same
mixed = scoring.consistency([good, over, good, unscorable])
assert mixed["distinct_decisions"] == 3 and mixed["agreement"] == 0.5, mixed

# Review runs: a planted defect must be named by a gate that demands changes.
DEFECT = {"evidence": ["tenant", "listByTenant", "leak|drops?"]}
REQUIRED = ["validator", "backend-code-review", "qa"]
ran = lambda **decisions: {a: {"decision": decisions.get(a.replace("-", "_"), "PASS"), "current": True} for a in REQUIRED}
leak = "listByTenant drops the tenant predicate when a severity is given."
fine = "listByTenant keeps the tenant predicate; nothing to change."

found = scoring.score_review(DEFECT, REQUIRED, ran(backend_code_review="CHANGES_REQUIRED"),
                             {"backend-code-review": leak, "qa": fine}, "PRE_PR_BLOCKED")
assert found["passed"] and found["found_by"] == ["backend-code-review"], found

missed = scoring.score_review(DEFECT, REQUIRED, ran(), {"backend-code-review": fine}, "PRE_PR_PASS")
assert not missed["passed"] and missed["failure"] == "defect not found", missed

# Naming the defect while passing the gate does not count.
waved = scoring.score_review(DEFECT, REQUIRED, ran(), {"backend-code-review": leak}, "PRE_PR_PASS")
assert not waved["passed"] and waved["mentioned_by"] == ["backend-code-review"] and waved["found_by"] == [], waved

# A gate rejecting for another reason is not a detection.
other = scoring.score_review(DEFECT, REQUIRED, ran(qa="CHANGES_REQUIRED"), {"qa": "No controller test."}, "PRE_PR_BLOCKED")
assert not other["passed"] and other["rejecting"] == ["qa"], other

# A stale or missing result means the gate did not run for this change.
partial_run = ran(backend_code_review="CHANGES_REQUIRED")
partial_run["qa"]["current"] = False
# That is expected when a gate rejected (the flow stops there), and a failure otherwise.
skipped = scoring.score_review(DEFECT, REQUIRED, partial_run, {"backend-code-review": leak}, "PRE_PR_BLOCKED")
assert skipped["passed"] and skipped["gates_not_run"] == ["qa"] and skipped["recorded"] == 2, skipped
unfinished = ran()
unfinished["qa"]["current"] = False
unfinished = scoring.score_review(None, REQUIRED, unfinished, {}, "PRE_PR_BLOCKED")
assert not unfinished["passed"] and unfinished["failure"] == "gates not run: qa", unfinished

# Control: no defect, so any gate demanding changes is a false alarm.
clean = scoring.score_review(None, REQUIRED, ran(), {}, "PRE_PR_PASS")
assert clean["passed"], clean
alarm = scoring.score_review(None, REQUIRED, ran(qa="BLOCKED"), {}, "PRE_PR_BLOCKED")
assert not alarm["passed"] and alarm["failure"] == "false alarm: qa", alarm
assert not scoring.score_review(None, [], {}, {}, "PRE_PR_BLOCKED")["passed"]

# Trace summary: attribute requests and reads to the agent that made them.
import tempfile
import tracing

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    for name, text in ((".harness/agents/qa/AGENT.md", "one two three\nfour five\n"), ("src/a.ts", "x y\n")):
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(text)
    usage = lambda prompt, out: {"input_tokens": 1, "cache_read_input_tokens": prompt - 1, "output_tokens": out}
    say = lambda mid, parent, use, content: {"type": "assistant", "parent_tool_use_id": parent,
                                              "message": {"id": mid, "usage": use, "content": content}}
    read = lambda path, **more: {"type": "tool_use", "id": "r", "name": "Read", "input": {"file_path": path, **more}}
    events = [
        say("m1", None, usage(100, 5), [{"type": "tool_use", "id": "launch", "name": "Agent", "input": {"subagent_type": "qa"}}]),
        say("m2", "launch", usage(300, 7), [read(str(root / ".harness/agents/qa/AGENT.md"))]),
        # The same message repeated for a second content block must not be counted twice.
        say("m2", "launch", usage(300, 7), [read("src/a.ts")]),
        say("m3", "launch", usage(500, 9), [read(".harness/agents/qa/AGENT.md", offset=2, limit=1)]),
        say("m4", None, usage(150, 2), [{"type": "text", "text": "done"}]),
        {"type": "result", "total_cost_usd": 1.0},
    ]
    traced = tracing.summarise(events, root)
    qa, lead = traced["agents"]["qa"], traced["agents"]["lead"]
    assert (qa["launches"], qa["requests"], qa["context_peak"], qa["prompt_tokens"]) == (1, 2, 500, 800), qa
    assert qa["words_read"] == {"agent-contract": 7, "project": 2} and qa["reads"] == 3, qa
    assert (lead["requests"], lead["prompt_tokens"], lead["tool_calls"]) == (2, 250, {"Agent": 1}), lead
    assert list(traced["files"]) == [".harness/agents/qa/AGENT.md", "src/a.ts"], traced["files"]
    assert traced["files"][".harness/agents/qa/AGENT.md"] == {"category": "agent-contract", "reads": 2, "words": 7, "agents": ["qa"]}
    assert tracing.category(".agents/skills/x/SKILL.md") == "skill" and tracing.category(".harness/runtime/claude/a.md") == "run-state"

print("EVAL SCORING TESTS: PASS")
