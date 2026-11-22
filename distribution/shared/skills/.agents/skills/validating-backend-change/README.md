# validating-backend-change

Backend-specific completion validation built on the generic `validating-changes` workflow.

It maps changed layers to the correct mechanical, unit, integration, E2E, migration, provider, and architecture checks; traces acceptance criteria to assertions; and distinguishes:

```text
PASSED
FAILED
BLOCKED
SKIPPED
UNAVAILABLE
INCONCLUSIVE
NOT_APPLICABLE
```

The skill produces strict merge/release evidence without performing code review or implementation.
