---
name: testing-react-components
description: Portable engineering capability `testing-react-components`. Use when
  the harness or a specialist agent explicitly requires this named capability.
---
# Testing React Components

## Purpose

Implement focused React component tests that prove behavior from the user's point of view.

Component tests should answer:

```text
What can the user perceive?
What can the user operate?
What happens after the interaction?
What accessible state is exposed?
```

Primary evidence:

- accessible roles and names;
- visible content;
- user interaction;
- keyboard behavior;
- focus behavior;
- loading, empty, error, success, and disabled states;
- integration with provided semantic dependencies.

The test should remain stable when internal implementation changes but user behavior does not.

## Governing Rules

Component tests SHOULD prioritize:

- accessible roles and names;
- user interactions;
- loading, empty, error, and success states;
- keyboard behavior;
- integration with provided dependencies.

Avoid assertions tightly coupled to:

- DOM structure;
- wrapper hierarchy;
- CSS class names;
- internal React state;
- hook implementation;
- setter calls;
- effect count;
- memoization;
- server-state-library internals.

CSS classes may be asserted only when styling itself is the accepted behavior and there is no stronger visual or semantic boundary.

## Use When

- Implementing tests for a React component or screen.
- Verifying accepted component states.
- Testing form submission or retry behavior.
- Testing keyboard interaction.
- Testing focus placement or restoration at component scope.
- Testing status or error communication.
- Testing a component with injected feature dependencies.
- Testing representative HTTP-backed UI behavior through the repository-approved boundary.
- Adding a regression test for a component-level escaped defect.
- Characterizing user-observable behavior before refactoring a component.

## Do Not Use When

- The task is to plan the whole test strategy.
- The task is pure Domain logic.
- The task is Application Use Case orchestration.
- The task is adapter mapping.
- The task is a custom hook with an independent contract.
- The behavior is primarily visual and requires real-browser visual evidence.
- The behavior requires a full route/deployment E2E boundary.
- The request is only accessibility design rather than test implementation.
- The test would duplicate a lower-level branch without proving distinct UI risk.

## Inputs

- Accepted component design.
- Accepted accessibility contract.
- Frontend test-strategy record.
- Component implementation.
- Feature dependencies and composition contract.
- Existing repository test tooling.
- Existing test render helpers/providers.
- Existing MSW or equivalent handlers when approved.
- Accepted states and error semantics.
- Repository-local `AGENTS.md`.

## Outputs

- Focused component test file(s).
- Test setup or fixtures only when needed.
- Semantic dependency doubles or handlers.
- Regression coverage.
- Test implementation record.
- Passing test evidence.

## Readiness Gate

Use one:

```text
READY_TO_TEST_REACT_COMPONENT
READY_WITH_CONDITIONS
RETURN_TO_COMPONENT_DESIGN
RETURN_TO_TEST_STRATEGY
DEPENDENCY_TEST_BOUNDARY_REQUIRED
ACCESSIBILITY_BEHAVIOR_REQUIRED
REAL_BROWSER_REQUIRED
BLOCKED
```

Stop when the accepted behavior is too ambiguous to write a meaningful assertion.

## Core Workflow

```text
accepted component behavior
→ identify user-observable contract
→ choose semantic query
→ render with minimal realistic dependencies
→ perform user interaction
→ assert visible/accessible outcome
→ add relevant state and recovery cases
→ remove implementation coupling
→ run focused tests
```

## Test Case Selection

Implement the cases selected by the accepted test strategy.

Common component cases:

```text
INITIAL
LOADING
EMPTY
READY
SUBMITTING
SUCCESS
VALIDATION_ERROR
SEMANTIC_ERROR
FORBIDDEN
UNAVAILABLE
RETRY
DISABLED
```

Only test states that belong to the component contract.

Do not create component tests for every provider/adapter variant when the component renders the same semantic state for them.

## Query Priority

Prefer queries that reflect how users and assistive technologies identify the interface.

Typical priority:

```text
role + accessible name
label
visible text
semantic status
stable test id only when no user-facing semantic selector exists
```

Avoid:

```text
generated class
DOM path
nth-child
wrapper selector
implementation-only data attribute
```

A test ID is an escape hatch, not the default.

## Accessible Role and Name

Prefer assertions such as:

```text
button named "Apply promotion"
textbox named "Campaign code"
alert or status containing the accepted message
heading named "Current promotion"
```

Do not query an icon, wrapper, or implementation class when the user interacts with the semantic control.

If the component has no accessible role or name where one is required, the test should reveal that defect rather than work around it with a brittle selector.

## Visible Text

Visible text is appropriate for:

- headings;
- help text;
- errors;
- empty-state content;
- summaries;
- success status;
- button labels.

Use exactness only when the wording itself is the contract.

Avoid coupling tests to punctuation or incidental copy when semantic behavior is what matters.

## User Interaction

Drive behavior through user actions.

Examples:

- type;
- click;
- submit;
- tab;
- press Enter;
- press Space;
- press Escape;
- choose option;
- retry;
- dismiss;
- open/close.

Do not call component props or internal handlers directly when the user can perform the interaction through the rendered UI.

## Form Submission

For a form test, verify the accepted observable contract:

- field can be located by label;
- user can enter value;
- submit action is discoverable;
- invalid or busy states behave correctly;
- semantic command/dependency receives the accepted intention;
- visible result is correct;
- user input is preserved or cleared according to accepted behavior;
- focus and status behavior are correct.

Do not assert the internal form-library state unless it is the public behavior.

## Dependency Injection

Component tests should inject semantic dependencies at the accepted boundary.

Examples:

```text
onApply
applyPromotion
feature contract
Use Case
test provider
```

Prefer narrow dependencies over:

```text
HttpClient
repository
global container
ServicesContext
```

Use the composition/test strategy already accepted by the repository.

Do not patch production global dependencies for ordinary component tests.

## Semantic Command Spies

A spy may verify that a user action causes a semantic outward intention.

Good:

```text
user submits campaign code
→ applyPromotion("SUMMER") called
```

Weak:

```text
setLoading(true) called
setError(undefined) called
dispatch({ type: ... }) called
```

Assert command inputs only when they are part of the component contract.

## HTTP-Backed Component Tests

When the component or hook is intentionally integrated with the approved HTTP/server-state boundary, prefer the repository-approved realistic mock server such as MSW over mocking `fetch` internals.

Representative integrated flow:

```text
component
→ feature hook/server-state layer
→ approved HTTP client
→ mock server boundary
```

Use this only for cases selected by the test strategy.

Do not retest every adapter mapping case from the component.

Do not assert internal cache entries or library fields.

## Server-State Libraries

Treat SWR, React Query, Relay, Apollo, RTK Query, or framework data tools as implementation details unless the repository's public feature contract exposes something intentionally.

Assert:

- loading state;
- data state;
- error state;
- stale/retained UI when accepted;
- retry behavior;
- visible update after mutation.

Do not assert:

- cache internals;
- query observer count;
- internal mutation state object;
- library callbacks with no user-visible meaning.

## Loading State

Verify when applicable:

- accepted loading indicator or skeleton;
- accessible status/busy semantics;
- retained content if accepted;
- disabled actions;
- no contradictory success/error content.

Do not assert spinner implementation details.

## Empty State

Verify:

- explicit empty-state message;
- next valid action when defined;
- no false error semantics;
- accessible structure.

Do not accept a blank component as an empty-state test unless blank output is the accepted behavior.

## Error State

Verify:

- accepted text;
- semantic error association;
- retry or recovery action;
- preserved user data when accepted;
- focus behavior when specified;
- no technical details leak.

Do not test provider error codes in the component when they are translated below.

## Success State

Verify:

- accepted visible result;
- status message where needed;
- updated data;
- enabled/disabled actions;
- focus preservation or movement;
- input clearing/preservation according to contract.

Do not assert internal mutation/cache mechanics.

## Disabled and Busy States

Distinguish:

```text
disabled
aria-disabled
busy
submitting
```

Test the actual accepted behavior:

- can or cannot receive focus;
- can or cannot activate;
- duplicate action prevention;
- visible state;
- accessible state.

Do not infer semantics from a CSS class.

## Keyboard Tests

Keyboard tests should cover accepted user behavior.

Examples:

- Tab reaches the control in logical order;
- Enter submits when appropriate;
- Space activates a button;
- Escape closes an allowed dialog;
- arrow keys move within an accepted composite widget;
- focus returns after closing an overlay.

Do not reproduce the full browser/platform keyboard suite for native elements.

Test the component-specific interaction and integration risk.

## Focus Tests

Use focus assertions when focus is part of the accepted behavior.

Examples:

- initial focus after opening;
- focus after validation;
- focus restoration;
- focus remains on triggering control after async update;
- focus moves to error summary when specified;
- disabled element is not incorrectly focused.

Do not add focus movement simply to make a test easier.

## Accessibility Assertions

Component tests can prove:

- roles;
- names;
- labels;
- descriptions;
- relationships;
- keyboard interaction;
- focus behavior;
- status semantics;
- disabled/busy/invalid state;
- some automated accessibility checks.

They cannot prove full WCAG conformance.

Do not state:

```text
component passed axe
→ WCAG AA compliant
```

Manual and broader evidence belong to the accepted accessibility/test strategy.

## Automated Accessibility Checks

Use the repository-approved automated accessibility tooling when selected by the test strategy.

Run it on meaningful component states, especially:

- ready;
- dialog open;
- form with errors;
- disabled/busy;
- dynamic result state.

Avoid running identical scans on trivial state permutations with no semantic difference.

A zero-violation result is evidence, not certification.

## Dialog Tests

When a dialog is part of the component contract, test relevant:

- trigger role/name;
- dialog name;
- initial focus;
- focus containment when the test environment supports it reliably;
- close action;
- Escape when accepted;
- focus restoration;
- destructive action state;
- status/error content.

Use the project design-system/headless primitive behavior; do not retest every vendor invariant in every feature.

## Menu and Composite Widget Tests

Test the feature-specific accepted behavior:

- trigger;
- expanded state;
- keyboard navigation;
- selected/current state;
- Escape;
- action result;
- focus return.

Do not duplicate the primitive library's entire test suite.

## Dynamic Status

When content updates without navigation, verify the semantic result:

- correct status/alert region when accepted;
- updated text;
- no contradictory message;
- focus remains or moves according to contract.

Avoid asserting live-region implementation markup more deeply than needed.

## State Preservation

Important recovery tests may verify:

- typed form data remains after server rejection;
- selected filters remain after retry;
- previous content remains during background refresh;
- focus remains stable.

This often catches user-facing regressions that lower-level tests cannot prove.

## Routing in Component Tests

Only include a router/provider when the component contract actually depends on:

- links/navigation;
- route params;
- location;
- route actions;
- context.

Use the smallest repository-approved render harness.

Do not render the full application for a local component test.

## Provider Setup

Build the minimum realistic provider tree.

Potential providers:

- router;
- theme;
- i18n;
- server-state cache;
- feature dependency provider.

Prefer reusable project test render helpers when they preserve explicit behavior.

Do not hide every dependency inside a magic global render helper.

## Test Data

Use minimal data that makes the behavior clear.

Prefer builders/factories already approved by the repository.

Include targeted cases when relevant:

- long label/text;
- empty list;
- permission state;
- locale;
- timezone;
- theme;
- disabled action.

Avoid giant snapshots and production payload fixtures when not needed.

## Async Tests

Wait for observable outcomes.

Good:

```text
wait until success text appears
wait until button is enabled
wait until status changes
```

Avoid:

```text
sleep 500ms
flush all promises repeatedly
wait for internal hook state
```

Do not hide races with arbitrary timeouts.

## Fake Timers

Use only when the component contract includes time:

- debounce;
- timeout;
- delayed dismissal;
- interval;
- animation-independent timer.

Do not use fake timers for all async UI tests.

Keep timer ownership and advancement explicit.

## Regression Tests

For a component-level escaped defect:

1. reproduce the user-visible failure;
2. write the smallest failing component test;
3. fix the behavior;
4. keep the regression assertion semantic;
5. avoid capturing unrelated DOM.

Example:

```text
bug: invalid submit cleared campaign code
→ regression test: typed code remains visible after semantic rejection
```

Do not add an E2E test when the component boundary proves the defect reliably.

## Characterization Tests

Before refactoring brownfield UI, capture:

- visible semantics;
- user interactions;
- accepted state transitions;
- important accessibility behavior.

Do not characterize accidental wrapper structure or class names.

## DOM Structure Assertions

Avoid:

```text
container.firstChild.firstChild
querySelector(".promotion-card > div:nth-child(2)")
exact child count
```

unless the DOM structure itself is an explicit external contract.

Prefer semantic relationships.

## CSS and Style Assertions

Avoid class assertions for:

- loading;
- error;
- selected;
- disabled;
- expanded;
- required.

Prefer semantic state.

Use visual regression or browser evidence for layout, theme, clipping, typography, and responsive behavior.

Style assertions may be justified for a specific runtime style value when it is the contract and no higher-fidelity test is necessary.

## Snapshots

Use snapshots sparingly.

Potential value:

- stable serialized output that is itself a contract;
- structured accessibility tree fixture if repository policy supports it;
- small stable generated markup.

Avoid:

- full component snapshots for every state;
- snapshots replacing semantic assertions;
- snapshots that change on harmless wrapper refactors.

## Test IDs

Use a test ID only when:

- no role/name/label/text selector represents the target;
- the element is semantically invisible but behaviorally important;
- the project has a stable test-ID policy.

The ID should describe stable purpose, not implementation.

## Negative Assertions

Use negative assertions when absence is part of the contract.

Examples:

- error removed after retry success;
- loading state no longer present;
- forbidden action absent;
- stale status replaced.

Avoid asserting many irrelevant things are absent.

## Test Isolation

Each test must own:

- rendered tree;
- provider/cache instance;
- fake/spies;
- mock-server scenario;
- storage state;
- timers;
- user/session fixture.

Reset only what the test modifies.

Do not rely on previous tests.

## Cache Isolation

When server-state cache is in the component harness:

- create isolated cache/client per test or accepted suite scope;
- clear between tests;
- disable unwanted retries if repository test policy says so;
- avoid background requests leaking across tests.

Do not share mutable server-state caches across independent component tests.

## Mock-Server Handler Scope

Override handlers per scenario.

Restore defaults after the test.

Do not use one giant handler that switches on hidden global variables.

Keep representative API scenarios readable.

## Failure Diagnostics

A good component test failure should reveal:

- missing semantic control;
- wrong visible state;
- wrong user action;
- missing status;
- wrong focus;
- wrong outward command.

Avoid failures dominated by:

- huge snapshots;
- generated classes;
- DOM dumps with no semantic clue;
- implementation-only call stacks.

## Test Naming

Name tests by behavior.

Good:

```text
preserves the campaign code when the server rejects it as expired
announces success without moving focus from the form
prevents a second submit while the request is pending
```

Weak:

```text
test component
calls handler
renders correctly
```

## Coverage and Duplication

Do not chase line coverage at the expense of behavior.

A component test should not duplicate:

- every Domain boundary case;
- every Use Case error mapping;
- every adapter schema failure;
- every hook internal transition;
- every E2E route branch.

Keep the cases that prove presentation and interaction risk.

## Real-Browser Escalation

Escalate out of component-test scope when the behavior requires fidelity not available in the repository's component environment.

Examples:

- layout/reflow;
- actual CSS rendering;
- sticky focus obscuration;
- real scrolling;
- browser-native dialog nuance;
- complex pointer geometry;
- visual themes;
- browser storage behavior not faithfully emulated.

Use:

```text
COMPONENT_TEST_SUFFICIENT
COMPONENT_PLUS_BROWSER_REQUIRED
VISUAL_TEST_REQUIRED
ROUTE_OR_E2E_REQUIRED
MANUAL_AT_REQUIRED
```

## Completion Status

Use:

```text
REACT_COMPONENT_TESTS_COMPLETE
REACT_COMPONENT_TESTS_COMPLETE_WITH_CONDITIONS
RETURN_TO_TEST_STRATEGY
REAL_BROWSER_EVIDENCE_REQUIRED
ACCESSIBILITY_EVIDENCE_REQUIRED
TEST_ENVIRONMENT_BLOCKED
BLOCKED
```

## Output

Use `assets/react-component-test-implementation-record.md`.

## Completion Criteria

- [ ] Cases come from accepted behavior and test strategy.
- [ ] Tests are user-centered and semantic.
- [ ] Roles and accessible names are preferred.
- [ ] User interactions drive behavior.
- [ ] Loading, empty, error, success, retry, disabled, and busy states are covered only when applicable.
- [ ] Keyboard behavior is tested where accepted.
- [ ] Focus behavior is tested where accepted.
- [ ] Form submission proves semantic intent and user-visible outcome.
- [ ] Feature dependencies are injected through the accepted boundary.
- [ ] HTTP integration uses the approved realistic boundary when required.
- [ ] Server-state-library internals are not asserted.
- [ ] Private React state, setter calls, Effects, reducers, refs, memoization, and wrapper hierarchy are not asserted.
- [ ] DOM and CSS implementation coupling is avoided.
- [ ] Accessibility automation is evidence, not a conformance claim.
- [ ] Async waits target observable outcomes rather than sleeps.
- [ ] Test data, cache, timers, handlers, and providers are isolated.
- [ ] Regression tests target the smallest user-visible defect.
- [ ] Scenarios do not duplicate lower-level tests without a distinct UI purpose.
- [ ] Real-browser or manual evidence is requested when component-environment fidelity is insufficient.
- [ ] Focused tests pass.
- [ ] No new testing library or unrelated refactor was introduced.

## References

- Read `references/user-centered-queries-and-assertions.md` first.
- Read `references/component-states-interactions-keyboard-and-focus.md`.
- Read `references/dependency-injection-http-and-server-state.md`.
- Read `references/accessibility-async-and-browser-escalation.md`.
- Read `references/isolation-regressions-and-anti-brittleness.md`.
- Read `references/react-component-test-audit.md` before completion.
