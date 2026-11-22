# Blocking Policy

## Purpose

Define when the execution loop:

```text
continues
waits
returns to remediation
or terminates
```

## Normalized Blocking Classes

```text
PASS
PASS_WITH_CONDITIONS
CHANGES_REQUIRED
PENDING_DECISION
PENDING_EVIDENCE
NOT_REQUIRED
```

Specialist vocabularies remain unchanged; orchestration may map them to these execution classes.

## Hard Block — Changes Required

When a specialist has a proven blocking defect:

```text
CHANGES_REQUIRED
```

the run cannot reach Reviewer-ready state until remediated.

Examples:

```text
REQUEST_CHANGES
ARCHITECTURE_CHANGES_REQUIRED
CHANGES_REQUESTED
QA_CHANGES_REQUIRED
PERFORMANCE_CHANGES_REQUIRED
SECURITY_CHANGES_REQUIRED
INFRASTRUCTURE_CHANGES_REQUIRED
Validator FAIL
Detail Analyst NOT READY
```

## Hard Block — Pending Decision

When safe remediation depends on an authoritative unresolved decision:

```text
PENDING_DECISION
```

do not let implementation invent the answer.

Possible independent reviews may continue if they do not depend on the decision.

The affected branch waits.

## Hard Block — Pending Evidence

When a gate cannot conclude without required evidence:

```text
PENDING_EVIDENCE
```

route the exact evidence request.

Independent reviews may continue.

Reviewer cannot complete while a REQUIRED gate remains pending evidence.

## Conditions

`PASS_WITH_CONDITIONS` may continue only when the owning specialist explicitly states the condition is non-blocking for the current transition.

Condition must include:

```text
owner
verification
deadline/gate when applicable
residual risk
```

## Advisories

Advisories never block unless later converted by an authoritative gate.

## Early Stop Policy

### Stop Whole Run Early

Only when continuing produces little useful independent evidence.

Examples:

```text
repository does not build at all
accepted behavior is absent for the entire change
change identity cannot be established
critical architecture decision invalidates all implementation
```

### Continue Independent Branches

If blocker is local:

```text
frontend browser test unavailable
```

backend Code Review/Security may continue.

This preserves parallel efficiency.

## Critical Security Finding

A critical/high Security blocker does not require aborting read-only independent reviews.

It does require:

```text
no readiness progression
```

until remediated.

## Validator Failure

Default:

```text
FAIL
→ stop broad review fan-out
```

Exception:

```text
independent read-only review still meaningful
```

must be explicitly recorded.

## Multiple Blockers

Collect independent blockers when useful.

Do not stop after first finding if other parallel agents are already running and can provide useful remediation information.

This reduces remediation cycles.

## Blocker Precedence at Integration

For Reviewer/final integration:

```text
CHANGES_REQUIRED
> PENDING_DECISION
> PENDING_EVIDENCE
> PASS_WITH_CONDITIONS
> PASS / NOT_REQUIRED
```

If a proven changes-required blocker exists alongside pending evidence:

```text
final integration remains changes required
```

because a concrete defect is already known.

## Waivers / Risk Acceptance

Only explicit authorized governance may disposition a blocker where policy permits.

A waiver never changes factual specialist status.

Example:

```text
CONTROL_FAIL
```

remains `CONTROL_FAIL`.

## Dynamic Trigger Is Blocking Until Classified

If a required new trigger is discovered:

```text
UNHANDLED_DYNAMIC_TRIGGER
```

Reviewer/final gate cannot pass until router classifies and resolves it.

## Terminal Failure

The pre-PR run terminates unsuccessful when:

```text
user/owner chooses not to remediate
required authoritative decision cannot be obtained
required evidence cannot be obtained
or
policy explicitly rejects the residual risk
```

Represent final state as:

```text
PRE_PR_FAIL
or
PRE_PR_BLOCKED
```

depending on whether the problem is a proven defect or unresolved prerequisite.
