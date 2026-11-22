---
name: refactoring-backend-toward-hexagonal-architecture
description: Refactors one existing backend behavior incrementally toward modular hexagonal architecture while preserving accepted behavior and public contracts. Use after brownfield profiling has identified a safe migration seam and target state. Protect the current behavior with characterization tests, move business decisions inward, introduce only the required repository or external-service ports, isolate concrete adapters, redirect one caller, validate the new path, and remove obsolete code only when safe. Do not perform a big-bang rewrite, invent a Domain model, change public or data contracts silently, create forwarding abstractions with no boundary value, or migrate several unrelated behaviors at once.
---

# Refactoring Backend Toward Hexagonal Architecture

## Purpose

Move one existing backend behavior toward:

```text
Delivery
→ Application
→ Domain
← ports
← Infrastructure adapters
```

using an incremental, behavior-preserving sequence.

The refactor should:

- preserve accepted public behavior;
- protect current behavior before movement;
- move one responsibility at a time;
- create only meaningful inward boundaries;
- keep production changes reversible;
- avoid unrelated cleanup;
- leave the touched path with no new or worsened architectural drift.

## Relationship to Other Skills

This skill executes a migration plan.

Use before it:

```text
adapting-backend-rules-to-existing-code
→ profiles current and target states
→ identifies seams, compatibility needs, and debt

extracting-domain-model-from-legacy-code
→ discovers candidate invariants and Domain concepts when business logic is unclear
```

Use during it:

```text
practicing-backend-tdd
focused Domain/Application/adapter/HTTP skills
```

Use after it:

```text
validating-backend-change
validating-backend-architecture
reviewing-backend-code
reviewing-backend-architecture
```

## Use When

- A current behavior is implemented in a controller, service, ORM model, job, or provider wrapper.
- A brownfield adaptation record defines a target state and safe seam.
- Characterization evidence can protect the current contract.
- One caller or one behavior can be redirected incrementally.
- Direct ORM or provider access must be isolated behind a port.
- Business rules must move into Domain or Application.
- A legacy path can coexist temporarily with the target path.
- A temporary facade or anti-corruption layer has an explicit exit condition.
- The goal is a focused refactor, not a repository redesign.

## Do Not Use When

- Business invariants are still unknown.
- There is no accepted current or target behavior.
- The task is greenfield implementation.
- The user asks to refactor the entire backend at once.
- Data migration, transaction, idempotency, security, or compatibility semantics are unresolved.
- The proposed seam only adds a forwarding wrapper without improving ownership or testability.
- Several unrelated modules would need to move simultaneously.
- The task is only to review or validate architecture.
- The change is purely mechanical and does not alter an architectural boundary.

## Inputs

- Brownfield adaptation record.
- Current-state and target-state maps.
- Selected behavior and acceptance criteria.
- Characterization tests or characterization plan.
- Safe seam and migration strategy.
- Public API, event, and persisted-data contracts.
- Transaction and side-effect ordering.
- Temporary deviations and debt ledger.
- Repository-local `AGENTS.md`.
- Definitive backend standard.
- Existing implementation and test commands.
- Rollout, rollback, and observability constraints.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the brownfield adaptation record.
3. Read the selected behavior and accepted contract.
4. Trace the current runtime path.
5. Confirm the target path and one migration seam.
6. Inspect current:
   - business decisions;
   - persistence;
   - provider calls;
   - error mapping;
   - transaction boundary;
   - public response/event;
   - test coverage.
7. Confirm current data compatibility and migration decisions.
8. Confirm tenant, authorization, idempotency, and partial-failure semantics.
9. Discover repository-native commands.
10. Do not begin if a material decision is unresolved.

## Outputs

- Refactoring execution plan.
- Current behavior characterization evidence.
- Selected seam and ownership change.
- Incremental code-change sequence.
- Focused TDD records.
- Compatibility and rollout evidence.
- Caller redirection evidence.
- Obsolete-path removal decision.
- Validation evidence.
- Hexagonal refactoring record.

## Core Sequence

```text
characterize current behavior
→ establish a safe seam
→ implement the inner contract
→ introduce the required port
→ implement the adapter
→ redirect one caller
→ validate old and new behavior
→ remove obsolete path when safe
```

## Unit of Refactoring

Refactor one behavior.

Good:

```text
Apply an eligible promotion to a subscription
```

Too broad:

```text
Refactor the promotions module
```

The refactor may touch several layers, but it must retain one behavioral thread.

## Readiness Gate

Use one:

```text
READY_TO_REFACTOR_ONE_BEHAVIOR
READY_WITH_CONDITIONS
CHARACTERIZATION_REQUIRED
DOMAIN_MODEL_EXTRACTION_REQUIRED
TARGET_BOUNDARY_DECISION_REQUIRED
TRANSACTION_DECISION_REQUIRED
DATA_MIGRATION_DECISION_REQUIRED
PUBLIC_COMPATIBILITY_DECISION_REQUIRED
SECURITY_OR_INTEGRITY_BLOCKER
BLOCKED
```

Stop when:

- current behavior cannot be characterized;
- the target ownership is unclear;
- tenant or authorization behavior is unsafe;
- transaction or partial-failure semantics are unresolved;
- legacy data cannot be mapped safely;
- the seam has no stable contract;
- rollback is impossible and the risk is not accepted.

## Stage 1 — Characterize the Current Behavior

Capture the behavior before changing ownership.

Characterize:

- accepted success;
- public response or event;
- state changes;
- authorization and tenant behavior;
- missing/invalid state;
- duplicate and replay behavior;
- persistence order;
- provider calls;
- partial failures;
- known compatibility quirks.

Characterization tests may start green.

They prove preservation, not the new target design.

## Characterization Test Quality

Prefer explicit assertions over oversized snapshots.

Verify observable behavior:

```text
input
→ output
→ durable state
→ external semantic call
```

Avoid locking in:

- internal call order with no contract value;
- private helper behavior;
- accidental framework details;
- known bugs that product intends to fix.

A known bug should have:

- a reproduction test;
- an accepted correction decision;
- a new expected test.

## Stage 2 — Select and Establish the Seam

Use the seam defined by brownfield adaptation, or stop if it is not accepted.

Possible seams:

- controller delegation;
- compatibility facade;
- repository port;
- external-service port;
- data mapper;
- Domain facade;
- transaction wrapper;
- route switch;
- event translator;
- feature-flag router.

A seam must:

- separate current and target ownership;
- expose a stable semantic contract;
- improve testability or dependency direction;
- have one owner;
- have a long-term role or removal condition.

## Bad Seams

Reject:

- `LegacyBridgeService`;
- generic `ServiceAdapter`;
- wrapper that forwards every method unchanged;
- Service Locator;
- compatibility object exposing ORM/SDK types inward;
- facade that duplicates business rules;
- flag branch with no cleanup plan.

## Stage 3 — Move Business Decisions Inward

Identify each decision in the current outer code.

Classify:

```text
DOMAIN_INVARIANT
APPLICATION_ORCHESTRATION
INFRASTRUCTURE_POLICY
DELIVERY_MAPPING
COMPATIBILITY_MAPPING
```

Move:

- invariants and state transitions to Domain;
- orchestration, authorization coordination, transaction policy, and side-effect order to Application;
- provider/database/framework translation to Infrastructure;
- HTTP status/body/header mapping to delivery;
- legacy contract translation to the compatibility seam.

Do not move technical details into Domain merely to reduce controller code.

## Domain Extraction During Refactor

When business concepts are already sufficiently understood, route to:

```text
modeling-domain-entities
modeling-domain-value-objects
designing-domain-services
testing-domain-models
```

When invariants are unclear, stop and route to:

```text
extracting-domain-model-from-legacy-code
```

Do not invent Entities or Value Objects from database tables alone.

## Stage 4 — Introduce the Application Boundary

Create or adapt one Use Case for the selected intention.

Route to:

```text
designing-application-use-cases
designing-application-dtos
testing-application-use-cases
```

The Use Case should:

- accept transport-neutral primitives;
- build Domain types;
- authorize with trusted context;
- depend on ports;
- delegate invariants to Domain;
- return a Response DTO or `void`;
- use stable semantic errors.

Do not make the legacy service itself the Use Case by renaming it.

## Stage 5 — Introduce Only Required Ports

Repository port:

```text
Domain
← repository port
← Infrastructure adapter
```

External-service port:

```text
Application
← provider-neutral port
← Infrastructure adapter
```

A port is required only when it protects an inward policy from a technical implementation.

Do not introduce:

- generic CRUD repositories;
- generic HTTP client ports;
- SDK-shaped ports;
- one port per helper function;
- speculative abstractions for future providers.

## Stage 6 — Isolate Persistence

Route to:

```text
designing-domain-repositories
implementing-repository-adapters
testing-repository-adapters
```

The adapter must own:

- ORM/database mapping;
- reconstitution;
- constraints;
- transaction mechanics;
- technical failure translation;
- migrations.

Refactoring must preserve or deliberately migrate:

- IDs;
- nullability;
- enums;
- timestamps;
- money/precision;
- unknown legacy data;
- uniqueness;
- versioning.

## Persistence Compatibility

For old and new data:

```text
read old
→ map explicitly
→ write compatible form
→ migrate/backfill
→ verify
→ retire compatibility
```

Do not silently default invalid legacy data.

Use one accepted policy:

```text
REPAIR
QUARANTINE
REJECT
COMPATIBILITY_MAP
MIGRATE
```

## Stage 7 — Isolate External Providers

Route to:

```text
designing-external-service-ports
implementing-external-service-adapters
testing-external-service-adapters
```

The adapter must own:

- SDK/API mapping;
- credentials;
- provider accounts;
- timeout;
- retries;
- rate limits;
- idempotency mechanism;
- provider errors;
- reconciliation;
- lifecycle and redaction.

Do not copy provider fields into Domain or Application DTOs.

## Stage 8 — Preserve Transactions and Side Effects

Before redirecting production traffic, compare:

```text
current order
target order
failure after every step
recovery behavior
duplicate risk
```

Do not change the order accidentally.

Examples:

```text
persist pending
→ call provider
→ reconcile
```

or:

```text
call provider
→ persist accepted result
```

The correct strategy must be accepted before implementation.

Do not hold a database transaction across a remote call unless explicitly accepted.

## Stage 9 — Redirect One Caller

Preferred first caller:

- one controller route;
- one job handler;
- one consumer;
- one command entry point.

Redirect:

```text
legacy caller
→ target Use Case or compatibility seam
```

Keep the remaining callers on the legacy path temporarily only when the migration plan permits it.

Record:

- caller;
- routing condition;
- feature flag if used;
- fallback policy;
- observability;
- rollback.

## Feature-Flag Routing

When used, define:

- owner;
- default;
- target environments;
- deterministic key;
- metrics;
- rollback behavior;
- expiry;
- removal ticket.

Do not use an indefinite flag to hide two permanent architectures.

## Strangler Refactor

For multiple callers:

```text
migrate caller 1
→ validate
→ migrate caller 2
→ validate
→ continue
→ remove legacy implementation
```

Each caller migration is a separate controlled step.

Do not reroute all callers at once merely because the new path exists.

## Parallel Run

Use only for side-effect-safe comparison.

Requirements:

- one authoritative result;
- no duplicate external command;
- no duplicate durable write;
- synthetic or sanitized data;
- explicit diff;
- bounded period;
- exit criteria.

A shadow path must not call a real provider or mutate production state.

## Stage 10 — Validate Equivalence and New Behavior

Run:

- characterization tests;
- new Domain tests;
- Use Case tests;
- real repository integration tests;
- external adapter tests;
- real HTTP E2E where applicable;
- migration/backfill checks;
- architecture validation;
- typecheck/lint/build.

Compare:

```text
accepted current contract
versus
target path behavior
```

Expected intentional changes must be explicitly accepted.

## Stage 11 — Remove or Retain the Legacy Path

Remove obsolete code only when:

- every intended caller is redirected;
- new path evidence is sufficient;
- compatibility period is complete;
- metrics show no required old-path use;
- rollback strategy no longer depends on it;
- data migration is verified;
- temporary deviation removal condition is met.

Otherwise retain it with:

- exact owner;
- usage telemetry;
- scope;
- risk;
- removal condition;
- next migration slice.

## Removal Checklist

Before deletion verify:

- routes/jobs/consumers;
- factory/composition references;
- tests and fixtures;
- feature flags;
- old configuration/secrets;
- database columns/tables;
- provider webhooks/subscriptions;
- docs and runbooks;
- dashboards/alerts;
- dead imports and generated artifacts.

Do not delete compatibility data before rollback and mixed-version windows close.

## TDD Strategy

Use:

```text
Reason
→ Red
→ Green
→ Refactor
→ Re-evaluate
```

for new target behavior and defects.

Characterization tests are the preservation safety net.

A typical sequence:

```text
characterization green
→ new Domain case red
→ Domain green
→ Use Case red/green
→ adapter integration red/green
→ caller redirection
→ end-to-end equivalence
```

## No Big-Bang Rewrite

Forbidden default plan:

```text
create all target modules
rewrite all controllers
replace all repositories
migrate all data
switch everything
delete legacy code
```

Use the smallest executable migration step that improves one behavior.

## Scope Control

Classify every edit:

```text
REQUIRED_TO_PRESERVE_BEHAVIOR
REQUIRED_FOR_TARGET_BOUNDARY
REQUIRED_COMPATIBILITY
SAFE_LOCAL_CLEANUP
DEFERRED_DEBT
UNRELATED
```

Only the first four may enter the refactor, and `SAFE_LOCAL_CLEANUP` must remain small.

Do not mix unrelated formatting, framework upgrades, or module reorganization.

## Architectural Drift

Before and after, classify:

```text
PRE_EXISTING
NEW
WORSENED
FIXED
ACCEPTED_TEMPORARY
```

Completion requires no new or worsened unaccepted drift.

A temporary facade or compatibility mapper is acceptable only with an exit path.

## Rollback

Define rollback at each migration step.

Consider:

- code route rollback;
- schema backward compatibility;
- dual-readable data;
- provider side effects;
- event versions;
- feature flag;
- secret/config removal;
- irreversible backfill.

Rollback must not assume external side effects can be undone.

## Observability

Instrument the migration seam:

- old versus new path count;
- success/failure;
- latency;
- semantic result differences;
- duplicate/retry behavior;
- reconciliation backlog;
- migration errors;
- remaining legacy callers.

Do not log secrets or sensitive payloads.

## Security and Integrity

The refactor must not temporarily weaken:

- authentication;
- authorization;
- tenant scoping;
- constraints;
- idempotency;
- input validation;
- secret isolation;
- error redaction;
- data-region/account selection.

A compatibility path with weaker safety is a blocker.

## Failure Classification

Use:

```text
CHARACTERIZATION_FAILURE
BEHAVIOR_REGRESSION
ARCHITECTURE_REGRESSION
COMPATIBILITY_FAILURE
DATA_MIGRATION_FAILURE
TRANSACTION_OR_RECONCILIATION_BLOCKER
SECURITY_OR_INTEGRITY_BLOCKER
DATABASE_ENVIRONMENT_BLOCKED
PROVIDER_ENVIRONMENT_BLOCKED
TEST_SETUP_FAILURE
CLEANUP_FAILURE
TOOLING_BLOCKED
```

## Refactoring Decisions

Use layer gates:

```text
CURRENT_BEHAVIOR_PROTECTED
SEAM_READY
INNER_MODEL_READY
APPLICATION_BOUNDARY_READY
ADAPTER_BOUNDARIES_READY
CALLER_REDIRECTED
TARGET_PATH_VALIDATED
LEGACY_PATH_REMOVABLE
LEGACY_PATH_RETAINED_WITH_EXIT_PLAN
```

## Final Decision

Use one:

```text
HEXAGONAL_REFACTOR_COMPLETE
HEXAGONAL_REFACTOR_COMPLETE_WITH_CONDITIONS
MORE_CALLERS_TO_MIGRATE
LEGACY_PATH_RETAINED
RETURN_TO_CHARACTERIZATION
RETURN_TO_DOMAIN_EXTRACTION
RETURN_TO_ADAPTATION_PLAN
DECISION_REQUIRED
VALIDATION_FAILED
BLOCKED
```

## Output

Use `assets/backend-hexagonal-refactoring-record.md`.

## Completion Criteria

- [ ] One behavior and one migration step were selected.
- [ ] Current behavior and public/data contracts were characterized.
- [ ] The seam has stable semantics and improves ownership or testability.
- [ ] Business decisions moved to the correct Domain/Application layer.
- [ ] Only required ports and adapters were introduced.
- [ ] Public contracts and accepted compatibility were preserved.
- [ ] Persistence and provider details remain in Infrastructure.
- [ ] Transaction, idempotency, side-effect ordering, and partial failures are explicit.
- [ ] One caller was redirected with rollback and observability.
- [ ] Focused and cross-layer validation actually ran.
- [ ] No new or worsened unaccepted drift remains.
- [ ] Temporary compatibility code has an owner and exit condition.
- [ ] Legacy code was removed only when all removal conditions were met.
- [ ] Unrelated repository cleanup was excluded.
- [ ] Final decision and next migration slice are explicit.

## References

- Read `references/characterization-and-safe-seams.md` first.
- Read `references/moving-responsibilities-inward.md` for ownership changes.
- Read `references/ports-adapters-and-compatibility.md` for boundaries.
- Read `references/caller-redirection-rollout-and-rollback.md` before switching traffic.
- Read `references/validation-removal-and-drift.md` before deleting legacy code.
- Read `references/transactions-data-and-external-effects.md` when state or providers are involved.
