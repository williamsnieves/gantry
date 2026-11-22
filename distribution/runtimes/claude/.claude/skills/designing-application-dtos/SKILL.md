---
name: designing-application-dtos
description: Designs stable backend Application Request and Response DTOs composed only of primitives and plain nested data, with explicit mapping to and from Domain types. Use when a Use Case boundary must accept transport-neutral input, expose a stable result contract, flatten or select Domain data, or prevent Entities, Value Objects, ORM rows, provider types, and HTTP objects from leaking across Application boundaries. Do not use to design HTTP schemas directly, implement controllers, create Domain models, return Entities, or invent contract fields not required by accepted consumers.
---

# Designing Application DTOs

## Purpose

Design Application Request and Response DTOs that:

- stabilize a Use Case boundary;
- contain only primitives and plain nested data;
- remain independent from HTTP, frameworks, ORM, and providers;
- map explicitly to and from Domain types;
- expose only fields required by accepted consumers;
- avoid leaking Entities or Value Objects;
- preserve semantic meaning without mirroring internal implementation.

The skill may design or implement DTO types and mapping functions when implementation is explicitly requested.

## Use When

- A Use Case requires a Request DTO.
- A Use Case must return a stable Response DTO.
- Too many primitive parameters need one coherent request object.
- A Domain result must be flattened, selected, nested, or transformed for consumers.
- Existing DTOs contain Entities, Value Objects, ORM rows, provider objects, or HTTP types.
- A Use Case currently returns an Entity.
- The Application contract must remain stable while Domain internals evolve.
- Command/query boundaries need distinct input and output shapes.

## Do Not Use When

- The request is to design an HTTP/OpenAPI schema only.
- The request is to implement a controller.
- The request is to model an Entity or Value Object.
- The accepted Use Case does not need a DTO.
- The requested fields are speculative or unsupported by consumers.
- The DTO would merely duplicate a Domain object wholesale.
- The task is provider mapping or persistence mapping.
- The project policy for request/response boundaries is unresolved.

## Inputs

- Accepted specification or OpenSpec change.
- Backend Rule Applicability Report.
- Backend Vertical Slice Plan.
- Application Use Case design.
- Relevant Domain Entities, Value Objects, and Domain results.
- Accepted consumer needs.
- Public API/event contract when it constrains Application shape.
- Project policy for DTO naming, optionality, dates, enums, pagination, and errors.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted behavior and consuming Use Case.
3. Inspect Domain types and `toPrimitives()` conventions.
4. Inspect current Application DTO naming and structure.
5. Identify accepted consumers and required fields.
6. Confirm policies for:
   - Request object threshold;
   - optional versus nullable fields;
   - date/time representation;
   - enum representation;
   - pagination;
   - versioning;
   - command/query outputs.
7. Distinguish Application DTOs from HTTP, persistence, and provider contracts.
8. Do not derive DTOs automatically from Entities or database rows.

## Outputs

- DTO suitability decision.
- Request and Response responsibilities.
- Primitive/plain field definitions.
- Optionality, nullability, enum, date/time, and nesting semantics.
- Primitive-to-Domain input mapping.
- Domain-to-DTO output mapping.
- Contract stability and compatibility notes.
- Validation ownership.
- Focused mapping test plan.
- Boundary audit.
- Application DTO design report.

## Core Principle

Application DTOs are boundary contracts:

```text
Delivery primitives
→ Request DTO
→ Application mapping
→ Domain

Domain result
→ Application mapping
→ Response DTO
→ Delivery
```

They are not Domain models, persistence rows, provider payloads, or HTTP framework objects.

## Workflow

1. **Confirm DTO need:** Determine whether a Request, Response, or both are justified.
2. **Define contract responsibility:** State what the DTO represents for the Use Case.
3. **Identify accepted fields:** Include only required consumer data.
4. **Choose shape:** Flat or nested based on semantic coherence.
5. **Define primitive types:** Strings, numbers, booleans, nulls, arrays, and plain objects.
6. **Define optionality and nullability:** Make absence semantics explicit.
7. **Define date/time and enum representation:** Follow project policy.
8. **Design input mapping:** Convert Request primitives to Domain types in Application.
9. **Design output mapping:** Convert Domain results to Response primitives explicitly.
10. **Define validation ownership:** Separate transport shape, Application interpretation, and Domain invariants.
11. **Check stability:** Avoid coupling to internal Domain or Infrastructure structure.
12. **Design tests:** Cover mapping, selection, flattening, nesting, optionality, and compatibility.
13. **Audit boundaries:** Reject Domain, ORM, provider, HTTP, and framework leakage.
14. **Report or implement:** Use the Application DTO design report.

## DTO Suitability

### Request DTO

Use when:

- inputs form one semantic request;
- the Use Case accepts several fields;
- boundary stability matters;
- optional/nested data requires explicit semantics;
- project policy requires it.

A direct primitive parameter may remain appropriate for a truly simple intention.

Do not create a Request DTO mechanically for every one-argument Use Case.

### Response DTO

Use when:

- consumers require explicit output;
- Domain data must be selected or transformed;
- internal Domain structure must remain hidden;
- several delivery boundaries share one Application result.

Use `void` when the accepted command has no meaningful response and project policy supports it.

## Primitive-Only Rule

DTOs may contain:

```text
string
number
boolean
null
arrays of DTO-safe values
plain nested objects
```

DTOs must not contain:

- Entities;
- Value Objects;
- Domain Services;
- ORM entities or rows;
- provider SDK objects;
- HTTP request/response types;
- framework decorators unless project policy explicitly treats decorated transport DTOs as a separate delivery model;
- Date objects when policy requires string timestamps.

## Request Design

A Request DTO describes the Application intention, not the HTTP transport.

Good:

```ts
type ApplyPromotionRequest = {
  subscriptionId: string
  campaignId: string
  actorId: string
}
```

Avoid:

```ts
type ApplyPromotionRequest = Request & {
  body: ProviderPayload
  prismaPromotion: PromotionRow
}
```

### Naming

Use intention-focused names:

```text
ApplyPromotionRequest
GetSubscriptionRequest
CancelSubscriptionRequest
```

Avoid generic names such as:

```text
PromotionDto
InputData
Payload
Params
```

unless project policy explicitly uses them.

## Response Design

A Response DTO represents the accepted Application result.

Good:

```ts
type ApplyPromotionResponse = {
  promotionId: string
  subscriptionId: string
  campaignId: string
  status: string
  appliedAt: string
}
```

It should expose only what consumers need.

Do not return the complete Entity merely because `toPrimitives()` exists.

`toPrimitives()` is a Domain serialization aid, not an automatic Application contract.

## Flat Versus Nested Shape

Use flat fields when:

- the result is small;
- consumers need a simple stable shape;
- nesting adds no semantic value.

Use nested plain objects when:

- fields form a meaningful sub-concept;
- repeated structures benefit from grouping;
- the accepted contract is hierarchical.

Example:

```ts
type OrderResponse = {
  id: string
  customer: {
    id: string
    name: string
  }
  total: {
    amount: number
    currency: string
  }
}
```

Do not mirror an aggregate tree automatically.

## Selected and Flattened Fields

DTO mapping may:

- select required fields;
- rename fields for stable Application meaning;
- flatten nested Domain structures;
- combine Domain values;
- derive simple presentation-neutral values;
- exclude internal state.

It must not:

- perform business calculations;
- query repositories;
- call providers;
- introduce transport formatting;
- hide missing accepted behavior.

## Optionality and Nullability

Define each field as one of:

```text
required
optional
nullable
optional and nullable
```

Do not treat them as interchangeable.

### Optional

The field may be omitted.

### Nullable

The field exists but has no value.

Use the repository's accepted semantics.

Document mapping for:

- absent input;
- explicit null;
- missing Domain value;
- unavailable data;
- backward-compatible fields.

## Defaults

Do not hide business defaults inside DTOs.

Defaults may belong to:

- Domain factories;
- Application Use Case;
- delivery parsing;
- project configuration.

A DTO type describes data; it should not silently choose business meaning.

## Enums

Represent enums according to project policy, usually as stable strings.

Define:

- accepted values;
- unknown-value handling;
- compatibility strategy;
- mapping to Domain enum/Value Object.

Do not expose provider enum names directly.

Do not use numeric enum ordinals as stable contracts unless explicitly accepted.

## Date and Time

Follow accepted policy.

Common safe representation:

```text
ISO 8601 string with timezone/offset
```

Define:

- source timezone;
- precision;
- nullability;
- formatting boundary;
- compatibility.

Do not expose host-local `Date` behavior implicitly.

Application mapping should convert Domain time representation into the accepted primitive.

## Numbers, Money, and Precision

Do not flatten Money ambiguously.

Preferred:

```ts
type MoneyDto = {
  amount: number
  currency: string
}
```

or project-approved minor-unit representation.

Document precision and rounding policy from accepted standards.

Do not invent rounding or currency conversion in DTO mapping.

## Identifiers

DTO identifiers are usually primitives:

```text
Id Value Object → string
```

Follow the project identifier policy internally.

Do not expose Value Object instances.

Do not mix multiple identifier formats for the same field without explicit compatibility requirements.

## Input Mapping

Application maps Request DTOs to Domain.

Example:

```text
subscriptionId: string → Id.create(subscriptionId)
campaignId: string → CampaignId/Id according to policy
amount + currency → Money.create(...)
```

Mapping should:

- be explicit;
- fail with Application/Domain semantics;
- preserve normalization policy;
- avoid controller-owned Domain construction unless accepted;
- avoid automatic reflection.

## Output Mapping

Map Domain to Response explicitly.

Example:

```text
promotion.id.toPrimitives() → promotionId
promotion.status → status string
promotion.appliedAt → ISO timestamp
```

Mapping may live:

- inside the Use Case;
- in a focused Application mapper;
- in a DTO factory;
- according to project policy.

Do not place the mapper in Infrastructure solely because DTOs are “external.”

## Mapping Functions

Use focused mapping functions when they improve clarity or reuse.

Examples:

```text
toApplyPromotionResponse(promotion)
toSubscriptionSummary(entity)
```

Avoid universal mappers such as:

```text
mapEntityToDto(entity, options)
```

that hide field selection and semantics.

## Validation Ownership

Separate three levels.

### Delivery Validation

- parse body/query/path;
- basic transport shape;
- content type;
- transport limits.

### Application Interpretation

- convert primitive IDs;
- construct Value Objects;
- interpret optional fields;
- reject invalid request semantics.

### Domain Validation

- invariants;
- lifecycle;
- value rules;
- business eligibility.

Do not duplicate Domain invariants in DTO decorators or schemas as the authoritative rule.

Transport validation may provide earlier feedback but Domain remains authoritative.

## HTTP Separation

An Application DTO is transport-neutral.

If the framework uses decorated HTTP DTO classes, prefer a clear separation:

```text
HTTP request schema/class
→ Application Request DTO
```

unless project policy explicitly merges them and accepts the coupling.

Do not import HTTP status codes, request objects, headers, or decorators into Application by default.

## Provider Separation

Provider request/response payloads belong in Infrastructure.

Map:

```text
Application port request
↔ provider payload
```

Do not reuse provider payloads as Application DTOs.

Provider fields, enums, and errors may change independently.

## Persistence Separation

Database rows and ORM models belong in Infrastructure.

Map:

```text
persistence row
↔ Domain
→ Application Response DTO
```

Do not return rows directly from repositories or Use Cases.

## Public API Contract Reconciliation

Application DTOs may align with a public API when that contract is accepted.

Still distinguish:

- Application meaning;
- HTTP serialization details;
- versioning;
- transport-specific headers/status;
- provider/database representations.

When public API and Domain differ, map explicitly rather than changing Domain to match transport convenience.

## Commands and Queries

When project architecture separates them:

### Command Request

Represents an intention to change state.

### Command Response

May be:

- `void`;
- created ID;
- focused result;
- accepted status.

### Query Request

Contains filters, ordering, pagination, or identity.

### Query Response

Contains selected primitive data or a read model.

Do not impose CQRS when project policy has not adopted it.

## Pagination

Define a stable Application pagination contract.

Example:

```ts
type PageRequest = {
  cursor?: string
  limit?: number
}

type PageResponse<T> = {
  items: T[]
  nextCursor: string | null
}
```

Only use shared generic pagination DTOs when project policy supports them and semantics are truly common.

Define:

- maximum/default limit ownership;
- cursor opacity;
- ordering;
- empty page behavior;
- null versus omitted next cursor.

## Versioning and Compatibility

When DTOs are public or shared:

- add fields compatibly when possible;
- avoid changing meaning in place;
- define deprecated fields;
- preserve stable enum values;
- coordinate consumers;
- version when required.

Do not carry obsolete fields indefinitely without an exit condition.

Application-internal DTOs may evolve more freely but still require coordinated callers.

## Response Errors

DTOs normally model successful Application results.

Errors should follow the project's Application error model.

Do not encode every failure as:

```ts
{ success: false, error: ... }
```

unless that is the accepted Result contract.

Do not include HTTP status codes in Application DTOs.

## Security and Privacy

Include only data required by accepted consumers.

Review:

- sensitive identifiers;
- PII;
- secrets/tokens;
- internal provider references;
- audit metadata;
- authorization-sensitive fields.

Do not expose data because it exists on the Entity.

Output minimization is part of DTO design.

## Mapping Tests

Test:

- valid Request-to-Domain mapping;
- invalid primitive conversion;
- normalization;
- selected fields;
- flattened/nested structures;
- enum conversion;
- date/time serialization;
- optional versus nullable fields;
- Money/precision mapping;
- sensitive/internal field exclusion;
- compatibility cases.

Do not test TypeScript type declarations as runtime behavior without a reason.

## Contract Tests

When DTOs form a shared/public contract, add schema or consumer contract tests according to project tooling.

Verify:

- field names;
- required/optional/nullability;
- enum values;
- date formats;
- nested shape;
- backward compatibility.

Application mapping tests and HTTP contract tests serve different boundaries.

## Existing DTO Refactoring

Warning signs:

- Domain objects inside DTOs;
- Entity returned from Use Case;
- ORM row reused as response;
- provider payload reused as request;
- one DTO used for create/update/read/provider/database;
- decorators mixed into Application;
- giant universal payload.

Incremental recovery:

```text
identify one Use Case boundary
→ define primitive Request/Response
→ add explicit mapping
→ migrate one controller/consumer
→ remove leaked type
→ repeat
```

Avoid repository-wide DTO rewrites unrelated to the accepted slice.

## Generic DTO Bases

Do not create a generic base DTO automatically.

Use shared types only for truly stable common semantics such as accepted pagination or Money primitives.

Avoid inheritance that obscures required fields or compatibility.

## Readiness Decision

Use one:

```text
READY_TO_IMPLEMENT_APPLICATION_DTOS
READY_WITH_CONDITIONS
NO_REQUEST_DTO_REQUIRED
NO_RESPONSE_DTO_REQUIRED
RETURN_TO_USE_CASE_DESIGN
RETURN_TO_SPECIFICATION
DECISION_REQUIRED
BLOCKED
```

## Output

Use `assets/application-dto-design-report.md`.

## Completion Criteria

- [ ] Request and/or Response DTO need confirmed.
- [ ] DTO responsibility tied to one accepted Use Case.
- [ ] Every field is required by accepted consumers.
- [ ] All fields are primitive or plain nested data.
- [ ] Optionality and nullability are explicit.
- [ ] Enum, date/time, identifier, Money, and precision semantics follow policy.
- [ ] Request-to-Domain mapping is explicit.
- [ ] Domain-to-Response mapping is explicit.
- [ ] Domain invariants remain in Domain.
- [ ] HTTP, ORM, provider, and framework types are excluded.
- [ ] Entities and Value Objects do not cross the Application boundary.
- [ ] Sensitive and internal fields are minimized.
- [ ] Mapping and contract tests are planned.
- [ ] Compatibility impact is explicit.
- [ ] No speculative fields, automatic Entity mirroring, or universal mapper introduced.

## References

- Read `references/dto-suitability-and-boundaries.md` first.
- Read `references/request-dto-design.md` for input contracts.
- Read `references/response-dto-design.md` for output contracts.
- Read `references/mapping-and-validation-ownership.md` for conversion rules.
- Read `references/optionality-enums-dates-and-money.md` for field semantics.
- Read `references/compatibility-security-and-testing.md` before completion.
- Read `references/refactoring-leaky-dtos.md` only for existing DTO migrations.
