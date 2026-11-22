---
name: designing-domain-repositories
description: Designs domain-oriented repository ports and deterministic InMemory implementations from actual Use Case needs. Use when Application requires persistence access to Entities or aggregate roots and the Domain contract must remain independent from databases, ORM models, DTOs, tables, query builders, or provider terminology. Produces repository responsibility, intention-revealing operations, Domain input/output types, absence and failure semantics, consistency expectations, InMemory behavior, test cases, ownership, and adapter handoff. Do not use to implement real persistence adapters, create generic CRUD interfaces, expose storage models, or invent queries without a consuming behavior.
...
---

# Designing Domain Repositories

## Purpose

Define a repository contract that expresses what the inner layers need from persistence without exposing how data is stored.

A well-designed repository:

- is owned by the Domain or Application side that needs it;
- uses Domain language;
- operates on Entities, aggregate roots, identifiers, and accepted Domain values;
- exposes only queries required by real Use Cases;
- defines absence and persistence-failure semantics;
- preserves aggregate consistency;
- has a deterministic, seedable InMemory implementation;
- can be implemented by Infrastructure without changing the inner contract.

## Use When

- A Use Case must load, save, search, or check the existence of a Domain Entity or aggregate root.
- Persistence needs must become an inward-facing port.
- A repository interface is currently shaped like generic CRUD.
- Storage rows, ORM types, or DTOs are leaking into Domain or Application.
- Use Case tests require a realistic InMemory repository.
- A new query must be justified from an accepted behavior.
- Repository ownership across modules must be clarified.

## Do Not Use When

- The request is to implement PostgreSQL, MongoDB, ORM, filesystem, or provider persistence.
- The operation is external-service collaboration rather than persistence.
- The concept is not a Domain Entity or aggregate root.
- The request is to design HTTP or Application DTOs.
- No accepted Use Case requires the proposed query.
- A generic base repository is requested only for convenience.
- The operation belongs to another capability and should use its public Application surface instead.
- The repository contract would return persistence rows, DTOs, or provider SDK types.

## Inputs

- Accepted specification or OpenSpec change.
- Backend Rule Applicability Report.
- Backend Vertical Slice Plan.
- Relevant Entities, Value Objects, Domain errors, and Use Case needs.
- Existing module boundaries and repository policies.
- Project conventions for absence, errors, transactions, pagination, ordering, and identifiers.
- Existing repository ports and InMemory patterns.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted behavior and relevant vertical slices.
3. Inspect the consuming Use Cases or their design.
4. Inspect the Entity or aggregate root being persisted.
5. Confirm repository ownership and module boundaries.
6. Confirm identifier, error, absence, pagination, ordering, and transaction policies.
7. Inspect existing repository and InMemory conventions.
8. Distinguish persistence needs from external-service collaboration.
9. Do not infer queries from database indexes, screens, or ORM convenience alone.

## Outputs

- Repository suitability and ownership decision.
- Responsibility statement.
- Required operations derived from Use Case needs.
- Domain-oriented signatures.
- Absence, duplicate, conflict, and failure semantics.
- Aggregate consistency and transaction assumptions.
- Query criteria, ordering, pagination, and uniqueness semantics.
- Seedable InMemory implementation design.
- Contract and InMemory test plan.
- Adapter implementation handoff.
- Repository design report.

## Core Principle

Design repositories from inward behavior:

```text
Use Case need
→ repository intention
→ Domain-oriented contract
→ InMemory implementation
→ real Infrastructure adapter
```

Do not design from storage mechanics:

```text
table columns
→ generic CRUD
→ ORM repository methods
→ leak outward
```

## Workflow

1. **Confirm repository suitability:** Verify persistence access is truly required.
2. **Resolve ownership:** Identify the capability and inner layer that owns the port.
3. **Trace consuming behaviors:** Derive every operation from accepted Use Cases.
4. **Define aggregate boundary:** Identify what is loaded and saved as one consistency unit.
5. **Design operation names:** Use Domain and intention-revealing language.
6. **Define signatures:** Use Entities, aggregate roots, IDs, Value Objects, and accepted criteria.
7. **Define semantics:** Absence, duplicates, conflicts, failures, ordering, pagination, and atomicity.
8. **Check module boundaries:** Prevent cross-capability persistence coupling.
9. **Design InMemory implementation:** Deterministic, seedable, contract-faithful, and isolated.
10. **Design tests:** Contract behavior, query semantics, identity, replacement, ordering, and isolation.
11. **Review proportionality:** Avoid unused operations and generic abstractions.
12. **Prepare adapter handoff:** Map every contract obligation to future Infrastructure evidence.
13. **Report:** Use the repository design report.

## Repository Suitability

Use a repository when an inner behavior needs persistence of an Entity or aggregate root.

Possible alternatives:

```text
external provider interaction
→ external-service port

read-only reporting projection
→ query/read-model port according to project architecture

pure Domain calculation
→ Entity, Value Object, or Domain Service

cross-capability action
→ public Application surface of owning capability
```

Do not call every data source a repository.

## Ownership

The port belongs inward.

Typical options:

- Domain owns a repository abstraction when persistence is part of the Domain language and the project adopts that convention.
- Application owns the port when it expresses a Use Case's external need.

Follow the repository's accepted architecture.

Infrastructure implements the port but does not own its contract.

### Cross-Module Rule

A capability must not directly consume another capability's concrete repository.

Prefer:

```text
Capability A Use Case
→ public Application port/surface of Capability B
```

Only share a repository contract when aggregate ownership and consistency boundaries genuinely require it and project policy explicitly supports it.

## Aggregate Boundary

Repositories usually load and save aggregate roots, not arbitrary internal children.

Define:

- root Entity;
- owned child Entities or Value Objects;
- consistency boundary;
- persistence unit;
- allowed partial reads, if any;
- whether direct child repositories are forbidden.

Do not expose internal persistence access that bypasses aggregate invariants.

## Deriving Operations

For each operation, cite the consuming behavior.

Good examples:

```text
findById(id)
findActiveBySubscriptionId(subscriptionId)
existsAppliedPromotion(subscriptionId, campaignId)
save(promotion)
```

Weak examples:

```text
getAll()
create()
update()
delete()
findByField(field, value)
query(filters)
```

Generic CRUD is acceptable only when it exactly matches accepted project convention and real use cases, not by default.

## Operation Names

Use Domain intention, not storage language.

Preferred:

```text
findById
findEligibleFor
existsForSubscriptionAndCampaign
save
removeExpiredBefore
```

Avoid:

```text
selectByPk
insertRow
updateTable
findByColumn
executeQuery
```

## Signatures

Inputs may include:

- Domain IDs;
- Value Objects;
- explicit criteria objects defined inward;
- accepted pagination and ordering objects;
- aggregate roots for save operations.

Outputs may include:

- Entity or aggregate root;
- `null`/`undefined`, Option, or Result according to project policy;
- readonly collections of Domain objects;
- existence boolean;
- accepted Domain query result.

Do not return:

- ORM entities;
- database rows;
- SQL records;
- Application/HTTP DTOs;
- provider SDK objects;
- raw query-builder results.

## Absence Semantics

Choose the established project policy.

Common valid forms:

```text
findById(id): Entity | null
findById(id): Option<Entity>
getById(id): Entity or throws Domain/Application not-found error
```

Do not mix `find` and `get` semantics inconsistently.

Document:

- whether absence is expected or exceptional;
- where not-found translation occurs;
- how InMemory and real adapters behave identically.

## Save Semantics

Define whether `save`:

- inserts or replaces by identity;
- supports both creation and update;
- enforces optimistic versioning;
- returns `void`, the saved Entity, or metadata;
- requires transaction context;
- rejects duplicates/conflicts;
- is idempotent for the same aggregate state.

Follow project policy.

Do not return persistence-generated rows merely because the ORM does.

## Query Criteria

When a query needs multiple parameters, prefer an inward criteria object only when it improves clarity and stability.

Criteria must:

- use Domain/Application language;
- be immutable;
- avoid database column names;
- define optional-field semantics;
- define ordering and pagination explicitly;
- avoid becoming a universal query DSL.

Do not introduce generic `filters: Record<string, unknown>`.

## Ordering and Pagination

Define observable semantics:

- stable ordering;
- tie-breakers;
- ascending/descending meaning;
- cursor or offset policy;
- page-size constraints;
- empty result;
- duplicate prevention across pages;
- consistency expectations.

Do not rely on database default ordering.

## Uniqueness and Existence

Existence operations should express the actual invariant.

Preferred:

```text
existsAppliedPromotion(subscriptionId, campaignId)
```

Avoid:

```text
exists(filters)
```

Remember that a pre-check alone may not enforce uniqueness under concurrency.

If uniqueness is authoritative, the design must also require a storage constraint, transaction, lock, or idempotency mechanism in the real adapter/application flow.

The repository port should expose the behavior needed without pretending it alone solves concurrency.

## Errors

Repository ports should not expose database-specific exceptions.

Define accepted categories such as:

```text
PERSISTENCE_UNAVAILABLE
CONFLICT
OPTIMISTIC_LOCK_FAILED
DUPLICATE
UNKNOWN_PERSISTENCE_FAILURE
```

Only expose categories needed by the Application contract.

Do not leak:

- SQLSTATE;
- ORM exception classes;
- driver errors;
- table/constraint names;
- provider response objects.

Infrastructure translates technical failures.

## Transactions

Do not add transaction methods to every repository by default.

Transaction ownership is a project policy and Application concern.

Possible designs:

- one repository operation is atomic;
- Unit of Work/transaction port;
- Application transaction boundary;
- adapter-managed atomic command.

Record:

- operations that must be atomic;
- consistency boundary;
- transaction owner;
- rollback semantics;
- whether multiple repositories participate.

Do not invent a Unit of Work if one repository operation is sufficient.

## Concurrency and Versioning

When relevant, define:

- expected version;
- optimistic lock behavior;
- duplicate/idempotency semantics;
- conflict result;
- retry ownership;
- isolation assumptions.

The port should express Domain/Application meaning rather than database mechanism.

Example:

```text
save(entity, expectedVersion)
→ success or CONCURRENT_MODIFICATION
```

Only if project policy and accepted behavior require versioning.

## Deletion

Prefer Domain semantics:

```text
remove(entity)
archive(id)
deleteExpiredBefore(cutoff)
```

Do not expose hard delete when accepted behavior is archive/deactivate.

Clarify:

- hard versus soft deletion;
- cascade behavior;
- not-found behavior;
- idempotency;
- audit/retention;
- aggregate consistency.

## InMemory Implementation

Every repository port used by Use Case tests should normally have an InMemory implementation when project policy requires it.

It must be:

- deterministic;
- seedable;
- isolated per test;
- faithful to contract semantics;
- based on Domain identity;
- free of ORM/database behavior;
- easy to inspect;
- capable of simulating accepted failures when useful.

### Seedability

Support explicit initial Domain objects.

Example concept:

```text
new InMemoryPromotionRepository([promotionA, promotionB])
```

Do not use hidden global fixtures.

### Identity Behavior

Saving an Entity with an existing identity should follow the documented save semantics.

Do not accidentally duplicate equal identities because object references differ.

### Defensive Isolation

Avoid tests mutating repository state through returned mutable collections or shared arrays.

Return copies or readonly results as appropriate.

### Deterministic Ordering

Match the contract's explicit ordering.

Do not depend on incidental Map or insertion behavior unless that is the documented contract.

### Failure Simulation

Provide controlled failure hooks only when they improve Use Case testing and match accepted failure categories.

Avoid turning the InMemory repository into a mock framework.

## InMemory Is Not a Mock

An InMemory repository is a working implementation of the port.

It should contain real contract behavior:

- identity lookup;
- save/replace semantics;
- queries;
- ordering;
- uniqueness behavior;
- absence semantics.

Mocks may still be used for narrow interaction tests if project policy allows, but they do not replace a required InMemory implementation.

## Contract Tests

Define a shared repository contract test suite when it adds reliable value.

The same behavioral cases may run against:

- InMemory implementation;
- real persistence adapter.

Typical contract cases:

- save and retrieve;
- replace by identity;
- absence;
- query semantics;
- stable ordering;
- pagination;
- duplicate/conflict;
- deletion/archive;
- version conflict;
- mapping round-trip where applicable.

Environment-specific adapter tests may add technical cases.

## Testing

### Port Design Tests

Usually represented through consuming Use Case tests and implementation contract tests rather than testing an interface itself.

### InMemory Tests

Cover:

- seed and retrieval;
- identity equality;
- save/replace;
- absence;
- query criteria;
- ordering;
- pagination;
- duplicates/conflicts;
- deletion semantics;
- state isolation;
- controlled failures.

### Real Adapter Handoff

Require future tests for:

- persistence mapping;
- real constraints;
- transactions;
- concurrency;
- technical error translation;
- migrations/schema compatibility;
- cleanup.

## Read Models and Projections

A reporting or list query may not need full aggregate reconstitution.

Use an explicit read-model/query port when project architecture accepts CQRS or projections.

Do not return Application DTOs from a Domain repository merely for convenience.

Keep write-model repositories focused on aggregate consistency.

## Generic Repository Bases

Do not create generic `Repository<T>` or CRUD base interfaces automatically.

They often:

- expose unused operations;
- erase Domain language;
- encourage cross-module coupling;
- leak storage assumptions;
- make unique queries awkward.

Use a generic base only when the project already adopts it and it preserves Domain-specific contracts.

Domain-specific repositories may extend a narrowly useful shared abstraction only when evidence supports it.

## Evolving Existing Repositories

Signs of a poor contract:

- CRUD-shaped API;
- DTO/ORM outputs;
- table/column terminology;
- broad generic filter;
- methods unused by any Use Case;
- cross-module direct access;
- inconsistent absence semantics.

Incremental recovery:

```text
trace consuming behavior
→ add one Domain-oriented operation
→ add InMemory behavior/tests
→ migrate one Use Case
→ implement adapter operation
→ remove obsolete generic method
```

Avoid big-bang repository rewrites.

## Boundary Guardrails

Repository port must not import:

- Infrastructure;
- ORM;
- database driver;
- HTTP;
- provider SDK;
- persistence schema;
- generated database types.

It may depend on:

- Domain Entities/aggregate roots;
- IDs and Value Objects;
- inward criteria/pagination types;
- accepted Domain/Application errors/results.

The real adapter maps persistence data at the Infrastructure boundary.

## Readiness Decision

Use one:

```text
READY_TO_IMPLEMENT_REPOSITORY_PORT
READY_WITH_CONDITIONS
NOT_A_REPOSITORY
ROUTE_TO_EXTERNAL_SERVICE_PORT
ROUTE_TO_READ_MODEL_PORT
RETURN_TO_USE_CASE_DESIGN
RETURN_TO_SPECIFICATION
DECISION_REQUIRED
BLOCKED
```

## Output

Use `assets/domain-repository-design-report.md`.

## Completion Criteria

- [ ] Persistence need and repository suitability confirmed.
- [ ] Port ownership and aggregate boundary resolved.
- [ ] Every operation traced to an accepted consuming behavior.
- [ ] Names and signatures use Domain language.
- [ ] Inputs/outputs exclude DTO, ORM, row, and provider types.
- [ ] Absence, save, duplicate, conflict, and failure semantics defined.
- [ ] Ordering and pagination are explicit when applicable.
- [ ] Transaction and concurrency expectations are recorded.
- [ ] Cross-module ownership is preserved.
- [ ] Seedable deterministic InMemory implementation designed.
- [ ] InMemory semantics match the real contract.
- [ ] Focused and contract tests planned.
- [ ] Real adapter obligations are handed off explicitly.
- [ ] No generic CRUD, query DSL, or unused operation introduced.
