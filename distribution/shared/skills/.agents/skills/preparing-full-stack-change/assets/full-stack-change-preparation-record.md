# Full-Stack Change Preparation Record

## Context

- Change:
- User story:
- Repository/system:
- OpenSpec:
- Full-stack standard:
- Backend standard:
- Frontend standard:
- Applicable `AGENTS.md`:
- Preparer/date:

## Request Enrichment

- Problem:
- Actor:
- Goal:
- Business outcome:
- Acceptance criteria:
- Constraints:
- Edge cases:
- Non-goals:
- Unknowns:
- Readiness:

## OpenSpec

- Existing capability/spec:
- Existing related change:
- Exploration findings:
- Conflicts:
- Decision: USE_EXISTING_CHANGE / EDIT_EXISTING_CHANGE / CREATE_NEW_CHANGE / NO_OPENSPEC_REQUIRED_BY_REPOSITORY / OPENSPEC_DECISION_BLOCKED
- Change ID:
- Required create/edit skill:
- Status:

## Full-Stack Capability

- Capability:
- Critical journey:
- Current behavior:
- Intended behavior:
- External provider:
- Security-sensitive:
- Data migration:
- Rollout risk:

## Backend Slice

- Capability owner:
- Domain changes:
- Application/use cases:
- DTOs:
- Ports:
- Repository/persistence:
- Provider adapters:
- HTTP/controller:
- Authorization:
- Composition:
- Tests/validation:
- Brownfield/refactor:
- Backend handoff skill(s):

## Frontend Slice

- Capability owner:
- Route/screen:
- Domain/Application:
- DTO/view data:
- HTTP/repository:
- Server state:
- Hooks/container:
- Components:
- Styling:
- Accessibility:
- Analytics/privacy:
- Tests/validation:
- Brownfield/refactor:
- Frontend handoff: `implementing-frontend-change`

## Shared Contract

### Endpoint / Operation

- Method:
- Path:
- Authentication:
- Authorization:
- Idempotency:
- Content type:

### Request DTO

| Field | Type | Required | Meaning / validation |
|---|---|---|---|
| | | | |

### Response DTO

| Field | Type | Meaning |
|---|---|---|
| | | |

### Error Contract

| Status/code | Semantic meaning | Frontend behavior |
|---|---|---|
| | | |

### Other Contracts

- Redirect/callback:
- Webhook:
- Event/message:
- Pagination:
- Sorting/filtering:
- Feature flag:

## Contract Ownership

| Decision | Owner | Consumers | Status |
|---|---|---|---|
| | | | |

## Compatibility

- Classification: ADDITIVE / BACKWARD_COMPATIBLE / BREAKING / MIGRATION_REQUIRED
- Existing consumers:
- Old contract:
- New contract:
- Compatibility adapter:
- Deprecation:
- Removal condition:

## Persistence / Migration

- Schema change:
- Migration:
- Backfill:
- Old/new code compatibility:
- Rollback:
- Owner:

## Deployment Sequence

```text

```

- Backend deploy first:
- Frontend deploy first:
- Feature flag:
- Provider setup:
- Migration timing:
- Rollback compatibility:

## Dependency Graph

```text

```

## Parallelization

| Task | Depends on | Parallelizable | Reason |
|---|---|---|---|
| | | | |

## Contract Mock / Fixture

- Required:
- Source of truth:
- Frontend fixture:
- Drift check:
- Consumer/provider contract test:

## Acceptance Criteria Ownership

| AC | Backend | Frontend | Shared contract | Verification |
|---|---|---|---|---|
| | | | | |

## Risk Triggers

### Security
- Trigger:
- STRIDE:
- Application security:
- Control verification:
- Frontend security:

### Privacy
- Trigger:
- Frontend privacy/analytics:
- Data governance owner:

### Performance
- Trigger:
- Backend:
- Frontend:
- Algorithmic complexity:

## Open Questions

| Question | Type | Blocking | Owner | Resolution |
|---|---|---|---|---|
| | PRODUCT / ARCHITECTURE / CONTRACT / THIRD_PARTY / NON_BLOCKING | | | |

## Decision Ledger

| Decision | Status | Owner |
|---|---|---|
| capability | | |
| API path/method | | |
| request DTO | | |
| response DTO | | |
| errors | | |
| authorization | | |
| idempotency | | |
| compatibility | | |
| deployment sequence | | |
| frontend ownership | | |
| backend ownership | | |

## Backend Handoff

- Goal:
- Accepted spec:
- Backend scope:
- Shared contracts:
- Owned acceptance criteria:
- Authorization:
- Persistence/provider:
- Compatibility:
- Dependencies:
- Expected validation:
- Open non-blocking questions:

## Frontend Handoff

- Goal:
- Accepted spec:
- Frontend scope:
- Stable API contract:
- View behavior:
- Permission UX:
- Accessibility:
- Analytics/privacy:
- Mock/fixture:
- Owned acceptance criteria:
- Dependencies:
- Expected validation:
- Open non-blocking questions:

## Verification Expectations

- Backend Domain/Application:
- Backend adapters/HTTP:
- Frontend adapters/runtime validation:
- Frontend component/hook:
- Contract:
- Critical browser journey:
- Security:
- Accessibility:
- Performance:

## Scope Control

- Newly discovered scope:
- Included:
- Deferred:
- Non-goals:
- Required future change:

## Final Decision

- Decision:
- Requirements ready:
- OpenSpec ready:
- Contract ready:
- Backend slice ready:
- Frontend slice ready:
- Compatibility ready:
- Sequence ready:
- Blocking questions:
- Ready for handoff:
