---
name: planning-frontend-test-strategy
description: 'Plans frontend test coverage by mapping each accepted behavior and risk to the lowest reliable test boundary: Domain, Application Use Case, adapter, hook, component, accessibility, visual, route integration, contract, or E2E. Use after vertical slices, component/hook/effect designs, adapters, composition, styling, and accessibility decisions are known. Define test matrices, risk coverage, test-double policy, realistic environments, regression ownership, CI placement, and evidence gaps. Prefer pure and deterministic tests, InMemory repositories for Use Cases, faithful adapter boundaries, semantic component tests, and a small set of critical E2E journeys. Do not implement tests, duplicate every scenario at every level, mock Domain behavior, replace InMemory ports with repository mocks, mock fetch internals when MSW or a faithful boundary is available, test private implementation details, or use all-E2E as the default strategy.'
---

# Planning Frontend Test Strategy

## Purpose

Create a proportionate frontend test strategy for one accepted change, capability, application, or package.

The strategy must map:

```text
accepted behavior and risk
→ cheapest reliable test boundary
→ realistic environment
→ appropriate test double
→ CI and regression evidence
```

Possible boundaries:

```text
Domain
Application Use Case
adapter
custom hook
component
accessibility
visual regression
route integration
package contract
E2E
manual or assistive-technology evidence
```

The goal is not maximum test count.

The goal is reliable confidence with minimal duplication.

## Governing Strategy

Tests SHOULD follow behavior and architectural boundaries.

For a rich business slice:

```text
Domain
→ Application Use Case
→ adapter integration
→ hook/component behavior
→ route or E2E confidence
```

For UI-only work:

```text
smallest meaningful presentation boundary
→ critical route/E2E evidence only when required
```

Inside-out is the default when rich Domain behavior exists.

Do not force Domain or Use Case tests when the selected frontend profile does not contain those boundaries.

## Use When

- A frontend slice is ready for implementation planning.
- The team must decide which behaviors belong in unit, integration, visual, or E2E tests.
- Existing coverage duplicates scenarios across levels.
- The current strategy relies mostly on E2E.
- Test doubles and realistic environments are unclear.
- A feature spans Domain, Use Cases, adapters, hooks, components, accessibility, themes, and routes.
- A package has several consumers.
- Brownfield behavior needs characterization and regression protection.
- CI time and flakiness require a deliberate split.
- Accessibility design needs automated and manual evidence.

## Do Not Use When

- The accepted behavior or slice is unresolved.
- The task is to write the tests.
- The task is only to test one hook or component.
- The architecture profile is unknown.
- The user asks for a testing-library selection unrelated to repository policy.
- The request is purely backend.
- The request is only to run existing tests.

## Inputs

- Accepted specification and acceptance criteria.
- Frontend vertical-slice plan.
- Architecture-profile decision.
- Component, hook, Effect, adapter, composition, styling, and accessibility records.
- Existing test tooling and repository conventions.
- CI pipeline and environment availability.
- Browser and assistive-technology support policy.
- Existing fixtures, factories, InMemory ports, sandboxes, emulators, or test servers.
- Production incidents and regression history when available.
- Repository-local `AGENTS.md`.

## Outputs

- Behavior-to-test matrix.
- Risk coverage map.
- Lowest-useful-boundary decisions.
- Test-double policy.
- Environment and data requirements.
- Accessibility and visual evidence plan.
- E2E journey selection.
- CI execution plan.
- Regression ownership and maintenance policy.
- Gaps, blocked evidence, and residual risks.
- Frontend test-strategy record.

## Core Workflow

```text
accepted behavior
→ inventory risks and boundaries
→ choose lowest reliable test level
→ select doubles and environments
→ remove duplicated scenarios
→ select critical E2E journeys
→ define accessibility and visual evidence
→ place suites in CI
→ define regression ownership
```

## Readiness Gate

Use one:

```text
READY_TO_PLAN_FRONTEND_TESTS
READY_WITH_CONDITIONS
RETURN_TO_VERTICAL_SLICE_PLAN
BEHAVIOR_OR_ACCEPTANCE_REQUIRED
ARCHITECTURE_BOUNDARY_REQUIRED
TEST_ENVIRONMENT_REQUIRED
ACCESSIBILITY_EVIDENCE_REQUIRED
E2E_SCOPE_REQUIRED
BLOCKED
```

Stop when a missing contract prevents selecting the correct test boundary.

## Test Boundary Principle

Use the lowest boundary that can prove the behavior without hiding the relevant integration risk.

Examples:

```text
pure eligibility rule
→ Domain test

user intention coordinating ports
→ Use Case test

HTTP payload mapping
→ adapter test

async hook state and cancellation
→ hook test

semantic UI interaction
→ component test

responsive theme rendering
→ visual test

critical user journey across route and backend boundary
→ E2E
```

Do not choose a lower boundary when it cannot observe the behavior.

Do not choose a higher boundary merely because it can.

## Behavior Inventory

For every accepted behavior record:

- actor and context;
- trigger;
- expected outcome;
- state/data effect;
- failure and recovery;
- accessibility consequence;
- visual consequence;
- external boundary;
- business criticality;
- historical regression risk.

Classify:

```text
PURE_RULE
USER_INTENTION
DATA_MAPPING
ASYNC_STATE_TRANSITION
UI_INTERACTION
ACCESSIBILITY_BEHAVIOR
VISUAL_BEHAVIOR
ROUTE_INTEGRATION
PACKAGE_CONTRACT
CRITICAL_JOURNEY
MANUAL_ONLY_EVIDENCE
```

## Risk Model

Assess:

```text
BUSINESS_CRITICALITY
USER_REACH
CHANGE_FREQUENCY
COMPLEXITY
EXTERNAL_DEPENDENCY
CONCURRENCY
ACCESSIBILITY_IMPACT
VISUAL_SENSITIVITY
SECURITY_OR_PRIVACY
REGRESSION_HISTORY
OBSERVABILITY_GAP
```

Use:

```text
LOW
MODERATE
HIGH
CRITICAL
```

Risk affects coverage depth, not automatic E2E selection.

A high-risk pure rule may still be best proven with exhaustive Domain tests plus one integrated confidence path.

## Domain Tests

Use for:

- Entities;
- Value Objects;
- pure Domain Services;
- deterministic invariants;
- state transitions;
- calculations;
- parsing or normalization that belongs to Domain.

Requirements:

- no React;
- no browser;
- no HTTP;
- no repository mocks;
- no clock unless clock is an explicit pure input or port;
- fast and deterministic.

Test:

- valid behavior;
- invalid behavior;
- boundaries;
- equivalence classes;
- state transitions;
- property-based cases when repository policy supports them.

Never mock Domain entities, Value Objects, or pure Domain Services.

## Application Use Case Tests

Use when a frontend Application layer coordinates a user intention.

Use:

- InMemory repository implementations;
- explicit stubs/spies for true external-service ports;
- controlled clock, ID generator, analytics, browser capability, or feature flag when they are real ports.

Verify:

- orchestration order only when behavior depends on it;
- returned semantic result;
- repository state;
- stable errors;
- cancellation or idempotency where accepted;
- no framework details.

Do not mock repositories when an InMemory implementation can exercise the real port contract.

Do not test private method calls.

## Adapter Tests

Use for:

- HTTP mapping;
- storage mapping;
- IndexedDB;
- browser/provider adapters;
- error translation;
- cancellation;
- pagination;
- malformed responses;
- auth refresh where adapter policy owns it;
- offline and migration behavior.

Use a realistic boundary:

```text
real sandbox
test server
MSW
contract fixture
emulator
browser storage implementation
provider sandbox
```

The strategy must prove:

- request mapping;
- response mapping;
- failure semantics;
- cancellation;
- lifecycle;
- no technical leakage.

Do not mock the adapter itself.

Do not use an InMemory repository as evidence that the concrete adapter works.

## HTTP UI Tests

For UI that communicates through HTTP, prefer MSW or the repository-approved equivalent over mocking `fetch` internals.

Use MSW when the test should exercise:

```text
component/hook
→ server-state or HTTP client
→ request/response behavior
```

Do not use MSW to retest every mapper case already covered by adapter tests.

Select representative integrated cases.

## Hook Tests

Test a custom hook independently when its behavior is reusable or complex enough to deserve a contract.

Verify observable:

- initial state;
- commands;
- transitions;
- async success;
- semantic and system errors;
- retry;
- reset;
- cancellation;
- stale-response handling;
- duplicate command behavior;
- dependency injection;
- cleanup.

Do not assert:

- internal setter calls;
- internal Effect count;
- exact reducer action sequence unless it is the public contract;
- use of `useMemo` or `useCallback`;
- private refs.

Pure reducers and helpers should be tested without rendering a hook.

Do not retest SWR, React Query, or framework internals.

## Component Tests

Prioritize:

- accessible roles and names;
- visible text and status;
- user interactions;
- keyboard behavior;
- focus behavior;
- loading, empty, error, success, disabled, and retry states;
- integration with injected semantic dependencies;
- state preservation;
- correct callbacks or user intentions.

Prefer user-observable queries.

Avoid assertions tied to:

- internal component names;
- wrapper hierarchy;
- arbitrary DOM depth;
- implementation-only class names;
- internal state;
- exact hook calls.

CSS classes may be asserted only when the styling contract itself is the behavior under test and no better evidence exists.

## Accessibility Tests

Automated and component-level checks may cover:

- names;
- roles;
- labels;
- descriptions;
- invalid ARIA;
- keyboard interaction;
- focus;
- error association;
- status messages;
- busy/disabled states;
- some contrast or structural issues.

They cannot prove full accessibility or WCAG conformance.

Plan manual or representative assistive-technology evidence for:

- logical reading order;
- meaningful alternatives;
- screen-reader announcements;
- complex widgets;
- focus strategy;
- zoom/reflow;
- text spacing;
- forced colors;
- cognitive usability;
- complete journeys.

Do not duplicate the complete accessibility matrix in every E2E test.

## Visual Regression Tests

Consider for:

- design-system primitives;
- complex responsive layouts;
- theme variants;
- charts;
- document rendering;
- pixel-sensitive UI;
- third-party widget integration;
- high-risk spacing or clipping;
- zoom or localization-sensitive layouts when the tooling supports it.

Define:

- viewport;
- theme;
- data fixture;
- animation disabling;
- fonts/assets;
- threshold;
- browser;
- baseline owner;
- review policy.

Do not snapshot every trivial component.

Visual tests do not prove semantics or interaction.

## Route Integration Tests

Use when behavior depends on:

- routing;
- loader/action integration;
- provider composition;
- URL state;
- server/client hydration;
- route error boundaries;
- package consumer assembly.

Keep route tests narrower than full E2E when a local application harness can prove the integration reliably.

## Package Contract Tests

For shared packages verify:

- public exports;
- consumer-safe types;
- styling/token contract;
- adapter injection;
- no deep imports;
- server/client entry points;
- compatibility with representative consumers;
- versioned behavior where required.

Do not expose internal implementation files solely to simplify tests.

## E2E Tests

Use for critical journeys that require confidence across real application boundaries.

Good candidates:

- authentication-dependent critical flow;
- revenue or entitlement path;
- route-to-route workflow;
- browser integration;
- server/client hydration;
- deployment configuration;
- real backend contract;
- one representative accessibility or retry path where browser behavior matters.

E2E should cover:

- essential success;
- one or few critical failures/recovery paths;
- integration risks not proved below.

Do not use E2E for:

- every validation branch;
- every provider error;
- pure business rules;
- every component state;
- every theme variant;
- exhaustive edge cases.

An all-E2E strategy is rejected.

## Critical Journey Selection

Rank journeys by:

- business impact;
- user frequency;
- integration breadth;
- production incident history;
- inability to prove lower;
- browser-specific behavior;
- deployment/configuration risk.

Use:

```text
E2E_REQUIRED
ROUTE_INTEGRATION_SUFFICIENT
LOWER_BOUNDARY_SUFFICIENT
MANUAL_PRODUCTION_CHECK_ONLY
NOT_IN_SCOPE
```

## Test Duplication

A scenario may appear at more than one level only when each level proves a different risk.

Example:

```text
invalid campaign code

Use Case
→ semantic outcome and repository behavior

component
→ visible message, focus, and preserved input

E2E
→ usually unnecessary unless backend or routing integration is high risk
```

Record the unique purpose of every duplicated case.

Reject duplication that adds no new evidence.

## Test Pyramid and Trophy

Do not enforce a numeric pyramid universally.

Use boundary and risk reasoning.

A frontend strategy may emphasize component/integration tests while retaining:

- pure tests for Domain and Application;
- faithful adapter tests;
- a small E2E set.

The exact shape depends on the architecture profile and product risk.

## Test Doubles

Classify:

```text
REAL_IMPLEMENTATION
IN_MEMORY_IMPLEMENTATION
FAKE
STUB
SPY
MOCK_SERVER
EMULATOR
SANDBOX
FIXTURE
VIRTUAL_CLOCK
NO_DOUBLE
```

Definitions:

- InMemory implementation: working port implementation with meaningful state.
- Fake: simplified working implementation.
- Stub: controlled response.
- Spy: records interaction while preserving explicit behavior.
- Mock server: simulates network boundary.
- Emulator: faithful local service/runtime.
- Sandbox: real external test environment.

Use the least synthetic double that keeps the test deterministic and focused.

## Never Mock

Never mock:

- Domain entities;
- Value Objects;
- pure Domain Services;
- repositories in Use Case tests when an InMemory implementation exists.

Avoid mocking:

- the unit being tested;
- React internals;
- framework internals;
- browser APIs when a faithful test implementation exists and behavior matters.

## Appropriate Stubs and Spies

Use for true external ports:

- analytics;
- clock;
- ID generation;
- geolocation;
- clipboard;
- notifications;
- file picker;
- third-party service;
- feature flags;
- nondeterministic provider boundaries.

A spy should verify only meaningful outward interaction.

## Environment Matrix

Potential environments:

```text
NODE
JSDOM
HAPPY_DOM
REAL_BROWSER
TEST_SERVER
MSW
EMULATOR
SANDBOX
STORYBOOK_OR_COMPONENT_HARNESS
PRODUCTION_SMOKE
ASSISTIVE_TECHNOLOGY
```

Select based on behavior.

Examples:

- pure Domain → Node;
- component semantics → DOM test environment;
- layout/visual → real browser;
- IndexedDB → faithful browser implementation or real browser;
- browser focus/scroll → real browser when DOM emulation is insufficient;
- provider integration → sandbox;
- screen-reader journey → representative AT environment.

Do not pretend JSDOM proves layout, CSS, focus scrolling, or browser rendering behavior it does not implement faithfully.

## Test Data

Define:

- factories/builders;
- valid defaults;
- boundary cases;
- locale and timezone;
- permissions;
- long text;
- theme;
- empty/large datasets;
- stable IDs and clock;
- sensitive-data redaction.

Avoid giant shared fixtures that obscure the behavior under test.

Prefer minimal scenario-specific data with reusable builders.

## Determinism

Control:

- clock;
- random IDs;
- network;
- animation;
- timezone;
- locale;
- feature flags;
- browser storage;
- ordering;
- concurrency.

Do not hide real race behavior by serializing all tests if concurrency is part of the contract.

## Flakiness Prevention

Design against:

- arbitrary sleeps;
- animation timing;
- shared accounts/data;
- uncontrolled retries;
- unstable selectors;
- test-order dependence;
- global mutable state;
- cross-test caches;
- background requests;
- timezone dependence;
- eventual consistency with no polling contract.

Prefer observable waits and deterministic state.

A retrying test is not automatically a stable test.

## Selectors

Prefer:

- accessible role and name;
- label;
- visible text;
- stable semantic test ID only when no user-facing selector exists;
- package or route contract.

Avoid:

- CSS implementation selectors;
- generated class names;
- DOM paths;
- text that is incidental and frequently changed when not the behavior under test.

Test IDs need ownership and semantic stability.

## CI Placement

Classify suites:

```text
PRE_COMMIT
PULL_REQUEST_FAST
PULL_REQUEST_BROWSER
MAIN_BRANCH
NIGHTLY
RELEASE_GATE
POST_DEPLOYMENT_SMOKE
MANUAL_REVIEW
```

Typical strategy:

- pure and component tests → fast PR;
- adapter/real-browser tests → PR or main depending on cost;
- visual regression → PR with review;
- E2E critical smoke → PR or release gate;
- broad cross-browser/provider sandbox → main/nightly;
- representative AT → scheduled/manual milestone and critical-change review.

Do not place every slow suite on every commit without value.

## Parallelization and Isolation

Define:

- shard strategy;
- isolated test data;
- unique users/tenants;
- server ports;
- browser contexts;
- cache/storage cleanup;
- sandbox rate limits;
- serial suites that are genuinely unavoidable.

Parallelization must not cause cross-test state leakage.

## Coverage

Code coverage is a diagnostic, not the strategy.

Use coverage to detect unexercised areas, not to replace behavior mapping.

Do not set a percentage as proof of quality.

Mutation testing may be considered for critical pure logic when repository policy supports it.

## Regression Plan

For every production bug or escaped defect decide:

- missing acceptance criterion;
- wrong test boundary;
- missing environment;
- weak assertion;
- fixture gap;
- observability gap;
- flaky test masking failure.

Add the smallest regression test that would have caught the defect reliably.

Do not automatically add an E2E test for every bug.

## Characterization Tests

For brownfield changes:

```text
observe current behavior
→ capture critical contract
→ introduce seam
→ change behavior
→ update expected contract intentionally
```

Characterization tests should preserve required behavior, not every accidental DOM detail.

## TDD Planning

TDD is preferred for behavior-heavy work.

Recommended cycle:

```text
REASON
→ RED
→ GREEN
→ REFACTOR
→ RE-EVALUATE
```

For a vertical slice:

```text
Domain behavior
→ Application orchestration
→ adapter mapping
→ hook state
→ component interaction
→ route/E2E confidence
```

Do not force TDD ceremony for mechanical renames, generated code, configuration-only changes, or purely visual exploration before behavior is accepted.

## Ownership and Maintenance

Every suite should have:

- capability owner;
- environment owner;
- fixture/data owner;
- visual baseline reviewer;
- E2E failure triage owner;
- flake-removal policy;
- deprecation/removal trigger.

Tests are production assets and require maintenance.

## Evidence Status

Use:

```text
PLANNED
IMPLEMENTED
PASSING
FAILING
FLAKY
BLOCKED_BY_ENVIRONMENT
MANUAL_EVIDENCE_REQUIRED
NOT_APPLICABLE
DEFERRED_WITH_TRIGGER
```

Do not mark unavailable evidence as passing.

## Final Decision

Use:

```text
FRONTEND_TEST_STRATEGY_READY
FRONTEND_TEST_STRATEGY_READY_WITH_CONDITIONS
RETURN_TO_ACCEPTANCE_OR_ARCHITECTURE
TEST_ENVIRONMENT_REQUIRED
ACCESSIBILITY_EVIDENCE_REQUIRED
E2E_SCOPE_REQUIRES_DECISION
BLOCKED
```

## Output

Use `assets/frontend-test-strategy-record.md`.

## Completion Criteria

- [ ] Accepted behavior and architecture boundaries are explicit.
- [ ] Every behavior maps to the lowest reliable test boundary.
- [ ] Risk and historical regression influence coverage.
- [ ] Domain tests remain pure.
- [ ] Use Case tests use InMemory repositories when available.
- [ ] True external ports use explicit stubs/spies/fakes.
- [ ] Adapter tests use realistic boundaries and verify mapping/failures.
- [ ] Hook tests cover observable transitions, races, cancellation, and commands only when justified.
- [ ] Component tests use semantic queries and observable behavior.
- [ ] Accessibility evidence combines automated and manual methods.
- [ ] Visual tests are limited to meaningful visual risks.
- [ ] E2E covers critical journeys rather than local branches.
- [ ] Every duplicated scenario proves a distinct risk.
- [ ] Test environments match the behavior being tested.
- [ ] Data, time, locale, storage, concurrency, and network are controlled.
- [ ] Flakiness risks and selector policy are explicit.
- [ ] CI placement is proportionate.
- [ ] Regression ownership and maintenance policy are defined.
- [ ] Blocked evidence and residual risk are honest.
- [ ] No test implementation, new library, or all-E2E strategy was produced.
