---
name: implementing-repository-adapters
description: Implements real Infrastructure persistence adapters behind existing repository ports. Use when a Domain/Application repository contract is already accepted and must be backed by SQL, document storage, ORM, filesystem, or another persistence technology. Maps persistence representations to Domain objects and back, reconstitutes valid aggregates, preserves contract semantics, translates technical failures, enforces real constraints, and adds isolated integration tests. Do not use to redesign repository ports, return persistence models, weaken Domain invariants, invent schema policy, or treat mocks as proof of persistence behavior.
...
---

# Implementing Repository Adapters

## Purpose

Implement an Infrastructure adapter that satisfies an existing inward-facing repository port using real persistence.

A correct adapter:

- preserves the exact repository contract;
- owns persistence and ORM/database details;
- maps records to Domain objects and back;
- reconstitutes valid Entities and Value Objects;
- rejects or reports invalid stored data explicitly;
- preserves aggregate and identity semantics;
- translates technical failures into accepted inward meanings;
- enforces authoritative uniqueness, versioning, and atomicity;
- is validated against isolated real persistence.

## Use When

- A repository port and its contract already exist.
- A PostgreSQL, MySQL, MongoDB, DynamoDB, ORM, filesystem, or equivalent implementation is needed.
- An InMemory implementation must be complemented by a real adapter.
- Persistence rows or ORM objects currently leak inward.
- Mapping, transactions, upsert, concurrency, constraints, or invalid stored data need explicit handling.
- A persistence implementation must satisfy shared repository contract tests.

## Do Not Use When

- The repository port is not yet designed.
- The task is external-provider integration.
- The request is to create a generic CRUD layer.
- The accepted schema, migration, or transaction policy is unresolved.
- The request is to bypass Domain construction for convenience.
- The request is only to mock a repository.
- The adapter would return ORM models, rows, or database errors to Application.

## Inputs

- Accepted repository port and design report.
- Domain Entity or aggregate root, Value Objects, errors, and reconstitution rules.
- InMemory repository behavior and contract tests.
- Persistence schema and migrations.
- ORM/driver conventions.
- Transaction, uniqueness, versioning, deletion, pagination, and ordering policies.
- Repository-native integration-test tooling.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the repository port completely.
3. Read the Domain construction and reconstitution rules.
4. Read the repository design report and InMemory semantics.
5. Inspect the persistence schema, migrations, indexes, and constraints.
6. Inspect local adapter, mapper, transaction, and test conventions.
7. Confirm absence, save, deletion, ordering, pagination, and conflict semantics.
8. Confirm transaction ownership and whether a Unit of Work exists.
9. Discover real database test commands and isolation strategy.
10. Do not infer schema or migration changes silently.

## Outputs

- Concrete repository adapter.
- Persistence-to-Domain mapper.
- Domain-to-persistence mapper.
- Technical error translator.
- Transaction and concurrency implementation.
- Shared contract and adapter-specific integration tests.
- Schema/migration impact report.
- Repository adapter implementation record.

## Core Boundary

```text
Domain/Application repository port
← implemented by Infrastructure adapter
↔ persistence mapper
↔ database/ORM/document store
```

Infrastructure depends inward. Inner layers do not import the adapter.

## Workflow

1. **Confirm implementation readiness:** Port, Domain model, schema, policy, and environment are resolved.
2. **Map contract obligations:** List every operation and semantic guarantee.
3. **Inspect persistence reality:** Schema, constraints, indexes, transactions, generated types, and legacy data.
4. **Design persistence mapping:** Record-to-Domain and Domain-to-record transformations.
5. **Implement reconstitution:** Use Domain factories/reconstitution, never field mutation.
6. **Implement repository operations:** Match absence, save, query, ordering, pagination, deletion, and conflict semantics.
7. **Implement authoritative constraints:** Uniqueness, idempotency, versioning, and atomicity.
8. **Translate technical failures:** Map database/ORM errors to accepted inward meanings.
9. **Define transaction behavior:** Respect project ownership and avoid hidden cross-operation transactions.
10. **Add isolated integration tests:** Run against real persistence.
11. **Run shared contract tests:** Compare behavior with the InMemory implementation.
12. **Test invalid stored data:** Detect corruption or incompatible legacy records.
13. **Validate migrations and cleanup:** Apply/reset reliably.
14. **Audit boundaries:** No ORM types or persistence details leak inward.
15. **Report:** Use the implementation record.

## Readiness Gate

Use one:

```text
READY_TO_IMPLEMENT_ADAPTER
READY_WITH_CONDITIONS
RETURN_TO_REPOSITORY_DESIGN
MIGRATION_DECISION_REQUIRED
TRANSACTION_DECISION_REQUIRED
BLOCKED
```

Stop when:

- the repository contract is ambiguous;
- schema cannot represent required invariants;
- transaction ownership is unresolved;
- authoritative duplicate behavior lacks a strategy;
- legacy data cannot be safely reconstituted;
- test persistence cannot be provisioned.

## Contract-First Implementation

For every repository operation record:

- input and output;
- expected absence behavior;
- identity semantics;
- ordering/pagination;
- atomicity;
- uniqueness/conflict;
- technical failure translation;
- required persistence query;
- required test.

Do not add adapter-only public operations to the repository port.

Private adapter helpers are acceptable.

## Mapping

### Persistence to Domain

Map raw values into:

- IDs;
- Value Objects;
- Entity/aggregate reconstitution inputs;
- nested Domain objects.

Never return an ORM object as if it were a Domain Entity.

### Domain to Persistence

Extract Domain primitives explicitly.

Do not serialize the entire Entity blindly when:

- persistence fields differ;
- internal fields must be excluded;
- version/metadata is adapter-owned;
- schema uses a different representation.

### Mapper Location

Keep mappers in Infrastructure near the adapter.

They may be:

- focused functions;
- mapper classes;
- repository-private helpers.

Avoid universal reflection-based mappers.

## Reconstitution

Use accepted Domain APIs such as:

```text
Entity.reconstitute(...)
ValueObject.create(...)
```

Do not:

- call private-field mutation;
- bypass validation with casts;
- construct partially valid objects;
- use ORM decorators as Domain construction;
- treat invalid storage as valid Domain state.

## Invalid Stored Data

Classify:

```text
CORRUPT_RECORD
INCOMPATIBLE_LEGACY_RECORD
UNKNOWN_ENUM
INVALID_VALUE_OBJECT
MISSING_REQUIRED_FIELD
INVALID_RELATION
```

Define whether the adapter:

- fails the operation;
- quarantines/skips only in an explicitly accepted read model;
- emits an operational alert;
- requires a migration;
- supports compatibility mapping.

Do not silently default invalid data into a valid Domain value.

## Save Semantics

Implement exactly the accepted contract.

Possible behaviors:

```text
insert only
replace by identity
upsert
save with expected version
append-only
```

Define:

- generated IDs;
- timestamps;
- version increments;
- returned value;
- duplicate behavior;
- affected-row expectations.

Do not use ORM `save()` semantics without checking whether they match the port.

## Update and Upsert

Upsert is not automatically correct.

Assess:

- creation versus update invariants;
- required expected version;
- lost-update risk;
- immutable fields;
- database conflict target;
- result semantics.

If Domain distinguishes creation and update materially, use distinct adapter logic even when the database supports upsert.

## Not Found

Preserve the port semantics.

Examples:

```text
findById → null
getById → not-found error
update expected row → conflict/not-found
delete idempotently → success even when absent
```

Do not let ORM-specific exceptions decide Application meaning accidentally.

## Uniqueness and Idempotency

Authoritative guarantees normally require one or more of:

- unique constraint;
- composite unique index;
- atomic insert-if-absent;
- transaction;
- lock;
- idempotency table;
- provider/database-supported conditional write.

An existence pre-check is not sufficient under concurrency.

Map duplicate/constraint errors into the accepted semantic result.

Do not expose constraint names inward.

## Optimistic Concurrency

When required:

- store version;
- include expected version in update;
- update conditionally;
- verify affected rows;
- map zero-row update to concurrent modification;
- increment deterministically.

Do not retry concurrency conflicts inside the adapter unless policy explicitly assigns retries there.

## Transactions

Respect the accepted owner.

### Adapter-Owned Atomic Operation

Use when one repository method can satisfy the consistency boundary.

### Application/Unit-of-Work Owned

Use when several repositories or operations must commit together.

The adapter must not start independent hidden transactions that break outer atomicity.

Avoid remote provider calls inside database transactions unless explicitly designed.

## SQL/Relational Mapping

Define:

- table and column mapping;
- joins;
- aggregate child loading;
- row ordering;
- null semantics;
- enum representation;
- decimal/date handling;
- N+1 risks;
- constraint mapping.

Use explicit ordering for child collections and paginated queries.

Do not rely on implicit database order.

## Document Mapping

Define:

- document version/schema version;
- nested object mapping;
- missing fields;
- backward compatibility;
- partial documents;
- atomic update semantics;
- index/uniqueness behavior.

Do not assume document shape equals Domain serialization forever.

## Dates and Time

Define:

- storage timezone;
- precision;
- driver conversion;
- serialization;
- comparison semantics.

Avoid host-local timezone conversion.

Test round trips at boundaries.

## Money and Numeric Precision

Use accepted persistence representation:

- integer minor units;
- decimal;
- amount plus currency.

Do not use floating-point conversions that violate Domain precision.

Test exact round trips and boundary values.

## Enums

Map explicitly between persistence values and Domain enums/Value Objects.

Unknown values are invalid stored data unless compatibility policy defines a fallback.

Do not cast strings blindly.

## Deletion and Archival

Implement accepted semantics:

- hard delete;
- soft delete;
- archive;
- deactivate;
- retention cleanup.

Ensure queries consistently include or exclude archived records.

Do not implement hard delete when the port says archive.

## Query and Pagination

Match:

- criteria semantics;
- stable ordering;
- tie-breakers;
- cursor/offset behavior;
- page size;
- empty result;
- duplicate prevention.

Opaque cursors should not expose internal implementation unless accepted.

Test concurrent insertion effects when contract requires stronger consistency.

## Cross-Module Data

Do not join directly across capabilities in a way that bypasses ownership unless architecture explicitly permits it.

Prefer owning capability ports or read models.

A database join is not automatically an architectural permission.

## Error Translation

Translate technical failures into accepted categories.

Examples:

```text
unique violation → DUPLICATE
serialization conflict → CONCURRENT_MODIFICATION
connection failure → PERSISTENCE_UNAVAILABLE
timeout → PERSISTENCE_TIMEOUT
invalid record → CORRUPT_STORED_DATA
```

Do not leak:

- SQLSTATE;
- ORM exception;
- driver stack;
- table/constraint names;
- connection strings.

Preserve technical cause internally for observability according to policy.

## Observability

Record safely:

- repository operation;
- duration;
- success/failure category;
- retry/transaction metadata;
- affected-row anomaly;
- correlation context.

Do not log sensitive rows or credentials.

Infrastructure owns database telemetry.

## Resource Lifecycle

Handle:

- connection/client lifecycle;
- transaction/session lifecycle;
- cursor/stream cleanup;
- test cleanup;
- shared versus transient clients.

Composition root owns long-lived client construction according to policy.

Repository methods must not create unmanaged global clients.

## Generated ORM Types

Generated types belong to Infrastructure.

Do not export them through repository ports or Application DTOs.

Regenerate from the source schema; do not hand-edit generated output.

## Integration Testing

Mocks do not prove adapter behavior.

Use real persistence through:

- Testcontainers;
- ephemeral database;
- isolated schema/database;
- documented emulator when it faithfully supports required behavior.

### Test Isolation

Use one or more:

- transaction rollback;
- unique database/schema;
- deterministic cleanup;
- isolated container;
- unique namespace.

Parallel tests must not collide.

### Required Cases

- schema/migrations apply;
- save and retrieve round trip;
- Value Object mapping;
- aggregate child mapping;
- absence;
- replace/update/upsert semantics;
- duplicate/constraint;
- ordering/pagination;
- transaction behavior;
- concurrency/version conflict;
- deletion/archive;
- invalid stored data;
- technical failure translation when feasible;
- cleanup.

## Shared Contract Tests

Run repository behavioral cases against:

- InMemory implementation;
- real adapter.

Contract tests prove semantic parity.

Adapter-specific tests prove technical behavior.

Do not force technical database cases into InMemory.

## Migration Impact

When implementation requires schema change:

- create/update migration according to tooling;
- test forward application;
- test compatibility with existing readers/writers;
- define backfill;
- define rollback/recovery;
- verify representative data;
- define monitoring and cleanup.

Do not silently mutate schema outside migration policy.

## Brownfield Data

For legacy records:

- characterize real shapes;
- define compatibility mapping;
- identify impossible Domain states;
- separate migration from adapter defaulting;
- track temporary branches and removal conditions.

Do not allow compatibility code to become permanent without an exit plan.

## Security

Use parameterized queries/ORM-safe APIs.

Review:

- tenant scoping;
- authorization assumptions;
- row-level security;
- sensitive encryption;
- injection;
- mass assignment;
- accidental broad queries;
- data minimization.

Repository adapters do not own actor authorization unless architecture explicitly places data-scoping there.

## Implementation Sequence

Recommended:

```text
1. map one contract behavior
2. add failing integration/contract test
3. implement focused mapper/query
4. pass round trip
5. add failure/constraint cases
6. add concurrency/transaction cases
7. run full repository contract
8. validate migrations and cleanup
```

## Boundary Guardrails

Adapter may import:

- repository port;
- Domain types;
- ORM/driver;
- Infrastructure config/errors/telemetry.

Adapter must not make inner layers import:

- ORM models;
- persistence records;
- database clients;
- generated DB types;
- technical exceptions.

## Output

Use `assets/repository-adapter-implementation-record.md`.

## Completion Criteria

- [ ] Repository contract and Domain reconstitution rules confirmed.
- [ ] Schema, migrations, constraints, and transaction policy inspected.
- [ ] Every port operation implemented with matching semantics.
- [ ] Persistence-to-Domain and Domain-to-persistence mapping is explicit.
- [ ] Invalid stored data is handled without silent coercion.
- [ ] Not-found, duplicate, conflict, timeout, and unavailable failures are translated.
- [ ] Authoritative uniqueness/idempotency and concurrency behavior are implemented.
- [ ] Transaction ownership is preserved.
- [ ] Stable ordering and pagination are explicit.
- [ ] Real isolated persistence tests pass.
- [ ] Shared contract tests pass against InMemory and real adapter.
- [ ] Migration and cleanup behavior is reproducible.
- [ ] No ORM, row, generated, or database types leak inward.
- [ ] No repository port redesign or speculative operation was introduced.
