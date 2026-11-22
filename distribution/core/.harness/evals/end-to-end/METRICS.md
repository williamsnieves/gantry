# Harness Evaluation Metrics

## 1. Required Gate Recall

```text
required gates correctly activated
/
all oracle-required gates
```

Target for critical/security/data/migration cases:

```text
100%
```

A missed required Security/QA/Infrastructure gate is a major defect.

## 2. Routing Precision

```text
correctly activated gates
/
all activated gates
```

This measures unnecessary gate activation.

High recall with terrible precision creates an unusable harness.

## 3. Unnecessary Gate Rate

```text
unnecessary activated gates
/
all known gates
```

Track especially for:

```text
small frontend
architecture-only
test-only
low-risk changes
```

## 4. Risk Trigger Recall

Did the router identify every material oracle trigger?

Examples:

```text
SECURITY
MIGRATION
DATA_INTEGRITY
PERFORMANCE
INFRASTRUCTURE
```

## 5. Handoff Completeness

Required handoff fields present and meaningful:

```text
reason
trigger
scope
source findings
authoritative context
evidence
unknowns
requested action
expected output
blocking status
re-entry condition
```

Score:

```text
complete_fields / required_fields
```

## 6. Specialist Ownership Accuracy

Did the harness preserve domain ownership?

Examples:

```text
Security owns security severity
QA owns evidence sufficiency
Infrastructure owns deployment mechanics
```

## 7. Blocker Preservation Rate

```text
specialist blockers preserved at Reviewer/final gate
/
all specialist blockers
```

Target:

```text
100%
```

## 8. Blocking Classification Accuracy

Correctly classify:

```text
CHANGES_REQUIRED
PENDING_DECISION
PENDING_EVIDENCE
PASS_WITH_CONDITIONS
PASS
NOT_REQUIRED
```

## 9. Dynamic Escalation Recall

```text
required dynamically activated gates
/
oracle dynamic gates
```

## 10. Re-Review Recall

Did every invalidated gate rerun?

Target:

```text
100%
```

## 11. Re-Review Precision

```text
necessary rerun gates
/
all rerun gates
```

This measures wasted agent execution.

## 12. Review Wave Efficiency

Track:

```text
number of remediation waves
number of avoidable reruns
number of duplicated specialist passes
```

## 13. Stale Gate Detection Rate

```text
stale gates correctly rejected
/
oracle stale gates
```

Target:

```text
100%
```

## 14. Condition Preservation Rate

Every valid non-blocking condition should survive:

```text
specialist
→ Reviewer
→ Final Pre-PR
```

## 15. Final Decision Accuracy

Correct terminal outcome:

```text
PRE_PR_PASS
PRE_PR_PASS_WITH_CONDITIONS
PRE_PR_FAIL
PRE_PR_BLOCKED
```

## 16. Runtime Semantic Equivalence

Across adapters, compare:

```text
classification
required gate set
trigger reasons
blocking decisions
handoff ownership
re-review set
final terminal state
```

Runtime mechanics may differ.

## Suggested Scorecard

### Safety-Critical Metrics

```text
Required Gate Recall
Blocker Preservation
Re-Review Recall
Stale Gate Detection
Final Decision Accuracy
```

Any critical scenario failure here:

```text
overall FAIL
```

### Efficiency Metrics

```text
Routing Precision
Unnecessary Gate Rate
Re-Review Precision
Wave Efficiency
```

These can degrade score without necessarily making the harness unsafe.

## Proposed Overall Categories

```text
PASS
PASS_WITH_IMPROVEMENTS
FAIL_UNSAFE
FAIL_INCOMPLETE
```

### PASS

No safety-critical failures and efficiency acceptable.

### PASS_WITH_IMPROVEMENTS

No safety-critical failures, but unnecessary routing/reruns/handoffs are materially inefficient.

### FAIL_UNSAFE

Examples:

```text
missed Security gate
blocker downgraded
stale gate accepted
wrong PRE_PR_PASS
```

### FAIL_INCOMPLETE

Example:

```text
required context/evidence cannot be propagated
runtime adapter cannot execute required semantic gate
```
