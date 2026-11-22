# Fixture — One Security Blocker

Same commit reviewed by all gates.

Results:

```text
Validator: PASS
Backend Code Review: APPROVE
Backend Architecture Review: ARCHITECTURE_APPROVED
QA: QA_APPROVED
Performance: PERFORMANCE_APPROVED
Security: SECURITY_CHANGES_REQUIRED
Infrastructure: INFRASTRUCTURE_APPROVED
Detail Analyst: READY
```

Security finding:

```text
SEC-003
cross-tenant update path lacks authoritative resource authorization
HIGH
blocking
```

Expected Reviewer:

- no majority vote;
- preserve Security blocker;
- final `NOT_READY_CHANGES_REQUIRED`;
- remediation likely invalidates Backend Code Review, Security, QA and Validator on affected path;
- do not rerun unrelated Performance/Infrastructure unless fix touches them.
