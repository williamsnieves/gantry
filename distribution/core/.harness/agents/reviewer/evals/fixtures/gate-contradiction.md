# Fixture — Gate Contradiction

Same commit identity claimed.

Validator:

```text
browser E2E: NOT RUN
environment unavailable
```

QA:

```text
QA_APPROVED
focus restoration proven by required browser E2E
```

Project policy says real-browser evidence is mandatory for this modal primitive.

Expected:

- detect factual contradiction;
- do not decide which report is true;
- route QA/Validator evidence reconciliation;
- final `BLOCKED_PENDING_EVIDENCE`.
