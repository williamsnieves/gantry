---
name: planning-backend-vertical-slices
description: Portable engineering capability `planning-backend-vertical-slices`. Use
  when the harness or a specialist agent explicitly requires this named capability.
---
# Planning Backend Vertical Slices

## Purpose

Transform a ready backend change into an implementation plan organized by observable business behavior rather than by technical folders or infrastructure components.

Each slice should deliver one coherent behavior through the necessary layers:

```text
Domain
→ Application
→ Ports
→ Infrastructure
→ HTTP or delivery boundary
→ Validation
```

The plan follows inside-out development per behavior. It does not require completing an entire Domain or module before exposing the first useful endpoint.

## Use When

- The backend change is accepted and ready for implementation planning.
- `applying-backend-engineering-standard` has identified applicable rules.
- A feature, bug fix, refactor, migration, contract, or reliability change must be decomposed into implementable backend behaviors.
- A task list is currently organized by technical layer, such as “create entity, create repository, create controller.”
- Multiple Domain, Application, Infrastructure, and test changes must be sequenced coherently.
- The user asks for backend vertical slices, inside-out order, implementation sequencing, or behavior-level tasks.

## Do Not Use When

- Accepted behavior or scope is materially unresolved.
- Backend applicability and project policies have not been established.
- The request is to implement code.
- The request is only to model one Entity, Value Object, Use Case, adapter, or controller in detail.
- The change is genuinely infrastructure-only and has no user/system behavior to slice.
- The requested plan would invent missing business rules or speculative capabilities.
- The plan would create modules or abstractions without a behavior that requires them.

## Inputs

- Accepted specification or OpenSpec change.
- Backend Rule Applicability Report.
- Existing backend topology and project policies.
- Relevant current code and tests.
- Public contract, data, migration, provider, security, reliability, and operational constraints.
- Existing task plan, if one must be corrected.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted change completely.
3. Read the Backend Rule Applicability Report.
4. Inspect the affected backend capability and surrounding code.
5. Identify current Domain, Application, Infrastructure, delivery, and composition boundaries.
6. Inspect existing tests and test infrastructure.
7. Identify public contracts, data migrations, providers, and rollout constraints.
8. Preserve accepted exclusions.
9. Do not infer missing behavior from preferred architecture.

## Outputs

- Vertical behavior inventory.
- Slice boundaries and observable outcomes.
- Per-slice Domain, Application, port, adapter, HTTP, composition, and test work.
- Inside-out implementation order.
- Dependencies between slices.
- Cross-cutting prerequisites and migrations.
- Recommended follow-up backend skills.
- Unresolved business or architecture questions.
- Planning readiness decision.

## Core Principle

Plan by behavior:

```text
Apply a valid promotion
Reject an expired promotion
Prevent duplicate application
Reject an unauthorized caller
```

Do not plan primarily by layer:

```text
Create entity
Create repository
Create service
Create controller
Write tests
```

Layer tasks are valid only inside a behavior slice.

## Workflow

1. **Confirm readiness:** Verify accepted behavior, applicability report, policies, scope, and unresolved decisions.
2. **Inventory observable behaviors:** Extract success, failure, permission, boundary, compatibility, and operational behaviors.
3. **Group behaviors into slices:** Create the smallest coherent independently verifiable units.
4. **Identify the first walking skeleton:** Choose the simplest meaningful end-to-end behavior.
5. **Map each slice across layers:** Domain, Application, ports, adapters, delivery, composition, and tests.
6. **Define inside-out order:** Start at the innermost affected behavior and move outward.
7. **Map TDD cases:** Use Reason → Red → Green → Refactor → Re-evaluate per relevant layer.
8. **Identify dependencies:** Shared prerequisites, contract sequencing, migrations, feature flags, and provider constraints.
9. **Separate cross-cutting work:** Only when genuinely shared across multiple slices.
10. **Check vertical completeness:** Ensure every slice reaches an observable or independently verifiable outcome.
11. **Check proportionality:** Avoid unnecessary modules, entities, ports, or abstractions.
12. **Route to focused skills:** Select the detailed skills needed by each slice.
13. **Report readiness:** Ready, ready with conditions, return to specification, decision required, or blocked.
14. **Report:** Use the backend vertical slice plan asset.

## Behavior Inventory

Extract behaviors from:

- acceptance criteria;
- scenarios;
- error semantics;
- permissions;
- state transitions;
- duplicate/retry behavior;
- public contracts;
- data compatibility;
- migration and rollout;
- observability and recovery.

Classify each behavior:

```text
HAPPY_PATH
BUSINESS_REJECTION
AUTHORIZATION
VALIDATION
NOT_FOUND
CONFLICT
IDEMPOTENCY
CONCURRENCY
EXTERNAL_FAILURE
DATA_MIGRATION
COMPATIBILITY
OBSERVABILITY
CLEANUP
```

Do not create a separate slice for every trivial validation branch when several branches belong to one coherent behavior.

## Slice Quality Criteria

A good slice:

- has one clear observable outcome;
- is small enough to implement and validate coherently;
- crosses only the layers it needs;
- can be tested independently;
- creates usable progress;
- minimizes speculative dependencies;
- preserves capability ownership;
- exposes unresolved decisions early.

A poor slice:

- is only “create database table”;
- is only “add controller”;
- spans unrelated behaviors;
- depends on every other slice before any result can be verified;
- creates ports or abstractions without a consumer;
- hides security, migration, or failure behavior until the end.

## Walking Skeleton

The first slice should be the simplest meaningful vertical path.

It should establish only the minimum required:

- Domain behavior, if any;
- one Use Case intention;
- necessary port;
- minimal adapter path;
- one delivery path;
- composition;
- focused evidence.

It should not attempt every error, provider, migration, or optimization in the first slice unless those are inseparable from correctness.

## Inside-Out Order

Default per slice:

```text
0. Reason about cases
1. Domain behavior and tests
2. Application Use Case and tests
3. Port contracts
4. Repository/external adapters and realistic integration
5. HTTP/event/job boundary
6. Composition and startup
7. Contract/E2E validation
8. Re-evaluate the slice
```

Skip a layer when the behavior does not need it.

### Infrastructure-Only Exception

Starting from Infrastructure is acceptable only when:

- the change is genuinely infrastructure-only;
- no new business behavior is introduced;
- the reason is explicit;
- verification remains complete.

Examples:

- rotating a database driver with unchanged behavior;
- updating generated infrastructure configuration;
- replacing an observability exporter.

## TDD Mapping

For each layer, plan:

```text
Reason
→ enumerate relevant cases
→ choose simplest meaningful case

Red
→ define one failing test

Green
→ minimum behavior

Refactor
→ improve design while green

Re-evaluate
→ choose next case or move outward
```

Do not create one giant task called “write tests.”

Map test level to the behavior and boundary:

- Domain unit test;
- Use Case test;
- repository/provider integration;
- HTTP/contract test;
- critical E2E;
- migration or operational verification.

## Layer Mapping

### Domain

Include only when behavior requires:

- identity;
- invariant;
- lifecycle;
- value semantics;
- pure domain policy;
- repository need expressed inward.

### Application

Include:

- one user/system intention;
- orchestration;
- ports;
- input/output DTOs;
- transaction or collaboration boundary.

### Infrastructure

Include only concrete needs:

- database mapping;
- provider SDK;
- HTTP transport;
- event publishing;
- cache;
- clock/randomness;
- configuration;
- migrations.

### Delivery Boundary

Include:

- HTTP controller;
- event consumer;
- background job;
- CLI or scheduler;
- public package API.

### Composition

Include:

- concrete construction;
- dependency wiring;
- lifecycle/configuration;
- startup smoke validation.

## Ports and Adapters

Create a port only when an inner behavior needs an external capability.

Record:

- owning inner layer;
- intention expressed by the port;
- required operations;
- error semantics;
- adapter candidates;
- integration environment.

Do not create one generic repository or provider port “for future use.”

## Dependencies Between Slices

Use explicit dependency types:

```text
BEHAVIOR_DEPENDENCY
CONTRACT_DEPENDENCY
DATA_DEPENDENCY
MIGRATION_DEPENDENCY
INFRASTRUCTURE_DEPENDENCY
ROLLOUT_DEPENDENCY
SECURITY_DEPENDENCY
NONE
```

Prefer slices that can proceed independently.

When one slice changes a public contract or data representation, sequence consumer and migration work explicitly.

## Cross-Cutting Work

Create a cross-cutting prerequisite only when multiple slices genuinely share it.

Examples:

- accepted public contract schema;
- migration foundation;
- idempotency storage mechanism;
- authorization policy;
- shared observability field.

Do not use “shared setup” as a bucket for miscellaneous technical tasks.

## Bug Fix Planning

For a defect:

1. define the incorrect observable behavior;
2. add a characterization or failing regression case;
3. locate the owning layer;
4. create the smallest vertical correction;
5. validate affected outward boundaries;
6. avoid unrelated refactoring.

## Refactor Planning

A refactor slice must preserve behavior.

Plan:

- characterization evidence;
- one seam or boundary at a time;
- target dependency direction;
- migration of callers;
- removal of obsolete code;
- architecture validation.

Do not mix broad behavioral changes into the same refactor slice.

## Migration Planning

Plan stages explicitly:

```text
prepare
→ dual-read/write or compatibility
→ migrate/backfill
→ switch
→ verify
→ cleanup
```

Each stage must define:

- readers and writers;
- compatibility;
- rollback/recovery;
- validation;
- observability;
- destructive-step approval.

## Slice Template

For every slice record:

```text
ID
Behavior
Observable outcome
Preconditions
Affected layers
Domain work
Application work
Ports
Adapters
Delivery boundary
Composition
Tests/evidence
Dependencies
Risks
Follow-up skills
Definition of done
```

## Recommended Skill Routing

Examples:

```text
Entity lifecycle/invariant
→ modeling-domain-entities

Value semantics
→ modeling-domain-value-objects

Pure cross-entity policy
→ designing-domain-services

Persistence need
→ designing-domain-repositories
→ implementing-repository-adapters

Use Case intention
→ designing-application-use-cases
→ designing-application-dtos

Provider capability
→ designing-external-service-ports
→ implementing-external-service-adapters

HTTP delivery
→ implementing-http-controllers

Wiring
→ wiring-backend-composition

Full execution
→ implementing-backend-inside-out
```

A slice may route to several skills, but only those triggered by its behavior.

## Unresolved Questions

Stop or mark a condition when planning requires an unaccepted decision about:

- business rule;
- capability ownership;
- public contract;
- identifier policy;
- transaction boundary;
- authorization ownership;
- idempotency strategy;
- migration;
- provider fallback;
- error semantics;
- rollout.

Do not bury unresolved decisions inside implementation tasks.

## Readiness Decision

Use one:

```text
READY_FOR_SLICE_IMPLEMENTATION
READY_WITH_CONDITIONS
RETURN_TO_SPECIFICATION
DECISION_REQUIRED
BLOCKED
INFRASTRUCTURE_ONLY_PLAN
```

## Output

Use `assets/backend-vertical-slice-plan.md`.

## Completion Criteria

- [ ] Ready change and applicability report confirmed.
- [ ] Observable behaviors inventoried.
- [ ] Behaviors grouped into coherent vertical slices.
- [ ] Walking skeleton selected.
- [ ] Each slice mapped only to required layers.
- [ ] Inside-out implementation order defined.
- [ ] TDD cases and test levels mapped.
- [ ] Ports and adapters justified by inner needs.
- [ ] Dependencies, migrations, and rollout sequencing explicit.
- [ ] Cross-cutting work kept minimal.
- [ ] Follow-up skills selected per slice.
- [ ] Unresolved decisions surfaced.
- [ ] No code, business rules, or unnecessary modules invented.

## References

- Read `references/readiness-and-behavior-inventory.md` first.
- Read `references/slice-design-and-walking-skeleton.md` to form slices.
- Read `references/inside-out-and-tdd-order.md` to sequence implementation.
- Read `references/layer-port-adapter-mapping.md` for layer responsibilities.
- Read `references/dependencies-migrations-and-rollout.md` when sequencing complex changes.
- Read `references/bugfix-refactor-and-infrastructure-only.md` for non-feature work.
- Read `references/slice-quality-and-readiness.md` before completion.
