---
name: testing-domain-models
description: Designs and implements pure unit tests for backend Entities, Value Objects, and Domain Services. Use when Domain behavior must be proven through public APIs, including valid and invalid construction, invariants, lifecycle transitions, collection encapsulation, equality, immutability, serialization, and pure calculations. Domain tests must not use databases, HTTP, filesystems, framework containers, infrastructure-controlled timers, external services, adapters, or mocks. Do not use for Application Use Cases, repository adapters, external-service adapters, HTTP endpoints, or implementation-detail assertions.
...
---

# Testing Domain Models

## Purpose

Create focused pure unit tests for:

- Entities;
- Value Objects;
- Domain Services.

The tests must prove observable Domain behavior while remaining independent from every outer layer.

Core rule:

```text
Domain object public API
→ pure input
→ observable Domain outcome
```

No Infrastructure or mocking is required.

## Use When

- Testing Entity construction, lifecycle, invariants, or behavior.
- Testing Value Object validation, equality, immutability, or operations.
- Testing a pure Domain Service.
- Adding regression coverage for a Domain rule.
- Replacing implementation-detail tests with behavioral tests.
- Detecting mocks or Infrastructure dependencies inside Domain tests.
- Building the Domain layer of an inside-out vertical slice.

## Do Not Use When

- Testing a Use Case.
- Testing a repository adapter.
- Testing an external provider adapter.
- Testing HTTP delivery.
- Testing framework wiring.
- The behavior belongs outside Domain.
- The test requires a database, network, filesystem, SDK, container, or mock.
- The test asserts private fields or constructor internals.
- The Domain behavior is still unspecified.

## Inputs

- Accepted Domain behavior.
- Entity, Value Object, or Domain Service implementation/design.
- Domain errors and result conventions.
- Repository test layout and naming conventions.
- Existing Domain fixtures/builders.
- Applicable `AGENTS.md` and backend standards.
- Current TDD progress record when part of an active cycle.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the Domain model public API.
3. Read accepted invariants and transitions.
4. Inspect neighboring Domain tests.
5. Confirm test colocation and command.
6. Identify:
   - valid construction;
   - invalid construction;
   - permitted behavior;
   - rejected behavior;
   - equality;
   - immutability;
   - serialization;
   - collection encapsulation;
   - boundary values.
7. Confirm time/randomness is supplied explicitly.
8. Do not import or mock Infrastructure.

## Outputs

- Domain test inventory.
- Focused unit tests.
- Test data builders or factories when justified.
- Coverage of accepted invariants and behaviors.
- Purity and implementation-detail audit.
- Domain testing record.

## Non-Negotiable Purity

Domain tests must not require:

- database;
- HTTP;
- filesystem;
- external services;
- provider SDKs;
- ORM;
- framework container;
- composition root;
- Infrastructure-controlled timers;
- mocks.

A Domain Service test passes real Domain objects and inspects real Domain values.

## Workflow

1. **Identify the model type:** Entity, Value Object, or Domain Service.
2. **Inventory accepted behavior:** Happy paths, failures, transitions, boundaries.
3. **Choose public entry points:** Factories, methods, operations, and serialization.
4. **Design pure fixtures:** Valid Domain defaults with explicit variations.
5. **Test valid construction:** Observable initial state and behavior.
6. **Test invalid construction:** Domain errors and invalid-state prevention.
7. **Test behavior and transitions:** Allowed and rejected operations.
8. **Test equality and immutability:** Where applicable.
9. **Test collections and serialization:** Encapsulation and primitive output.
10. **Test boundaries:** Time, Money, ranges, empty values, duplicates, limits.
11. **Audit purity:** No outer-layer dependency or mocking.
12. **Audit assertions:** Public behavior, not implementation details.
13. **Run focused and neighboring Domain tests.**
14. **Record evidence:** Use the Domain testing record.

## Entity Tests

Entity tests should cover accepted cases such as:

- valid creation;
- identity;
- default lifecycle state;
- valid transition;
- rejected transition;
- invariant preservation;
- intent-revealing behavior;
- collection additions/removals;
- collection encapsulation;
- serialization;
- reconstitution when part of accepted public behavior;
- terminal states;
- regression cases.

### Test Through Public API

Preferred:

```ts
const promotion = Promotion.create(validProps)

promotion.activate(now)

expect(promotion.status).toBe(PromotionStatus.Active)
```

Avoid:

```ts
expect((promotion as any)._status).toBe("ACTIVE")
```

Do not mutate private state to prepare a case.

Use public factories, reconstitution APIs, or valid builders.

## Entity Identity

Test identity semantics only according to accepted design.

Possible cases:

- same ID means same Entity identity;
- different IDs mean different Entity identity;
- mutable attributes do not redefine identity.

Do not accidentally use deep object equality when the Entity contract defines identity equality.

## Lifecycle Transitions

For each accepted transition test:

```text
Given valid source state
When intent-revealing operation occurs
Then target state and related observable values are correct
```

For rejected transitions:

```text
Given invalid source state
When operation occurs
Then Domain error is produced
And state remains unchanged
```

Test terminal states explicitly when accepted.

## Entity Collections

Verify:

- valid additions/removals;
- duplicate semantics;
- capacity/empty constraints;
- child invariant preservation;
- returned collections cannot mutate Entity state;
- ordering only when Domain behavior defines it.

Do not assert internal array type or storage implementation.

## Value Object Tests

Value Object tests should cover:

- valid factory creation;
- invalid input rejection;
- normalization when accepted;
- equality by semantic value;
- inequality;
- immutability;
- operations return new instances;
- original instance remains unchanged;
- scalar or composite `toPrimitives()`;
- boundary values;
- compatibility checks.

## Equality

Test all semantic attributes.

Example:

```ts
expect(Money.create(10, "EUR").equals(Money.create(10, "EUR"))).toBe(true)
expect(Money.create(10, "EUR").equals(Money.create(10, "USD"))).toBe(false)
```

Do not use reference equality to prove Value Object equality.

## Immutability

For an operation:

```ts
const original = Money.create(10, "EUR")
const result = original.add(Money.create(5, "EUR"))

expect(original.equals(Money.create(10, "EUR"))).toBe(true)
expect(result.equals(Money.create(15, "EUR"))).toBe(true)
expect(result).not.toBe(original)
```

Do not mutate the object or its primitive representation.

## Serialization

Verify the accepted primitive form.

Examples:

```text
Id → string
Money → { amount, currency }
DateRange → { start, end }
Entity → accepted Domain primitives
```

Do not treat serialization tests as permission to expose all Domain state through Application DTOs.

Test that returned composite primitive objects or arrays do not permit mutation of internal Domain state.

## Domain Service Tests

Domain Services use pure unit tests.

Provide:

- real Entities;
- real Value Objects;
- explicit primitive context;
- real pure Domain policies.

Inspect:

- returned Value Objects;
- decisions;
- result types;
- Domain errors;
- output invariants;
- non-mutation of inputs;
- determinism.

Do not inject:

- repositories;
- providers;
- clock adapters;
- SDK clients;
- mocks.

If current time is needed, pass the value explicitly.

## Domain Service Matrices

Table-driven tests are useful for decision matrices.

Example:

```text
promotion status × subscription state × current time
→ eligibility decision
```

Keep each row readable and tied to accepted rules.

Do not hide unrelated rules inside a giant parameter table.

## Pure Calculation Properties

For calculations and allocations test properties such as:

- total is preserved;
- outputs are non-negative;
- compatible currencies/units are enforced;
- ordering is deterministic when defined;
- repeated execution yields equivalent results;
- inputs remain unchanged.

Property-based testing is optional and must follow repository tooling.

Do not introduce it merely because the service is mathematical.

## Error Assertions

Follow the project convention:

- specific Domain error class;
- stable Domain code;
- Result failure;
- explicit decision.

Prefer stable semantic assertions.

Avoid exact error-message assertions unless the message is an accepted contract.

Never assert HTTP status in Domain tests.

## Time

Use explicit fixed Domain time values.

Do not use:

- real clock;
- fake timers for Infrastructure;
- `Date.now()` as an uncontrolled dependency;
- sleep.

Boundary cases may include:

- exact start;
- exact expiration;
- immediately before/after;
- timezone/precision behavior defined by the Domain.

## Randomness and IDs

Provide deterministic IDs or random inputs explicitly.

Do not call uncontrolled generators in tests unless generation itself is the Value Object behavior under test and can be asserted safely.

A test builder should accept explicit IDs for identity-sensitive cases.

## Test Data Builders

Use builders when they reduce noise and preserve valid defaults.

Good builder behavior:

- creates valid Domain objects;
- exposes intention-revealing variations;
- uses deterministic values;
- keeps the active rule visible.

Example:

```ts
aPromotion().active().expiringAt(expiry).build()
```

Avoid:

- giant universal builders;
- hidden invalid defaults;
- automatic current time;
- random identifiers;
- builders that mutate private fields;
- builders that reproduce Domain logic.

## Test Naming

Name tests by behavior.

Preferred:

```text
creates an active promotion with valid conditions
rejects redemption when promotion is expired
returns a new Money value when adding compatible currency
```

Avoid:

```text
test create
works
method should return true
```

## Arrange, Act, Assert

Keep behavior visible.

```text
Arrange valid Domain state
Act through one public operation
Assert observable Domain outcome
```

Several assertions are acceptable when they describe one coherent behavior.

Do not split every field into a separate test mechanically.

## Implementation-Detail Assertions

Avoid assertions against:

- private fields;
- constructor calls;
- internal helper calls;
- exact collection implementation;
- method invocation counts inside Domain;
- internal event arrays unless events are public accepted behavior;
- serialization implementation mechanism.

Tests should survive safe refactoring.

## Mocks Are Forbidden

Do not mock Entities, Value Objects, or Domain Services.

Do not use mocking libraries merely to construct Domain tests.

If a Domain object appears to require a repository or provider mock, the production design likely contains Infrastructure leakage.

Route that issue to the appropriate modeling skill.

## Colocation

Follow the repository convention that tests belong inside the business module rather than one repository-wide technical folder.

Example:

```text
promotion/
  domain/
  tests/
    unit/
      Promotion.test.ts
      Money.test.ts
      PromotionEligibilityPolicy.test.ts
```

Exact topology follows the repository.

## Coverage Strategy

Aim for behavioral confidence, not raw percentage.

Prioritize:

1. invariants;
2. lifecycle transitions;
3. rejection paths;
4. boundary values;
5. equality/immutability;
6. serialization/collections;
7. regressions.

Do not write low-value getter tests to inflate coverage.

## Mutation Testing

Use mutation testing only when repository tooling supports it and risk justifies it.

It can reveal weak assertions around invariants and calculations.

Do not make mutation tooling a mandatory local prerequisite unless project policy says so.

## Regression Tests

A regression test must reproduce the prior failure through public behavior.

Prefer:

```text
Given the smallest valid reproduction
When the public operation runs
Then the corrected Domain outcome occurs
```

Do not encode the old implementation structure.

## Reconstitution Tests

Test reconstitution when:

- it is an accepted Domain public API;
- persistence mapping relies on it;
- legacy compatibility or invalid persisted state matters.

Cover:

- valid reconstructed state;
- invalid impossible state;
- identity;
- lifecycle fields;
- nested Value Objects.

Do not duplicate every repository mapping case in Domain tests.

## Invalid Partial Construction

Verify invalid states cannot be constructed through public APIs.

Examples:

- missing required attributes;
- invalid Value Object;
- inconsistent lifecycle timestamps;
- empty required collection;
- incompatible Money.

Do not test TypeScript compile-time impossibilities as runtime behavior unless runtime inputs can reach them.

## Test Execution

Run:

1. active/focused test file;
2. Domain unit suite for the module;
3. relevant broader unit suite;
4. typecheck/lint according to change and repository policy.

Record exact commands.

Do not claim unexecuted tests passed.

## Failure Classification

Use:

```text
PRODUCT_FAILURE
TEST_FAILURE
TEST_SETUP_FAILURE
FLAKY_TEST
TOOLING_BLOCKED
UNAVAILABLE_TEST_CAPABILITY
```

Domain tests should not normally be environment blocked. A database/network requirement indicates incorrect test design or production leakage.

## Purity Audit

Before completion confirm the tests do not import:

- Infrastructure paths;
- Application Use Cases;
- repository implementations;
- external adapters;
- HTTP/framework modules;
- composition factories;
- mocking libraries without a justified unrelated test utility.

Static import checks may enforce this.

## Readiness Decision

Use one:

```text
DOMAIN_TESTS_COMPLETE
DOMAIN_TESTS_COMPLETE_WITH_CONDITIONS
MORE_DOMAIN_CASES_REQUIRED
RETURN_TO_DOMAIN_MODELING
RETURN_TO_SPECIFICATION
TEST_HARNESS_REPAIR_REQUIRED
BLOCKED
```

## Output

Use `assets/domain-testing-record.md`.

## Completion Criteria

- [ ] Model type and accepted behavior identified.
- [ ] Tests are pure units with no Infrastructure or mocks.
- [ ] Public APIs are used for setup, action, and assertion.
- [ ] Valid and invalid construction are covered where applicable.
- [ ] Invariants and transitions are covered.
- [ ] Value equality and immutability are covered where applicable.
- [ ] Collections and serialization are covered where applicable.
- [ ] Domain Services use real Domain inputs and outputs.
- [ ] Time and randomness are deterministic and explicit.
- [ ] Assertions target semantic behavior, not implementation details.
- [ ] Tests are colocated according to repository convention.
- [ ] Focused and relevant neighboring tests were executed.
- [ ] Failure or blocked evidence is classified honestly.
- [ ] No low-value speculative tests or mock-based Domain design was introduced.
