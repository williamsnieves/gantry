# Gate Dependency Contract

## Purpose

Define only the minimum dependencies needed for valid routing.

This is **not yet** the full review-ordering or parallelism policy.

## Minimum Dependency Rules

### Accepted Behavior Before Behavior Review

Code Review and QA require enough accepted behavior to judge correctness.

If missing:

```text
BLOCKED_PENDING_DECISION
```

### Implementation Before Code Review

Code Review requires reviewable implementation.

### Implementation/Test Evidence Before Validator

Validator requires repository state on which commands can run.

### Architecture Review Requires Architecture-Relevant Change

Do not run architecture review merely because implementation exists.

### Performance Requires Target/Symptom/Evidence Trigger

Performance may request evidence before completing.

### Security Threat Modeling Requires Trust/Architecture Context

STRIDE needs enough:

```text
assets
actors
flows
trust boundaries
```

### Security Control Verification Requires Accepted Control Baseline

Do not invent controls.

### Infrastructure Requires Accepted Deployment Target

Infrastructure cannot safely choose unresolved topology/provider decisions.

### Reviewer Requires Gate Set + Specialist Outputs

Reviewer is an integration gate.

It should not run as the first review step.

## Dependency States

Use:

```text
READY
WAITING_FOR_INPUT
WAITING_FOR_DECISION
WAITING_FOR_EVIDENCE
ALREADY_SATISFIED
NOT_APPLICABLE
```

## Deferred to Later Roadmap

The following are intentionally NOT fully defined here:

```text
which compatible agents execute in parallel
exact global review sequence
blocker precedence across all gates
when execution stops early
final pre-PR command/gate
```

Those are separate upcoming harness artifacts.
