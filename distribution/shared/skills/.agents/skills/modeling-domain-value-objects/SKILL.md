---
name: modeling-domain-value-objects
description: Portable engineering capability `modeling-domain-value-objects`. Use
  when the harness or a specialist agent explicitly requires this named capability.
---
# Modeling Domain Value Objects

## Purpose

Create or evolve Domain Value Objects that:

- are defined entirely by their attributes;
- have no independent identity or lifecycle;
- are immutable;
- reject invalid state at creation;
- compare by semantic value;
- expose safe operations without side effects;
- serialize to primitives or plain objects;
- remain independent from Application and Infrastructure.

The skill may design or implement the Value Object and focused Domain tests when implementation is explicitly requested.

## Use When

- A primitive carries business meaning and constraints.
- The same validation appears in multiple callers.
- A scalar or composite value must be impossible to represent incorrectly.
- Arithmetic or transformation must preserve domain constraints.
- Equality by value is required.
- Domain logic currently relies on raw strings, numbers, dates, or objects.
- A repository or DTO boundary should map into a stable Domain representation.
- A generic or typed identifier decision has already been established by project policy.

Examples:

```text
Email
Money
Percentage
DateRange
Id
PromotionCode
Currency
Duration
```

## Do Not Use When

- The concept has stable identity and lifecycle and should be an Entity.
- The behavior belongs to a Domain Service spanning multiple objects.
- The object is only a Request/Response DTO.
- The request is to create an ORM column wrapper or provider SDK type.
- The desired constraints are not accepted.
- The identifier strategy is material and unresolved.
- The object must be mutable by design.
- A primitive is sufficiently expressive and has no domain-specific constraints or behavior.

## Inputs

- Accepted specification or OpenSpec change.
- Backend Rule Applicability Report.
- Backend Vertical Slice Plan.
- Existing Domain model and tests.
- Project identifier policy.
- Domain error convention.
- Numeric, currency, date/time, normalization, and serialization policies where applicable.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted behavior and slice.
3. Inspect neighboring Value Objects, Entities, errors, and tests.
4. Confirm project conventions for:
   - private constructors;
   - static factories;
   - equality;
   - `toPrimitives()`;
   - Domain errors;
   - identifiers.
5. Identify normalization rules only when explicitly accepted.
6. Distinguish scalar and composite Value Objects.
7. Do not infer constraints solely from database columns or UI validation.

## Outputs

- Value Object suitability decision.
- Semantic responsibility.
- Attribute model.
- Constraint catalog.
- Factory and normalization strategy.
- Equality semantics.
- Immutable operations.
- Serialization shape.
- Focused Domain tests.
- Risks, unresolved decisions, and follow-up skills.
- Value Object modeling report.

## Core Definition

A Value Object:

```text
has no identity
+ is defined by its attributes
+ is immutable
+ compares by value
```

Two instances are equal when every semantically relevant attribute is equal.

## Workflow

1. **Confirm suitability:** Determine whether the concept is a Value Object.
2. **Define semantic responsibility:** State what domain meaning it represents.
3. **Model attributes:** Identify scalar or composite values and relevant types.
4. **Catalog constraints:** Define accepted and rejected values.
5. **Design construction:** Use private construction and validating factories.
6. **Define normalization:** Apply only accepted canonicalization.
7. **Define equality:** Include every semantically relevant attribute.
8. **Design operations:** Return new valid instances without mutation.
9. **Define serialization:** Scalar primitive or plain composite object.
10. **Design errors:** Use Domain semantics, not transport/provider errors.
11. **Design tests:** Cover construction, equality, immutability, operations, and serialization.
12. **Check boundaries:** Remove DTO, ORM, framework, and SDK concerns.
13. **Review proportionality:** Avoid unnecessary abstractions and generic base classes.
14. **Report or implement:** Use the Value Object modeling report.

## Suitability Test

```text
If the concept has stable identity and lifecycle:
    route to modeling-domain-entities.
Else if it is defined completely by attributes and has domain meaning:
    model a Value Object.
Else if pure behavior belongs to no one object:
    consider designing-domain-services.
Else:
    keep the primitive or return to specification.
```

Do not create a Value Object merely to wrap every primitive.

## Scalar Versus Composite

### Scalar Value Object

Represents one primitive value.

Examples:

```text
Email → string
Percentage → number
Id → string
```

Its `toPrimitives()` returns the scalar.

### Composite Value Object

Represents multiple values that form one semantic unit.

Examples:

```text
Money → amount + currency
DateRange → start + end
Address → street + city + postalCode + country
```

Its `toPrimitives()` returns a plain object.

## Construction

### Private Constructor

Use controlled construction:

```ts
class Email {
  private constructor(readonly value: string) {}

  static create(value: string): Email {
    // validate
    return new Email(value)
  }
}
```

### Assignment-Only Constructor

Constructors assign already validated values.

Do not perform business validation in the constructor.

### Factory Responsibility

Factories:

- validate input;
- normalize only when accepted;
- reject invalid values;
- create valid instances;
- may expose semantic constants or modes.

Examples:

```text
Money.zero(currency)
Percentage.create(value)
DateRange.create(start, end)
```

Invalid state must be unrepresentable through public APIs.

## Constraints

Classify constraints:

### Structural

- non-empty;
- format;
- length;
- valid character set;
- required fields.

### Range

- positive/non-negative;
- minimum/maximum;
- precision;
- supported enum or currency.

### Relational

- start precedes end;
- lower bound does not exceed upper bound;
- amount and currency form a valid combination.

### Semantic

- supported business code;
- valid checksum;
- allowed domain suffix;
- accepted granularity.

Do not place repository lookups or provider validation inside a Value Object.

## Normalization

Normalization changes representation while preserving accepted meaning.

Examples only when accepted:

- trimming surrounding whitespace;
- canonical lowercase for case-insensitive email;
- uppercasing currency code;
- canonical date/time representation.

Normalization must be:

- deterministic;
- side-effect free;
- documented;
- applied before validation when appropriate;
- consistent with equality and serialization.

Do not normalize when case, whitespace, precision, or formatting is semantically relevant.

## Immutability

All properties are `readonly`.

Never expose setters.

Operations never mutate the current instance.

Forbidden:

```ts
add(other: Money): void {
  this.amount += other.amount
}
```

Preferred:

```ts
add(other: Money): Money {
  return Money.create(
    this.amount + other.amount,
    this.currency
  )
}
```

The original instance remains unchanged.

Derived results must satisfy all constraints.

## Equality

Every Value Object implements value equality according to project convention.

```ts
equals(other: Money): boolean {
  return (
    this.amount === other.amount &&
    this.currency === other.currency
  )
}
```

Equality must:

- compare every semantically relevant attribute;
- be type-safe;
- align with normalization;
- remain consistent with serialization;
- not use object reference.

Do not ignore currency, unit, timezone, or other semantic attributes.

## Safe Operations

Operations should express domain meaning and return new instances.

Examples:

```text
Money.add(other)
Money.subtract(other)
Percentage.applyTo(amount)
DateRange.contains(date)
DateRange.overlaps(other)
PromotionCode.normalized()
```

### Compatibility Checks

Operations involving two Value Objects must validate compatibility.

Examples:

- Money currencies must match;
- quantities must use compatible units;
- date/time zones must follow accepted policy;
- ranges must share comparable semantics.

Do not silently convert units or currencies unless an accepted conversion service/policy exists.

## Money

A Money Value Object should define:

- amount representation;
- currency;
- precision/rounding policy;
- valid range;
- arithmetic;
- currency mismatch behavior;
- serialization.

Do not use binary floating-point for money when project policy requires integer minor units or decimal arithmetic.

Do not invent a rounding policy.

## Date and Time Value Objects

Define:

- timezone interpretation;
- inclusivity/exclusivity;
- precision;
- ordering;
- invalid ranges;
- serialization format.

Do not rely on host-local timezone implicitly.

## Identifiers

`Id` is a Value Object.

Use the centrally selected project policy:

```text
generic Id
or
typed identifiers
```

Do not introduce one typed ID locally when the project uses generic `Id`.

Do not collapse typed identifiers to raw strings inside Domain.

Generation may occur in Domain/Application according to project policy, but provider-specific generators must not leak into the Value Object.

## Errors

Use Domain errors representing invalid value semantics.

Avoid:

- HTTP status exceptions;
- ORM validation exceptions;
- provider SDK errors;
- UI validation messages.

Application and delivery layers translate Domain errors.

Error messages or codes should be stable according to project policy.

## Serialization

Every Value Object implements `toPrimitives()` when required by the standard.

### Scalar

```ts
toPrimitives(): string {
  return this.value
}
```

### Composite

```ts
toPrimitives(): {
  amount: number
  currency: string
} {
  return {
    amount: this.amount,
    currency: this.currency
  }
}
```

Serialization must not:

- return DTO classes;
- use database column names solely for persistence;
- expose framework decorators;
- return provider types;
- mutate internal state.

## Generic Base Classes

Do not create a generic `ValueObject<T>` base class automatically.

Use one only when:

- the repository already adopts it;
- it enforces useful shared semantics;
- it does not obscure domain behavior;
- equality and serialization remain correct for composite types.

Avoid inheritance that hides validation, equality, or domain intent.

## Testing

Do not mock Value Objects.

### Required Test Categories

- valid construction;
- invalid construction;
- normalization;
- equality and inequality;
- immutability;
- original instance unchanged;
- valid operations;
- incompatible operations;
- boundary/range cases;
- derived-result validation;
- scalar/composite serialization;
- regression cases.

### Property-Oriented Tests

For mathematically rich Value Objects, consider properties such as:

```text
a.add(zero) equals a
a.add(b) leaves a and b unchanged
equality is reflexive, symmetric, transitive
range construction always enforces start <= end
```

Use property-based testing only when it adds reliable value.

## Evolving Primitive Obsession

Incremental sequence:

```text
identify repeated rule
→ create Value Object
→ add focused tests
→ migrate one boundary
→ migrate Domain/Application callers
→ remove primitive bypasses
```

Do not migrate the entire repository unless required by the accepted change.

Map primitives at Application or Infrastructure boundaries.

## Boundary Guardrails

A Value Object must not import:

- Application;
- Infrastructure;
- HTTP;
- ORM;
- provider SDK;
- UI/framework code;
- environment configuration.

It may depend on:

- Domain errors;
- other accepted Value Objects;
- pure Domain helpers;
- stable shared Domain contracts.

## Readiness Decision

Use one:

```text
READY_TO_IMPLEMENT_VALUE_OBJECT
READY_WITH_CONDITIONS
NOT_A_VALUE_OBJECT
ROUTE_TO_ENTITY
ROUTE_TO_DOMAIN_SERVICE
KEEP_PRIMITIVE
RETURN_TO_SPECIFICATION
DECISION_REQUIRED
BLOCKED
```

## Output

Use `assets/domain-value-object-modeling-report.md`.

## Completion Criteria

- [ ] Value Object suitability confirmed.
- [ ] Semantic responsibility and attributes defined.
- [ ] Constraints cataloged.
- [ ] Private construction and validating factory designed.
- [ ] Invalid state is unrepresentable.
- [ ] Normalization is explicit and accepted.
- [ ] All state is immutable.
- [ ] Operations are side-effect free and return valid instances.
- [ ] Equality includes every semantic attribute.
- [ ] Compatibility checks are explicit.
- [ ] Scalar/composite serialization is correct.
- [ ] Domain errors are transport-independent.
- [ ] Focused tests cover construction, equality, immutability, operations, and serialization.
- [ ] No DTO, ORM, provider, or framework concerns leaked into Domain.
- [ ] No generic abstraction or business constraint invented.

## References

- Read `references/value-object-suitability.md` first.
- Read `references/construction-validation-and-normalization.md` for factories and constraints.
- Read `references/immutability-equality-and-operations.md` for behavior.
- Read `references/money-date-range-and-identifiers.md` when those types apply.
- Read `references/serialization-and-errors.md` for boundary semantics.
- Read `references/value-object-testing.md` before completion.
- Read `references/evolving-primitive-obsession.md` only for existing code migrations.
