---
name: designing-application-use-cases
description: Designs backend Application Use Cases around one user or system intention, with a stable execute boundary, primitive request input, explicit DTO or void output, inward-owned ports, thin orchestration, and Domain behavior delegated to Entities, Value Objects, and Domain Services. Use when an accepted vertical slice needs Application coordination across repositories or external services. Do not use for controllers, infrastructure adapters, generic service classes, multi-intention workflows, direct Use Case chaining, or unresolved business behavior.
---

# Designing Application Use Cases

## Purpose

Design an Application Use Case that represents one explicit user or system intention.

A well-designed Use Case:

- has one intention-revealing responsibility;
- exposes one stable `execute` boundary;
- receives primitives through a Request DTO when appropriate;
- converts boundary primitives into Domain types;
- orchestrates repositories and external-service ports;
- delegates business invariants to Domain objects;
- returns an Application Response DTO or `void`;
- depends only on inward abstractions;
- remains independent from HTTP, ORM, providers, and framework details.

The skill may design or implement the Use Case and its focused tests when implementation is explicitly requested.

## Use When

- A vertical slice requires Application orchestration.
- Several Domain objects, repositories, or provider-neutral ports must collaborate.
- A controller or job currently contains business workflow logic.
- A large “service” class contains several application operations.
- A Use Case receives too many primitives or leaks Domain objects outward.
- Existing Use Cases call other Use Cases directly.
- Concrete adapters are injected into Application.
- Application logic must become independently testable.

## Do Not Use When

- The behavior belongs entirely inside one Entity or Value Object.
- The behavior is a pure cross-object Domain rule.
- The request is to implement an HTTP controller.
- The request is to implement a repository or provider adapter.
- The desired intention contains several independently meaningful operations.
- The accepted behavior or error semantics remain unresolved.
- The request is to design DTOs only.
- The operation is merely a framework lifecycle hook with no Application intention.

## Inputs

- Accepted specification or OpenSpec change.
- Backend Rule Applicability Report.
- Backend Vertical Slice Plan.
- Relevant Domain Entities, Value Objects, Domain Services, and repository ports.
- External collaboration requirements.
- Project policy for Request/Response DTOs, errors, transactions, authorization, and identifiers.
- Existing Use Cases and tests.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted behavior and vertical slice.
3. Inspect the relevant Domain model.
4. Inspect existing repository and external-service ports.
5. Confirm project policies for:
   - `execute` signature;
   - Request/Response DTOs;
   - `void` results;
   - exceptions versus Result;
   - transaction ownership;
   - authorization ownership;
   - identifiers.
6. Inspect neighboring Use Cases and tests.
7. Identify the delivery boundary without importing it into Application.
8. Distinguish Domain behavior from Application orchestration.
9. Do not infer missing business decisions.

## Outputs

- Use Case suitability and intention.
- Responsibility statement.
- Request and Response boundary.
- Primitive-to-Domain conversion plan.
- Required repository and external-service ports.
- Orchestration sequence.
- Transaction, authorization, idempotency, and failure semantics.
- Focused Use Case test plan.
- Boundary and dependency audit.
- Follow-up skills and readiness decision.
- Application Use Case design report.

## Core Principle

One Use Case represents one intention:

```text
ApplyPromotion
CancelSubscription
SendPasswordReset
GenerateInvoice
```

Avoid broad containers:

```text
SubscriptionService
PromotionManager
BillingOperations
```

A Use Case is not merely a class with an `execute` method. Its responsibility must be one coherent Application action.

## Workflow

1. **Confirm Use Case suitability:** Determine whether Application orchestration is required.
2. **Define one intention:** Name the user or system action.
3. **Define entry boundary:** Request DTO, direct primitive, or no input according to policy.
4. **Convert primitives to Domain:** Create IDs and Value Objects at the boundary.
5. **Identify dependencies:** Repository ports, external-service ports, clock, transaction, authorization context.
6. **Define orchestration:** Load, authorize, invoke Domain behavior, collaborate, persist, and return.
7. **Protect Domain ownership:** Move invariants and calculations to Domain.
8. **Prevent Use Case chaining:** Extract shared Domain behavior or lower-level ports instead.
9. **Define output:** Response DTO or `void`, never an Entity by default.
10. **Define error semantics:** Domain/Application meanings independent from transport.
11. **Define transaction and idempotency:** Only where accepted behavior requires them.
12. **Design tests:** Use InMemory repositories and controlled port fakes.
13. **Check boundaries:** No concrete adapters, frameworks, DTO leakage, or HTTP semantics.
14. **Review proportionality:** Keep orchestration thin and avoid speculative dependencies.
15. **Report or implement:** Use the Application Use Case design report.

## Use Case Suitability

```text
If behavior belongs to one Entity:
    route to modeling-domain-entities.
Else if it is immutable value behavior:
    route to modeling-domain-value-objects.
Else if it is a pure cross-object business rule:
    route to designing-domain-services.
Else if it coordinates persistence, external collaboration, authorization, or transactions:
    design an Application Use Case.
Else:
    return to specification or keep the operation simpler.
```

## One Intention Per Use Case

A Use Case should answer:

```text
What user or system intention does this execute?
```

Good:

```text
ApplyPromotionUseCase
ExpirePromotionUseCase
GetActivePromotionUseCase
```

Poor:

```text
PromotionUseCase
ManagePromotionsUseCase
CreateUpdateDeletePromotionUseCase
```

### Split Criteria

Split when operations have different:

- actors;
- authorization;
- transaction boundaries;
- outputs;
- failure semantics;
- lifecycle;
- release value;
- tests;
- external dependencies.

Do not split trivial internal steps that only form one coherent intention.

## Execute Boundary

Follow the project's accepted convention.

Common forms:

```ts
execute(request: ApplyPromotionRequest): Promise<ApplyPromotionResponse>
execute(request: ApplyPromotionRequest): Promise<void>
execute(id: Id): Promise<PromotionResponse>
```

Prefer one Request object when the input is semantically grouped or exceeds the project threshold.

Do not introduce an arbitrary “three arguments means DTO” rule unless project policy says so.

The boundary should remain stable even when internal orchestration evolves.

## Request Inputs

Application Request DTOs should normally contain primitives or plain nested data.

Examples:

```ts
type ApplyPromotionRequest = {
  subscriptionId: string
  campaignId: string
  actorId: string
}
```

Application converts them:

```text
string → Id
string → PromotionCode
number + currency → Money
```

Do not require controllers to construct Domain objects unless the project explicitly adopts that policy.

Do not accept ORM rows, provider SDK objects, or HTTP request types.

## Primitive-to-Domain Conversion

Create Domain types near the Application boundary.

Benefits:

- delivery remains transport-focused;
- Application owns input interpretation;
- Domain receives valid types;
- tests use the same conversion path.

Invalid primitive input should become the project-approved Application/Domain error, not an HTTP response.

## Dependencies

A Use Case may depend on inward ports such as:

- repository ports;
- external-service ports;
- clock;
- ID generator;
- transaction boundary;
- authorization policy/context;
- event publisher port;
- feature-policy port.

Every dependency must be justified by the intention.

Do not inject:

- Prisma/TypeORM repositories;
- HTTP clients;
- provider SDK clients;
- framework loggers;
- controllers;
- other Use Cases.

## Port Ownership

The Application layer owns ports for external collaboration it needs.

The Use Case depends on the interface, not the concrete adapter.

```text
Application Use Case
→ PaymentGateway port
← StripePaymentGateway adapter in Infrastructure
```

Repository ownership follows the project's accepted architecture.

## Orchestration Sequence

A common sequence:

```text
1. validate/construct Domain input
2. load required Domain objects
3. perform application-level authorization
4. invoke Entity/Value Object/Domain Service behavior
5. call external port when required
6. persist aggregate changes
7. publish/record accepted events through a port when required
8. map result to Response DTO or return void
```

Not every Use Case needs every step.

## Thin Orchestration

Application coordinates; Domain decides.

Application may decide:

- what to load;
- in which order;
- which port to call;
- transaction scope;
- which Domain operation to invoke;
- how to map Domain result outward.

Application should not implement:

- Entity lifecycle rules;
- Money arithmetic;
- eligibility formulas;
- domain state mutation through setters;
- provider-specific error parsing.

## Preventing Use Case Chaining

Do not inject one Use Case into another by default.

Bad:

```text
ApplyPromotionUseCase
→ ValidatePromotionUseCase
→ SavePromotionUseCase
```

Problems:

- hidden transaction and authorization boundaries;
- duplicated DTO mapping;
- unclear ownership;
- hard-to-test workflows;
- circular dependencies.

Prefer:

- shared Entity/Value Object behavior;
- Domain Service;
- repository/external port;
- private Application helper for non-independent orchestration;
- explicit higher-level workflow only when architecture accepts it.

If an operation is independently meaningful to an actor, it may remain its own Use Case, but a larger Use Case should not reuse it as an internal library without an explicit orchestration policy.

## Authorization

Clarify where authorization occurs.

### Application-Level Authorization

Use when permission depends on:

- actor identity;
- ownership;
- roles/scopes;
- loaded resource;
- tenant;
- operation.

The delivery layer authenticates and passes trusted actor context according to policy.

The Use Case makes the operation-level authorization decision or calls an inward authorization policy/port.

### Domain Authorization

Only business eligibility intrinsic to Domain state belongs in Domain.

Do not pass HTTP framework principals or token objects into Application.

## Transactions

Define the smallest required atomic boundary.

Record:

- participating repositories;
- external side effects;
- commit point;
- rollback behavior;
- event publication strategy;
- transaction owner.

Do not add a transaction dependency automatically.

A single atomic repository operation may be sufficient.

Avoid holding database transactions open across remote provider calls unless the accepted design explicitly requires and justifies it.

## Idempotency

When repeated invocation can produce harmful side effects, define:

- idempotency key/source;
- authoritative uniqueness;
- duplicate result;
- operation atomicity;
- provider idempotency support;
- retry ownership;
- persisted state.

Do not rely only on frontend disabling or a non-atomic pre-check.

## External Collaboration

The Use Case expresses provider-neutral intention.

Example:

```text
promotionProvider.apply(...)
notificationSender.send(...)
clock.now()
```

Provider-specific request/response/error types remain in Infrastructure.

Use Case handles Application meanings:

```text
PROMOTION_REJECTED
PROVIDER_UNAVAILABLE
DELIVERY_FAILED
```

according to accepted error policy.

## Error Semantics

Use the repository-approved convention:

```text
throw Application/Domain error
return Result<Response, Error>
return explicit decision/result
```

Do not choose a new model locally.

Classify failures:

- invalid input;
- not found;
- unauthorized/forbidden;
- business rejection;
- conflict/duplicate;
- external unavailable;
- persistence failure;
- concurrency conflict;
- unexpected.

Do not return HTTP status codes from Application.

Controllers translate Application outcomes to transport semantics.

## Output

Use Cases should return:

- Response DTO;
- primitive/Value Object only when explicitly accepted;
- `void`.

Do not return Entities by default.

Returning Entities leaks:

- mutable lifecycle behavior;
- internal structure;
- Domain serialization concerns;
- accidental coupling to presentation.

Use explicit Response DTO mapping.

## Mapping

Map explicitly:

```text
Entity/Value Object
→ Response DTO primitives
```

Do not use automatic reflection-based mapping when it hides contract decisions.

Only expose fields required by Application consumers.

Do not serialize the entire Entity because it is convenient.

## Query Use Cases

Query Use Cases may:

- use repositories returning Domain objects;
- use a dedicated read-model port when architecture accepts it;
- map to Response DTOs;
- define ordering and pagination.

Do not force full aggregate loading for a projection when an accepted read-model port exists.

Do not let query optimization leak ORM/query-builder types into Application.

## Commands Versus Queries

When the project adopts command/query separation:

- commands change state and usually return `void`, ID, or a focused result;
- queries return Response DTOs and do not mutate state.

Do not impose CQRS if the repository has not adopted it.

## Clocks, IDs, and Randomness

Use inward ports or explicit resolved values according to project policy.

Examples:

```text
Clock.now()
IdGenerator.next()
RandomSource.generate()
```

Application may call these ports and pass values into Domain factories/services.

Do not call system time, UUID libraries, or randomness directly when determinism and project policy require abstractions.

## Logging and Observability

Do not inject Infrastructure-specific loggers into every Use Case by default.

Application may emit structured events or use an accepted observability port when the project standard requires it.

Do not log sensitive Domain or Request data indiscriminately.

Operational logging often belongs in delivery, middleware, or Infrastructure.

## Feature Flags and Configuration

Use an inward policy/configuration port only when behavior depends on runtime configuration.

Do not read environment variables directly.

Stable accepted Domain policy should preferably be modeled as Domain values or explicit inputs.

## Testing

Use Case tests prove orchestration and observable Application behavior.

Prefer:

- real Entities and Value Objects;
- real Domain Services;
- InMemory repositories;
- controlled fakes/stubs for external ports;
- deterministic clock/ID sources.

### Required Test Categories

- successful intention;
- invalid primitive input;
- not found;
- authorization failure;
- business rejection;
- duplicate/conflict;
- repository failure when meaningful;
- provider failure;
- persistence after successful Domain behavior;
- no persistence after rejected behavior;
- idempotency/retry semantics;
- Response DTO mapping;
- transaction/concurrency cases when applicable.

### Interaction Assertions

Assert interactions only when they are part of Application behavior.

Examples:

- repository save not called after rejection;
- provider called once after eligibility;
- event recorded after persistence.

Avoid asserting incidental call order unless semantically required.

## Fakes Versus Mocks

Use InMemory repositories as real port implementations.

Use focused fakes/stubs for provider-neutral ports.

Avoid mocks that simply reproduce implementation structure.

A fake should expose controllable outcomes and recorded calls without leaking provider types.

## Multi-Step Workflows

A long-running or multi-stage workflow may require:

- process manager;
- saga;
- workflow Use Case;
- job coordination;
- persisted state machine.

Do not squeeze it into one synchronous Use Case if accepted lifecycle is asynchronous.

This requires an explicit architecture decision.

## Existing Application Service Refactoring

Warning signs:

- many unrelated public methods;
- direct adapter imports;
- HTTP/ORM types;
- duplicated Domain rules;
- Entity setters;
- Use Case chaining;
- giant primitive parameter lists;
- inconsistent error mapping.

Incremental recovery:

```text
identify one intention
→ create one Use Case
→ define Request/Response
→ inject ports
→ move Domain behavior inward
→ migrate one controller/job
→ remove obsolete service method
```

Avoid broad rewrites unrelated to the accepted slice.

## Boundary Guardrails

Application Use Case must not import:

- Infrastructure implementations;
- ORM/database drivers;
- HTTP frameworks;
- provider SDKs;
- controllers;
- framework request/response objects;
- environment configuration.

It may depend on:

- Domain;
- Application DTOs;
- repository ports;
- external-service ports;
- accepted Application errors/results;
- transaction/clock/ID ports.

## Readiness Decision

Use one:

```text
READY_TO_IMPLEMENT_USE_CASE
READY_WITH_CONDITIONS
NOT_A_USE_CASE
ROUTE_TO_ENTITY
ROUTE_TO_VALUE_OBJECT
ROUTE_TO_DOMAIN_SERVICE
RETURN_TO_SLICE_PLANNING
RETURN_TO_SPECIFICATION
DECISION_REQUIRED
BLOCKED
```

## Output

Use `assets/application-use-case-design-report.md`.

## Completion Criteria

- [ ] Application orchestration need confirmed.
- [ ] One user/system intention defined.
- [ ] `execute` boundary follows project policy.
- [ ] Request input uses primitives/plain data.
- [ ] Primitive-to-Domain conversion is explicit.
- [ ] Every dependency is an inward port and justified.
- [ ] Domain rules remain in Entities, Value Objects, or Domain Services.
- [ ] No Use Case chaining exists without explicit architecture.
- [ ] Authorization, transactions, idempotency, and external collaboration are explicit where applicable.
- [ ] Output is a Response DTO or `void`, not an Entity by default.
- [ ] Error semantics are transport-independent.
- [ ] Tests use Domain objects, InMemory repositories, and controlled port fakes.
- [ ] No concrete adapter, ORM, HTTP, provider, or environment dependency leaks into Application.
- [ ] No unrelated intention or speculative dependency was added.

## References

- Read `references/use-case-suitability-and-intention.md` first.
- Read `references/execute-boundary-and-inputs.md` for Request design.
- Read `references/orchestration-domain-and-ports.md` for responsibility boundaries.
- Read `references/errors-transactions-and-idempotency.md` when those concerns apply.
- Read `references/output-and-mapping.md` for Response design.
- Read `references/use-case-testing.md` before completion.
- Read `references/refactoring-application-services.md` only for existing service migrations.
