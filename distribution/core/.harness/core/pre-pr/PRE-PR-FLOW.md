# Pre-PR Flow

## Purpose

Define the complete portable execution loop from a routed implementation change to final pre-PR readiness.

## State Machine

```text
ROUTING_READY
    ↓
IMPLEMENTATION_STABLE
    ↓
VALIDATION_READY
    ↓
SPECIALIST_REVIEWS_RUNNING
    ↓
SPECIALIST_REVIEWS_COMPLETE
    ↓
REMEDIATION_REQUIRED ───────────────┐
    ↓                               │
REMEDIATION_IN_PROGRESS             │
    ↓                               │
TARGETED_REVALIDATION               │
    └───────────────────────────────┘
    ↓
DETAIL_ANALYSIS_READY
    ↓
REVIEWER_READY
    ↓
REVIEWER_COMPLETE
    ↓
FINAL_PRE_PR_GATE
    ↓
PRE_PR_PASS / PRE_PR_PASS_WITH_CONDITIONS
```

Blocking states may interrupt transitions:

```text
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
FAILED_REQUIRES_CHANGES
```

## Phase 0 — Routing

Input:

```text
change identity
work mode
scope
risk triggers
accepted behavior
project policy
existing fresh gates
```

Output:

```text
portable routing plan
```

Routing determines:

```text
which agents are REQUIRED
which are CONDITIONAL
which are NOT_TRIGGERED
which are NOT_APPLICABLE
which are ALREADY_SATISFIED
```

Do not proceed with an ambiguous required gate set.

## Phase 1 — Implementation Stable

Before formal review fan-out:

```text
the intended implementation/config/test state must be stable enough
for multiple agents to inspect the same change identity
```

This does not mean perfect.

It means:

```text
no active conflicting implementation edits
change identity can be recorded
reviewers can inspect a coherent state
```

If implementation is still being materially rewritten:

```text
WAIT
```

rather than generating stale reviews immediately.

## Phase 2 — Validator

Validator is the first normal implementation gate when applicable.

Why:

```text
cheap mechanical failures
should be detected before expensive specialist review
```

Validator runs repository-native required checks.

Result:

```text
PASS
CONDITIONAL PASS
FAIL
```

### Validator FAIL

If failure indicates:

```text
build/type/lint/test breakage that makes specialist review unreliable
```

use hard stop.

If failure is:

```text
narrow, well-understood, and specialist review can still produce useful independent evidence
```

the orchestrator may allow selected read-only specialists to continue according to `BLOCKING-POLICY.md`.

Default:

```text
FAIL
→ remediation before full fan-out
```

## Phase 3 — Specialist Review Fan-Out

Run all routed specialists whose prerequisites are satisfied.

Possible:

```text
Backend Code Review
Backend Architecture Review
Frontend Code Review
Frontend Architecture Review
QA
Performance
Security
Infrastructure
```

Use safe parallelism from:

```text
PARALLELISM-POLICY.md
```

Do not wait unnecessarily for one independent specialist before starting another.

## Phase 4 — Dynamic Escalation

During review, an agent may discover a new trigger.

Example:

```text
Frontend Code Review
→ PII sent to analytics
→ Security becomes REQUIRED
```

The orchestrator must:

1. record trigger source;
2. update routing plan;
3. activate newly required gate;
4. pass a typed handoff;
5. include the new gate in final completeness checks.

Never hide dynamic expansion.

## Phase 5 — Fan-In

When the current specialist set completes, collect:

```text
original decisions
findings
conditions
evidence
handoffs
new triggers
re-entry requirements
```

Do not normalize away specialist vocabularies.

## Phase 6 — Determine Remediation Need

If one or more specialists require changes:

```text
REMEDIATION_REQUIRED
```

Create a root-cause-aware remediation plan.

Prefer dependency order:

```text
authoritative decision
→ architecture
→ implementation
→ tests/evidence
→ specialist re-verification
```

Do not fix findings in arbitrary report order.

## Phase 7 — Remediation

Implementation owner applies the required change.

Agents remain reviewers, not implementers, unless a distinct implementation agent/workflow is explicitly active.

Record new change identity.

## Phase 8 — Targeted Revalidation

Use `RE-REVIEW-POLICY.md`.

Re-run only gates invalidated by the remediation.

Examples:

```text
test-only remediation
→ QA + Validator

tenant authorization fix
→ Backend Code Review + Security + QA + Validator

Terraform rollback fix
→ Infrastructure + Validator
  + Security only if IAM/secrets/trust changed
```

Repeat until:

```text
no change-required blockers remain
```

or the run becomes:

```text
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
```

## Phase 9 — Detail Analyst

Run Detail Analyst after implementation and specialist results have converged enough to inspect cross-artifact completeness.

It checks propagation such as:

```text
spec
code
tests
config
docs
flags
migration notes
runbooks
```

A Detail Analyst `NOT READY` returns to targeted remediation.

## Phase 10 — Reviewer

Reviewer consumes all applicable fresh gates.

Reviewer checks:

```text
gate completeness
freshness
contradictions
conditions
waivers
root-cause consolidation
re-entry graph
```

Expected terminal reviewer decisions:

```text
READY_FOR_PRE_PR_GATE
READY_FOR_PRE_PR_GATE_WITH_CONDITIONS
NOT_READY_CHANGES_REQUIRED
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
```

## Phase 11 — Final Pre-PR Gate

The final gate verifies the integrity of the whole run.

It does not redo specialist judgment.

It verifies:

```text
current change identity matches reviewed identity
routing plan is complete
all REQUIRED gates terminal
Reviewer terminal decision allows progression
Validator evidence is current
conditions are valid for PR transition
no unresolved dynamic trigger exists
no stale required report exists
final artifact/report set is complete
```

Terminal states:

```text
PRE_PR_PASS
PRE_PR_PASS_WITH_CONDITIONS
PRE_PR_FAIL
PRE_PR_BLOCKED
```

## PR Creation

PR creation is deliberately outside this gate.

A runtime adapter may later map:

```text
PRE_PR_PASS
→ allow PR creation action
```

The portable core only determines readiness.
