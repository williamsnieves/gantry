"""Score a routing plan written by an agent against a scenario oracle.

Pure functions, no I/O beyond reading the oracle file, so they can be unit
tested without an agent runtime.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path

import yaml

AGENTS = (
    "validator",
    "detail-analyst",
    "backend-code-review",
    "backend-architecture-review",
    "frontend-code-review",
    "frontend-architecture-review",
    "qa",
    "performance",
    "security",
    "infrastructure",
    "reviewer",
)
APPLICABILITY = ("REQUIRED", "CONDITIONAL", "NOT_APPLICABLE", "NOT_TRIGGERED", "ALREADY_SATISFIED", "BLOCKED")
WORK_MODES = (
    "DISCOVERY",
    "ARCHITECTURE_ONLY",
    "IMPLEMENTATION",
    "REVIEW_ONLY",
    "REMEDIATION",
    "MIGRATION",
    "RELEASE_ONLY",
)
INACTIVE = ("NOT_APPLICABLE", "NOT_TRIGGERED")
OMITTED = "OMITTED"
# Top-level keys of core/routing/templates/routing-plan.template.yaml.
TEMPLATE_KEYS = (
    "routing_plan_version",
    "harness_contract_version",
    "change_identity",
    "work_mode",
    "scopes",
    "risk_triggers",
    "accepted_behavior_sources",
    "existing_gate_results",
    "agents",
    "new_dynamic_triggers",
    "deferred_questions",
    "notes",
)


def load_oracle(scenario_file: Path) -> dict:
    """Normalise a scenario file into {work_mode, scopes, risk_triggers, routing}."""
    data = yaml.safe_load(scenario_file.read_text(encoding="utf-8"))
    oracle = data.get("oracle") or {}
    routing = dict(oracle.get("routing") or {})
    if not routing:
        # architecture-only style: agents listed directly under `oracle`.
        routing = {k: v for k, v in oracle.items() if k in AGENTS}
        if oracle.get("implementation_agents"):
            for agent in ("backend-code-review", "frontend-code-review"):
                routing.setdefault(agent, oracle["implementation_agents"])
    unknown = [a for a in routing if a not in AGENTS] + [v for v in routing.values() if v not in APPLICABILITY]
    if unknown:
        raise ValueError(f"{scenario_file.name}: oracle has unknown agents or states: {unknown}")
    inputs = data.get("input") or {}
    return {
        "id": data["id"],
        "work_mode": inputs.get("work_mode"),
        "scopes": list(inputs.get("scopes") or []),
        "risk_triggers": list(inputs.get("risk_triggers") or []),
        "routing": routing,
    }


def validate_plan(plan: object) -> list[str]:
    """Return the ways a plan departs from the routing-plan template."""
    if not isinstance(plan, dict):
        return ["plan is not a YAML mapping"]
    problems = [f"missing key: {key}" for key in TEMPLATE_KEYS if key not in plan]
    if "work_mode" in plan and plan["work_mode"] not in WORK_MODES:
        problems.append(f"work_mode {plan['work_mode']!r} is not a known work mode")
    for key in ("scopes", "risk_triggers"):
        if key in plan and not isinstance(plan[key], list):
            problems.append(f"{key} is not a list")
    agents = plan.get("agents")
    if "agents" in plan and not isinstance(agents, list):
        problems.append("agents is not a list")
    elif isinstance(agents, list):
        seen: set[str] = set()
        for index, entry in enumerate(agents):
            if not isinstance(entry, dict) or "agent" not in entry:
                problems.append(f"agents[{index}] has no agent name")
                continue
            name = entry["agent"]
            if name not in AGENTS:
                problems.append(f"agents[{index}] names unknown agent {name!r}")
            if name in seen:
                problems.append(f"agent {name!r} is listed more than once")
            seen.add(name)
            if entry.get("applicability") not in APPLICABILITY:
                problems.append(f"agent {name!r} has invalid applicability {entry.get('applicability')!r}")
            if not str(entry.get("reason") or "").strip():
                problems.append(f"agent {name!r} has no reason")
        for name in AGENTS:
            if name not in seen:
                problems.append(f"agent {name!r} is not classified")
    return problems


def plan_routing(plan: object) -> dict[str, str] | None:
    """Extract {agent: applicability} from a plan, or None if it cannot be read."""
    if not isinstance(plan, dict) or not isinstance(plan.get("agents"), list):
        return None
    routing: dict[str, str] = {}
    for entry in plan["agents"]:
        if isinstance(entry, dict) and entry.get("agent") in AGENTS and entry.get("applicability") in APPLICABILITY:
            routing.setdefault(entry["agent"], entry["applicability"])
    return routing or None


LABEL_KEYS = ("dimension", "id", "name", "type", "scope")


def _label(item: object) -> str:
    """Name of a scope or trigger entry.

    The template does not say what an entry looks like, and agents write either
    a bare name or a mapping such as {dimension: SECURITY, trigger: ...}.
    """
    if isinstance(item, dict):
        for key in LABEL_KEYS:
            if key in item:
                return str(item[key]).strip().upper()
        return "UNLABELLED"
    return str(item).strip().upper()


def _shape(actual: object) -> str:
    if not isinstance(actual, list) or not actual:
        return "empty"
    kinds = {"mapping" if isinstance(item, dict) else "name" for item in actual}
    return kinds.pop() if len(kinds) == 1 else "mixed"


def _set_score(expected: list[str], actual: object) -> dict:
    actual_set = {_label(item) for item in actual} if isinstance(actual, list) else set()
    expected_set = {item.upper() for item in expected}
    return {
        "shape": _shape(actual),
        "missing": sorted(expected_set - actual_set),
        "extra": sorted(actual_set - expected_set),
        "recall": round(len(expected_set & actual_set) / len(expected_set), 3) if expected_set else 1.0,
    }


def score_plan(plan: object, oracle: dict) -> dict:
    """Compare a plan with an oracle.

    Verdict rules:
    - an agent the oracle marks REQUIRED must be REQUIRED (a miss is the safety failure);
    - an agent the oracle marks NOT_TRIGGERED / NOT_APPLICABLE must not be REQUIRED;
    - an agent the oracle marks CONDITIONAL accepts any state;
    - the work mode must match.
    """
    schema_problems = validate_plan(plan)
    routing = plan_routing(plan)
    result: dict = {
        "schema_valid": not schema_problems,
        "schema_problems": schema_problems,
        "scorable": routing is not None,
    }
    if routing is None:
        result.update(passed=False, failure="plan has no readable agents list")
        return result

    missed, unnecessary, agents, exact = [], [], {}, 0
    for agent, expected in oracle["routing"].items():
        actual = routing.get(agent, OMITTED)
        agents[agent] = {"expected": expected, "actual": actual}
        same_class = actual == expected or (expected in INACTIVE and actual in (*INACTIVE, OMITTED))
        exact += same_class
        if expected == "REQUIRED" and actual != "REQUIRED":
            missed.append(agent)
        elif expected in INACTIVE and actual == "REQUIRED":
            unnecessary.append(agent)
    required = [a for a, state in oracle["routing"].items() if state == "REQUIRED"]
    work_mode_ok = isinstance(plan, dict) and plan.get("work_mode") == oracle["work_mode"]
    failures = []
    if missed:
        failures.append("missed required gate: " + ", ".join(missed))
    if unnecessary:
        failures.append("unnecessary gate: " + ", ".join(unnecessary))
    if not work_mode_ok:
        failures.append(f"work mode {plan.get('work_mode')!r}, expected {oracle['work_mode']!r}")
    result.update(
        passed=not failures,
        failure="; ".join(failures) or None,
        work_mode={"expected": oracle["work_mode"], "actual": plan.get("work_mode"), "match": work_mode_ok},
        scopes=_set_score(oracle["scopes"], plan.get("scopes")),
        risk_triggers=_set_score(oracle["risk_triggers"], plan.get("risk_triggers")),
        agents=agents,
        missed_required=missed,
        unnecessary=unnecessary,
        required_recall=round((len(required) - len(missed)) / len(required), 3) if required else 1.0,
        state_agreement=round(exact / len(oracle["routing"]), 3),
        required_set=sorted(a for a, state in routing.items() if state == "REQUIRED"),
    )
    return result


def consistency(scores: list[dict]) -> dict:
    """How often repeated trials of one scenario reach the same routing decision."""
    signatures = [
        (score["work_mode"]["actual"], tuple(score["required_set"])) if score.get("scorable") else ("UNSCORABLE", ())
        for score in scores
    ]
    most_common = Counter(signatures).most_common(1)[0][1] if signatures else 0
    return {
        "trials": len(signatures),
        "distinct_decisions": len(set(signatures)),
        "agreement": round(most_common / len(signatures), 3) if signatures else None,
    }
