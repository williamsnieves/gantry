---
name: testing-application-use-cases
description: Designs and implements focused tests for backend Application Use Cases using real Domain objects, contract-faithful InMemory repositories, and explicit stubs or spies for external-service ports. Use when orchestration, primitive-to-Domain conversion, authorization, missing state, Domain delegation, persistence outcomes, response DTOs, idempotency, transactions, or external side-effect failures must be verified. Prefer observable state and result verification over incidental interaction assertions. Do not use repository mocks as a substitute for InMemory implementations, mock Entities or Value Objects, call real databases or providers, or test HTTP and Infrastructure details.
---

# Testing Application Use Cases

## Purpose

Create focused tests for Application Use Cases.

A correct Use Case test proves:

- one Application intention;
- primitive or Request DTO input interpretation;
- conversion into Domain types;
- repository loading and persistence through contract-faithful InMemory implementations;
- Domain behavior through real Entities, Value Objects, and Domain Services;
- provider-neutral external collaboration through explicit stubs or spies;
- authorization, conflicts, idempotency, and side-effect ordering;
- Response DTO or `void` output;
- state and observable outcome rather than implementation structure.

## Core Test Boundary

```text
Application Request
→ Use Case
→ real Domain behavior
→ InMemory repositories
→ explicit external-port doubles
→ observable result and state
```

No real database, provider SDK, HTTP framework, controller, or composition root is required.

## Use When

- Testing an Application Use Case.
- Testing primitive-to-Domain conversion.
- Testing orchestration across repositories and external-service ports.
- Testing not-found, authorization, business rejection, conflict, or duplicate behavior.
- Testing persistence after accepted Domain behavior.
- Testing no persistence after rejection or external failure.
- Testing Response DTO mapping.
- Testing idempotency or side-effect ordering.
- Replacing repository mocks with InMemory repositories.
- Replacing provider SDK mocks with provider-neutral port doubles.
- Adding a regression test around Application orchestration.

## Do Not Use When

- Testing Entities, Value Objects, or Domain Services in isolation.
- Testing a real repository adapter.
- Testing a provider SDK or HTTP protocol.
- Testing a controller or endpoint.
- Testing composition or startup lifecycle.
- The Use Case contract or side-effect semantics are unresolved.
- The test uses a concrete Infrastructure adapter.
- The test mocks Domain objects.
- The test asserts private implementation details or every method call.

## Inputs

- Accepted Use Case behavior.
- Application Request and Response DTOs.
- Repository and external-service ports.
- InMemory repository implementations.
- Real Domain Entities, Value Objects, and Domain Services.
- Application error/result conventions.
- Authorization, transaction, idempotency, and ordering policies.
- Existing Use Case tests and test builders.
- Applicable `AGENTS.md` and backend standards.
- Current TDD progress record when part of an active cycle.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the Use Case public `execute()` contract.
3. Read accepted orchestration and failure semantics.
4. Inspect repository ports and their InMemory implementations.
5. Inspect external-service ports and existing test doubles.
6. Inspect real Domain behavior used by the Use Case.
7. Confirm Request/Response DTO mapping.
8. Confirm authorization, idempotency, transaction, and side-effect ordering.
9. Discover the narrowest relevant test command.
10. Do not infer missing behavior from the implementation.

## Outputs

- Use Case behavior inventory.
- InMemory repository setup.
- Explicit provider-neutral stubs/spies.
- Focused Use Case tests.
- State/outcome verification.
- Interaction assertions only where semantically required.
- Test execution evidence.
- Application Use Case testing record.

## Testing Strategy

Default collaborators:

```text
Domain objects
→ real

Domain Services
→ real

Repositories
→ InMemory implementations

External-service ports
→ explicit stubs/spies/fakes

Clock / ID generator
→ deterministic port doubles
```

Forbidden substitutes:

```text
mock Entity
mock Value Object
mock Domain Service
mock repository interface instead of existing InMemory
real database
real provider SDK
HTTP controller
composition root
```

## Workflow

1. **Confirm the intention:** Identify the single Use Case behavior under test.
2. **Inventory cases:** Success, missing state, authorization, rejection, conflict, side effects, output, and regression cases.
3. **Build valid Domain state:** Use public factories/builders and explicit deterministic values.
4. **Seed InMemory repositories:** Match repository contract semantics.
5. **Configure external-port doubles:** Explicit semantic outcomes and recorded calls.
6. **Execute through the public boundary:** Call `execute(request)`.
7. **Verify result:** Response DTO, `void`, or semantic error/result.
8. **Verify state:** Persisted aggregates and repository-visible outcomes.
9. **Verify meaningful interactions:** Only where behavior depends on whether/when a port was called.
10. **Verify negative side effects:** No save/call after earlier rejection.
11. **Verify deterministic behavior:** Fixed time, IDs, idempotency keys, and ordered data.
12. **Audit boundaries:** No Infrastructure, SDK, HTTP, or Domain mocks.
13. **Run focused and neighboring tests.**
14. **Record evidence:** Use the Application Use Case testing record.

## Behavior Inventory

Consider applicable cases:

- successful intention;
- invalid primitive input;
- missing Entity or aggregate;
- unauthenticated or forbidden actor;
- Domain business rejection;
- duplicate/conflict;
- concurrency/version conflict;
- repository failure with Application meaning;
- external provider rejection;
- external unavailable/timeout;
- idempotent replay;
- transaction/side-effect ordering;
- persistence after success;
- no persistence after failure;
- Response DTO mapping;
- regression.

Do not create cases not supported by accepted behavior.

## Prefer State Verification

Primary assertions should inspect observable outcomes.

Examples:

```text
Use Case response
persisted aggregate state
repository query result
recorded Domain outcome
semantic Application error
```

Prefer:

```ts
await useCase.execute(request)

const saved = await promotionRepository.findById(promotionId)
expect(saved?.status).toBe(PromotionStatus.Applied)
```

over:

```ts
expect(promotionRepository.save).toHaveBeenCalledTimes(1)
```

when persisted state is the real behavior.

## Interaction Verification

Interaction assertions are valid when the interaction itself is semantically relevant.

Examples:

- provider is not called after Domain rejection;
- repository is not saved after provider failure;
- provider receives the accepted idempotency key;
- event publisher is called only after successful persistence;
- external port is called once for one accepted command.

Avoid asserting:

- every repository read;
- exact incidental call order;
- internal helper calls;
- constructor behavior;
- implementation-specific branching.

## InMemory Repositories

Use contract-faithful InMemory implementations.

They should support accepted semantics such as:

- seed data;
- lookup;
- save/replace by identity;
- query behavior;
- absence;
- duplicates/conflicts;
- ordering;
- failure simulation when explicitly supported.

Do not replace them with:

```ts
const repository = {
  findById: jest.fn(),
  save: jest.fn(),
}
```

when an accepted InMemory implementation exists.

## Why Avoid Repository Mocks

Repository mocks often:

- duplicate implementation details;
- permit impossible states;
- hide save/replace semantics;
- omit query behavior;
- make state verification difficult;
- couple tests to call order;
- diverge from real and InMemory contracts.

Use InMemory state as the observable test surface.

## InMemory Test Isolation

Each test should receive a fresh repository instance or explicitly reset state.

Do not share mutable InMemory repositories across tests.

Seed only the data required by the case.

Avoid hidden global fixtures.

## Failure Simulation

When the InMemory repository contract includes controlled failure support, use it for meaningful Application cases.

Examples:

- persistence unavailable;
- conflict on save;
- optimistic concurrency failure.

Do not turn the InMemory implementation into a generic mocking framework.

If technical database failure behavior is the subject, use repository-adapter integration tests instead.

## External-Port Doubles

External collaborations use explicit provider-neutral doubles.

### Stub

Returns a configured semantic result or failure.

```ts
const campaignProvider = new StubCampaignProvider({
  result: { status: "APPLIED", externalReference: "ext-1" },
})
```

### Spy

Records accepted Application-level calls.

```ts
expect(campaignProvider.calls).toEqual([
  {
    subscriptionId,
    campaignId,
    idempotencyKey,
    tenantId,
  },
])
```

### Fake

Implements minimal deterministic provider-neutral behavior when useful.

Do not import provider SDK request/response types.

## Double Design

A good double:

- implements the port;
- accepts semantic configuration;
- exposes deterministic outcomes;
- records neutral calls when needed;
- does not reproduce the provider protocol;
- does not contain business rules;
- does not silently default to success.

Avoid universal doubles with many unrelated options.

## Real Domain Objects

Use real:

- Entities;
- Value Objects;
- Domain Services;
- Domain errors/results.

Do not mock them to force Use Case branches.

Build valid state through public Domain APIs.

The Use Case test should fail when Domain behavior changes incorrectly.

## Primitive-to-Domain Conversion

Test accepted boundary conversion.

Examples:

- string → `Id`;
- amount/currency → `Money`;
- timestamp string → accepted Domain time representation;
- enum string → Domain value;
- invalid primitive → semantic Application/Domain failure.

The controller is not required.

Call the Use Case with primitives or its Request DTO.

## Invalid Input

Test invalid primitive values that can reach Application.

Do not duplicate every transport-shape case.

Examples:

- malformed ID accepted by Request type but rejected during Domain conversion;
- unsupported enum value;
- invalid Money amount/currency;
- inconsistent optional fields.

HTTP-required/JSON-shape validation belongs to controller tests.

## Missing State

Use an empty or selectively seeded InMemory repository.

Verify:

- semantic not-found result/error;
- later collaborators are not called;
- no save occurs;
- no unrelated state changes.

Do not configure a repository mock to throw merely because absence exists.

## Authorization

Use trusted actor/tenant primitives in the Request.

Seed ownership/tenant state.

Verify:

- allowed actor succeeds;
- forbidden actor receives the accepted semantic failure;
- provider and save are not called after denial;
- body-supplied spoofing is not part of the Use Case test unless the Application contract explicitly includes it.

Authentication transport belongs to HTTP tests.

## Domain Delegation

Verify observable outcomes, not that a specific Domain method was called.

The test should prove that accepted Domain rules influence the Use Case.

Avoid mocking a Domain Service only to assert invocation.

Use the real policy and build cases that expose its result.

## Business Rejection

Examples:

- expired promotion;
- invalid lifecycle state;
- incompatible Money;
- eligibility denied.

Verify:

- semantic error/decision;
- no provider call if rejection occurs before collaboration;
- no save if state must remain unchanged;
- persisted state remains unchanged.

## Side-Effect Ordering

When accepted behavior depends on order, test through outcomes.

Example:

```text
eligibility
→ provider command
→ persistence
```

Cases:

- Domain rejection: provider and save absent;
- provider rejection: save absent;
- provider accepted: save occurs;
- persistence fails after provider acceptance: accepted recovery/error semantics are produced.

Do not assert exact call order unless it is the only observable way to prove a critical contract.

## External Failure Cases

Test semantic failures exposed by the port:

- rejected;
- rate limited;
- unavailable;
- timeout;
- duplicate/idempotent success;
- pending;
- unknown external failure.

Do not test HTTP status or provider error codes.

Those belong to adapter tests.

## Idempotency

When applicable, verify:

- Request carries the accepted idempotency key;
- same key is passed to the port;
- duplicate/idempotent success maps correctly;
- state is not duplicated;
- repeated execution has the accepted outcome;
- no new key is generated unexpectedly.

Do not claim concurrency safety solely from an InMemory test when authoritative protection belongs to real persistence.

## Transactions and Partial Failure

Use Case tests may prove semantic orchestration around accepted transaction ports or Unit of Work doubles.

Test:

- success commits;
- failure rolls back according to the port contract;
- external side effects are ordered according to policy;
- partial failure produces accepted recovery behavior.

Do not emulate database transaction internals.

Real atomicity belongs to adapter/integration tests.

## Response DTOs

Verify exact Application output:

- selected fields;
- primitive-only values;
- enum strings;
- dates/timestamps;
- nullability/optionality;
- no Entity or Value Object leakage;
- no provider/persistence fields.

Avoid broad snapshots for stable DTOs when explicit assertions are clearer.

## `void` Use Cases

For commands returning `void`, verify:

- state;
- emitted/called accepted side effect;
- semantic errors;
- no unexpected return contract.

Do not invent a Response DTO only to make the test easier.

## Query Use Cases

For queries, verify:

- criteria conversion;
- repository/read-model behavior;
- ordering/pagination;
- primitive Response DTO mapping;
- empty results;
- authorization/filtering.

Use a contract-faithful InMemory query/read-model port.

Do not test SQL or ORM query details.

## Clocks and IDs

Use deterministic port doubles.

Example:

```ts
const clock = new FixedClock(appliedAt)
const idGenerator = new FixedIdGenerator(promotionId)
```

Verify generated/resolved values appear in Domain state and Response DTO where accepted.

Do not use real time or uncontrolled random IDs.

## Builders

Use Domain builders/factories with valid deterministic defaults.

Application-specific setup builders may group:

- InMemory repositories;
- fixed clock;
- fixed ID generator;
- provider stub;
- Use Case construction.

Keep override points explicit.

Avoid a universal test harness with hidden behavior.

## Recommended Test Harness

A focused setup function may return:

```ts
{
  useCase,
  promotionRepository,
  subscriptionRepository,
  campaignProvider,
  clock,
}
```

It must:

- construct fresh state per test;
- use real Domain objects;
- use accepted port implementations;
- make configured failure visible;
- avoid global mutable state.

## Test Naming

Name tests by intention and outcome.

Preferred:

```text
applies an eligible promotion and persists the resulting state
rejects when the subscription does not exist
does not call the provider when eligibility fails
returns an idempotent success without duplicating state
```

Avoid implementation-centric names:

```text
calls save
calls dependency twice
execute works
```

## Arrange, Act, Assert

Keep Application orchestration visible.

```text
Arrange Domain state and port outcomes
Act through execute(request)
Assert response and observable state
```

Interaction assertions follow state/result assertions when necessary.

## Errors

Follow project convention:

- exception class/code;
- Result failure;
- explicit Application decision.

Assert stable semantic meaning.

Do not assert:

- HTTP status;
- provider SDK error;
- SQLSTATE;
- raw technical message;
- stack trace.

## Regression Tests

Reproduce the smallest Application-level failure.

Examples:

- provider called before authorization;
- save occurred after rejection;
- primitive ID was not converted;
- returned DTO leaked an Entity;
- duplicate replay created a second record.

Do not encode implementation details of the old bug.

## Colocation

Follow the repository convention for tests inside the business module.

Example:

```text
promotion/
  application/
  tests/
    unit/
      ApplyPromotionUseCase.test.ts
```

Exact topology follows the repository.

## Test Execution

Run:

1. focused Use Case test;
2. Application unit suite for the capability;
3. relevant Domain tests;
4. typecheck/lint according to scope;
5. broader suite proportionally.

Record exact commands and real outcomes.

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

Use Case unit tests should not require database/network access.

A real dependency requirement indicates incorrect composition or test design.

## Boundary Audit

Tests and Use Cases must not import:

- concrete repository adapters;
- ORM/database clients;
- provider SDKs;
- HTTP/framework types;
- controllers;
- composition factories;
- environment readers.

Application may depend only on Domain, DTOs, ports, and accepted Application types.

## Readiness Decision

Use one:

```text
APPLICATION_USE_CASE_TESTS_COMPLETE
APPLICATION_USE_CASE_TESTS_COMPLETE_WITH_CONDITIONS
MORE_APPLICATION_CASES_REQUIRED
RETURN_TO_USE_CASE_DESIGN
RETURN_TO_PORT_DESIGN
RETURN_TO_DOMAIN_MODELING
TEST_HARNESS_REPAIR_REQUIRED
BLOCKED
```

## Output

Use `assets/application-use-case-testing-record.md`.

## Completion Criteria

- [ ] One accepted Use Case intention is under test.
- [ ] Real Entities, Value Objects, and Domain Services are used.
- [ ] Repositories use fresh contract-faithful InMemory implementations.
- [ ] External collaborations use explicit provider-neutral stubs/spies/fakes.
- [ ] Primitive-to-Domain conversion is covered.
- [ ] Success, missing state, authorization, rejection, and relevant external failures are covered.
- [ ] State and Response DTO outcomes are verified.
- [ ] Meaningful negative side effects are verified.
- [ ] Repository mocks and Domain mocks are absent.
- [ ] Real database, provider, HTTP, and composition dependencies are absent.
- [ ] Time, IDs, and idempotency keys are deterministic.
- [ ] Interaction assertions are limited to semantically relevant behavior.
- [ ] Focused and neighboring test commands were actually executed.
- [ ] No speculative cases or Infrastructure behavior were tested at the Application level.

## References

- Read `references/use-case-test-boundary.md` first.
- Read `references/inmemory-repositories.md` for state-oriented repository testing.
- Read `references/external-port-doubles.md` for stubs, spies, and fakes.
- Read `references/outcomes-state-and-interactions.md` for assertion strategy.
- Read `references/failures-idempotency-and-side-effects.md` for negative paths.
- Read `references/use-case-test-audit.md` before completion.
