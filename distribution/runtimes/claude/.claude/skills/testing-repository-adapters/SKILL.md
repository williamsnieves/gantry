---
name: testing-repository-adapters
description: Designs and implements integration tests for backend repository adapters using isolated real persistence. Use when persistence mappings, Domain reconstitution, migrations, constraints, transactions, ordering, pagination, deletion, concurrency, invalid stored data, technical failure translation, cleanup, or shared repository contract parity must be proven. Prefer Testcontainers, ephemeral databases, isolated schemas, or faithful emulators. Do not use mocks or InMemory repositories as proof of real persistence behavior, do not leak ORM/database types into assertions, and do not claim blocked infrastructure tests passed.
---

# Testing Repository Adapters

## Purpose

Prove that a concrete repository adapter satisfies its inward repository contract against real isolated persistence.

A correct repository-adapter test suite validates:

- migrations and schema readiness;
- Domain-to-persistence and persistence-to-Domain mapping;
- valid aggregate reconstitution;
- save, replace, insert, update, or upsert semantics;
- absence and not-found behavior;
- uniqueness and authoritative duplicate protection;
- ordering and pagination;
- transactions and rollback;
- concurrency and optimistic locking;
- deletion, soft deletion, or archival;
- invalid stored data handling;
- technical failure translation;
- deterministic cleanup and isolation;
- parity with shared repository contract tests.

## Core Test Boundary

```text
repository port contract
→ concrete Infrastructure adapter
→ real isolated persistence
→ observable Domain result and database behavior
```

Mocks and InMemory implementations are not substitutes for this boundary.

## Use When

- Testing a SQL, document, key-value, filesystem, or other persistence adapter.
- Verifying ORM/driver mappings.
- Verifying Domain reconstitution from stored records.
- Testing migrations and constraints.
- Testing duplicate protection under concurrency.
- Testing transactions or version conflicts.
- Testing ordering, pagination, or deletion semantics.
- Testing invalid or legacy stored data.
- Testing technical database failure translation.
- Running shared contract tests against the real adapter.
- Repairing flaky or non-isolated persistence tests.

## Do Not Use When

- Testing Domain models.
- Testing Application Use Cases with InMemory repositories.
- Testing external provider adapters.
- Testing HTTP endpoints.
- The repository port or adapter contract is unresolved.
- The test uses only mocks or an InMemory repository.
- The environment cannot provide any faithful persistence boundary and the result is being presented as fully verified.
- The task is to redesign the repository interface.
- Assertions depend on ORM internals instead of accepted behavior.

## Inputs

- Accepted repository port and design report.
- Concrete repository adapter.
- Domain Entities, Value Objects, errors, and reconstitution APIs.
- Persistence schema and migration tooling.
- ORM/driver configuration.
- Shared repository contract tests.
- Project policies for test databases, isolation, cleanup, transactions, concurrency, and generated schema.
- Existing integration-test harness.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the repository port and adapter implementation.
3. Read Domain construction and reconstitution behavior.
4. Inspect schema, migrations, indexes, and constraints.
5. Inspect existing persistence-test harness and commands.
6. Confirm the strongest available environment:
   - Testcontainers;
   - ephemeral database;
   - isolated schema/database;
   - faithful official emulator.
7. Confirm migration and reset procedures.
8. Confirm parallel-test isolation.
9. Confirm technical error translation semantics.
10. Do not infer missing schema, cleanup, or transaction policy.

## Outputs

- Repository adapter test inventory.
- Isolated persistence provisioning.
- Migration and cleanup procedure.
- Shared contract test execution.
- Adapter-specific integration tests.
- Concurrency and failure tests.
- Environment/failure classification.
- Repository adapter testing record.
- Optional helper scripts or harness design for bootstrap/reset/namespace generation.

## Workflow

1. **Confirm readiness:** Port, adapter, schema, migrations, Domain mapping, and test environment are available.
2. **Select isolation strategy:** Container, database, schema, namespace, or emulator.
3. **Provision persistence:** Start or connect to a safe isolated instance.
4. **Apply migrations:** From the same source used by production.
5. **Create deterministic test namespace:** Avoid parallel collision.
6. **Run shared repository contract tests:** Compare accepted semantics.
7. **Test round trips:** Domain → persistence → Domain.
8. **Test mapping boundaries:** IDs, Value Objects, enums, dates, Money, collections.
9. **Test write semantics:** Insert, replacement, update, upsert, versions.
10. **Test constraints and concurrency:** Duplicate, conditional update, atomicity.
11. **Test query semantics:** Absence, ordering, pagination, filters.
12. **Test transaction behavior:** Commit, rollback, outer transaction participation.
13. **Test deletion/archive behavior.**
14. **Test invalid and legacy stored data.**
15. **Test technical failure translation where feasible.**
16. **Verify cleanup and handle closure.**
17. **Classify infrastructure failures honestly.**
18. **Record exact commands and evidence.**

## Readiness Gate

Use one:

```text
READY_TO_TEST_REPOSITORY_ADAPTER
READY_WITH_CONDITIONS
RETURN_TO_ADAPTER_IMPLEMENTATION
MIGRATION_OR_SCHEMA_DECISION_REQUIRED
TEST_ENVIRONMENT_REQUIRED
ISOLATION_STRATEGY_REQUIRED
BLOCKED
```

Stop when:

- migrations cannot be applied reproducibly;
- schema differs from the adapter expectation;
- required constraints do not exist;
- test data cannot be isolated safely;
- concurrent behavior cannot be exercised at the real boundary;
- credentials point to a shared or production database;
- the adapter returns persistence types instead of Domain objects.

## Real Persistence Requirement

Preferred order:

```text
Testcontainers
→ ephemeral dedicated database
→ isolated schema/database
→ faithful official emulator
```

A local mock server, ORM mock, or InMemory implementation does not prove persistence behavior.

When the real environment is unavailable:

- run truthful lower-level mapping tests if useful;
- classify the real boundary as blocked;
- document residual uncertainty;
- provide the exact command/environment still required.

## Environment Safety

Never run destructive tests against:

- production;
- shared staging data;
- developer databases without explicit isolation;
- an environment selected by ambiguous defaults.

Require an explicit test environment marker where project policy supports it.

Fail safely if the target looks non-test.

## Testcontainers

When supported:

- use a pinned compatible database image;
- start one container per suite or worker according to cost;
- expose connection details only to the test process;
- apply production migrations;
- wait for readiness;
- close the container deterministically;
- record startup failures separately from product failures.

Do not reuse an arbitrary developer container without explicit policy.

## Ephemeral Database or Schema

When containers are unavailable:

- create a unique database/schema per worker or suite;
- generate deterministic or collision-resistant names;
- apply migrations;
- set search path/connection explicitly;
- drop the namespace after tests;
- clean up after partial failure.

Do not rely solely on truncating shared tables when parallel tests can collide.

## Unique Test Namespace

A namespace may use:

```text
test_<suite>_<worker>_<random-or-run-id>
```

Requirements:

- valid database identifier;
- collision resistant;
- traceable to the run;
- safely escaped;
- removed after execution.

Do not include secrets or personal data in names.

## Migrations

Tests must apply migrations from the authoritative production source.

Verify:

- clean-database migration;
- current schema version;
- indexes and constraints;
- migration ordering;
- representative existing-data compatibility when relevant;
- cleanup/reset.

Do not create tables manually in test code unless project policy explicitly uses schema fixtures as the authoritative source.

## Migration Failure

Classify:

```text
MIGRATION_PRODUCT_FAILURE
MIGRATION_ENVIRONMENT_FAILURE
MIGRATION_TOOLING_BLOCKED
```

Do not continue adapter assertions against a partially migrated schema.

## Shared Contract Tests

Repository contract tests should run against:

- InMemory implementation;
- concrete real adapter.

Shared cases may include:

- save and find;
- absence;
- replacement;
- query semantics;
- duplicate behavior;
- ordering;
- deletion/archival.

Adapter-specific technical tests remain separate.

Do not force database-specific failures into InMemory contract tests.

## Round-Trip Tests

Verify:

```text
Domain aggregate
→ adapter save
→ database
→ adapter read
→ semantically equivalent Domain aggregate
```

Assert:

- identity;
- Value Objects;
- lifecycle;
- nested children;
- ordering where accepted;
- timestamps and precision;
- Money and decimal precision;
- optional/null values;
- serialization-relevant fields.

Do not use raw ORM-object equality as the main assertion.

## Mapping Tests

Test explicit boundary cases:

- ID representation;
- enum mapping;
- unknown enum;
- UTC/time precision;
- decimal/Money;
- nullable values;
- composite Value Objects;
- collection ordering;
- schema-version fields;
- encrypted or transformed fields when accepted.

Use Domain equality or public primitives where appropriate.

## Invalid Stored Data

Insert malformed records through a low-level test helper only when required to bypass adapter safeguards.

Cases:

- unknown enum;
- invalid Value Object;
- missing required field;
- inconsistent lifecycle timestamps;
- invalid child relationship;
- incompatible legacy schema.

Verify the accepted result:

```text
CORRUPT_STORED_DATA
INCOMPATIBLE_LEGACY_RECORD
migration required
explicit compatibility mapping
```

Do not silently default the record into valid Domain state.

## Save Semantics

Test the exact repository contract:

- insert only;
- replace by identity;
- update;
- upsert;
- append-only;
- expected-version save.

Verify:

- created/updated rows;
- immutable fields;
- generated values;
- version increments;
- affected-row expectations;
- return behavior.

Do not assume the ORM's generic `save()` semantics match the contract.

## Duplicate and Unique Constraints

Test real authoritative protection.

Cases:

- first insert succeeds;
- duplicate insert yields accepted semantic conflict;
- concurrent duplicate attempts result in exactly one accepted stored state;
- technical constraint name does not leak inward.

Avoid pre-check-only tests.

A `find` followed by `insert` without an actual unique/atomic mechanism is insufficient.

## Concurrency

Use concurrent operations against the real adapter.

Test applicable cases:

- duplicate creation;
- optimistic version conflict;
- conditional update;
- serialization/deadlock translation;
- lost update prevention;
- transaction isolation behavior.

Keep concurrency tests deterministic enough to diagnose.

Use barriers/latches or database primitives rather than arbitrary sleeps.

## Optimistic Locking

Verify:

- initial version;
- successful update with expected version;
- version increment;
- stale version rejected;
- stored state remains correct;
- conflict maps to accepted semantic error.

Do not retry automatically in the test unless retry ownership belongs to the adapter.

## Transactions

Test accepted ownership.

### Adapter-Owned Atomic Method

Verify complete commit or rollback for one repository operation.

### Outer Transaction / Unit of Work

Verify several adapter calls participate in one supplied transaction/session and do not commit independently.

Cases:

- all operations succeed;
- later failure rolls all back;
- resource/session cleanup occurs.

Do not test remote provider calls inside database transactions unless that architecture is explicitly accepted.

## Query Semantics

Test:

- exact criteria;
- tenant scoping;
- absence;
- multiple matches;
- stable ordering;
- tie-breaker;
- pagination;
- cursor/offset behavior;
- archived/deleted filtering;
- empty page.

Never rely on implicit database row order.

## Pagination

Verify:

- first page;
- next page;
- empty page;
- limit boundaries;
- stable tie-breaker;
- no duplicates across pages;
- cursor opacity if public;
- invalid cursor behavior.

Test concurrent insertion effects only when the contract defines consistency expectations.

## Deletion and Archival

Test exact semantics:

- hard delete;
- soft delete;
- archive;
- deactivate;
- idempotent delete;
- not-found delete;
- query visibility;
- retention metadata.

Do not infer hard delete from a method named `delete`.

## Technical Failure Translation

Where feasible, provoke or simulate at the real boundary:

- database unavailable;
- timeout;
- unique violation;
- serialization conflict;
- deadlock;
- invalid transaction;
- connection closed.

Verify mapping to accepted inward meanings.

Do not assert raw SQLSTATE, ORM exception class, or connection text as the public outcome.

A narrow driver/ORM fault injection may be used only to provoke the actual adapter translation path.

## ORM/Driver Assertions

Assertions may inspect raw persistence only for adapter-specific technical behavior:

- row count;
- exact stored precision;
- index/constraint effect;
- soft-delete column;
- version field;
- migration result.

The main contract assertion must remain Domain/inward behavior.

Do not expose ORM rows through the repository just to simplify tests.

## Cleanup

Tests must clean:

- records;
- schemas/databases;
- transactions;
- connections;
- containers;
- cursors/sessions;
- temporary files if persistence uses them.

Cleanup requirements:

- runs after success and failure;
- is idempotent;
- does not hide the primary test failure;
- closes open handles;
- supports parallel execution.

## Reset Strategies

Possible strategies:

```text
transaction rollback per test
truncate/reset tables
fresh schema per test/suite
fresh container per suite
fresh database per worker
```

Choose based on:

- transaction behavior under test;
- parallelism;
- migration cost;
- isolation;
- database capabilities.

Do not use transaction rollback for tests that specifically need independent transaction commits.

## Parallelism

Define:

- worker-specific namespace;
- connection limits;
- container reuse;
- cleanup ownership;
- serialization of migration tests;
- concurrency-test isolation.

If the suite cannot run in parallel safely, mark and configure it explicitly rather than accepting random collisions.

## Deterministic Data

Use:

- explicit IDs;
- fixed timestamps;
- exact Money values;
- explicit ordering positions;
- unique test namespace;
- stable seeds.

Do not use uncontrolled current time or random data when assertions depend on it.

## Test Harness Helpers

Useful helpers may include:

- database/container bootstrap;
- migration runner;
- namespace generator;
- reset/cleanup;
- low-level malformed-record insertion;
- transaction helper;
- barrier for concurrency tests.

Helpers must not hide:

- which database is used;
- when migrations run;
- transaction boundaries;
- cleanup failures;
- real adapter construction.

## Potential Scripts

Roadmap-compatible optional scripts:

```text
scripts/start-test-database
scripts/apply-test-migrations
scripts/reset-test-database
scripts/generate-test-namespace
scripts/run-repository-integration-tests
```

Use repository-native language/tooling.

Do not introduce scripts when existing commands already solve the problem.

## Test Naming

Preferred:

```text
saves and reconstitutes a Promotion with ordered conditions
returns null when the Promotion does not exist
rejects concurrent duplicate subscription-campaign inserts
rolls back both writes when the outer transaction fails
reports incompatible stored status without defaulting it
```

Avoid:

```text
database works
save called
prisma test
```

## Test Execution

Run:

1. migration/bootstrap check;
2. focused adapter integration test;
3. shared repository contract suite;
4. relevant migration/schema tests;
5. relevant broader integration suite;
6. cleanup/handle verification;
7. typecheck/lint according to scope.

Record exact commands and real outcomes.

## Failure Classification

Use:

```text
PRODUCT_FAILURE
TEST_FAILURE
MIGRATION_PRODUCT_FAILURE
DATABASE_ENVIRONMENT_BLOCKED
CREDENTIALS_BLOCKED
NETWORK_BLOCKED
TEST_SETUP_FAILURE
CLEANUP_FAILURE
FLAKY_TEST
TOOLING_BLOCKED
UNAVAILABLE_TEST_CAPABILITY
```

Do not convert infrastructure unavailability into a passing test.

## Flakiness

Investigate:

- shared rows;
- schema collisions;
- implicit ordering;
- real time;
- unclosed transactions;
- leaked clients;
- race timing;
- container readiness;
- migration races.

Use explicit readiness checks and barriers.

Do not add arbitrary sleeps as the primary fix.

## Boundary Audit

Tests and adapters must not cause inner layers to import:

- ORM models;
- database clients;
- generated persistence types;
- migration tooling;
- technical exceptions.

The test may import Infrastructure because Infrastructure is the subject.

The repository result must remain Domain-oriented.

## Readiness Decision

Use one:

```text
REPOSITORY_ADAPTER_TESTS_COMPLETE
REPOSITORY_ADAPTER_TESTS_COMPLETE_WITH_CONDITIONS
MORE_ADAPTER_CASES_REQUIRED
RETURN_TO_ADAPTER_IMPLEMENTATION
RETURN_TO_REPOSITORY_DESIGN
MIGRATION_REPAIR_REQUIRED
TEST_HARNESS_REPAIR_REQUIRED
REAL_PERSISTENCE_BLOCKED
BLOCKED
```

## Output

Use `assets/repository-adapter-testing-record.md`.

## Completion Criteria

- [ ] Real isolated persistence is used.
- [ ] Target environment is confirmed safe for destructive tests.
- [ ] Authoritative migrations apply reproducibly.
- [ ] Shared repository contract tests pass against the real adapter.
- [ ] Domain round trips and reconstitution are verified.
- [ ] IDs, Value Objects, enums, dates, Money, collections, and nullability are mapped correctly.
- [ ] Save/update/upsert semantics match the port.
- [ ] Real unique constraints and duplicate translation are tested.
- [ ] Transaction and concurrency behavior are tested where applicable.
- [ ] Query ordering, pagination, and deletion/archive semantics are explicit.
- [ ] Invalid stored data is not silently coerced.
- [ ] Technical failures translate safely.
- [ ] Cleanup is deterministic and closes all resources.
- [ ] Parallel isolation is defined.
- [ ] Exact commands and failures are recorded honestly.
- [ ] Mocks or InMemory tests are not presented as real persistence proof.
- [ ] No ORM/database type leaks into inward contracts.

## References

- Read `references/real-persistence-and-isolation.md` first.
- Read `references/migrations-and-test-bootstrap.md` for schema setup.
- Read `references/round-trips-mapping-and-invalid-data.md` for Domain mapping.
- Read `references/constraints-transactions-and-concurrency.md` for authoritative writes.
- Read `references/queries-pagination-and-deletion.md` for read semantics.
- Read `references/failures-cleanup-and-flakiness.md` for operational reliability.
- Read `references/repository-test-audit.md` before completion.
