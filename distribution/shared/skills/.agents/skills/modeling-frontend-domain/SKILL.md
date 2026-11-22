---
name: modeling-frontend-domain
description: Decides whether a frontend Domain model is justified and, when it is, models frontend-relevant entities, Value Objects, pure Domain Services, invariants, domain errors, deterministic transformations, and optional repository ports. Use for rich local interaction, offline behavior, client-side decision support, deterministic product rules, shared validation experience, or stateful client models. Preserve backend authority for server-enforced invariants and avoid duplicating backend logic merely for symmetry. Domain must remain independent of React, browser APIs, HTTP, routing, CSS, design systems, storage libraries, Application, and Infrastructure. Do not create ceremonial Domain layers for UI-only formatting, passive API bags, trivial transformations, or rules whose only authority belongs to the server.
...
---

# Modeling Frontend Domain

## Purpose

Decide whether a frontend Domain layer is justified.

If it is, model only the frontend-relevant business concepts and pure rules that materially improve:

- correctness;
- local behavior;
- rich interaction;
- offline capability;
- deterministic decision support;
- validation experience;
- testability.

The first output may legitimately be:

```text
NO_FRONTEND_DOMAIN_REQUIRED
```

A Domain layer is not a maturity badge.

Complexity must be earned.

## Governing Standard

Frontend Domain owns:

- frontend-relevant entities;
- Value Objects;
- pure business rules;
- state-independent transformations;
- repository ports when the frontend truly models persistence or remote collections as domain access;
- domain errors;
- invariants.

Frontend Domain MUST NOT depend on:

- React;
- browser APIs;
- HTTP;
- routing;
- CSS;
- design systems;
- storage libraries;
- Application;
- Infrastructure.

Not every frontend feature requires Domain.

## Use When

- Rich client behavior has meaningful invariants.
- Offline or local-first behavior exists.
- The user edits a complex local model before persistence.
- Deterministic client-side product rules improve interaction.
- Validation needs more than field-shape checking.
- Several UI surfaces need the same pure product semantics.
- A local draft has identity and lifecycle.
- A complex editor state has business meaning independent of React.
- Client-side decision support or previews need deterministic rules.
- Domain tests would provide meaningful confidence independent of UI and transport.

## Do Not Use When

- The feature only displays remote data.
- Logic is presentation-only formatting.
- A calculation belongs purely to view formatting.
- The server is the only authority and no local decision is needed.
- The model would merely copy an API response.
- A Value Object would validate nothing.
- An Entity would be a passive property bag.
- A Domain Service would only forward parameters.
- The feature has no meaningful pure product rule.
- Domain is proposed only to mirror backend folder structure.

## Inputs

- Accepted behavior/specification.
- Architecture-profile decision.
- Vertical-slice plan.
- Server-authoritative rules.
- Offline/local requirements.
- Optimistic behavior requirements.
- Data ownership and persistence needs.
- Existing backend/domain contracts when available.
- Existing frontend Domain patterns.
- Serialization needs.
- Repository-local `AGENTS.md`.

## Outputs

- Frontend Domain justification decision.
- Local versus server authority matrix.
- Domain concept inventory.
- Entity model where justified.
- Value Object model where justified.
- Pure Domain Service model where justified.
- Domain errors.
- Repository-port decision where justified.
- Serialization boundary.
- Domain test matrix.
- Frontend Domain modeling record.

## Core Workflow

```text
accepted behavior
→ identify business semantics
→ separate presentation and transport concerns
→ separate frontend authority from backend authority
→ decide whether Domain is justified
→ model smallest valid concepts
→ define invariants and behavior
→ define serialization
→ define tests
```

## Readiness Gate

Use one:

```text
READY_TO_DECIDE_FRONTEND_DOMAIN
READY_WITH_CONDITIONS
BEHAVIOR_REQUIRED
AUTHORITY_BOUNDARY_REQUIRED
OFFLINE_POLICY_REQUIRED
PERSISTENCE_DECISION_REQUIRED
NO_FRONTEND_DOMAIN_REQUIRED
BLOCKED
```

Do not start modeling entities before answering whether the frontend needs a Domain layer.

## Domain Justification Test

A frontend Domain model is justified when at least one meaningful condition exists:

```text
rich local behavior
offline operation
client-side decision support
deterministic product rules
shared validation semantics
stateful local product model
meaningful invariant protection
```

It is not justified merely because:

```text
backend has Domain
feature has API types
component is large
TypeScript types exist
logic is repeated twice
```

## Frontend Versus Backend Authority

For every rule classify:

```text
FRONTEND_AUTHORITATIVE
BACKEND_AUTHORITATIVE
SHARED_SEMANTICS_BACKEND_AUTHORITATIVE
FRONTEND_PREVIEW_ONLY
LOCAL_ONLY_RULE
UNKNOWN_REQUIRES_DECISION
```

Examples:

### Backend authoritative

- entitlement;
- payment authorization;
- inventory guarantee;
- final price;
- server permissions;
- promotion eligibility enforced server-side.

Frontend may mirror some semantics for UX but MUST NOT become the final authority.

### Frontend authoritative

- local editor invariant;
- local draft consistency before persistence;
- offline-only state transition;
- deterministic client-only interaction rule.

### Shared semantics, backend authoritative

The frontend may run the same conceptual rule for immediate feedback, but final acceptance belongs to the server.

The model must make that authority explicit.

## Avoid Backend Duplication

Do not copy backend business rules into frontend Domain simply to reduce server round trips or create “clean architecture symmetry.”

Duplicated rules create:

- drift;
- contradictory outcomes;
- duplicated release coordination;
- false frontend authority.

Duplication may be justified only when:

- local behavior genuinely requires it;
- immediate user feedback matters;
- offline behavior requires it;
- deterministic preview is part of accepted product behavior;
- ownership and synchronization are explicit.

## Presentation Versus Domain

Presentation logic includes:

- formatting dates for display;
- choosing labels;
- CSS classes;
- local open/closed state;
- sorting purely for display;
- truncating text;
- responsive behavior.

These normally do not justify Domain.

Domain logic includes:

- invariant-preserving state transitions;
- semantic validation;
- business-significant calculations;
- deterministic product decisions;
- local entity lifecycle;
- meaningful rules shared across interactions.

Do not move presentation logic into Domain merely because it is “pure.”

## Infrastructure Versus Domain

Transport and provider concerns remain outside Domain.

Examples not allowed in Domain:

```text
HTTP status
AxiosError
Response
localStorage
IndexedDB API
SWR key
React Query key
URLSearchParams
JSON provider DTO
snake_case transport object
```

Domain may expose primitives or domain types that Infrastructure maps.

## Application Versus Domain

Domain owns business meaning and invariants.

Application owns user/system intentions and orchestration.

Example:

```text
Domain
PromotionDraft.applyCode(code)

Application
ApplyPromotion.execute(request)
→ repository
→ Domain behavior
→ result
```

Do not place remote orchestration in Domain.

Do not place pure invariant logic in Use Cases merely because the user triggered it.

## Entities

Use an Entity when identity matters across state changes.

Entity requirements:

- stable identity when identity is meaningful;
- invariants protected;
- intent-revealing behavior;
- no framework concerns;
- no public mutation that permits invalid state.

Good conceptual behavior:

```text
draft.rename(...)
draft.addItem(...)
draft.removeItem(...)
draft.publish()
```

Weak passive bag:

```text
class Draft {
  id
  title
  items
}
```

with unrestricted public mutation.

Do not create an Entity when a plain immutable value is enough.

## Entity Identity

Identity should represent product semantics.

Possible identity sources:

- persisted ID;
- locally generated draft ID;
- composite semantic identity.

Do not use random IDs merely to justify an Entity.

If two instances with the same values are interchangeable, a Value Object may be a better fit.

## Entity Invariants

An Entity should make invalid transitions impossible or explicit.

Examples:

```text
cannot publish empty draft
cannot add duplicate unique item
cannot edit locked draft
cannot transition archived → active without restore
```

Do not rely on UI disabling alone to protect an Entity invariant.

## Entity Mutation

Prefer behavior methods over unrestricted property mutation.

Operations may:

- return a new immutable Entity;
- mutate private internal state while preserving invariants;
- return a Result according to project conventions.

Choose the repository's accepted style.

Do not expose setters that let callers create impossible states.

## Value Objects

Use a Value Object when:

- equality is by value;
- semantic validation exists;
- operations are value-based;
- identity does not matter.

Value Objects MUST be compared by value.

They SHOULD be immutable.

Operations SHOULD return new instances.

Examples:

```text
CampaignCode
Money
Percentage
EmailAddress
DateRange
Quantity
LocaleCode
EditorSelectionRange
```

Only use these when they carry meaningful semantics.

## Value Object Creation

When invalid states are possible, create through a validated boundary.

Possible patterns:

```text
CampaignCode.create(raw)
CampaignCode.parse(raw)
Result<CampaignCode, CampaignCodeError>
```

Do not make the constructor public if it allows invalid values and the project convention supports controlled creation.

## Value Object Serialization

Serialization SHOULD produce:

- primitives;
- transport-safe structures.

Example:

```text
CampaignCode
→ string
```

Do not serialize hidden framework or class internals.

Infrastructure owns transport casing and provider shape.

## Domain Services

Use a Domain Service only when pure logic:

- belongs to Domain;
- spans multiple domain concepts;
- does not naturally belong to one Entity or Value Object.

Prefer a pure function.

Examples:

```text
calculateDraftCompletion(...)
resolveLocalConflict(...)
estimatePreviewPrice(...)
```

when these are genuinely Domain semantics.

Domain Services MUST NOT:

- call HTTP;
- access browser storage;
- import React;
- depend on concrete adapters;
- manage UI state.

## Domain Service Restraint

Do not create a service when:

- behavior fits naturally on an Entity;
- a Value Object owns the operation;
- logic is presentation formatting;
- it only forwards arguments.

Avoid `SomethingManager`, `SomethingHelper`, or `SomethingService` without a clear domain reason.

## Domain Errors

Domain errors represent semantic invalidity.

Examples:

```text
InvalidCampaignCode
DraftAlreadyPublished
DuplicateDraftItem
InvalidDateRange
QuantityOutOfRange
```

Domain errors MUST NOT encode:

```text
HTTP 409
Axios timeout
Response status
IndexedDB failure
```

Those belong outward.

## Error Modeling

Choose the repository's established style:

- typed result;
- explicit error class;
- discriminated union;
- validated factory.

Do not invent a new global error framework for one feature.

## Deterministic Transformations

Frontend Domain may own state-independent deterministic transformations when they express product semantics.

Examples:

- merge offline edit operations;
- normalize semantic selection ranges;
- calculate domain progress;
- resolve deterministic local state.

A pure transformation is not automatically Domain.

Ask whether a product stakeholder could meaningfully name the behavior.

## Local Drafts

Offline/local drafts often justify Domain when they have:

- identity;
- lifecycle;
- invariants;
- merge rules;
- validation;
- persistence-independent behavior.

Separate:

```text
Draft Domain model
≠
IndexedDB representation
```

Infrastructure maps between them.

## Rich Editor State

Rich editor Domain may be justified when state represents product semantics such as:

- document blocks;
- semantic selection;
- constraints;
- transitions;
- commands;
- conflict resolution.

It is not justified for:

- cursor pixel coordinates;
- DOM selection APIs;
- toolbar open state;
- CSS selection highlighting.

Keep browser/editor-library mechanics outward.

## Client-Side Pricing or Preview

A pricing or preview model may be Domain only when:

- product behavior explicitly requires deterministic local calculation;
- it is clearly a preview/estimate;
- backend remains authoritative when appropriate;
- stale rule risk is accepted and governed.

Do not present preview output as final authoritative result unless that authority is accepted.

## Validation

Distinguish:

```text
shape validation
domain validation
server validation
```

### Shape validation

Examples:

- required string;
- JSON structure;
- enum membership.

Often boundary/Application/Infrastructure concern.

### Domain validation

Examples:

- semantic code format;
- valid range;
- local invariant.

### Server validation

Examples:

- promotion exists;
- user eligible;
- payment accepted.

Do not turn server-only validation into frontend Domain authority.

## Optimistic Behavior

Optimistic UI does not automatically imply Domain.

Domain may help when optimistic state has meaningful transitions or conflict rules.

Otherwise the server-state layer may own optimistic cache behavior.

Classify:

```text
DOMAIN_OPTIMISTIC_RULE
SERVER_STATE_OPTIMISTIC_BEHAVIOR
PRESENTATION_OPTIMISTIC_STATE
```

Do not duplicate the same optimistic rule in several layers.

## Offline Behavior

Offline operation is a strong Domain signal when users can:

- create;
- edit;
- transition;
- validate;
- reconcile.

Domain should remain independent of:

- Service Worker;
- IndexedDB;
- localStorage;
- sync engine SDK.

Those are Infrastructure.

## Repository Ports in Frontend Domain

A repository port MAY belong in Domain when the frontend genuinely models:

- persistence of domain aggregates;
- domain collections;
- offline domain storage;
- remote collections as domain access.

Examples:

```text
DraftRepository
DocumentRepository
CartRepository
```

Do not create a Domain repository port merely to wrap every API endpoint.

If the port represents an Application-oriented remote service or command, Application may be the better owner.

## Repository Port Decision

Use:

```text
DOMAIN_REPOSITORY_PORT_JUSTIFIED
APPLICATION_PORT_PREFERRED
NO_PORT_REQUIRED
PORT_OWNERSHIP_REQUIRES_DECISION
```

Ask:

- Does this repository speak Domain language?
- Does Domain need the abstraction?
- Is persistence part of the domain model?
- Would the port remain meaningful without HTTP?

## Serialization Boundary

Define explicit conversion between:

```text
Domain
↔ Application DTO
↔ Infrastructure/provider type
```

Do not let transport shape become Domain by coincidence.

If API and Domain shapes currently match, mapping may still be intentionally explicit if the boundary matters.

## Dates and Time

Domain date handling must define semantics:

- instant;
- local date;
- date-time;
- timezone;
- range;
- inclusive/exclusive boundary.

Do not allow implicit browser locale/timezone behavior inside Domain.

Prefer primitives or established date/value abstractions according to repository policy.

## Numeric Semantics

For money, percentages, quantities, and measurements define:

- units;
- precision;
- rounding;
- allowed range;
- serialization.

Do not use floating-point arithmetic casually for money when exact semantics matter.

Do not introduce a money library unless already accepted.

## Equality

Entities:

```text
identity equality
```

Value Objects:

```text
value equality
```

Do not mix these semantics.

## Immutability

Immutability is strongly preferred for Value Objects.

Entities may use immutable or controlled mutable internals.

The invariant matters more than style.

Do not require deep cloning everywhere.

## Naming

Use product/domain language.

Good:

```text
PromotionDraft
CampaignCode
SelectionRange
CompletionPercentage
```

Weak:

```text
DataModel
FrontendEntity
BusinessObject
DomainHelper
```

Names should reveal meaning, not architectural category alone.

## Shared Domain

Move Domain concepts to shared only when:

- multiple capabilities truly share the same semantics;
- ownership is clear;
- changes should evolve centrally;
- the concept is not merely visually or structurally similar.

Do not create speculative `shared/domain`.

## Backend Domain Reuse

When generated/shared contracts exist, distinguish:

```text
shared contract
≠
shared executable business logic
```

A shared TypeScript package may legitimately expose stable Value Objects or pure rules when organizational ownership supports it.

Do not couple frontend delivery to backend runtime code.

Do not assume sharing code is always safer than duplicating a small stable semantic contract.

## Framework Independence

Domain code should be executable in a plain non-browser test environment.

A practical diagnostic:

```text
Can this Domain behavior run without React, DOM, fetch, router, storage, or CSS?
```

If no, the concept may be in the wrong layer.

## Domain Tests

Domain tests are pure.

They SHOULD cover:

- invariant preservation;
- valid transitions;
- invalid transitions;
- Value Object boundaries;
- equality;
- deterministic services;
- serialization primitives;
- edge cases.

They MUST NOT require:

- React;
- HTTP;
- browser;
- storage.

Do not mock Domain entities, Value Objects, or pure Domain Services.

## Property-Based Testing

Property-based tests may be useful when:

- invariant space is broad;
- transformations have algebraic properties;
- ranges are large.

Use only when repository tooling supports it.

Do not introduce a new testing library solely for this.

## Domain Model Size

Prefer the smallest model that expresses the accepted semantics.

Possible valid output:

```text
one Value Object
```

or:

```text
one Entity + one Value Object
```

Do not build a full DDD aggregate hierarchy because the skill is named Domain.

## No-Domain Decision

When Domain is not justified, record why.

Example:

```text
NO_FRONTEND_DOMAIN_REQUIRED

Reason:
The feature renders remote promotion data and submits one code.
All eligibility rules remain server-authoritative.
The only client transformations are display formatting.
```

Then route concerns to:

- Application;
- adapter;
- hook/component;
- server-state;
- presentation.

A no-Domain decision is a successful outcome.

## Over-Modeling Signals

Flag:

- class wrapping one API payload;
- Value Object with no validation/behavior;
- Service forwarding parameters;
- repository port mirroring endpoint names;
- Domain types containing provider DTO names;
- frontend duplicate of server policy with no local need;
- aggregate with one passive property;
- generic abstractions created “for the future.”

Use:

```text
PROPORTIONATE_DOMAIN
UNDERMODELED_DOMAIN
OVERMODELED_DOMAIN
NO_DOMAIN_REQUIRED
```

## Under-Modeling Signals

A Domain model may be missing when:

- invalid local states are common;
- UI repeatedly reimplements the same invariant;
- offline transitions are scattered through hooks;
- complex editor rules live inside React state updates;
- deterministic product calculations are duplicated across components.

Do not automatically respond by creating more classes; identify the smallest semantic boundary.

## Domain Decision Record

For each concept record:

- name;
- type;
- responsibility;
- identity/equality;
- invariants;
- authority;
- operations;
- errors;
- serialization;
- persistence ownership;
- tests.

## Final Decision

Use:

```text
FRONTEND_DOMAIN_MODEL_READY
FRONTEND_DOMAIN_MODEL_READY_WITH_CONDITIONS
NO_FRONTEND_DOMAIN_REQUIRED
RETURN_TO_PRODUCT_BEHAVIOR
AUTHORITY_BOUNDARY_REQUIRES_DECISION
PERSISTENCE_BOUNDARY_REQUIRES_DECISION
BLOCKED
```

## Output

Use `assets/frontend-domain-modeling-record.md`.

## Completion Criteria

- [ ] Domain justification is decided before modeling.
- [ ] No-Domain is accepted as a valid outcome.
- [ ] Frontend versus backend authority is explicit.
- [ ] Server-enforced invariants remain backend-authoritative.
- [ ] Presentation-only transformations are excluded.
- [ ] Transport/provider/storage/framework concerns are excluded.
- [ ] Entities exist only when meaningful identity exists.
- [ ] Entities protect invariants and expose intent-revealing behavior.
- [ ] Value Objects use value equality and meaningful semantic validation.
- [ ] Domain Services are pure and only used when behavior has no natural owner.
- [ ] Domain errors are semantic rather than technical.
- [ ] Offline/local/editor behavior is modeled independently from browser storage and UI libraries.
- [ ] Optimistic behavior has one clear owner.
- [ ] Repository ports are created only when Domain ownership is justified.
- [ ] Serialization produces primitives or transport-safe structures.
- [ ] Dates, units, precision, and equality semantics are explicit when relevant.
- [ ] Shared Domain abstractions require real shared semantics and ownership.
- [ ] The model is the smallest one that expresses accepted behavior.
- [ ] Domain tests are pure and require no React/browser/HTTP/storage.
- [ ] No backend rule is duplicated merely for architectural symmetry.
- [ ] No framework, testing library, or persistence implementation is introduced.
- [ ] Final Domain decision is explicit.
