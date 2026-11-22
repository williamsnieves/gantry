# QA Review Report

## Gate Decision

- Decision: QA_APPROVED / QA_APPROVED_WITH_CONDITIONS / QA_CHANGES_REQUIRED / BLOCKED_PENDING_DECISION / BLOCKED_PENDING_EVIDENCE
- Review version:
- Reviewer:
- Date:
- Target change / PR:
- Scope: BACKEND / FRONTEND / FULL_STACK
- Re-QA required: yes/no

## Authoritative Basis

- Applicable `AGENTS.md`:
- Accepted specification / OpenSpec:
- Acceptance criteria:
- Relevant architecture decisions:
- Known unresolved behavior:
- Validator report:
- Code Review reports:
- Architecture Review reports:

## Risk Profile

| Behavior / seam | Risk | Why | Critical failure |
|---|---|---|---|
| | CRITICAL / HIGH / MEDIUM / LOW | | |

## Acceptance Criteria Traceability

| AC | Behavior | Evidence layer | Evidence | Status |
|---|---|---|---|---|
| AC-001 | | Domain / Application / Adapter / Hook / Component / HTTP E2E / Browser E2E / Other | | PROVEN / PARTIALLY_PROVEN / UNPROVEN / NOT_TESTABLE_HERE / NOT_APPLICABLE |

## Test Inventory

| Test / suite | Layer | Behavior proved | Boundary realism | Deterministic? | Duplicative? |
|---|---|---|---|---|---|
| | | | | | |

## Critical Scenario Matrix

| Scenario | Relevant? | Evidence | Status | Gap |
|---|---|---|---|---|
| Essential success | | | | |
| Authorization / tenant denial | | | | |
| Business rejection | | | | |
| Invalid boundary input | | | | |
| Dependency failure | | | | |
| Timeout | | | | |
| Retry | | | | |
| Duplicate | | | | |
| Race / concurrency | | | | |
| Partial failure | | | | |
| Recovery | | | | |
| Rollback / compensation | | | | |
| Empty / not-found | | | | |
| Migration / compatibility | | | | |

## Test Quality Assessment

### Observable Contracts
- Strong evidence:
- Implementation-detail assertions:
- False-confidence tests:

### Mocking
- Appropriate mocks:
- Over-mocking:
- Production logic duplicated in fakes:

### Environment Realism
- Unit/component limitations:
- Browser evidence:
- Database/infrastructure evidence:
- Provider sandbox/emulator evidence:

### Test Data
- Isolation:
- Cleanup/reset:
- Parallel safety:
- Production/shared dependency risk:

### Determinism / Flakiness
- Fixed sleeps:
- Timing races:
- Shared state:
- Order dependence:
- Randomness:
- Network/environment instability:

## Regression Protection

| Escaped/known defect | Original failure mechanism | Regression layer | Proven? |
|---|---|---|---|
| | | | |

## Full-Stack Seam Review

- Request mapping:
- Response mapping:
- Error semantics:
- Authorization assumptions:
- Date/enum/null mapping:
- Rollout compatibility:
- Contract evidence:

## Over-Testing / Redundancy

- Duplicate business-rule coverage:
- E2E branches better proven lower:
- Visual tests for semantic behavior:
- Excessive runtime/cost:
- REDUNDANT_TESTING findings:

## QA Findings

### QA-001 — [Title]

- Severity: CRITICAL / HIGH / MEDIUM / LOW
- Confidence: HIGH / MEDIUM / LOW
- Category: ACCEPTANCE_TRACEABILITY / CRITICAL_SCENARIO / NEGATIVE_COVERAGE / RECOVERY / RACE_CONCURRENCY / AUTHORIZATION / ADAPTER_CONTRACT / HTTP_INTEGRATION / USER_JOURNEY / ACCESSIBILITY_EVIDENCE / VISUAL_EVIDENCE / TEST_QUALITY / OVER_MOCKING / ENVIRONMENT_REALISM / TEST_DATA / FLAKINESS / REGRESSION_PROTECTION / REDUNDANT_TESTING / FULLSTACK_SEAM / MISSING_EVIDENCE
- Acceptance criterion / risk:
- Missing or weak evidence:
- Escaped-failure scenario:
- Existing test inspected:
- Why insufficient:
- Smallest remediation:
- Correct test/evidence layer:
- Blocking: yes/no
- Owner / handoff:
- Re-entry evidence:

## Product / Architecture Questions

| ID | Decision needed | Why QA cannot infer it | Blocking? | Route |
|---|---|---|---|---|
| | | | | |

## Handoffs

| Finding / need | Recipient | Expected output | Blocking | Re-entry condition |
|---|---|---|---|---|
| | Implementation / Validator / Backend Code Review / Frontend Code Review / Backend Architecture Review / Frontend Architecture Review / Security / Performance / Accessibility / Detail Analyst / Reviewer / Product | | yes/no | |

## Residual QA Risk

- Untested accepted behavior:
- Environment limitations:
- Deferred browser/provider evidence:
- Known flaky areas:
- Accepted non-blocking gaps:

## QA Summary

- Critical findings:
- High findings:
- Medium findings:
- Low findings:
- Blocking decisions:
- Blocking evidence gaps:
- Coverage confidence:
- Why final decision is justified:

## Exact Next Action

-
