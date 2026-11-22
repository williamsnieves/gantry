---
name: testing-frontend-domain-and-use-cases
description: Portable engineering capability `testing-frontend-domain-and-use-cases`.
  Use when the harness or a specialist agent explicitly requires this named capability.
---
# Testing Frontend Domain and Use Cases

## Purpose

Test the frontend's inner business/application layers independently from React and Infrastructure.

The two core boundaries are:

```text
Domain public API
→ pure input
→ observable Domain outcome
```

and:

```text
Application Request
→ Use Case
→ real Domain behavior
→ InMemory repositories
→ true external-port doubles
→ observable result/state
```

These tests remain valid regardless of whether the UI later uses React, Next.js, SWR, React Query, CSS Modules, Tailwind, or another delivery stack.

## Governing Standard

Frontend standard requirements:

```text
Domain tests
→ pure
→ no React
→ no HTTP
→ no browser dependency

Use Case tests
→ SHOULD use InMemory repositories

Repositories
→ do not mock when an InMemory implementation can exercise the real port contract

True external-service ports
→ stubs/spies allowed
```

Preserve fast deterministic tests.

## Use When

- Testing a frontend Entity, Value Object, or Domain Service.
- Testing an Application Use Case.
- Testing primitive-to-Domain conversion.
- Testing orchestration across repositories.
- Testing authorization/capability decisions in Application when that is accepted ownership.
- Testing missing state, conflicts, Domain rejection, or idempotency.
- Testing provider-neutral external-service collaboration.
- Adding fast regression coverage beneath React.
- Replacing repository mocks with InMemory repositories.
- Moving business tests out of component/E2E layers.

## Do Not Use When

- Testing a React component.
- Testing a custom hook.
- Testing SWR/React Query cache behavior.
- Testing an HTTP/storage/provider adapter.
- Testing browser APIs.
- Testing routing.
- Testing visual behavior.
- Testing E2E journeys.
- Testing a real provider or database.
- The behavior belongs only to Presentation.

## Inputs

- Accepted Domain/Application behavior.
- Domain model public APIs.
- Use Case `execute()` contract.
- Request/Response DTOs.
- Repository ports.
- InMemory repository implementations.
- True external-service ports.
- Error/result conventions.
- Deterministic clock/ID/randomness strategy.
- Existing frontend test conventions.
- Applicable `AGENTS.md`.

## Outputs

- Domain behavior inventory.
- Use Case behavior inventory.
- Pure Domain tests.
- InMemory repository setup.
- True external-port doubles.
- Fast deterministic Use Case tests.
- Boundary/purity audit.
- Frontend Domain/Application testing record.

# Boundary Decision

Classify the behavior first:

```text
DOMAIN_TEST
USE_CASE_TEST
ADAPTER_TEST
HOOK_TEST
COMPONENT_TEST
E2E_TEST
```

If the behavior can be proven at Domain or Use Case level, do not require React just because the application is frontend.

# Domain Tests

Domain tests MUST be pure.

Forbidden dependencies:

```text
React
React Testing Library
DOM
jsdom APIs
window
document
localStorage
IndexedDB
HTTP
fetch
Axios
SWR
React Query
router
provider SDK
repository adapter
composition root
```

The test should instantiate real Domain values and call public APIs.

# Domain Model Types

Applicable:

```text
Entity
Value Object
Domain Service
pure Domain policy
```

Do not create Domain tests for an anemic interface that has no Domain behavior.

# Public Behavior

Test public behavior, not private structure.

Good:

```ts
const range = DateRange.create(start, end)

expect(range.durationInDays()).toBe(5)
```

Avoid:

```ts
expect((range as any)._start).toEqual(start)
```

# Domain Invariants

Test accepted invariants such as:

```text
valid construction
invalid construction
boundary values
normalization
equality
immutability
allowed transitions
rejected transitions
collection rules
pure calculations
serialization/toPrimitives where public
```

Do not invent invariants not supported by the accepted model.

# Entity Tests

Typical cases:

```text
identity
initial state
valid transition
invalid transition
terminal state
collection changes
state remains unchanged after rejection
```

Use public factories/reconstitution APIs.

Do not mutate private state to prepare scenarios.

# Value Object Tests

Typical cases:

```text
valid value
invalid value
normalization
semantic equality
immutability
boundary values
derived operations
```

Use semantic equality rather than reference equality.

# Domain Service Tests

Domain Services should be tested with real Domain objects.

No repository mocks, React context, or browser dependencies.

A pure service:

```text
Domain values
→ Domain result
```

# Time in Domain Tests

If Domain behavior depends on time:

```text
pass explicit now
```

or use an accepted deterministic Domain/Application clock abstraction.

Do not depend on the real system clock.

# Randomness in Domain Tests

Inject/provide deterministic values.

Do not let tests depend on random UUIDs, Math.random, locale, or timezone unless those are explicit test inputs.

# Timezone

If date semantics matter, use explicit timezone/instant data.

Avoid environment-dependent parsing.

# Use Case Tests

Use Case tests prove Application orchestration.

Default collaborators:

```text
Domain objects
→ real

Domain Services
→ real

Repositories
→ InMemory

True external-service ports
→ explicit stubs/spies/fakes

Clock / ID generator
→ deterministic doubles
```

# Frontend Application Boundary

A frontend Use Case may orchestrate capabilities such as:

```text
load a semantic resource
apply a local/domain decision
persist through a repository port
record a provider-neutral analytic event
request a browser-neutral capability port
return a Response DTO
```

The test should remain independent of React/browser implementation.

# InMemory Repositories

Use contract-faithful InMemory implementations when repository ports exist.

They should support the semantics needed by the accepted port:

```text
seed
find
save
replace
query
absence
duplicate/conflict
ordering if contractual
controlled failure if accepted
```

Do not create a jest mock for every repository method when a real InMemory implementation exists.

# Why InMemory Instead of Repository Mocks

InMemory repositories allow state-oriented assertions:

```text
execute Use Case
→ inspect repository state
```

rather than coupling tests to:

```text
save called once
find called before save
```

They also exercise more of the actual repository port semantics.

# InMemory Isolation

Each test gets a fresh InMemory repository or explicit reset.

Do not share mutable repository state between tests.

Do not depend on test execution order.

# Use Case Input

Call the public Use Case boundary.

Example:

```ts
await useCase.execute({
  subscriptionId,
  promotionCode,
})
```

Do not call internal helper methods.

# Primitive-to-Domain Conversion

If the Use Case owns conversion:

```text
primitive request
→ Value Object / Entity ID
```

test invalid conversion through the Use Case contract where accepted.

Do not duplicate pure Value Object test cases exhaustively at Use Case level.

# Observable Result

Prefer assertions on:

```text
Response DTO
semantic result
persisted aggregate
repository query result
stable Application error
external semantic effect
```

# State Verification

Preferred:

```ts
await useCase.execute(request)

const saved = await subscriptions.findById(id)

expect(saved?.promotion).toEqual(expectedPromotion)
```

over:

```ts
expect(subscriptions.save).toHaveBeenCalledTimes(1)
```

when persisted state is what matters.

# Interaction Assertions

Spies are appropriate when the interaction itself is behavior.

Examples:

```text
analytics event emitted after success
external port not called after Domain rejection
clock used to timestamp accepted command
ID generator used once
provider-neutral notification sent
```

Do not assert every incidental call.

# True External-Service Ports

A true external-service port represents a capability whose state is not meaningfully modeled by an InMemory repository.

Examples may include:

```text
AnalyticsPort
Clock
IdGenerator
NotificationPort
TelemetryPort
FeatureFlagPort
ClipboardPort
FilePickerPort
BrowserNavigationPort
```

only when those ports are part of accepted Application design.

Use semantic stubs/spies.

Do not mock concrete vendor SDKs here.

# External Port Stub

A stub returns a configured semantic result.

Example:

```ts
class StubEligibilityService implements EligibilityPort {
  result = Eligibility.accepted()

  async check(): Promise<Eligibility> {
    return this.result
  }
}
```

# External Port Spy

A spy records semantically relevant calls.

Example:

```ts
class SpyAnalytics implements AnalyticsPort {
  events: AnalyticsEvent[] = []

  track(event: AnalyticsEvent) {
    this.events.push(event)
  }
}
```

Avoid jest mocks when a small explicit fake/stub communicates the contract more clearly.

# Concrete Adapter Prohibition

Do not instantiate:

```text
HttpClient
Axios adapter
fetch adapter
localStorage adapter
IndexedDB adapter
SWR cache
provider SDK
```

inside Use Case tests.

Those belong to adapter tests.

# React Prohibition

Do not wrap Use Cases in:

```text
renderHook
render
act
QueryClientProvider
RouterProvider
```

to test Application behavior.

If a hook merely delegates to a Use Case, test the Use Case here and the hook separately only for its own behavior.

# Server-State Prohibition

Do not involve query cache behavior.

This skill should not test:

```text
query key
staleTime
revalidation
optimistic cache
SWR mutate
React Query invalidation
```

Those belong to `integrating-frontend-server-state` and related test boundaries.

# Browser Port Distinction

If Application owns a browser-neutral port:

```text
ClipboardPort
NavigationPort
StorageRepository
```

test against the port double/InMemory implementation.

Do not access `navigator.clipboard`, router objects, or localStorage directly.

Adapter tests prove the concrete browser implementation separately.

# Behavior Inventory

For a Use Case, consider only accepted cases:

```text
success
missing state
invalid primitive input
Domain rejection
conflict
authorization/capability rejection
external semantic failure
persistence failure with Application meaning
idempotent replay
response mapping
negative side effects
regression
```

Do not produce a combinatorial test matrix with cases the contract does not define.

# Missing State

Example:

```text
repository returns no subscription
→ Use Case returns stable NOT_FOUND result/error
→ no later external effect occurs
```

Test observable semantics.

# Domain Rejection

Example:

```text
aggregate rejects transition
→ Use Case surfaces stable Application/Domain result
→ repository state unchanged
→ external effect not emitted
```

Do not re-test every internal Domain invariant here.

# Conflict

Test stable conflict semantics if part of the Application contract.

Do not simulate HTTP 409 in a Use Case test.

`409` is delivery/adapter detail.

Use:

```text
SubscriptionConflict
```

or the accepted stable semantic result.

# Authorization / Capability

If Application receives an actor/capability context, test accepted allow/deny semantics.

Do not treat frontend authorization as backend security enforcement.

The test proves UI/Application behavior only.

# Idempotency

If Use Case contract supports idempotent execution, test observable replay semantics.

Do not add idempotency cases speculatively.

# Transactions / Ordering

Only assert ordering when it is semantically required.

Example:

```text
persist successful state
→ then emit event
```

may matter if the contract defines it.

Avoid brittle exact call-order assertions otherwise.

# Negative Side Effects

Important cases:

```text
no analytics after rejection
no save after external failure
no navigation command after failed result
no duplicate event on idempotent replay
```

Use interaction assertions where absence of the effect is behavior.

# Response DTOs

Verify stable outward Application data.

Do not assert internal Entity private representation.

# Error Semantics

Assert stable errors/results.

Avoid raw strings when the architecture defines typed errors/codes.

Do not expose provider/transport errors in Application tests.

# Determinism

Control:

```text
time
IDs
randomness
locale
timezone
external semantic outcomes
```

No network.

No real browser.

No arbitrary sleeps.

# Async Use Cases

Await semantic completion.

Use controlled promises/stubs if sequencing matters.

Do not use timers/sleeps to “wait until done.”

# Concurrency

Test concurrency only if the Use Case contract defines it.

Use deterministic coordination rather than timing races.

# Test Builders

Builders are useful when Domain state is verbose.

A builder should create valid defaults and make variations explicit.

Example:

```ts
aSubscription()
  .withStatus("active")
  .withPromotion(...)
  .build()
```

Do not hide the behavior under test behind opaque fixture magic.

# Fixtures

Prefer semantic fixtures:

```text
active subscription
expired promotion
authorized actor
```

over giant JSON payloads.

Provider payload fixtures belong to adapter tests.

# Naming

Name tests by behavior.

Good:

```text
rejects an expired promotion
does not persist when eligibility check fails
returns subscription summary after successful renewal
```

Weak:

```text
test execute
works
case 3
```

# Arrange / Act / Assert

Keep cases readable.

Use clear phases when helpful.

Avoid excessive setup abstractions for small pure tests.

# Test Independence

Each test should be independently runnable.

No shared mutable state.

No order dependence.

No global patching.

# Test Speed

These tests should be fast enough to run continuously during development.

If a Domain/Use Case test needs seconds, network, browser startup, or a real database, the boundary is wrong.

# Coverage

Do not optimize for line coverage alone.

Cover accepted behavior/risk:

```text
invariants
critical transitions
failure semantics
orchestration
negative side effects
regressions
```

# Duplicate Coverage Audit

Avoid testing the same business rule through:

```text
Domain
Use Case
Hook
Component
E2E
```

unless each layer adds distinct risk.

Default:

```text
Domain invariant
→ Domain test

Application orchestration
→ Use Case test

Hook-specific async/state contract
→ hook test

UI interaction
→ component test

critical cross-boundary journey
→ E2E
```

# Frontend-Specific Example

Suppose:

```text
PromotionCode
→ Domain Value Object

ApplyPromotion
→ Use Case

PromotionRepository
→ repository port

AnalyticsPort
→ external port

usePromotion
→ hook

PromotionPanel
→ component
```

Tests:

```text
PromotionCode validation
→ Domain test

ApplyPromotion orchestration
→ Use Case test with InMemoryPromotionRepository + SpyAnalytics

SWR mutation/cache
→ server-state/hook boundary

Panel loading/error interaction
→ component test

full apply-promotion user flow
→ E2E only if risk justifies
```

# Domain Test Example

```ts
describe("PromotionCode", () => {
  it("normalizes accepted input", () => {
    const code = PromotionCode.create(" summer25 ")

    expect(code.value).toBe("SUMMER25")
  })

  it("rejects empty input", () => {
    expect(() => PromotionCode.create("   ")).toThrow()
  })
})
```

Use project error/result conventions.

# Use Case Test Example

```ts
it("applies an eligible promotion and persists the subscription", async () => {
  const subscriptions = new InMemorySubscriptionRepository()
  const eligibility = new StubPromotionEligibility()
  const analytics = new SpyAnalytics()

  const subscription = anActiveSubscription()
  subscriptions.seed(subscription)
  eligibility.result = EligiblePromotion.accepted(...)

  const useCase = new ApplyPromotion({
    subscriptions,
    eligibility,
    analytics,
    clock: fixedClock,
  })

  const result = await useCase.execute({
    subscriptionId: subscription.id.value,
    code: "SUMMER25",
  })

  expect(result.status).toBe("applied")
  expect((await subscriptions.findById(subscription.id))?.promotion).toBeDefined()
  expect(analytics.events).toContainEqual(expect.objectContaining({
    type: "promotion_applied",
  }))
})
```

Do not copy exact syntax if the project API differs.

# Repository Contract Fidelity

An InMemory repository should behave like the port semantics, not like a convenient array.

If port defines:

```text
save replaces by identity
findById returns Maybe
list is ordered
duplicate insert conflicts
```

InMemory should preserve those semantics.

If not, Use Case tests can produce false confidence.

# InMemory Reuse

If both frontend and backend share a Domain/Application package, reuse the same InMemory repository where architecture permits.

Do not create a frontend-only duplicate solely because UI code imports the Use Case.

# Frontend Package Boundaries

A frontend package may contain Domain/Application tests even if consumed by React.

Keep imports from:

```text
domain
application
test-support
```

not:

```text
presentation
infrastructure concrete adapters
```

# Test-Support Ownership

Reusable test doubles may live in:

```text
test-support
testing
__fixtures__
in-memory
```

according to repository conventions.

Avoid exporting test-only doubles from production public APIs unless the package intentionally exposes a testing subpath.

# Production Leakage

Do not add test-only flags/methods to Domain objects to make tests easier.

Use accepted public APIs/builders/test support.

# InMemory Failure Modes

Only simulate repository failures that correspond to accepted port/Application behavior.

Do not add generic “throw anything” switches to every InMemory repository.

# Spy Restraint

If state proves the behavior, do not also assert every call.

Use spies for effects that have no stateful repository representation.

# Mock Restraint

Use mocks sparingly.

Explicit semantic doubles are usually clearer.

Do not mock:

```text
Entity
Value Object
Domain Service
repository port when InMemory exists
```

# Snapshot Tests

Avoid snapshots for Domain/Application behavior.

Use explicit semantic assertions.

# Framework Assertions

No assertions about:

```text
React renders
hook calls
query counts
DOM
class names
router
```

# Regression Tests

For a bug, add the lowest-level test that reproduces the actual faulty contract.

Example:

```text
promotion could be applied twice
```

If root cause is Domain invariant:

```text
Domain regression test
```

If Domain is correct but Use Case persists twice:

```text
Use Case regression test
```

Do not default to E2E.

# TDD Compatibility

This skill works with RED/GREEN/REFACTOR.

During RED:

```text
test fails for one accepted behavior
```

During GREEN:

```text
minimal Domain/Application implementation
```

During REFACTOR:

```text
tests remain behavioral and deterministic
```

# Execution Strategy

Run:

```text
focused test file
→ neighboring Domain/Application tests
→ broader frontend unit suite when appropriate
```

Do not require browser/E2E suite for every pure inner-layer change unless repository policy mandates it.

# Failure Diagnosis

If a pure test fails, inspect:

```text
behavior contract
fixture validity
InMemory contract fidelity
deterministic inputs
actual Domain/Application implementation
```

Do not “fix” by mocking more internals.

# Boundary Audit

A passing test suite can still be architecturally wrong.

Audit imports for:

```text
react
react-dom
@testing-library/react
fetch/axios
browser globals
concrete adapters
provider SDK
router
server-state library
```

These imports should not appear in Domain/Use Case tests except test-runner infrastructure that does not affect behavior.

# Final Decision

Use:

```text
FRONTEND_DOMAIN_USE_CASE_TESTS_READY
FRONTEND_DOMAIN_USE_CASE_TESTS_READY_WITH_CONDITIONS
DOMAIN_TESTS_NOT_REQUIRED
USE_CASE_TESTS_NOT_REQUIRED
INMEMORY_REPOSITORY_REQUIRED
EXTERNAL_PORT_DOUBLE_REQUIRED
RETURN_TO_BEHAVIOR_OR_ARCHITECTURE
BLOCKED
```

## Output

Use `assets/frontend-domain-use-case-testing-record.md`.

## Completion Criteria

- [ ] Behavior is classified as Domain or Use Case rather than Presentation/adapter behavior.
- [ ] Domain tests have no React, HTTP, browser, concrete Infrastructure, or mocks.
- [ ] Domain tests use real public Domain APIs.
- [ ] Invariants/transitions/equality/immutability/boundaries are tested only where accepted.
- [ ] Time/randomness/timezone inputs are deterministic.
- [ ] Use Case tests call the public Application boundary.
- [ ] Real Domain objects/services are used.
- [ ] Repositories use fresh contract-faithful InMemory implementations.
- [ ] Repository mocks are avoided when InMemory exists.
- [ ] True external-service ports use explicit semantic stubs/spies/fakes.
- [ ] Concrete provider SDKs/adapters are absent.
- [ ] State/result assertions are preferred over incidental interaction assertions.
- [ ] Negative side effects are asserted where semantically important.
- [ ] Stable Application errors/results are asserted rather than transport/provider details.
- [ ] No React hook/component/query-cache behavior is tested here.
- [ ] No real network/browser/database is used.
- [ ] Tests are independent and fast.
- [ ] Fixtures/builders remain semantic and transparent.
- [ ] Duplicate business coverage across hook/component/E2E layers is avoided.
- [ ] Regression tests live at the lowest boundary containing the defect.
- [ ] Focused and neighboring Domain/Application tests pass.
- [ ] Final testing status is explicit.

## References

- Read `references/domain-test-purity-and-public-behavior.md` first.
- Read `references/use-case-tests-inmemory-repositories-and-state-verification.md`.
- Read `references/external-port-doubles-and-interaction-restraint.md`.
- Read `references/determinism-fixtures-builders-and-regressions.md`.
- Read `references/frontend-boundaries-and-duplicate-test-avoidance.md`.
- Read `references/inmemory-contract-fidelity-and-test-support.md`.
- Read `references/frontend-domain-use-case-testing-audit.md` before completion.
