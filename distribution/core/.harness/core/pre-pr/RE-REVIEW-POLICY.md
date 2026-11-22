# Re-Review Policy

## Principle

A remediation invalidates only the gates whose evidence/claims are materially affected.

Goal:

```text
minimum safe re-review set
```

not:

```text
rerun everything
```

## Inputs

For each remediation record:

```text
source findings
changed files/surfaces
changed contracts
changed architecture
changed tests
changed config/IaC
changed security controls
changed deployment/migration behavior
```

## Invalidation Classes

```text
DIRECTLY_INVALIDATED
POTENTIALLY_INVALIDATED
UNAFFECTED
```

## Common Patterns

### Backend Bug Fix

```text
Backend Code Review
Validator
QA for affected behavior
```

Add Security if security root cause/path changed.

Add Backend Architecture Review if boundary/ownership changed.

### Frontend Bug Fix

```text
Frontend Code Review
Validator
QA
```

Add Frontend Architecture Review if state/composition/profile changed.

### Test-Only Fix

```text
QA
Validator
Reviewer
```

Code Review may remain fresh if production code unchanged.

### Architecture Refactor

```text
relevant Architecture Review
relevant Code Review
QA
Validator
```

plus domain specialists triggered by architecture change.

### Security Fix

Usually:

```text
relevant Code Review
Security
QA for regression/control behavior
Validator
```

Add Architecture Review if trust/ownership architecture changed.

### Performance Fix

Usually:

```text
relevant Code Review
Performance
Validator
QA if user behavior changed
```

Add Infrastructure if resource/runtime config changed.

### Infrastructure Fix

```text
Infrastructure
Validator
```

Add Security when:

```text
IAM
network
secret
CI trust
```

changed.

Add Performance when sizing/capacity behavior changed.

### Migration Fix

Usually:

```text
Backend Architecture Review
Backend Code Review
QA
Infrastructure
Validator
```

plus Security/Performance if relevant.

## Detail Analyst Re-Review

Re-run when remediation changes cross-artifact propagation:

```text
spec
docs
config
flags
runbooks
migration plan
```

If fix is purely local and previous completeness remains valid, it may stay fresh.

## Reviewer Always Re-Runs

Every remediation loop that changes a gate result returns through Reviewer before final pre-PR.

## Final Gate Always Re-Runs

Any post-Reviewer change invalidates final pre-PR.

## Freshness Record

Every gate result should carry:

```text
change_identity
evidence_identity
reviewed_scope
```

The orchestrator records invalidation reason.

## No Blind Reuse

A previous PASS can be reused only when:

```text
reviewed scope unchanged
+
evidence still valid
+
change identity relation is understood
```

## No Blind Rerun

Do not consume cost/time rerunning unrelated specialists.

## Re-Entry Envelope

Each remediation cluster should define:

```text
root_cause_id
source_findings
implementation_owner
required_change
invalidated_gates
validator_checks_to_rerun
expected_terminal_results
reviewer_reentry
```
