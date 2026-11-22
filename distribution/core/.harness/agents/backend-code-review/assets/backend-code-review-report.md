# Backend Code Review Report

## Gate Decision

- Decision: APPROVE / APPROVE_WITH_NON_BLOCKING_COMMENTS / APPROVE_WITH_CONDITIONS / REQUEST_CHANGES / BLOCKED_PENDING_DECISION / BLOCKED_PENDING_EVIDENCE
- Review version:
- Reviewer:
- Date:
- Target change / PR:
- Backend scope:
- Re-review required: yes/no

## Authoritative Basis

- Applicable `AGENTS.md`:
- Accepted requirement / OpenSpec:
- Backend engineering standard:
- Decision register / accepted exceptions:
- Relevant ADR / architecture validation:
- Known unresolved decisions:

## Review Scope

### Changed
-

### Directly Affected
-

### Necessary Context
-

### Explicitly Excluded
-

## Validation Evidence

| Evidence | Status | Source / command | Notes |
|---|---|---|---|
| Formatter | PASSED / FAILED / BLOCKED / UNAVAILABLE / NOT_APPLICABLE / INCONCLUSIVE | | |
| Lint | | | |
| Type/static checks | | | |
| Tests | | | |
| Build | | | |
| Architecture checks | | | |
| Migrations/schema checks | | | |
| Other repository gates | | | |

## Change Behavior Map

```text
input
→ validation
→ domain conversion
→ application decision
→ side effects
→ persistence
→ output
```

- Primary behavior:
- State changes:
- External side effects:
- Persistence effects:
- Public/API/event contracts:
- Security/tenant boundary:

## Findings

### BCR-001 — [Title]

- Severity: CRITICAL / HIGH / MEDIUM / LOW
- Confidence: HIGH / MEDIUM / LOW
- Category: correctness / domain / application / persistence / external-adapter / http / composition / security / data-integrity / idempotency / migration-compatibility / testing / operations
- Violated contract / rule:
- Location:
- Trigger / failure scenario:
- Evidence:
- Impact:
- Existing control/test inspected:
- Why insufficient:
- Smallest remediation direction:
- Verification:
- Blocking: yes/no
- Handoff / owner:

## Verified Strengths

Only record material verified strengths that reduce uncertainty.

-

## Questions / Missing Decisions

| ID | Question / decision | Why needed | Blocking? | Route |
|---|---|---|---|---|
| | | | | |

## Residual Risk

- Untested/unavailable paths:
- Pre-existing risks activated by the change:
- Environment limitations:
- Deferred non-blocking risks:

## Handoffs

| Finding / need | Recipient | Expected output | Blocking | Re-entry condition |
|---|---|---|---|---|
| | Implementation / Validator / Backend Architecture Review / QA / Security / Performance / Detail Analyst | | yes/no | |

## Review Summary

- Critical findings:
- High findings:
- Medium findings:
- Low findings:
- Blocking unresolved decisions:
- Blocking evidence gaps:
- Non-blocking comments:
- Why final decision is justified:

## Exact Next Action

-
