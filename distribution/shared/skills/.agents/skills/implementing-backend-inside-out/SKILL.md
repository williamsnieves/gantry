---
name: implementing-backend-inside-out
description: Orchestrates implementation of one ready backend vertical behavior from Domain outward through Application, adapters, HTTP, testing, and architecture validation. Use after backend rule application and vertical-slice planning have produced a ready behavior. Route each layer to the focused modeling, implementation, TDD, testing, composition, and validation skills; preserve one behavior at a time; move outward only when the current inner contract is sufficiently proven; and stop when a material product, architecture, transaction, migration, security, or external-provider decision is missing. This skill coordinates work and evidence; it does not replace the focused skills or invent missing requirements.
...
---

# Implementing Backend Inside-Out

## Purpose

Implement one ready backend vertical behavior from the core outward.

Mandatory implementation direction:

```text
Domain
→ Application Use Case
→ Repository / External Adapters
→ HTTP
→ Composition
→ Validation
```

Default development rhythm inside each applicable layer:

```text
Reason
→ Red
→ Green
→ Refactor
→ Re-evaluate
```

This is an orchestration skill.

It selects and sequences focused skills, maintains the vertical-behavior state, checks readiness between layers, and produces one consolidated implementation record.

It must not replace the detailed work of:

- Domain modeling skills;
- Application design skills;
- adapter implementation skills;
- HTTP implementation;
- composition;
- focused testing;
- architecture validation.

## Use When

- `applying-backend-engineering-standard` has accepted the change.
- `planning-backend-vertical-slices` has produced a ready vertical behavior.
- The behavior introduces or changes backend business behavior.
- Several backend layers must be implemented coherently.
- The team needs explicit layer gates and evidence before moving outward.
- A regression spans Domain, Application, Infrastructure, and HTTP.
- A brownfield slice can be migrated incrementally while preserving behavior.
- An agent must know which focused skill to invoke next.

## Do Not Use When

- The change is not ready for backend planning.
- Acceptance criteria or ownership are materially unresolved.
- The task is purely Infrastructure and introduces no business behavior.
- The request is only to model one Entity, implement one adapter, or run one test suite.
- The task is a broad module rewrite rather than one vertical behavior.
- The goal is to bypass focused skills and generate all layers at once.
- A decision is missing and the proposed solution would be speculative.
- The current layer has unresolved failing tests or architecture violations that block outward movement.

## Inputs

- Backend change classification and selected rules.
- Ready vertical-slice plan.
- One selected vertical behavior.
- Acceptance criteria and error semantics.
- Repository topology and local `AGENTS.md`.
- Existing Domain, Application, Infrastructure, HTTP, and composition code.
- Migration and compatibility requirements.
- Test commands and environment capabilities.
- Relevant implementation and validation records from focused skills.
- Accepted decisions and exceptions.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the backend rule-application report.
3. Read the vertical-slice plan.
4. Select exactly one ready behavior.
5. Confirm:
   - accepted input and output;
   - invariants;
   - error semantics;
   - authorization;
   - persistence needs;
   - external-service needs;
   - transaction and idempotency ownership;
   - HTTP exposure;
   - compatibility/migration constraints.
6. Discover existing tests and commands.
7. Inspect current layer ownership.
8. Identify missing decisions before implementation.
9. Do not broaden the behavior silently.

## Outputs

- One inside-out implementation state record.
- Focused-skill routing for each layer.
- TDD evidence per behavioral case.
- Layer readiness decisions.
- Implemented Domain, Application, adapters, HTTP, and composition changes as applicable.
- Focused test evidence.
- Architecture validation evidence.
- Blocker or decision request when implementation cannot proceed safely.
- Final behavior-level completion decision.

## Core Unit of Work

The unit is one vertical behavior, not an entire module.

Example:

```text
Apply an eligible campaign promotion to one subscription
```

Not:

```text
Build the whole promotions module
```

The behavior may cross every layer while remaining small enough to reason about and verify.

## Primary Workflow

```text
0. Confirm readiness
1. Reason about the behavior
2. Implement Domain
3. Implement Application
4. Implement required ports
5. Implement adapters
6. Implement HTTP
7. Wire composition
8. Run focused and cross-layer validation
9. Validate architecture
10. Re-evaluate completion
```

Each applicable implementation step uses:

```text
Reason
→ Red
→ Green
→ Refactor
→ Re-evaluate
```

## Stage 0 — Confirm Readiness

Before coding, verify the behavior has:

- stable acceptance criteria;
- a clear owning capability;
- defined actor/tenant context;
- input and output semantics;
- known invariants;
- known success and failure meanings;
- known persistence/external dependencies;
- known migration or compatibility constraints;
- a testable completion condition.

Use one:

```text
READY_FOR_INSIDE_OUT_IMPLEMENTATION
READY_WITH_CONDITIONS
RETURN_TO_VERTICAL_SLICE_PLANNING
RETURN_TO_SPECIFICATION
ARCHITECTURE_DECISION_REQUIRED
PRODUCT_DECISION_REQUIRED
BLOCKED
```

Do not proceed under `RETURN_*`, `*_DECISION_REQUIRED`, or `BLOCKED`.

## Stage 1 — Reason About the Behavior

Create a behavior map:

```text
Trigger
→ Domain decision/change
→ Application orchestration
→ persistence/external effects
→ delivery response
```

Enumerate cases:

- simplest success;
- Domain rejection;
- missing state;
- authorization;
- duplicate/conflict;
- persistence failure;
- external failure;
- idempotent replay;
- transport validation;
- migration/compatibility edge.

Select exactly one active case for the current TDD cycle.

Do not implement the whole matrix simultaneously.

## Stage 2 — Domain

Determine whether the behavior requires:

- Entity change;
- Value Object;
- Domain Service;
- Domain error/result;
- repository port change.

Route to:

```text
modeling-domain-entities
modeling-domain-value-objects
designing-domain-services
designing-domain-repositories
testing-domain-models
practicing-backend-tdd
```

### Domain Gate

Move outward only when the current Domain behavior:

- is expressed through public intent-revealing APIs;
- protects invariants;
- has deterministic pure tests;
- has no Infrastructure dependency;
- has no unresolved Domain decision;
- is sufficiently complete for the selected behavior.

Use:

```text
DOMAIN_READY_FOR_APPLICATION
DOMAIN_READY_WITH_CONDITIONS
MORE_DOMAIN_CASES_REQUIRED
RETURN_TO_DOMAIN_MODELING
RETURN_TO_SPECIFICATION
BLOCKED
```

## Stage 3 — Application

Design or update:

- one Use Case intention;
- Request DTO;
- Response DTO or `void`;
- repository dependencies;
- external-service ports;
- authorization;
- transaction, idempotency, and side-effect ordering.

Route to:

```text
designing-application-use-cases
designing-application-dtos
designing-external-service-ports
testing-application-use-cases
practicing-backend-tdd
```

Use real Domain objects, InMemory repositories, and explicit external-port doubles in tests.

### Application Gate

Move outward only when:

- one intention is explicit;
- primitive input becomes Domain types;
- Domain rules are delegated inward;
- ports are provider-neutral;
- output is DTO or `void`;
- semantic failures are stable;
- tests prove state and outcome;
- no concrete adapter, HTTP, SDK, ORM, or composition dependency exists.

Use:

```text
APPLICATION_READY_FOR_ADAPTERS
APPLICATION_READY_WITH_CONDITIONS
MORE_APPLICATION_CASES_REQUIRED
RETURN_TO_USE_CASE_DESIGN
RETURN_TO_PORT_DESIGN
RETURN_TO_DOMAIN
BLOCKED
```

## Stage 4 — Ports

Repository ports belong to Domain.

External-service ports belong to Application.

Confirm each port is required by the selected Use Case.

Avoid speculative CRUD or generic provider clients.

Ports must define:

- operation semantics;
- absence/conflict behavior;
- success/failure meaning;
- transaction ownership;
- idempotency or async behavior where relevant;
- testing double expectations.

Do not create a port merely to wrap a library.

## Stage 5 — Repository Adapters

When persistence is required, route to:

```text
implementing-repository-adapters
testing-repository-adapters
practicing-backend-tdd
```

Implement:

- persistence mapping;
- Domain reconstitution;
- save/query semantics;
- constraints;
- transactions;
- error translation;
- migrations and compatibility.

### Repository Gate

Require:

- shared contract parity;
- real isolated persistence evidence;
- authoritative migrations;
- round-trip mapping;
- required constraints and concurrency behavior;
- deterministic cleanup;
- no ORM/database leakage inward.

Use:

```text
REPOSITORY_ADAPTER_READY
REPOSITORY_ADAPTER_READY_WITH_CONDITIONS
MIGRATION_DECISION_REQUIRED
TRANSACTION_DECISION_REQUIRED
REAL_PERSISTENCE_BLOCKED
RETURN_TO_REPOSITORY_DESIGN
BLOCKED
```

## Stage 6 — External-Service Adapters

When an external capability is required, route to:

```text
implementing-external-service-adapters
testing-external-service-adapters
practicing-backend-tdd
```

Implement:

- provider request/response mapping;
- semantic failures;
- credentials and tenant selection;
- timeout;
- retry;
- rate limit;
- idempotency;
- ambiguous outcomes;
- reconciliation;
- client lifecycle and redaction.

### External Adapter Gate

Require:

- no SDK/provider leakage inward;
- safe credential strategy;
- strongest safe evidence level;
- accepted retry/idempotency behavior;
- honest sandbox/environment classification;
- cleanup and residual uncertainty recorded.

Use:

```text
EXTERNAL_ADAPTER_READY
EXTERNAL_ADAPTER_READY_WITH_CONDITIONS
TEST_CREDENTIALS_REQUIRED
PROVIDER_ENVIRONMENT_BLOCKED
RESILIENCE_DECISION_REQUIRED
RETURN_TO_EXTERNAL_PORT_DESIGN
BLOCKED
```

## Adapter Ordering

Repository and external adapters may be implemented in either order after Application ports are stable.

Choose based on the active case and risk.

Do not implement HTTP before the required Application contract and adapter path are sufficiently proven.

## Stage 7 — HTTP

Route to:

```text
implementing-http-controllers
testing-backend-http-e2e
practicing-backend-tdd
```

Implement:

- accepted route and method;
- transport validation;
- trusted authentication context;
- Request DTO mapping;
- one Use Case invocation;
- status/body/header mapping;
- semantic error translation;
- safe unknown error.

### HTTP Gate

Require:

- controller is thin;
- no repository/provider access;
- no Domain business logic;
- no Entity response;
- public contract tests pass;
- representative real-HTTP E2E passes or is honestly blocked;
- technical details do not leak.

Use:

```text
HTTP_READY_FOR_COMPOSITION
HTTP_READY_WITH_CONDITIONS
MORE_HTTP_CONTRACT_CASES_REQUIRED
RETURN_TO_CONTROLLER_IMPLEMENTATION
RETURN_TO_APPLICATION
HTTP_ENVIRONMENT_BLOCKED
BLOCKED
```

## Stage 8 — Composition

Route to:

```text
wiring-backend-composition
```

Wire:

- concrete repository adapters;
- concrete external adapters;
- Use Cases;
- controllers;
- configuration;
- startup/shutdown;
- test reset.

Current policy:

```text
get*    → cached shared Infrastructure
create* → fresh transient Use Case
```

No runtime DI container or Service Locator.

### Composition Gate

Require:

- concrete selection centralized;
- configuration validated;
- shared/transient lifecycle correct;
- controller receives Use Case;
- Domain/Application do not import composition;
- startup, shutdown, and reset are deterministic;
- composition tests pass.

Use:

```text
COMPOSITION_READY_FOR_VALIDATION
COMPOSITION_READY_WITH_CONDITIONS
CONFIGURATION_DECISION_REQUIRED
LIFECYCLE_DECISION_REQUIRED
RETURN_TO_ADAPTER_OR_CONTROLLER
BLOCKED
```

## Stage 9 — Focused Validation

Execute applicable evidence:

```text
Domain unit tests
Application Use Case tests
repository adapter integration tests
external adapter integration/contract tests
HTTP E2E
typecheck
lint
format check
build
```

Use focused commands first, then proportionate broader checks.

Do not claim unexecuted checks passed.

Classify blocked external or database capabilities honestly.

## Stage 10 — Architecture Validation

Route to:

```text
validating-backend-architecture
```

Validate:

- `Infrastructure → Application → Domain`;
- module/public-contract boundaries;
- repository/external adapter isolation;
- controller thinness;
- no Use Case chaining;
- DTO/Domain separation;
- composition-root isolation;
- no Service Locator;
- test-boundary correctness;
- cycles and transitive leaks.

Architecture violations block completion unless they are accepted documented exceptions.

## TDD Integration

For every behavioral case:

```text
Reason
→ Red
→ Green
→ Refactor
→ Re-evaluate
```

The orchestration record links to the focused TDD record.

Do not keep several active TDD cases across different layers without an explicit reason.

Normally finish the current inner-layer case before moving outward.

## Case Propagation Across Layers

The same behavior should remain traceable.

Example:

```text
Domain case:
eligible Promotion can be applied

Application case:
ApplyPromotionUseCase loads, authorizes, applies, and persists

Adapter case:
Promotion repository round-trips applied state

HTTP case:
POST promotion endpoint returns 201 and durable state
```

Each layer proves its own boundary.

Do not copy all Domain permutations into HTTP E2E.

## Moving Outward

Move outward when the inner contract is sufficiently proven for the selected vertical behavior.

This does not require completing the entire module.

Example:

```text
one accepted Promotion.apply behavior
→ one ApplyPromotion Use Case
→ required adapters
→ one HTTP endpoint
```

Pending unrelated module cases remain separate slices or later TDD cases.

## Infrastructure-Only Exception

Starting from Infrastructure or HTTP is acceptable only when:

- no new business behavior exists;
- the change is genuinely technical;
- the reason is explicit;
- affected contracts are already stable;
- validation remains complete.

Examples:

- database driver upgrade;
- telemetry exporter change;
- HTTP framework security patch;
- generated client regeneration.

Do not classify a new endpoint, persistence rule, provider behavior, or lifecycle decision as infrastructure-only.

## Brownfield Adaptation

For existing coupled code:

```text
characterize current behavior
→ establish safe seam
→ implement inner contract
→ introduce port
→ implement adapter
→ redirect one caller
→ validate
→ remove obsolete path when safe
```

Use accepted temporary compatibility seams.

Do not require a full architecture rewrite.

Route broader migration design to:

```text
adapting-backend-rules-to-existing-code
```

## Migration Behavior

When the vertical behavior changes persisted data or public contracts, include stages such as:

```text
prepare
→ compatibility
→ migrate/backfill
→ switch
→ verify
→ cleanup
```

Stop for a missing migration decision.

Do not hide schema or data compatibility inside adapter code.

## Transactions

Transaction ownership must be explicit before implementation.

Possible owners:

- one repository adapter atomic method;
- Application Unit of Work;
- database transaction passed through ports;
- asynchronous process/saga.

Do not hold a database transaction across a remote provider call unless explicitly accepted.

Stop when partial-failure semantics are unresolved.

## Side-Effect Ordering

Define ordering before implementation.

Example:

```text
authorize
→ evaluate Domain
→ call provider
→ persist accepted result
```

or:

```text
persist pending state
→ call provider
→ reconcile final state
```

The correct order depends on accepted failure and recovery semantics.

Do not invent it.

## Idempotency

Trace idempotency from public boundary to authoritative protection:

```text
HTTP idempotency key
→ Application Request
→ external port / persistence mechanism
→ replay result
```

Verify:

- key ownership;
- same-key propagation;
- duplicate semantics;
- authoritative constraint or provider mechanism;
- ambiguous outcome reconciliation;
- one durable effect.

## Authorization and Tenancy

Trace trusted context:

```text
authentication
→ controller
→ Request DTO
→ Use Case authorization
→ tenant-scoped repositories/providers
```

Do not trust body fields for identities that must come from authentication.

Stop if tenant ownership or cross-tenant behavior is unresolved.

## Security and Privacy

At each layer ask:

- what data enters;
- what data leaves;
- what is persisted;
- what is sent externally;
- what may be logged;
- what must be redacted;
- what tenant/account/region applies;
- what secrets are used;
- what public errors are safe.

A security-sensitive missing decision blocks outward movement.

## Observability

Add observability at the owning outer layer without leaking technical dependencies inward.

Trace:

- semantic operation;
- correlation;
- safe actor/tenant;
- outcome;
- latency;
- retry;
- external reference;
- failure classification.

Do not inject Infrastructure loggers into Domain by default.

## Decision Stops

Stop immediately when a material decision is missing.

Examples:

```text
PRODUCT_DECISION_REQUIRED
DOMAIN_INVARIANT_DECISION_REQUIRED
AUTHORIZATION_DECISION_REQUIRED
TRANSACTION_DECISION_REQUIRED
MIGRATION_DECISION_REQUIRED
IDEMPOTENCY_DECISION_REQUIRED
EXTERNAL_PROVIDER_DECISION_REQUIRED
ERROR_CONTRACT_DECISION_REQUIRED
SECURITY_DECISION_REQUIRED
COMPATIBILITY_DECISION_REQUIRED
```

The stop record must contain:

- exact question;
- why implementation depends on it;
- options supported by current evidence;
- consequences;
- recommended decision owner;
- work that can safely continue, if any.

Do not choose silently.

## Failure Handling

Classify execution failures:

```text
PRODUCT_FAILURE
ARCHITECTURE_FAILURE
TEST_FAILURE
DATABASE_ENVIRONMENT_BLOCKED
PROVIDER_ENVIRONMENT_BLOCKED
CREDENTIALS_BLOCKED
TOOLING_BLOCKED
CLEANUP_FAILURE
FLAKY_TEST
```

Environment blockers do not become product failures or passes.

## Scope Control

For the selected behavior, track:

```text
IN_SCOPE
REQUIRED_SUPPORTING_CHANGE
DEFERRED_FOLLOW_UP
OUT_OF_SCOPE
```

A supporting change is allowed only when required to complete the behavior safely.

Do not opportunistically refactor unrelated modules.

## Consolidated Evidence

The final record should reference:

- backend rule application;
- vertical-slice plan;
- Domain implementation/testing;
- Application implementation/testing;
- repository adapter implementation/testing;
- external adapter implementation/testing;
- controller/HTTP E2E;
- composition;
- architecture validation;
- remaining environment evidence.

Do not duplicate every focused report. Summarize and link to it.

## Final Decision

Use one:

```text
VERTICAL_BEHAVIOR_COMPLETE
VERTICAL_BEHAVIOR_COMPLETE_WITH_CONDITIONS
MORE_CASES_REQUIRED_IN_CURRENT_LAYER
RETURN_TO_INNER_LAYER
RETURN_TO_SPECIFICATION
DECISION_REQUIRED
VALIDATION_FAILED
ARCHITECTURE_VIOLATIONS_FOUND
ENVIRONMENT_EVIDENCE_BLOCKED
BLOCKED
```

## Output

Use `assets/backend-inside-out-implementation-record.md`.

## Completion Criteria

- [ ] One ready vertical behavior was selected.
- [ ] Scope and acceptance criteria remained stable.
- [ ] Domain was implemented and tested before outward behavior depended on it.
- [ ] Application Use Case and DTOs were implemented with provider-neutral ports.
- [ ] Required repository and external adapters were implemented and tested at real boundaries.
- [ ] HTTP controller is thin and tested through the real protocol where applicable.
- [ ] Composition selects concrete adapters explicitly and manages lifecycle safely.
- [ ] TDD evidence exists for active behavioral cases.
- [ ] Focused tests and proportionate broader validation were actually executed.
- [ ] Architecture validation found no unaccepted blocking violation.
- [ ] Idempotency, transactions, authorization, migration, and side-effect ordering are explicit when applicable.
- [ ] Environment blockers and residual uncertainty are reported honestly.
- [ ] No missing product or architecture decision was guessed.
- [ ] No unrelated module-wide rewrite or speculative behavior was introduced.
- [ ] Final behavior-level decision is explicit.
