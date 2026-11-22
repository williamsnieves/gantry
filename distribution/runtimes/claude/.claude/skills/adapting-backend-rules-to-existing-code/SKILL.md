---
name: adapting-backend-rules-to-existing-code
description: Adapts the definitive backend engineering standard to an existing brownfield codebase without forcing an unrelated rewrite. Use when a backend change lands in legacy, layered, framework-centric, transaction-script, ORM-first, service-heavy, or partially hexagonal code. Profile the current architecture, define the target state, select change-local mandatory rules, identify safe migration seams, protect behavior with characterization evidence, prevent new or worsened drift, and record accepted temporary deviations in a debt ledger. Do not silently waive mandatory invariants, demand repository-wide conformance for a local change, or convert the task into a big-bang refactor.
---

# Adapting Backend Rules to Existing Code

## Purpose

Apply the backend standard safely inside an existing codebase whose current architecture does not fully match the target.

The skill must:

- profile the current architecture;
- distinguish target standard from existing reality;
- avoid rewriting unrelated code;
- define a safe incremental adoption plan;
- record accepted temporary deviations.

Required outputs:

```text
current-state map
target-state map
change-local rules
migration seams
debt ledger
```

## Use When

- A feature must be added to a legacy backend.
- Business logic currently lives in controllers, services, ORM models, jobs, or provider wrappers.
- The repository has mixed architectural styles.
- A change touches known architecture debt.
- A new vertical slice should follow the target standard while interoperating with legacy code.
- Existing public contracts or persistence schemas must be preserved.
- Temporary adapters, facades, anti-corruption layers, or compatibility seams may be required.
- A team needs to decide what must be fixed now versus tracked for later.
- Architecture validation finds pre-existing violations near the change.

## Do Not Use When

- The repository is greenfield and already follows the target standard.
- The task is to refactor the entire backend.
- The task is only to review code or architecture.
- The current behavior is unknown and no characterization evidence can be produced.
- The user explicitly wants a big-bang migration plan.
- A mandatory security, data-integrity, or tenant-isolation issue is being treated as optional debt.
- The task is to invent target rules not present in the definitive standard.
- The requested change can be completed cleanly with focused implementation skills and no legacy adaptation.

## Inputs

- Definitive backend engineering standard.
- Repository-local `AGENTS.md`.
- Current change or vertical slice.
- Existing architecture and module topology.
- Current runtime behavior and public contracts.
- Existing tests, logs, schemas, migrations, and integration boundaries.
- Architecture validation findings.
- Decision register and accepted exceptions.
- Operational constraints, release cadence, and migration tolerance.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the definitive backend standard.
3. Read the selected change or vertical-slice plan.
4. Map the code paths touched by the behavior.
5. Inspect:
   - controllers/routes;
   - services/use cases;
   - Domain-like objects;
   - repositories/ORM access;
   - providers/SDKs;
   - transactions;
   - configuration/composition;
   - tests.
6. Identify public contracts and persisted data that must remain compatible.
7. Distinguish:
   - existing debt;
   - new change-local risk;
   - mandatory invariant;
   - default;
   - project policy;
   - accepted exception.
8. Confirm what can be changed safely in the current delivery window.
9. Do not infer behavior solely from names or intended architecture.

## Outputs

- Current-state architecture map.
- Target-state architecture map.
- Change-local rule set.
- Migration seam inventory.
- Characterization and safety-net plan.
- Incremental adoption sequence.
- Accepted temporary deviation register.
- Debt ledger.
- Completion and handoff decision.
- Brownfield adaptation record.

## Core Principle

Improve the architecture around the selected behavior without requiring unrelated cleanup.

```text
understand current behavior
→ protect it
→ introduce a safe seam
→ move one responsibility toward target architecture
→ redirect one caller
→ validate
→ record remaining debt
```

## Workflow

1. **Confirm brownfield scope:** One change or behavior, not the entire repository.
2. **Profile current state:** Layers, dependencies, runtime path, ownership, and debt.
3. **Define target state:** Only for the selected behavior and adjacent required boundaries.
4. **Classify rules:** Mandatory now, default now, deferred, not applicable, or accepted temporary deviation.
5. **Protect current behavior:** Characterization tests and contract evidence.
6. **Identify migration seams:** Stable boundaries where new abstractions can be introduced.
7. **Choose incremental strategy:** Wrap, extract, route, parallel-run, strangler, or compatibility adapter.
8. **Implement change-local architecture:** Use focused backend skills.
9. **Preserve contracts and data:** Public API, events, persistence, and operational behavior.
10. **Validate no new/worsened drift:** Focused tests and architecture validation.
11. **Record temporary deviations:** Owner, risk, scope, and removal condition.
12. **Update debt ledger:** What remains, why, and when it becomes actionable.
13. **Produce handoff:** Next safe slice or remediation skill.

## Readiness Gate

Use one:

```text
READY_TO_ADAPT_BROWNFIELD_CHANGE
READY_WITH_CONDITIONS
CURRENT_BEHAVIOR_CHARACTERIZATION_REQUIRED
TARGET_STATE_DECISION_REQUIRED
PUBLIC_CONTRACT_DECISION_REQUIRED
DATA_MIGRATION_DECISION_REQUIRED
SECURITY_OR_INTEGRITY_BLOCKER
BLOCKED
```

Stop when:

- current behavior cannot be determined;
- public compatibility is unresolved;
- data migration or transaction semantics are unknown;
- the proposed seam would introduce tenant/security risk;
- the change would require unrelated repository-wide restructuring;
- an accepted exception is missing owner or removal condition.

## Current-State Map

Map what exists, not what the code claims to be.

Include:

- entry points;
- business decisions;
- state mutation;
- persistence;
- external side effects;
- error translation;
- transaction ownership;
- configuration and construction;
- test coverage;
- module dependencies;
- public contracts.

Example:

```text
HTTP controller
→ LegacyPromotionService
  → Prisma client
  → Acme SDK
  → status mapping
  → response shaping
```

Do not rename `LegacyPromotionService` as a Use Case unless it actually follows the Use Case boundary.

## Current-State Classification

Classify components by actual responsibility:

```text
DOMAIN-LIKE
APPLICATION-LIKE
INFRASTRUCTURE
DELIVERY
MIXED
UNKNOWN
```

A single class may be `MIXED`.

Record evidence:

- imports;
- constructor dependencies;
- side effects;
- data types;
- public methods;
- runtime call path.

## Target-State Map

Define the target for the selected behavior:

```text
Controller
→ Application Use Case
→ Domain
→ repository/external ports
→ Infrastructure adapters
→ composition
```

The target map should include only:

- the selected behavior;
- required supporting contracts;
- compatibility seams;
- migration exit points.

Do not design the entire future repository.

## Change-Local Rules

For each relevant standard rule classify:

```text
MANDATORY_NOW
DEFAULT_NOW
DEFERRED_WITH_REASON
ACCEPTED_TEMPORARY_DEVIATION
NOT_APPLICABLE
```

Examples normally mandatory now:

- no new Domain-to-Infrastructure dependency;
- no new Application-to-concrete-adapter dependency;
- no credentials or tenant bypass;
- no raw provider/database errors inward;
- no new controller-to-ORM access;
- new business behavior uses Domain/Application boundaries;
- tests cover the new behavior;
- no new or worsened architecture violation.

Existing unrelated violations may remain if they are not worsened and are recorded.

## Mandatory Invariants Cannot Be Deferred Casually

Examples that normally block:

- cross-tenant data access;
- loss of authoritative uniqueness;
- unsafe transaction behavior;
- credential leakage;
- silent corruption/defaulting;
- public technical error leakage;
- unbounded duplicate side effect;
- incompatible data write without migration strategy.

Do not place these in a generic debt backlog merely to ship.

## Local Improvement Rule

A brownfield change should normally satisfy:

```text
new code meets target rules
existing code is not worsened
touched legacy code improves or remains stable
unrelated debt is not mandatory scope
```

When touching an existing violation, decide:

- fix now;
- isolate behind a seam;
- accept temporarily with explicit record;
- stop because risk is too high.

## Characterization Tests

Before moving behavior, capture what must remain stable.

Characterize:

- accepted outputs;
- side effects;
- error semantics;
- ordering;
- persisted data;
- public status/body/events;
- integration calls;
- edge cases known from incidents.

Characterization tests may start green.

They are not the Red test for new behavior.

Do not freeze accidental bugs unless compatibility requires it and the decision is explicit.

## Characterization Evidence Sources

Use:

- existing tests;
- API contracts;
- production-safe logs/metrics;
- schemas;
- database constraints;
- provider documentation;
- incident reproductions;
- domain experts;
- fixture snapshots when stable and safe.

Do not rely on one oversized snapshot as the only behavior description.

## Migration Seams

A seam is a boundary where behavior can be redirected or isolated safely.

Common seams:

- facade around a legacy service;
- repository port in front of direct ORM access;
- external-service port around SDK usage;
- adapter around legacy data shapes;
- controller-to-Use Case delegation;
- domain facade around an anemic model;
- event translation layer;
- transaction boundary;
- compatibility DTO mapper;
- public module contract.

A seam must have:

- clear owner;
- stable input/output;
- test coverage;
- removal or long-term role;
- no hidden Service Locator behavior.

## Seam Selection

Prefer seams that:

- minimize changed callers;
- preserve public behavior;
- isolate technical dependencies;
- allow incremental tests;
- can be removed or retained intentionally;
- do not duplicate business decisions.

Avoid seams that merely add forwarding layers without changing dependency direction or testability.

## Compatibility Adapter

A compatibility adapter may translate:

```text
legacy request/data/error
↔ target port/DTO/Domain contract
```

It belongs in the outer/compatibility layer.

It must not pollute the target Domain/Application contract with legacy fields.

Record whether it is:

```text
TEMPORARY
LONG_LIVED_ANTI_CORRUPTION_LAYER
PUBLIC_COMPATIBILITY_BOUNDARY
```

## Strangler Pattern

For a large legacy capability:

```text
route one behavior to new path
leave remaining behavior on legacy path
measure and validate
migrate next behavior
remove legacy path when empty
```

Do not duplicate writes without an explicit consistency plan.

Routing must be deterministic and observable.

## Parallel Run

Parallel execution may compare old and new behavior.

Requirements:

- one authoritative writer;
- side effects suppressed or isolated on comparison path;
- safe handling of PII;
- result diffing;
- bounded duration;
- exit criteria.

Never send duplicate real provider commands merely to compare implementations.

## Read/Write Migration

Possible staged patterns:

### Read New, Write Legacy

Useful only when new read model is compatible and authoritative source remains clear.

### Write Both

High risk.

Requires:

- explicit authoritative source;
- idempotency;
- ordering;
- failure handling;
- reconciliation;
- rollback/repair;
- observability.

### Backfill Then Switch

Use:

```text
prepare schema
→ backfill
→ verify
→ dual-compatible release
→ switch reads/writes
→ monitor
→ cleanup
```

Do not choose a pattern silently.

## Public Contract Preservation

Protect:

- route/method;
- request/response shape;
- error codes/statuses;
- events;
- headers;
- idempotency behavior;
- ordering/pagination;
- persistence identifiers;
- external references.

A deliberate contract change needs an accepted versioning/migration decision.

Do not use architecture cleanup as justification for accidental API breakage.

## Persisted Data Compatibility

Map:

- old rows/documents;
- new Domain model;
- null/default semantics;
- unknown enums;
- lifecycle fields;
- precision/timezone;
- IDs;
- versioning;
- backfill requirements.

Invalid legacy data must be handled explicitly:

```text
reject
repair
quarantine
compatibility-map
migrate
```

Do not silently coerce impossible states.

## Transaction and Side-Effect Preservation

Legacy code may combine database and remote calls unsafely.

Before changing order, document current behavior:

```text
current order
failure after each step
recovery behavior
duplicate risk
```

Then define target behavior with an accepted decision.

Do not “improve” the transaction sequence without understanding operational consequences.

## Error Compatibility

Map:

```text
legacy error
→ target semantic error
→ existing public contract
```

Temporary compatibility mapping may preserve old HTTP status or code while inner layers adopt semantic errors.

Do not move HTTP status into Domain/Application.

Keep compatibility translation at delivery or adapter boundaries.

## Module Boundaries in Mixed Architectures

New code should follow the target capability/layer structure.

Legacy callers may use an explicit facade.

Example:

```text
legacy controller
→ NewApplyPromotionFacade
  → ApplyPromotionUseCase
```

Prefer changing the controller to call the Use Case directly when safe.

A facade is justified when:

- several legacy callers need the same compatibility translation;
- framework constraints require it;
- migration is staged.

Do not create a generic `LegacyBridgeService`.

## Focused Skill Routing

Use:

```text
extracting-domain-model-from-legacy-code
→ when business invariants are unclear

refactoring-backend-toward-hexagonal-architecture
→ when moving behavior through seams

implementing-backend-inside-out
→ when the selected behavior is ready for full vertical implementation

validating-backend-architecture
→ to verify no new/worsened drift

focused modeling/adapter/testing skills
→ for each target layer
```

This skill defines the adaptation plan and constraints.

It may coordinate focused work but does not replace those skills.

## Temporary Deviations

A temporary deviation record must contain:

- ID;
- violated rule;
- exact scope;
- rationale;
- risk;
- owner;
- creation date;
- expiry or removal condition;
- monitoring;
- remediation skill;
- link to debt item;
- check/suppression mechanism.

Example:

```text
BA-DEV-004
Application still imports LegacyPromotionGateway
Scope: one compatibility facade
Removal: after callers migrate to CampaignProvider port
Owner: Promotions team
```

No owner or removal condition means the deviation is not accepted.

## Debt Ledger

Track architecture debt created or retained near the change.

Fields:

- ID;
- title;
- current state;
- target state;
- impact;
- risk;
- scope;
- dependency;
- recommended next slice;
- owner;
- trigger;
- status.

Status:

```text
OPEN
BLOCKED
PLANNED
IN_PROGRESS
ACCEPTED_TEMPORARY
RESOLVED
WONT_FIX_WITH_DECISION
```

Do not list generic repository complaints unrelated to the change.

## Debt Trigger

A debt item should become actionable when a concrete trigger occurs:

- next change in module;
- provider migration;
- schema version;
- traffic threshold;
- incident;
- contract version;
- removal of legacy caller;
- deadline.

Avoid “fix someday.”

## No New or Worsened Drift

Compare architecture validation before and after.

Classify:

```text
PRE_EXISTING
NEW
WORSENED
FIXED
ACCEPTED_TEMPORARY
```

Completion normally requires:

- no new unaccepted violations;
- no worsened violations;
- any touched temporary deviation is still bounded;
- target seam is validated.

## Change-Local Completion

The brownfield change is complete when:

- behavior is correct;
- public/data compatibility is preserved or deliberately migrated;
- target boundaries exist for the selected behavior;
- characterization and new-behavior tests pass;
- no new/worsened drift remains;
- temporary seams/deviations are documented;
- debt ledger identifies the next safe step.

The whole repository need not be compliant.

## Big-Bang Rewrite Guard

Reject plans such as:

```text
move every module
replace every service
rewrite all repositories
change every DTO
introduce a new framework
```

unless the task explicitly asks for a separately governed rewrite program.

For normal feature work, produce the smallest safe adoption step.

## Scope Classification

Use:

```text
REQUIRED_FOR_CURRENT_BEHAVIOR
REQUIRED_COMPATIBILITY
SAFE_LOCAL_IMPROVEMENT
DEFERRED_DEBT
UNRELATED
BLOCKING_RISK
```

Only the first three normally belong in implementation scope.

`BLOCKING_RISK` must be resolved or formally decided.

## Validation

Apply:

- characterization tests;
- focused Domain/Application tests;
- adapter integration tests;
- HTTP contract/E2E tests;
- migration/backfill checks;
- architecture validation;
- observability checks;
- rollback/recovery evidence.

Do not over-rely on E2E when focused tests can prove inner behavior more clearly.

## Rollback

Define rollback for compatibility/migration steps:

- code rollback;
- schema backward compatibility;
- dual-readable data;
- event version compatibility;
- provider operation recovery;
- feature flag or route switch;
- backfill reversibility.

A rollback plan must not assume data can be undone when it cannot.

## Feature Flags

Use flags only when they support a defined migration:

- deterministic routing;
- owner;
- default;
- environment policy;
- telemetry;
- expiry;
- cleanup.

Do not leave permanent architecture branches hidden behind flags.

## Observability

Measure the seam:

- old/new path usage;
- result differences;
- errors;
- latency;
- duplicate/retry behavior;
- data reconciliation;
- contract failures;
- remaining legacy callers.

Observability must not leak sensitive data.

## Security

Brownfield constraints do not justify:

- tenant bypass;
- raw credential reuse in inner layers;
- production secret exposure;
- unsafe data copying;
- missing authorization;
- weaker validation;
- public technical errors.

Security/integrity regressions are blockers, not normal debt.

## Failure Classification

Use:

```text
PRODUCT_BEHAVIOR_FAILURE
COMPATIBILITY_FAILURE
DATA_MIGRATION_FAILURE
ARCHITECTURE_REGRESSION
CHARACTERIZATION_GAP
TEST_ENVIRONMENT_BLOCKED
DECISION_REQUIRED
SECURITY_OR_INTEGRITY_BLOCKER
```

## Final Decision

Use one:

```text
BROWNFIELD_ADAPTATION_READY
BROWNFIELD_ADAPTATION_READY_WITH_CONDITIONS
MORE_CHARACTERIZATION_REQUIRED
TARGET_STATE_DECISION_REQUIRED
MIGRATION_DECISION_REQUIRED
ACCEPTED_DEVIATION_REQUIRED
SECURITY_OR_INTEGRITY_BLOCKER
BLOCKED
```

## Output

Use `assets/backend-brownfield-adaptation-record.md`.

## Completion Criteria

- [ ] Scope is one change or vertical behavior.
- [ ] Current architecture is mapped from evidence.
- [ ] Target architecture is defined only for required scope.
- [ ] Applicable rules are classified change-locally.
- [ ] Current behavior and public/data contracts are characterized.
- [ ] Safe migration seams are explicit.
- [ ] Incremental strategy avoids a big-bang rewrite.
- [ ] New code follows target boundaries.
- [ ] Existing unrelated debt is not forced into scope.
- [ ] No mandatory security/integrity rule is deferred casually.
- [ ] No new or worsened unaccepted architecture drift remains.
- [ ] Temporary deviations include owner and removal condition.
- [ ] Debt ledger is concrete and change-adjacent.
- [ ] Migration, rollback, and observability are defined when applicable.
- [ ] Focused tests and architecture validation provide actual evidence.
- [ ] Final decision and next safe slice are explicit.

## References

- Read `references/current-and-target-state-mapping.md` first.
- Read `references/change-local-rule-selection.md` for scope decisions.
- Read `references/characterization-and-migration-seams.md` before moving behavior.
- Read `references/compatibility-data-and-transactions.md` for risky migrations.
- Read `references/deviations-and-debt-ledger.md` before accepting debt.
- Read `references/brownfield-validation-and-completion.md` before finalizing.
