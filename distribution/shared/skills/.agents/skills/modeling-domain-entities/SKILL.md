---
name: modeling-domain-entities
description: Portable engineering capability `modeling-domain-entities`. Use when
  the harness or a specialist agent explicitly requires this named capability.
---
# Modeling Domain Entities

## Purpose

Create or evolve a Domain Entity that:

- has stable identity;
- represents a meaningful lifecycle;
- protects its own invariants;
- exposes intent-revealing business behavior;
- never exposes a partially valid state;
- keeps mutable collections encapsulated;
- remains independent from Application and Infrastructure;
- serializes only to primitives or plain objects when the project uses that convention.

The skill designs and may implement the Entity and its focused Domain tests when implementation is explicitly requested.

## Use When

- A backend vertical slice requires a business object with stable identity and lifecycle.
- Existing code models a business concept as a mutable data bag.
- Setters allow invalid transitions.
- Construction can produce partially valid state.
- Entity-owned invariants are currently enforced in Use Cases, controllers, or adapters.
- Internal arrays or maps are exposed directly.
- Persistence or DTO concerns have leaked into Domain.
- An existing Entity needs a new accepted behavior or transition.

## Do Not Use When

- The concept is defined only by its attributes and should be a Value Object.
- The behavior belongs to a pure Domain Service spanning multiple Entities or Value Objects.
- The request is to design a persistence/ORM model.
- The object is a Request/Response DTO.
- The concept has no stable identity or lifecycle.
- The desired behavior is not accepted or remains ambiguous.
- The request is only to create getters, setters, or a generic data container.
- The project policy for identifiers is material and unresolved.

## Inputs

- Accepted specification or OpenSpec change.
- Backend Rule Applicability Report.
- Backend Vertical Slice Plan.
- Existing Domain model and tests.
- Project identity policy.
- Domain error conventions.
- Serialization convention, if any.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted behavior for the Entity.
3. Read the relevant slice and applicable Domain rules.
4. Inspect neighboring Entities, Value Objects, errors, and tests.
5. Confirm the project's identifier policy:
   - shared generic `Id`; or
   - centrally adopted typed identifiers.
6. Confirm construction and serialization conventions.
7. Identify current lifecycle states and valid transitions.
8. Distinguish Domain state from DTO, persistence, and provider representations.
9. Do not infer business invariants from database constraints alone.

## Outputs

Depending on the request:

- Entity responsibility and identity decision.
- Lifecycle and transition model.
- Invariant catalog.
- Construction strategy.
- Intent-revealing operations.
- Collection encapsulation strategy.
- Equality semantics.
- `toPrimitives()` design when applicable.
- Focused Domain test cases.
- Risks, unresolved decisions, and follow-up skills.
- Entity modeling report.

## Core Entity Criteria

A concept is an Entity when it has:

```text
stable identity
+ meaningful lifecycle
+ behavior that protects invariants
```

Entity equality is identity-based.

A concept should not become an Entity merely because it is stored in a database or has an `id` column.

## Workflow

1. **Confirm entity suitability:** Determine whether the concept is truly an Entity.
2. **Resolve identity policy:** Use the repository-approved generic or typed identifier strategy.
3. **Define responsibility:** State what behavior and invariants the Entity owns.
4. **Model lifecycle:** Identify states, transitions, terminal states, and prohibited transitions.
5. **Catalog invariants:** Separate creation, transition, collection, and cross-object rules.
6. **Design construction:** Prevent partially valid instances.
7. **Design behavior:** Replace generic setters with intent-revealing operations.
8. **Encapsulate collections:** Protect mutable internal collections.
9. **Define equality:** Compare by stable identity.
10. **Define serialization:** Use Domain primitives only when the project convention requires it.
11. **Design tests:** Cover public behavior, invariants, transitions, and encapsulation.
12. **Check boundaries:** Remove DTO, ORM, framework, and provider dependencies.
13. **Review proportionality:** Avoid unnecessary factories, inheritance, or abstraction.
14. **Report or implement:** Use the Entity modeling report.

## Entity Suitability Test

Use this decision:

```text
If the concept is defined only by attributes and has no identity/lifecycle:
    route to modeling-domain-value-objects.
Else if behavior belongs naturally to one identified object:
    model an Entity.
Else if pure behavior spans multiple domain objects and belongs to none:
    consider designing-domain-services.
Else:
    return to specification or domain analysis.
```

## Identity

An Entity must have stable identity across state changes.

### Equality

Equality must be based on identity, not every attribute.

Two Entities with the same attributes but different IDs are distinct.

Two instances representing the same ID are the same Entity even when their current snapshots differ.

### Identifier Policy

Follow the repository policy.

Possible accepted policies:

```text
shared generic Id
typed entity-specific identifiers
```

Do not mix both strategies opportunistically.

Do not expose raw primitive IDs when the project standard requires an `Id` Value Object.

Do not introduce typed identifiers locally when the project has centrally chosen a generic `Id`.

## Responsibility

Write a concise responsibility statement:

```text
SubscriptionPromotion owns the lifecycle and invariants of applying
one promotion to one subscription.
```

The Entity should own behavior that protects its own state and invariants.

It should not own:

- HTTP parsing;
- authorization orchestration outside its own business state;
- database queries;
- provider SDK calls;
- application workflows;
- DTO mapping;
- transaction management.

## Lifecycle Modeling

Identify:

- initial state;
- valid states;
- transitions;
- transition preconditions;
- state effects;
- terminal states;
- forbidden transitions;
- idempotent transitions, if accepted.

Example:

```text
Draft → Active → Redeemed
Draft → Expired
Active → Expired
Redeemed → no further transition
```

Do not encode lifecycle as unrestricted `setStatus`.

Prefer:

```text
promotion.activate()
promotion.redeem()
promotion.expire()
```

## Invariant Catalog

Classify invariants.

### Creation Invariants

Must hold before an instance can exist.

Examples:

- valid identity;
- required owner;
- positive amount;
- supported initial state;
- non-empty collection when required.

### Transition Invariants

Must hold before state changes.

Examples:

- only active promotions can be redeemed;
- an expired Entity cannot be reactivated;
- a terminal Entity cannot be modified.

### Collection Invariants

Examples:

- duplicate items are forbidden;
- maximum collection size;
- all children belong to the same owner;
- removed items cannot remain active.

### Temporal Invariants

Examples:

- start time precedes end time;
- an operation cannot occur after expiration;
- timestamps are monotonic when required.

### Cross-Object Invariants

Keep inside the Entity only when it has all required domain objects and the rule naturally belongs there.

If the rule requires repositories, provider calls, or orchestration, do not inject Infrastructure into the Entity.

Route to Application or a pure Domain Service as appropriate.

## Construction

Entities must never expose partially valid states.

### Public Constructor

A public assignment-only constructor may be used when:

- every accepted argument directly creates a valid Entity;
- no defaults or semantic creation modes exist;
- no validation beyond already validated Value Objects is required.

### Private Constructor and Named Factories

Use when creation requires:

- validation;
- defaults;
- semantic creation modes;
- generated initial state;
- distinction between new creation and reconstitution.

Example modes:

```text
create(...)
reconstitute(...)
restore(...)
```

Factories should reveal intent.

Do not create factories mechanically when a public assignment-only constructor is sufficient.

### Constructor Responsibility

The constructor should assign state.

Complex validation and semantic decisions should occur before construction, usually in a named factory or private helper.

## New Creation Versus Reconstitution

Distinguish:

### New Creation

Applies creation rules and defaults.

```text
Promotion.create(...)
```

### Reconstitution

Restores an already valid persisted snapshot without replaying “new Entity” defaults.

```text
Promotion.reconstitute(...)
```

Reconstitution must still reject structurally invalid or impossible Domain state according to project policy.

It must not accept raw persistence rows or ORM models directly.

Infrastructure maps persistence data to Domain primitives and Value Objects before reconstitution.

## Rich Behavior

Expose operations that communicate business intent.

Preferred:

```text
order.confirm()
order.addItem(item)
promotion.redeem(at)
subscription.cancel(reason)
```

Avoid:

```text
setStatus(...)
setItems(...)
setExpired(...)
update(data)
```

An operation should:

1. validate its preconditions;
2. preserve invariants;
3. update state atomically within the Entity;
4. return an accepted Domain result, event, or `void` according to policy;
5. reject invalid transitions with the project-approved Domain error model.

## Setters

Public generic setters are forbidden when they allow callers to bypass invariants.

A narrowly scoped private mutation helper may be acceptable internally when it does not expose invalid transitions.

Getters should expose only required information.

Do not create getters mechanically for every private field.

## Collections

Internal mutable collections must remain encapsulated.

Do not return the internal array, set, or map directly.

Allowed strategies:

```text
return a copy
return a readonly view
provide domain-specific query methods
provide controlled add/remove operations
```

Example:

```ts
getItems(): readonly OrderItem[] {
  return [...this.items];
}
```

Or:

```ts
hasItem(id: Id): boolean
itemCount(): number
```

The caller must not be able to mutate Entity state without using Entity behavior.

## Child Objects and Aggregate Scope

Do not treat every nested object as independently mutable.

Clarify:

- which object is the consistency boundary;
- whether children have identity;
- which operations are allowed through the root;
- which invariants span the collection.

Do not invent aggregate rules beyond accepted behavior.

## Equality

Provide identity equality according to local convention.

Example intent:

```text
entity.equals(other)
```

Equality must not compare persistence metadata, timestamps, or all mutable attributes.

Hashing or collection-key behavior must remain consistent with identity semantics when relevant.

## Serialization

Implement `toPrimitives()` only when the repository uses this convention.

It must:

- return primitives or plain objects;
- recursively serialize nested Domain objects;
- preserve Domain meaning;
- remain independent from DTOs, ORM records, and provider types.

It must not:

- contain database column names solely for persistence;
- include ORM decorators;
- return Application DTO classes;
- perform provider mapping;
- contain framework-specific serialization logic.

A scalar Value Object should serialize to its scalar primitive.

A composite Value Object should serialize to a plain object.

## Domain Errors

Use the repository-approved Domain error policy.

Errors should represent invariant or transition violations, not transport status codes.

Avoid:

```text
HttpException
BadRequestException
409 response objects
provider error classes
```

inside Domain.

Application or Infrastructure translates Domain outcomes to transport semantics.

## Domain Events

Use Domain Events only when accepted architecture and behavior require them.

Do not emit events automatically for every mutation.

When used, define:

- event meaning;
- occurrence time;
- payload primitives;
- ownership;
- publication boundary;
- transaction semantics.

Do not publish directly from the Entity through Infrastructure.

## Testing

Test public behavior and invariants.

Do not mock:

- Entities;
- Value Objects;
- Domain Services.

### Required Test Categories

- valid construction;
- invalid construction;
- identity equality;
- each accepted transition;
- each prohibited transition;
- invariant preservation;
- collection encapsulation;
- serialization when applicable;
- reconstitution when applicable;
- regression behavior for evolved Entities.

### Test Style

Prefer:

```text
Given valid Domain objects
When intent-revealing operation executes
Then observable state/result satisfies invariants
```

Avoid asserting private implementation details.

## Evolving an Existing Entity

When adding behavior:

1. characterize current accepted behavior;
2. identify the owning invariant;
3. add one failing public-behavior test;
4. add the smallest intent-revealing operation;
5. preserve existing valid transitions;
6. update serialization only when the Domain shape changes;
7. identify callers relying on anemic setters;
8. remove obsolete mutation paths only after callers migrate.

Do not rewrite the Entity broadly unless required for the accepted slice.

## Anemic Entity Recovery

Signs:

- public setters;
- state changed externally;
- Use Cases duplicate invariant checks;
- controller decides lifecycle;
- Entity is only an interface/type;
- callers replace internal collections.

Recovery sequence:

```text
characterize behavior
→ identify one invariant
→ add intent operation
→ migrate one caller
→ remove bypass path
→ repeat
```

Avoid a big-bang rewrite.

## Boundary Guardrails

Domain Entity must not import:

- Application;
- Infrastructure;
- frameworks;
- HTTP libraries;
- ORM libraries;
- provider SDKs;
- environment/config modules.

Domain may depend on:

- other accepted Domain types;
- Value Objects;
- Domain errors;
- pure Domain Services;
- stable shared Domain contracts.

## Readiness Decision

Use one:

```text
READY_TO_IMPLEMENT_ENTITY
READY_WITH_CONDITIONS
NOT_AN_ENTITY
ROUTE_TO_VALUE_OBJECT
ROUTE_TO_DOMAIN_SERVICE
RETURN_TO_SPECIFICATION
DECISION_REQUIRED
BLOCKED
```

## Output

Use `assets/domain-entity-modeling-report.md`.

## Completion Criteria

- [ ] Entity suitability confirmed.
- [ ] Stable identity and project ID policy resolved.
- [ ] Responsibility and lifecycle defined.
- [ ] Creation, transition, collection, and temporal invariants cataloged.
- [ ] Partially valid construction prevented.
- [ ] Named factories used only when justified.
- [ ] Intent-revealing operations replace generic mutation.
- [ ] Collections remain encapsulated.
- [ ] Equality is identity-based.
- [ ] Serialization is Domain-only and convention-driven.
- [ ] Domain remains independent from Application and Infrastructure.
- [ ] Focused public-behavior tests designed or implemented.
- [ ] Existing callers and migration needs identified.
- [ ] No ORM, DTO, HTTP, provider, or speculative behavior leaked into the Entity.

## References

- Read `references/entity-suitability-and-identity.md` first.
- Read `references/lifecycle-and-invariants.md` to model states and rules.
- Read `references/construction-and-reconstitution.md` for valid creation.
- Read `references/rich-behavior-and-collections.md` for Entity operations.
- Read `references/serialization-errors-and-events.md` when those concerns apply.
- Read `references/entity-testing.md` before completion.
- Read `references/evolving-anemic-entities.md` only for existing or brownfield models.
