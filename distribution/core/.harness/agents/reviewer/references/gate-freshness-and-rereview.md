# Gate Freshness and Re-Review

## Principle

A specialist approval is valid only for the implementation/evidence state it reviewed.

## Stale Result

Mark:

```text
STALE_GATE_RESULT
```

when a later change materially affects the reviewed concern.

Examples:

```text
authorization code changes
→ invalidate Code Review + Security + relevant QA

schema/migration changes
→ invalidate Backend Code Review + QA + Infrastructure

frontend state refactor
→ invalidate Frontend Code Review + Frontend Architecture Review + QA

IAM/workflow changes
→ invalidate Infrastructure + Security
```

## Do Not Re-Run Everything

Re-run only invalidated gates.

A doc-only fix does not automatically invalidate Performance.

A test-only addition does not automatically invalidate Architecture Review.

## Evidence Identity

Track when possible:

```text
commit SHA
diff range
test artifact version
deployment environment
schema version
config version
```

If identity cannot be matched and matters to readiness:

```text
BLOCKED_PENDING_EVIDENCE
```

## Re-Entry

Every blocker should state:

```text
fix/decision
→ owner
→ invalidated specialist gates
→ Validator if needed
→ Reviewer
```
