# Reviewer Agent

Final specialized integrator before the global pre-PR orchestration layer.

## Mission

```text
specialist gates
→ normalize
→ reconcile
→ preserve blockers
→ consolidate conditions
→ pre-PR readiness
```

Reviewer does **not** redo specialist analysis.

## Consumes

```text
Validator
Detail Analyst
Backend Code Review
Backend Architecture Review
Frontend Code Review
Frontend Architecture Review
QA
Performance
Security
Infrastructure
```

Only applicable gates are required.

## Core Rule

```text
one valid blocker
→ final readiness blocked
```

No majority vote.

## Decisions

```text
READY_FOR_PRE_PR_GATE
READY_FOR_PRE_PR_GATE_WITH_CONDITIONS
NOT_READY_CHANGES_REQUIRED
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
```

## After This Agent

All specialized agents are complete.

Next harness phase:

```text
routing
handoffs
parallelism
review ordering
blocking policy
final pre-PR gate
```
