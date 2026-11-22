# Repository Adapter Testing Record

## Context

- Change ID:
- Repository port:
- Concrete adapter:
- Persistence technology:
- ORM/driver:
- Domain aggregate:
- Test framework:
- Shared contract suite:
- Focused command:

## Readiness and Safety

- Test environment:
- Destructive-test safety marker:
- Isolation strategy:
- Parallel strategy:
- Credentials/source:
- Schema/migration source:
- Conditions/blockers:

## Provisioning

- Container/database/schema:
- Image/version:
- Namespace:
- Readiness check:
- Connection configuration:
- Startup command:
- Shutdown command:

## Migrations

| Migration check | Command | Result/classification |
|---|---|---|
| Clean database | | |
| Current version | | |
| Indexes/constraints | | |
| Representative upgrade | | |

## Shared Contract Tests

| Contract case | InMemory | Real adapter | Notes |
|---|---|---|---|
| | | | |

## Round Trips and Mapping

| Case | Domain input | Persistence concern | Domain result |
|---|---|---|---|
| | | | |

### Mapping Coverage

- IDs:
- Value Objects:
- Enums:
- Unknown enums:
- Dates/timezone/precision:
- Money/decimals:
- Collections/order:
- Nullability:
- Legacy/schema version:

## Write Semantics

- Insert:
- Replace:
- Update:
- Upsert:
- Generated values:
- Versioning:
- Affected rows:
- Return semantics:

## Constraints and Concurrency

| Case | Mechanism | Expected result | Evidence |
|---|---|---|---|
| Duplicate | | | |
| Concurrent duplicate | | | |
| Stale version | | | |
| Atomic conditional write | | | |

## Transactions

- Owner:
- Commit:
- Rollback:
- Outer transaction participation:
- Partial failure:
- Resource cleanup:

## Query Behavior

- Absence:
- Criteria:
- Tenant scoping:
- Ordering:
- Tie-breaker:
- Pagination:
- Empty page:
- Archived/deleted visibility:

## Invalid Stored Data

| Invalid shape | Injection method | Expected inward result |
|---|---|---|
| | | |

## Technical Failure Translation

| Technical condition | Inward meaning | Test method |
|---|---|---|
| | | |

## Cleanup and Reliability

- Per-test reset:
- Suite cleanup:
- Container/client closure:
- Partial-failure cleanup:
- Open handles:
- Parallel collisions:
- Flakiness findings:

## Commands and Evidence

| Command | Scope | Result/classification |
|---|---|---|
| | | |

## Boundary Audit

- ORM rows returned:
- Generated DB types exposed:
- Raw technical errors exposed:
- Port changed for test convenience:
- Mocks/InMemory used as real proof:

## Final Status

- Decision:
- Conditions:
- Known failures:
- Residual risks:
- Missing real-boundary evidence:
- Required follow-up:
