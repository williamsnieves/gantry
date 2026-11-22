# Repository Adapter Implementation Record

## Context

- Change ID:
- Repository port:
- Adapter:
- Persistence technology:
- ORM/driver:
- Domain aggregate:
- Schema/migrations:
- Transaction policy:
- Test environment:

## Readiness

- Contract complete:
- Domain reconstitution API:
- Schema compatibility:
- Migration required:
- Transaction/concurrency decisions:
- Blockers/conditions:

## Contract Mapping

| Port operation | Persistence operation | Semantics preserved | Test |
|---|---|---|---|
| | | | |

## Persistence Mapping

### Record to Domain

| Persistence field | Domain target | Conversion/validation |
|---|---|---|
| | | |

### Domain to Record

| Domain source | Persistence field | Conversion |
|---|---|---|
| | | |

### Reconstitution

- Entity factory:
- Nested objects:
- Unknown enums:
- Invalid records:
- Compatibility branches:

## Write Semantics

- Insert/update/upsert:
- Identity:
- Generated values:
- Immutable fields:
- Versioning:
- Affected-row expectations:
- Returned result:

## Constraints and Concurrency

- Unique constraints:
- Idempotency:
- Atomic operations:
- Expected version:
- Conflict translation:
- Retry ownership:

## Transactions

- Owner:
- Scope:
- Participating operations:
- Outer transaction compatibility:
- Rollback behavior:
- Remote side effects:

## Query Semantics

- Criteria:
- Ordering:
- Tie-breakers:
- Pagination:
- Archived/deleted filtering:
- Empty/absence behavior:

## Error Translation

| Technical condition | Inward meaning | Observability |
|---|---|---|
| | | |

## Integration Tests

| Test | Environment | Result |
|---|---|---|
| | | |

## Shared Contract Tests

- InMemory result:
- Real adapter result:
- Differences:
- Adapter-only cases:

## Migration and Brownfield

- Migration:
- Forward validation:
- Existing data:
- Backfill:
- Compatibility:
- Recovery/rollback:
- Cleanup/removal condition:

## Security and Operations

- Tenant scoping:
- Query safety:
- Sensitive data:
- Logging/redaction:
- Metrics/traces:
- Client/session lifecycle:
- Test cleanup:

## Boundary Audit

- ORM/generated types exposed:
- Persistence records exposed:
- Technical errors exposed:
- Port changes:
- Cross-module data access:

## Final Status

- Decision:
- Remaining blockers:
- Residual risks:
- Required follow-up:
