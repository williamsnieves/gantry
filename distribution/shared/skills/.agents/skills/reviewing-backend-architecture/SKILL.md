---
name: reviewing-backend-architecture
description: Portable engineering capability `reviewing-backend-architecture`. Use
  when the harness or a specialist agent explicitly requires this named capability.
---
# Reviewing Backend Architecture

## Purpose

Evaluate whether a backend architectural change is:

- correctly owned;
- aligned with modular hexagonal boundaries;
- proportionate to the behavior;
- testable and operable;
- safe to migrate;
- free from unnecessary abstraction and drift.

This skill reviews architectural decisions.

It complements:

```text
validating-backend-architecture
→ checks structural compliance

reviewing-backend-code
→ checks implementation defects

reviewing-backend-architecture
→ challenges the architectural choices themselves
```

## Use When

- A change introduces a module, port, adapter, Use Case, Domain Service, facade, event, transaction boundary, or composition pattern.
- A vertical slice crosses several backend layers.
- A brownfield change adds migration seams or temporary deviations.
- The team must decide whether an abstraction is necessary.
- A new dependency direction is technically valid but may be conceptually wrong.
- A migration may create dual ownership, duplicate writes, or long-lived complexity.
- Architecture drift or accidental complexity is suspected.
- A design/PR needs architectural approval before merge.

## Do Not Use When

- Only import-direction checks are required.
- Only code-level correctness/security/testing findings are required.
- The architecture has not been proposed or implemented enough to inspect.
- The user asks to implement the recommended changes.
- The task is to redesign the entire backend without scope.
- A finding is merely a stylistic preference.
- The standard or accepted decisions do not support the criticism.

## Inputs

- Accepted behavior or change specification.
- Architecture proposal, ADR, PR, diff, or target module.
- Definitive backend standard.
- Repository-local `AGENTS.md`.
- Architecture validation report.
- Code review report when available.
- Current and target architecture maps.
- Ports, adapters, DTOs, composition, schemas, migrations, and tests.
- Accepted exceptions and debt ledger.
- Operational and rollout constraints.

## Outputs

- Architecture review scope.
- Decision and ownership map.
- Architectural findings.
- Complexity and proportionality assessment.
- Migration and reversibility assessment.
- Accepted deviation assessment.
- Questions requiring product/architecture decisions.
- Final architecture review decision.
- Backend architecture review report.

## Core Review Questions

1. Is the behavior owned by the correct module and layer?
2. Is each new abstraction required by a real boundary?
3. Are ports provider/persistence-neutral and placed inward?
4. Are adapters concrete and isolated outward?
5. Is one Use Case one intention?
6. Is composition explicit and centralized?
7. Are transaction, idempotency, and side-effect semantics owned clearly?
8. Does the migration preserve compatibility and provide an exit path?
9. Does the design reduce or increase accidental complexity?
10. Can the architecture be tested and operated honestly?

## Workflow

1. **Confirm behavior and scope.**
2. **Map current and proposed architecture.**
3. **Identify architectural decisions introduced by the change.**
4. **Review ownership by capability and layer.**
5. **Review ports, adapters, DTOs, Use Cases, and Domain boundaries.**
6. **Review composition and lifecycle.**
7. **Review transactions, idempotency, and external side effects.**
8. **Review migration, compatibility, reversibility, and observability.**
9. **Challenge abstraction necessity and accidental complexity.**
10. **Compare against existing architecture validation and code review.**
11. **Classify findings and avoid duplicates.**
12. **Produce an architecture decision.**

## Scope

Classify architecture elements as:

```text
INTRODUCED_BY_CHANGE
MODIFIED_BY_CHANGE
DIRECTLY_DEPENDED_ON
PRE_EXISTING_ADJACENT
UNRELATED
```

Review findings should normally concern the first three.

Do not use the review to inventory unrelated repository debt.

## Architecture Decision Inventory

List new or changed decisions such as:

- capability/module ownership;
- Entity or Value Object introduction;
- Domain Service;
- repository port;
- external-service port;
- Use Case boundary;
- DTO contract;
- adapter selection;
- transaction/Unit of Work;
- event or async workflow;
- compatibility facade;
- composition factory;
- migration seam;
- feature flag;
- temporary deviation.

Every significant abstraction should have a reason tied to behavior.

## Ownership Review

Check whether each responsibility belongs in the correct place.

### Domain

Owns:

- invariants;
- lifecycle;
- semantic decisions;
- pure calculations;
- Domain errors;
- repository contracts in Domain language.

### Application

Owns:

- one intention per Use Case;
- orchestration;
- authorization coordination;
- transaction and side-effect policy;
- Request/Response DTOs;
- external-service ports.

### Infrastructure

Owns:

- database/provider/framework details;
- mappings;
- retries/timeouts;
- credentials;
- HTTP delivery;
- composition;
- technical observability.

A structurally valid dependency may still be conceptually misplaced.

## Module Ownership

Review:

- which capability owns the behavior;
- whether shared code is truly shared;
- whether a new module has a cohesive business purpose;
- whether cross-module dependencies use stable contracts;
- whether a module imports another module's orchestration;
- whether ownership becomes ambiguous.

Avoid creating shared modules for one consumer.

## Ports

A port is justified when it protects an inward policy from an outer capability.

Review:

- owner;
- semantic operation;
- abstraction stability;
- provider/persistence neutrality;
- number of consumers;
- testing value;
- lifecycle and failure semantics.

Question ports that merely mirror:

- generic CRUD;
- SDK interfaces;
- ORM repositories;
- HTTP clients;
- one implementation with no meaningful boundary.

One implementation does not automatically invalidate a port if the boundary is real.

## Adapter Review

Check whether adapters:

- implement one accepted port;
- translate technical data and failures;
- remain replaceable;
- avoid business rules;
- do not expose technical types inward;
- have the correct lifecycle;
- are selected only in composition.

Question “adapters” that are thin aliases with no translation or boundary value.

## Use Case Architecture

Review:

- one intention;
- input/output contract;
- Domain delegation;
- dependency set;
- side-effect order;
- transaction owner;
- idempotency;
- error semantics;
- no Use Case chaining.

A higher-level workflow may deserve its own Use Case rather than chaining lower-level Use Cases.

## Domain Model Proportionality

Assess whether the Domain model is:

- rich enough to protect accepted invariants;
- not overbuilt beyond current behavior;
- free from persistence/provider concerns;
- explicit about identity, equality, and transitions;
- testable as pure units.

Avoid both:

```text
anemic transaction script hiding real invariants
```

and:

```text
speculative aggregate/event/policy hierarchy with no accepted need
```

## DTO and Contract Architecture

Review whether:

- Request DTOs are transport-neutral primitives;
- Response DTOs expose only accepted data;
- Domain objects remain internal;
- public contracts are stable;
- versioning/migration is considered;
- provider/database fields do not become public accidentally.

DTO duplication is acceptable when it protects boundaries.

## Composition

Review:

- centralized concrete selection;
- explicit factories;
- shared versus transient lifecycle;
- configuration validation;
- startup/readiness/shutdown;
- test reset;
- absence of runtime Service Locator.

Current policy:

```text
get*    → cached shared Infrastructure
create* → fresh transient Use Case
```

Question scattered factories and hidden global dependency state.

## Transactions

Architecture review must identify the transaction owner.

Possible owners:

- repository atomic method;
- Application Unit of Work;
- process manager/saga;
- asynchronous state machine.

Review:

- atomic boundary;
- remote calls;
- partial failures;
- rollback;
- compensation;
- reconciliation;
- retry ownership.

A database transaction spanning a remote call is a high-risk decision requiring explicit justification.

## Idempotency

Review end-to-end ownership:

```text
public key
→ Application
→ persistence/provider
→ replay result
```

Check:

- authoritative mechanism;
- same-key reuse;
- duplicate semantics;
- ambiguous completion;
- durable result;
- cross-provider risk;
- public contract.

Idempotency must not exist only in HTTP middleware if durable or external side effects occur later.

## Events and Async Workflows

Review whether events are necessary for:

- decoupling;
- independent transaction boundaries;
- async completion;
- cross-module notification.

Question events used only to avoid a direct, valid Application dependency.

Check:

- event ownership;
- delivery semantics;
- idempotent consumers;
- ordering;
- outbox/inbox when required;
- versioning;
- observability;
- replay.

Do not require event-driven architecture by default.

## Accidental Complexity

Look for complexity not justified by current behavior:

- generic repositories;
- universal service interfaces;
- runtime DI container;
- strategy/factory chains with one stable choice;
- event buses for local synchronous decisions;
- duplicate DTO hierarchies without boundary value;
- excessive indirection;
- parallel old/new code with no exit plan;
- abstraction around pure functions without ownership benefit.

A finding must explain maintenance or correctness impact.

## Under-Design

Also detect insufficient architecture:

- controller owns business/persistence logic;
- Use Case contains provider protocol;
- no authoritative uniqueness;
- no transaction owner;
- no migration plan;
- implicit global dependencies;
- DTO returns Entity;
- tenant boundary not represented;
- remote partial failure ignored.

The goal is proportionate design, not minimum number of files.

## Migration Architecture

For brownfield changes review:

```text
current state
→ seam
→ target state
→ migration steps
→ removal condition
```

Check:

- one authoritative path;
- compatibility;
- backfill;
- mixed-version deployment;
- rollback;
- observability;
- removal of temporary branches;
- debt owner.

Reject dual-write or parallel side effects without reconciliation.

## Reversibility

Assess:

- code rollback;
- schema backward compatibility;
- data irreversibility;
- provider side effects;
- event compatibility;
- feature-flag rollback;
- migration checkpoints.

“Can revert the PR” is not sufficient when data or external effects changed.

## Architectural Drift

Classify:

```text
NEW_DRIFT
WORSENED_DRIFT
PRE_EXISTING
FIXED
ACCEPTED_TEMPORARY
```

Review whether the change:

- adds new outward dependencies;
- bypasses module contracts;
- increases mixed responsibility;
- introduces permanent compatibility layers;
- broadens an exception;
- weakens architecture tests.

No new or worsened unaccepted drift should remain.

## Temporary Deviations

Review every deviation for:

- exact rule;
- scope;
- reason;
- risk;
- owner;
- expiry/removal condition;
- monitoring;
- suppression/check;
- next migration step.

A deviation without an exit path is architecture, not temporary debt.

## Testing Architecture

Review whether test design supports the architecture:

- Domain pure unit tests;
- Use Case tests with real Domain and InMemory repositories;
- repository adapter tests with real persistence;
- provider adapter tests with contract/sandbox evidence;
- HTTP E2E through real HTTP;
- architecture checks for boundaries.

Question architecture that can only be tested through broad E2E or extensive mocking.

## Operability

Review architecture support for:

- configuration;
- readiness;
- shutdown;
- timeout;
- retries;
- tracing;
- correlation;
- metrics;
- reconciliation;
- cleanup;
- incident diagnosis.

Do not require observability abstractions inside Domain.

## Performance and Scale Decisions

Only review performance architecture when relevant.

Check:

- query shape;
- N+1 dependencies;
- connection/client lifecycle;
- transaction duration;
- batch versus per-item operations;
- async boundaries;
- caching ownership;
- consistency semantics.

Do not invent scale requirements.

## Evidence

Use:

1. accepted architecture decisions;
2. code and dependency graph;
3. schemas/migrations;
4. tests;
5. runtime topology;
6. validation reports;
7. operational evidence;
8. explicit reasoning from failure scenarios.

Do not report abstract concerns without a plausible concrete impact.

## Relationship to Architecture Validation

`validating-backend-architecture` answers:

```text
Does the code violate the defined structural rules?
```

This skill answers:

```text
Are the architectural choices coherent and appropriate?
```

Examples:

- A provider port can be structurally correct but unnecessarily generic.
- An event can respect dependency direction but create accidental complexity.
- A compatibility facade can be structurally valid but lack an exit path.
- A transaction boundary can be layered correctly but operationally unsafe.

## Relationship to Code Review

Avoid duplicating implementation defects already captured by `reviewing-backend-code`.

Architecture findings should focus on:

- ownership;
- boundaries;
- lifecycle;
- migration;
- architectural consequences;
- systemic risk.

Reference the code-review finding when it is the implementation manifestation of a larger architecture issue.

## Finding Categories

```text
OWNERSHIP
BOUNDARY
ABSTRACTION
DOMAIN_MODEL
APPLICATION_FLOW
PORT_ADAPTER
COMPOSITION
TRANSACTION
IDEMPOTENCY
EVENTING
MIGRATION
COMPATIBILITY
OPERABILITY
TESTABILITY
ARCHITECTURAL_DRIFT
```

## Severity

### Critical

Architecture creates cross-tenant/security compromise, unrecoverable data corruption, or unbounded duplicate external effects.

### High

Architecture has unsafe transaction/reconciliation semantics, wrong ownership, concrete dependency inversion, permanent migration ambiguity, or serious public/data compatibility risk.

### Medium

Architecture introduces bounded accidental complexity, testability weakness, incomplete removal plan, or new non-blocking drift.

### Low

Local architecture clarity or governance issue with limited impact.

## Finding Format

Each finding must include:

- ID;
- title;
- severity;
- category;
- confidence;
- status;
- decision/standard basis;
- evidence;
- architectural consequence;
- failure or evolution scenario;
- recommendation;
- alternatives considered;
- validation or decision required.

## Decision Questions

Use questions rather than findings when:

- several valid architectures exist;
- transaction or recovery policy is unresolved;
- product compatibility policy is missing;
- scale or consistency requirement is unknown.

State:

- options;
- tradeoffs;
- blocked work;
- recommended decision owner.

Do not silently choose.

## Final Decision

Use one:

```text
ARCHITECTURE_APPROVED
ARCHITECTURE_APPROVED_WITH_CONDITIONS
ARCHITECTURE_CHANGES_REQUIRED
BLOCKED_PENDING_ARCHITECTURE_DECISION
BLOCKED_PENDING_PRODUCT_DECISION
BLOCKED_PENDING_EVIDENCE
```

## Remediation Routing

Route recommendations to:

```text
implementing-backend-inside-out
adapting-backend-rules-to-existing-code
refactoring-backend-toward-hexagonal-architecture
extracting-domain-model-from-legacy-code
focused Domain/Application/adapter/composition skills
validating-backend-architecture
```

Do not perform the refactor during review.

## Output

Use `assets/backend-architecture-review-report.md`.

## Completion Criteria

- [ ] Behavior, scope, current state, and proposed architecture were understood.
- [ ] Module and layer ownership were reviewed.
- [ ] New ports, adapters, DTOs, Use Cases, and Domain abstractions were justified.
- [ ] Composition and lifecycle were reviewed.
- [ ] Transactions, idempotency, and partial failures were reviewed.
- [ ] Events and async boundaries were reviewed only when applicable.
- [ ] Migration, compatibility, reversibility, and exit paths were reviewed.
- [ ] Accidental complexity and under-design were both considered.
- [ ] Testing and operability support the architecture.
- [ ] New/worsened drift and temporary deviations were assessed.
- [ ] Findings are architectural, evidenced, actionable, and non-duplicative.
- [ ] Personal preferences and invented requirements were excluded.
- [ ] Unresolved choices were raised as decisions rather than guessed.
- [ ] Final decision reflects evidence and blocking questions.
- [ ] No code was modified during the review.

## References

- Read `references/ownership-boundaries-and-proportionality.md` first.
- Read `references/ports-adapters-use-cases-and-domain.md` for core choices.
- Read `references/transactions-idempotency-events-and-operability.md` for systemic risks.
- Read `references/migration-reversibility-and-drift.md` for brownfield evolution.
- Read `references/architecture-findings-and-decisions.md` before reporting.
