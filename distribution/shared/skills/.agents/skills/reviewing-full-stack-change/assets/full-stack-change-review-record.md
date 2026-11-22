# Full-Stack Change Review Record

## Context

- Change:
- OpenSpec/specification:
- Preparation record:
- Backend scope:
- Frontend scope:
- Shared contract:
- Deployment/compatibility plan:
- Applicable `AGENTS.md`:
- Reviewer/date:

## Readiness

- Specification available:
- Specification validated:
- Backend implementation available:
- Backend evidence available:
- Frontend implementation available:
- Frontend evidence available:
- Contract evidence available:
- Required risk reviews available:
- Mechanical validation available:
- Initial state:

## Specification Validation

- Accepted change/spec:
- Validation evidence:
- Acceptance criteria:
- Non-goals:
- Spec drift:
- Status: SPEC_IMPLEMENTATION_ALIGNED / SPEC_DRIFT_IMPLEMENTATION_AHEAD / SPEC_DRIFT_SPEC_AHEAD / SPEC_CONFLICT

## Backend Evidence

| Evidence | Status | Blocking findings |
|---|---|---|
| backend change validation | | |
| architecture validation/review | | |
| code review | | |
| tests/build/runtime | | |
| security/performance | | |

- Backend result: PASS / PASS_WITH_FINDINGS / FAIL / NOT_AVAILABLE

## Frontend Evidence

| Evidence | Status | Blocking findings |
|---|---|---|
| architecture validation | | |
| architecture review | | |
| tests | | |
| accessibility | | |
| security/privacy/performance | | |
| build/runtime | | |

- Frontend result: PASS / PASS_WITH_FINDINGS / FAIL / NOT_AVAILABLE

## Shared Contract Matrix

| Contract element | Spec | Backend | Frontend | Mock/test | Docs | Result |
|---|---|---|---|---|---|---|
| method/path | | | | | | |
| request DTO | | | | | | |
| response DTO | | | | | | |
| errors | | | | | | |
| authorization | | | | | | |
| idempotency | | | | | | |
| redirect/callback | | | | | | |

## Request Contract

| Field | Spec | Backend accepts | Frontend sends | Result |
|---|---|---|---|---|
| | | | | |

## Response Contract

| Field | Spec type/nullability | Backend emits | Frontend schema/consumer | Result |
|---|---|---|---|---|
| | | | | |

## Error Contract

| Status/code | Spec | Backend | Frontend behavior | Result |
|---|---|---|---|---|
| | | | | |

## Authorization

- Accepted permission/capability:
- Backend authoritative enforcement:
- Tenant/resource ownership:
- Negative test:
- Frontend UX behavior:
- 401/403 behavior:
- Result:

## Idempotency / Retry

- Applicable:
- Accepted contract:
- Client behavior:
- Backend behavior:
- Lost response/retry:
- Double submit:
- Result:

## Provider / Redirect / Callback

- Provider:
- Backend response:
- Frontend navigation:
- Cancel:
- Success:
- Callback:
- Correlation/state:
- Delayed callback behavior:
- Result:

## Compatibility / Rollout

- Classification:
- Old frontend + new backend:
- New frontend + old backend:
- Feature flag:
- Migration state:
- Removal/deprecation:
- Rollback:
- Result:

## Other Contract Semantics

### Pagination
- Result:

### Date / Time
- Result:

### Money / Currency
- Result:

### Events / Webhooks
- Result:

## Mock / Fixture Drift

| Fixture/mock | Accepted contract source | Drift | Result |
|---|---|---|---|
| | | | |

## Acceptance Criteria Traceability

| AC | Spec | Backend evidence | Frontend evidence | Contract evidence | Journey | Status |
|---|---|---|---|---|---|---|
| | | | | | | |

## Critical Journey Trace

```text
user action
→ frontend
→ request
→ backend
→ domain/application
→ persistence/provider
→ response/error
→ frontend state
→ user-visible outcome
```

- Journey:
- Failure branches:
- Evidence:
- Result:

## Adversarial Review

- Artifact:
- Retry/replay:
- partial success:
- timeout after commit:
- stale state:
- double submit:
- provider reordering:
- mixed versions:
- authorization mismatch:
- error mismatch:
- rollback:
- Findings:

## Detail Analysis

- Artifact:
- enum propagation:
- labels/translations:
- error messages:
- mocks/fixtures:
- config/env:
- permissions:
- analytics events:
- docs/API examples:
- stale references:
- Findings:

## Risk Evidence

### Security
- Required:
- Evidence:
- Blocking:

### Privacy
- Required:
- Evidence:
- Blocking:

### Performance
- Required:
- Evidence:
- Blocking:

### Algorithmic Complexity
- Required:
- Evidence:
- Blocking:

## Mechanical Validation

- Validator Agent:
- Lint:
- Typecheck:
- Tests:
- Build:
- E2E:
- Missing checks:
- Status:

## Documentation

| Surface | Impact | Action | Status |
|---|---|---|---|
| OpenSpec | | | |
| API docs | | | |
| README | | | |
| architecture docs | | | |
| migration/runbook | | | |
| analytics/security docs | | | |

- `updating-documentation` required:
- Documentation result: DOCS_NOT_REQUIRED / DOCS_UPDATE_REQUIRED / DOCS_UPDATED / DOCS_BLOCKED

## Findings

### FS-001 — [Title]

- Source:
- Priority:
- Spec/AC:
- Backend state:
- Frontend state:
- Contract mismatch:
- Impact:
- Owner: BACKEND / FRONTEND / SHARED_CONTRACT / FULL_STACK / INFRASTRUCTURE / SECURITY / PRODUCT / DOCUMENTATION / THIRD_PARTY
- Required fix:
- Verification:
- Status:

## Finding Aggregation

- Duplicate findings consolidated:
- Pre-existing not worsened:
- Pre-existing worsened:
- Change introduced:
- Change required to fix:

## Final Gate

- Spec valid:
- Backend acceptable:
- Frontend acceptable:
- Contract aligned:
- ACs complete:
- Adversarial blockers resolved:
- Detail blockers resolved:
- Risk reviews complete:
- Mechanical validation complete:
- Docs complete:

## Final Decision

- Decision:
- Blocking findings:
- Required contract repair:
- Required spec update:
- Required docs:
- Required risk review:
- Residual risk:
- Ready for merge/release:
