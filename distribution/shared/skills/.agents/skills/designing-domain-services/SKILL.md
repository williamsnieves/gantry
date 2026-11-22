---
name: designing-domain-services
description: Designs pure backend Domain Services for business behavior that spans multiple Entities or Value Objects and does not naturally belong to a single Domain object. Use when accepted domain logic requires coordination or calculation across Domain objects without repositories, provider calls, transactions, frameworks, or application orchestration. Produces service responsibility, inputs, outputs, invariants, operation semantics, error behavior, tests, and boundary checks. Do not use for Use Cases, Infrastructure services, repositories, provider adapters, mutable state holders, generic utility classes, or behavior that belongs inside an Entity or Value Object.
...
---

# Designing Domain Services

## Purpose

Design a pure Domain Service that represents business behavior which:

- belongs to the Domain;
- spans multiple Domain objects or concepts;
- does not naturally belong to one Entity or Value Object;
- is deterministic and side-effect free;
- depends only on Domain types and explicit primitive inputs;
- returns Domain results without performing I/O;
- remains independent from Application and Infrastructure.

The skill may design or implement the service and its focused Domain tests when implementation is explicitly requested.

## Use When

- A business rule requires several Entities or Value Objects.
- A pure calculation belongs to no single Domain object.
- The same cross-object business rule is duplicated in multiple Use Cases.
- Putting the rule in one Entity would give that Entity unnatural responsibility.
- Accepted behavior requires a Domain policy, evaluator, matcher, calculator, selector, or allocator.
- A rule requires explicit domain context such as a date, rate, policy, or collection that can be passed as input without I/O.

Examples:

```text
PromotionEligibilityPolicy
DiscountCalculator
AllocationPolicy
PricingPolicy
ScheduleConflictDetector
CommissionCalculator
```

## Do Not Use When

- The behavior belongs naturally to one Entity or Value Object.
- The behavior is application orchestration.
- The operation must load or save data.
- The operation calls an external provider.
- The operation owns transaction boundaries.
- The operation is an HTTP, event, job, or framework service.
- The requested object is only a generic utility.
- The service would be stateless but merely wrap one Entity method.
- The business rule is unresolved or speculative.

## Inputs

- Accepted specification or OpenSpec change.
- Backend Rule Applicability Report.
- Backend Vertical Slice Plan.
- Relevant Entities, Value Objects, Domain errors, and tests.
- Project Domain result/error conventions.
- Time, currency, precision, and policy decisions where applicable.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted behavior and relevant vertical slice.
3. Inspect affected Entities, Value Objects, and existing Domain Services.
4. Confirm the behavior does not belong naturally to one Domain object.
5. Identify every required input explicitly.
6. Identify whether any required information would need I/O.
7. Separate pure Domain policy from Application orchestration.
8. Confirm Domain error and result conventions.
9. Do not introduce repositories, providers, transactions, or framework dependencies.

## Outputs

- Domain Service suitability decision.
- Responsibility statement.
- Domain inputs and outputs.
- Preconditions and invariants.
- Operation semantics.
- Determinism and side-effect analysis.
- Error/result model.
- Service statelessness decision.
- Focused test plan.
- Boundary audit.
- Follow-up skills and readiness decision.
- Domain Service design report.

## Core Definition

A Domain Service is appropriate when:

```text
business behavior
+ spans several Domain objects or concepts
+ belongs to no single Entity/Value Object
+ requires no I/O
= Domain Service
```

A Domain Service is not a general-purpose “service layer.”

## Workflow

1. **Confirm service suitability:** Prove the behavior cannot live naturally in one Entity or Value Object.
2. **Define responsibility:** State one clear domain responsibility.
3. **Identify inputs:** Use Domain objects, Value Objects, or explicit primitives.
4. **Identify outputs:** Return Domain objects, Value Objects, decisions, or pure result types.
5. **Catalog preconditions and invariants:** Define accepted and rejected cases.
6. **Design operation semantics:** Use intent-revealing method names.
7. **Ensure purity:** Remove I/O, mutable hidden state, clocks, randomness, and environment access.
8. **Inject explicit context:** Pass time, rates, policies, or thresholds as inputs when accepted.
9. **Define errors/results:** Use Domain semantics.
10. **Design tests:** Cover deterministic behavior, boundaries, combinations, and non-mutation.
11. **Check proportionality:** Avoid a service when an Entity/Value Object operation is simpler.
12. **Check boundaries:** Confirm Domain-only dependencies.
13. **Report or implement:** Use the Domain Service design report.

## Suitability Test

```text
If one Entity owns the state and invariant:
    put behavior on that Entity.
Else if one Value Object fully owns the value semantics:
    put behavior on that Value Object.
Else if pure behavior spans multiple Domain objects:
    use a Domain Service.
Else if repositories/providers/transactions are required:
    use an Application Use Case plus ports.
Else:
    return to specification/domain analysis.
```

## Responsibility

A Domain Service should have one intention-revealing responsibility.

Good:

```text
PromotionEligibilityPolicy
DiscountAllocationPolicy
ScheduleConflictDetector
```

Weak:

```text
DomainService
PromotionService
BusinessLogicHelper
CommonUtils
```

The name should reveal the business capability or decision.

## Inputs

Prefer explicit Domain inputs.

Examples:

```text
Promotion
Subscription
Money
DateRange
CurrentTime
EligibilityContext
```

### Explicit Context

If a rule depends on current time, pass it:

```ts
policy.evaluate(promotion, subscription, now)
```

Do not call the system clock inside Domain.

If a rule depends on exchange rates or external configuration, the actual provider lookup belongs outside Domain.

The Domain Service may receive an already resolved Domain value:

```ts
calculator.calculate(basePrice, rate)
```

## Outputs

Possible outputs:

```text
Value Object
Entity or updated copy, when accepted
Domain decision enum
Domain result type
Domain policy outcome
collection of Domain allocations
```

Avoid returning:

- HTTP responses;
- Application DTOs;
- ORM models;
- provider SDK objects;
- framework result wrappers;
- untyped dictionaries when a Domain type is appropriate.

## Purity

A Domain Service should be deterministic for the same inputs.

It must not:

- access repositories;
- call providers;
- read environment variables;
- use global mutable state;
- publish events directly;
- open transactions;
- call the system clock implicitly;
- generate uncontrolled random values;
- mutate input objects unexpectedly.

### Randomness

When accepted Domain behavior requires randomness, pass a deterministic Domain abstraction or resolved value according to project policy.

Do not hide random generation inside a static helper.

## Statelessness

Domain Services are normally stateless.

Allowed constructor dependencies are other pure Domain collaborators or immutable accepted policy configuration.

Do not inject:

- repositories;
- HTTP clients;
- loggers tied to Infrastructure;
- ORM clients;
- message buses;
- environment/config services.

If the service stores mutable state across calls, reconsider whether it is actually an Entity or Application service.

## Entity Mutation

Prefer operations that:

- call Entity behavior;
- return a decision;
- return new Value Objects;
- return a Domain result.

A Domain Service must not bypass Entity invariants by mutating private state.

If it coordinates state changes across several Entities without persistence, it should invoke their public intent-revealing methods.

Persistence and transaction coordination remain in Application.

## Invariants and Preconditions

Classify:

### Input Preconditions

- required Domain objects;
- compatible units/currencies;
- valid lifecycle states;
- valid temporal context.

### Cross-Object Invariants

- promotion belongs to the subscription plan;
- allocations sum to the available amount;
- schedules do not overlap;
- commission participants are eligible.

### Output Invariants

- no negative amount;
- allocation totals remain exact;
- result uses compatible currency;
- decision is exhaustive.

## Errors and Results

Use the repository-approved Domain convention.

Possible approaches:

```text
throw Domain error
return Result<DomainValue, DomainError>
return explicit decision enum
```

Do not choose a new error architecture locally.

Errors should describe domain meaning:

```text
INCOMPATIBLE_CURRENCY
PROMOTION_NOT_ELIGIBLE
ALLOCATION_EXCEEDS_AVAILABLE_AMOUNT
```

Not:

```text
HTTP_400
DATABASE_ERROR
PROVIDER_TIMEOUT
```

## Static Function Versus Service Class

Use a pure function when:

- the repository accepts functional Domain design;
- there is one simple operation;
- no service identity or policy grouping is needed.

Use a service class when:

- several related pure operations form one domain policy;
- project convention prefers classes;
- named construction/configuration improves intent.

Do not create a class only because the word “service” appears in the roadmap.

## Policy Configuration

Immutable accepted policy may be provided through:

- Value Objects;
- explicit constructor parameters;
- method inputs;
- named policy objects.

Examples:

```text
maximum discount percentage
allocation strategy
business calendar
rounding policy
```

Configuration must be domain-defined and deterministic.

Environment lookup and remote policy retrieval happen outside Domain.

## Time

Pass time explicitly as:

- a Domain Value Object;
- a primitive timestamp/date according to project policy;
- an Application-provided clock result.

This makes tests deterministic and avoids hidden dependency.

Do not introduce a Domain service that calls `Date.now()` internally.

## Collections

When processing collections:

- do not mutate caller-owned arrays;
- preserve deterministic ordering when behavior requires it;
- define duplicate semantics;
- define empty-collection behavior;
- define precision/aggregation rules;
- return readonly or copied results.

## Arithmetic and Precision

For Money, percentages, allocations, or rates:

- use accepted Value Objects;
- define currency/unit compatibility;
- apply accepted precision and rounding policy;
- preserve total invariants;
- test boundaries and accumulation.

Do not invent rounding, floating-point, or conversion policy.

## Domain Events

A Domain Service may produce a Domain event description only when accepted architecture requires it.

It must not publish the event.

Application or Infrastructure handles publication and transaction semantics.

## Testing

Do not mock Domain objects or the Domain Service.

### Required Test Categories

- accepted happy paths;
- every business rejection;
- combinations of Domain inputs;
- boundary values;
- empty/duplicate collections;
- time boundaries;
- currency/unit incompatibility;
- output invariants;
- deterministic repeated execution;
- input non-mutation;
- regression cases.

### Table-Driven Tests

Use table-driven tests for policy matrices when they improve clarity.

Example:

```text
promotion state × subscription state × date → eligibility decision
```

### Property-Oriented Tests

For allocation/calculation services, consider:

- totals are preserved;
- outputs are non-negative;
- ordering is deterministic;
- repeated execution yields equal results;
- inputs remain unchanged.

## Avoiding Application Leakage

A Domain Service must not:

- fetch a Subscription;
- authorize a caller;
- save an Entity;
- call a payment API;
- retry a provider;
- map HTTP errors;
- manage a transaction;
- coordinate logging/metrics.

An Application Use Case performs those actions and invokes the Domain Service with resolved Domain inputs.

## Avoiding Anemic Entities

Do not move behavior into a Domain Service merely to keep Entities as data bags.

If one Entity clearly owns an invariant or transition, place behavior there.

Bad:

```text
PromotionDomainService.redeem(promotion)
```

when `Promotion.redeem()` naturally owns the transition.

Good:

```text
PromotionEligibilityPolicy.evaluate(promotion, subscription, now)
```

when eligibility spans both concepts.

## Existing Service Refactoring

Signs of an impure or oversized Domain Service:

- repository/provider dependencies;
- transaction handling;
- DTO mapping;
- broad unrelated methods;
- mutable internal cache;
- HTTP errors;
- direct field mutation;
- duplicated Entity invariants.

Incremental recovery:

```text
characterize behavior
→ separate pure decision
→ move owned invariants into Entities/Value Objects
→ move I/O orchestration into Use Case
→ retain one focused Domain policy
→ remove obsolete service methods
```

## Boundary Guardrails

Domain Service must not import:

- Application;
- Infrastructure;
- ORM;
- HTTP frameworks;
- provider SDKs;
- environment/config services;
- message buses;
- Infrastructure loggers.

It may depend on:

- Entities;
- Value Objects;
- Domain errors/results;
- pure Domain policies;
- stable shared Domain contracts.

## Readiness Decision

Use one:

```text
READY_TO_IMPLEMENT_DOMAIN_SERVICE
READY_WITH_CONDITIONS
NOT_A_DOMAIN_SERVICE
ROUTE_TO_ENTITY
ROUTE_TO_VALUE_OBJECT
ROUTE_TO_APPLICATION_USE_CASE
RETURN_TO_SPECIFICATION
DECISION_REQUIRED
BLOCKED
```

## Output

Use `assets/domain-service-design-report.md`.

## Completion Criteria

- [ ] Domain Service suitability confirmed.
- [ ] One focused business responsibility defined.
- [ ] Inputs and outputs use Domain semantics.
- [ ] Cross-object invariants and preconditions cataloged.
- [ ] Operation is deterministic and side-effect free.
- [ ] Time, randomness, rates, and policy context are explicit.
- [ ] No repositories, providers, transactions, or framework dependencies exist.
- [ ] Entity invariants remain on the owning Entity.
- [ ] Result/error semantics follow project policy.
- [ ] Input collections and Domain objects are not mutated unexpectedly.
- [ ] Focused tests cover behavior, boundaries, determinism, and invariants.
- [ ] No generic service, helper, or speculative abstraction introduced.
