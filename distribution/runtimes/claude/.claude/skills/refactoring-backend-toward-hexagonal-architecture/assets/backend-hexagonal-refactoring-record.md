# Backend Hexagonal Refactoring Record

## Context

- Change ID:
- Selected behavior:
- Capability/module:
- Current entry point:
- Brownfield adaptation record:
- Governing standard:
- Repository-local rules:
- Refactor owner:

## Readiness

- Current behavior understood:
- Characterization available:
- Target state accepted:
- Seam accepted:
- Public compatibility resolved:
- Data compatibility resolved:
- Transaction/partial-failure resolved:
- Security/tenant behavior resolved:
- Initial decision:
- Conditions/blockers:

## Current Runtime Path

```text
entry point
→ legacy orchestration
→ decisions
→ persistence/provider
→ response/event
```

- Business decisions currently located:
- Persistence:
- External services:
- Error mapping:
- Transaction owner:
- Public contract:
- Known operational risks:

## Target Runtime Path

```text
delivery
→ Use Case
→ Domain
→ ports
→ adapters
→ composition
```

- Domain:
- Application:
- Repository port/adapter:
- External port/adapter:
- Delivery:
- Composition:
- Compatibility boundary:

## Refactor Scope

| Change | Classification | Included |
|---|---|---|
| | REQUIRED_TO_PRESERVE_BEHAVIOR / REQUIRED_FOR_TARGET_BOUNDARY / REQUIRED_COMPATIBILITY / SAFE_LOCAL_CLEANUP / DEFERRED_DEBT / UNRELATED | |

## Characterization Evidence

| Behavior/contract | Test/evidence | Initial result | Final result |
|---|---|---|---|
| | | | |

- Known bug reproduction:
- Intentional behavior changes:
- Missing characterization:
- Characterization decision:

## Seam

- Type:
- Current side:
- Target side:
- Semantic contract:
- Owner:
- Test coverage:
- Long-term role/removal condition:
- Why it improves the architecture:

## Responsibility Movement

| Current responsibility | Classification | Target owner | Focused skill | Evidence |
|---|---|---|---|---|
| | DOMAIN_INVARIANT / APPLICATION_ORCHESTRATION / INFRASTRUCTURE_POLICY / DELIVERY_MAPPING / COMPATIBILITY_MAPPING | | | |

## Domain Stage

- Entities/Value Objects:
- Domain Services:
- Invariants moved:
- Tests:
- Gate:

## Application Stage

- Use Case:
- Request/Response DTOs:
- Authorization/tenancy:
- Transaction/idempotency:
- Repository ports:
- External ports:
- Tests:
- Gate:

## Adapter Stage

### Repository

- Adapter:
- Mapping/reconstitution:
- Migration/compatibility:
- Constraints/concurrency:
- Integration tests:
- Gate:

### External Service

- Adapter:
- Provider mapping:
- Retry/timeout/idempotency:
- Reconciliation:
- Evidence level:
- Gate:

## Transaction and Side Effects

### Current order

1.
2.
3.

### Target order

1.
2.
3.

- Atomic boundary:
- Partial failure:
- Recovery/reconciliation:
- Accepted decision:

## Caller Redirection

- Caller:
- Previous target:
- New target:
- Routing/feature flag:
- Default:
- Rollback:
- Observability:
- Redirected result:

## Compatibility and Migration

- Public API/event:
- Existing data:
- Unknown/invalid states:
- Backfill:
- Mixed-version support:
- Dual-read/write:
- One authoritative path:
- Cleanup condition:

## Validation Evidence

| Check | Command/evidence | Result/classification |
|---|---|---|
| Characterization | | |
| Domain | | |
| Application | | |
| Repository integration | | |
| Provider integration | | |
| HTTP E2E | | |
| Migration/backfill | | |
| Typecheck/lint/build | | |
| Architecture before/after | | |

## Drift Comparison

- Pre-existing:
- New:
- Worsened:
- Fixed:
- Accepted temporary:

## Legacy Path Removal

- Remaining callers:
- Compatibility window:
- Rollback dependency:
- Data migration verified:
- Feature flag usage:
- Old configuration/secrets:
- Tests/fixtures:
- Removal decision:
- Owner and exit condition if retained:

## Residual Debt

| Debt item | Risk | Owner | Trigger | Next skill/slice |
|---|---|---|---|---|
| | | | | |

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Legacy path state:
- Next caller or behavior:
- Required follow-up:
