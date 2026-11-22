# Frontend Code Review Report

## Gate Decision

- Decision: APPROVE / APPROVE_WITH_NON_BLOCKING_COMMENTS / APPROVE_WITH_CONDITIONS / REQUEST_CHANGES / BLOCKED_PENDING_DECISION / BLOCKED_PENDING_EVIDENCE
- Review version:
- Reviewer:
- Date:
- Target change / PR:
- Frontend scope:
- Architecture profile:
- Re-review required: yes/no

## Authoritative Basis

- Applicable `AGENTS.md`:
- Accepted requirement / OpenSpec / story:
- Frontend engineering standard:
- Project policies / accepted deviations:
- Relevant API/contracts:
- Known unresolved behavior/design decisions:

## Review Scope

### Changed
-

### Directly Affected
-

### Necessary Context
-

### Explicitly Excluded
-

## Validation / Test Evidence

| Evidence | Status | Source | Notes |
|---|---|---|---|
| Format/lint | PASSED / FAILED / BLOCKED / UNAVAILABLE / NOT_APPLICABLE / INCONCLUSIVE | | |
| Type checks | | | |
| Build | | | |
| Frontend architecture validation | | | |
| Component tests | | | |
| Hook tests | | | |
| Adapter tests | | | |
| Visual tests | | | |
| E2E/user journey | | | |
| Browser/runtime evidence | | | |

## User Behavior Map

```text
user action
→ UI state
→ hook/application command
→ adapter/server-state interaction
→ result/error
→ rendered/accessibility outcome
```

- Primary action:
- Loading behavior:
- Success behavior:
- Empty behavior:
- Error/retry behavior:
- Disabled/submitting behavior:
- Navigation/focus behavior:
- External side effect:

## React / Async Review

### State
- Sources of truth:
- Derived state:
- Reset/persistence:
- Cross-route/user leakage:

### Effects
- Synchronization purpose:
- Dependency correctness:
- Cleanup:
- Duplicate work:

### Async / Server State
- Cancellation:
- Stale response protection:
- Mutation duplication:
- Optimistic update/rollback:
- Retry/reset:
- Invalidations/refetch:

## Forms / Accessibility

- Labels/names:
- Keyboard:
- Focus:
- Error association:
- Status announcements:
- Disabled/read-only:
- Critical accessible path:

## Contract / Adapter Review

- Request mapping:
- Response mapping:
- Runtime validation:
- Error semantics:
- Date/enum/null mapping:
- Cancellation:
- Raw transport leakage:

## Security / Privacy / Performance

### Security
-

### Privacy / Analytics
-

### Performance
-

## Findings

### FCR-001 — [Title]

- Severity: CRITICAL / HIGH / MEDIUM / LOW
- Confidence: HIGH / MEDIUM / LOW
- Category: CORRECTNESS / RENDERING / STATE / EFFECT / ASYNC_RACE / SERVER_STATE / FORM / ACCESSIBILITY / CONTRACT_ADAPTER / SECURITY / PRIVACY / PERFORMANCE / VISUAL_BEHAVIOR / TEST_EVIDENCE / ERROR_RECOVERY / COMPATIBILITY
- Accepted behavior / rule:
- Location:
- Trigger / scenario:
- Evidence:
- Observed behavior:
- Impact:
- Existing test/guard inspected:
- Why insufficient:
- Smallest remediation direction:
- Verification:
- Blocking: yes/no
- Handoff / owner:

## Architecture Questions Routed

| ID | Structural concern | Why not a code-review finding | Route |
|---|---|---|---|
| | | | Frontend Architecture Review |

## Verified Strengths

Only material verified strengths.

-

## Questions / Missing Decisions

| ID | Question | Why needed | Blocking? | Route |
|---|---|---|---|---|
| | | | | Product / Design / Architecture |

## Residual Risk

- Browser/device evidence unavailable:
- Untested states:
- External contract uncertainty:
- Pre-existing risk activated:
- Deferred non-blocking risk:

## Handoffs

| Finding / need | Recipient | Expected output | Blocking | Re-entry condition |
|---|---|---|---|---|
| | Implementation / Validator / Frontend Architecture Review / QA / Accessibility / Security / Performance / Detail Analyst / Reviewer | | yes/no | |

## Review Summary

- Critical findings:
- High findings:
- Medium findings:
- Low findings:
- Blocking decisions:
- Blocking evidence gaps:
- Non-blocking comments:
- Why final decision is justified:

## Exact Next Action

-
