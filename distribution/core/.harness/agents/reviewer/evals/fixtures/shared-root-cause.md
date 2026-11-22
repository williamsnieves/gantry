# Fixture — Shared Root Cause Across Gates

Same commit.

Findings:

```text
BCR-004
repository update omits tenant predicate
REQUEST_CHANGES

SEC-002
cross-tenant mutation possible
SECURITY_CHANGES_REQUIRED

QA-005
no cross-tenant denial regression evidence
QA_CHANGES_REQUIRED
```

Other gates pass.

Expected:

- create one root-cause cluster:
  tenant authorization enforcement incomplete;
- preserve:
  code remediation,
  security verification,
  QA regression evidence;
- after fix require Backend Code Review + Security + QA + Validator + Reviewer;
- final `NOT_READY_CHANGES_REQUIRED`.
