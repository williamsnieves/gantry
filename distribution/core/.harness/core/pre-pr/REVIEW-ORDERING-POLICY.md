# Review Ordering Policy

## Goal

Minimize wasted expensive review while preserving independent specialist discovery.

## Canonical Macro Order

```text
1. Route
2. Stabilize implementation
3. Validator
4. Specialist fan-out
5. Remediation / targeted re-review loop
6. Detail Analyst
7. Reviewer
8. Final Pre-PR Gate
```

## Why Validator First

Validator catches cheap mechanical failures:

```text
syntax
format
lint
type
build
test execution
```

before expensive multi-agent reasoning.

Default:

```text
Validator PASS
→ broad specialist fan-out
```

## Soft Exception

Selected read-only specialists may start despite a narrow Validator failure if:

```text
their evidence remains meaningful
and
orchestrator records the limitation
```

Example:

```text
visual snapshot update missing
```

may not prevent backend Security review.

This is an optimization, not a license to ignore broken builds.

## Specialist Internal Order

No universal linear order exists.

Use dependencies.

### Usually Parallel

```text
Backend Code Review
Frontend Code Review
relevant Architecture Reviews
QA
Security
Performance
Infrastructure
```

when inputs are ready.

### Decision Before Remediation

If a gate is:

```text
BLOCKED_PENDING_DECISION
```

and the decision determines architecture/implementation:

```text
resolve decision first
```

Do not implement speculative fixes.

### Architecture Before Structural Refactor

If architecture gate proves the architecture choice must change:

```text
architecture remediation
→ implementation
→ code review
```

Do not polish code around a rejected architecture.

### Product Decision Before QA Expectation

If QA cannot define expected retry/error behavior:

```text
product/architecture decision
→ implementation/test update
→ QA
```

### Security Architecture Before Security Fix

If root cause is trust/authorization ownership:

```text
architecture/security decision
→ implementation
→ Security verification
```

when required.

### Performance Evidence Before Infrastructure Sizing

```text
Performance evidence
→ Infrastructure sizing/autoscaling config
```

not the reverse.

## Detail Analyst Timing

Run after specialist convergence because it needs a near-final cross-artifact state.

It should not be the first review gate.

It may run earlier for exploratory completeness, but final Detail Analyst readiness must reflect the latest change identity.

## Reviewer Timing

Reviewer is a fan-in integrator.

It runs after every required specialist gate is terminal.

## Final Pre-PR Timing

Final gate runs after Reviewer.

No specialist should normally be launched for the first time after final pre-PR begins.

If final gate detects an unhandled trigger/missing gate:

```text
PRE_PR_BLOCKED
→ return to routing
```

## Remediation Ordering

Within a blocker cluster, prefer:

```text
1. unresolved authoritative decision
2. architecture/root cause
3. implementation
4. regression tests/evidence
5. specialist verification
6. Validator
7. Detail Analyst if cross-artifact state changed
8. Reviewer
```

This prevents repeated rework.

## No Global Agent Sequence by Name

Avoid:

```text
Security always after QA
Performance always after Security
Infrastructure always last
```

unless a concrete dependency requires it.

The harness is a DAG, not a fixed checklist.
