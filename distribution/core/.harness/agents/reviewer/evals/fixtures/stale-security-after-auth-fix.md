# Fixture — Stale Security After Authorization Fix

Original commit A:

```text
Security: SECURITY_CHANGES_REQUIRED
SEC-001 missing authorization
```

Commit B changes authorization code and adds negative tests.

Reports:

- Backend Code Review is rerun on B and APPROVE.
- QA is rerun on B and QA_APPROVED.
- Validator PASS on B.
- Security report is still from A.
- Performance and Infrastructure are fresh and unaffected.

Expected:

- Security report is stale because root cause changed;
- require focused Security re-review/control verification;
- do not rerun unrelated Performance/Infrastructure;
- final `BLOCKED_PENDING_EVIDENCE`.
