---
name: testing-react-hooks
description: Implements focused tests for React custom hooks whose reusable or complex behavior deserves an independent contract. Use to verify observable state transitions, semantic commands, async success and failure, retry, cancellation, stale-response protection, optimistic updates, cleanup, dependency injection, and feature-semantic wrappers around approved server-state libraries. Reuse the repository-approved hook-testing harness and realistic dependencies. Do not test internal setter calls, reducer action sequences, Effect counts, refs, memoization, callback identity unless semantically required, server-state-library internals, concrete adapters, or behavior better proven at component, adapter, or E2E boundaries.
---

# Testing React Hooks

## Purpose

Implement tests for a custom hook when its behavior is sufficiently reusable or complex to deserve an independent contract.

A hook test answers:

```text
Given these dependencies and inputs,
when the consumer invokes this semantic command,
what observable state or result does the hook expose?
```

Test:

- observable state;
- semantic commands;
- valid transitions;
- async success and failure;
- retry;
- cancellation;
- stale-response protection;
- duplicate-command policy;
- optimistic update and rollback when accepted;
- cleanup;
- dependency injection;
- server-state wrapper semantics.

Do not test how React internally produced those outcomes.

## Governing Standard

Custom hooks encapsulate reusable React behavior, state, and integration.

They SHOULD NOT become a second Application layer.

Hook tests SHOULD verify:

```text
observable state transitions
+ commands
```

They SHOULD NOT verify internal implementation details such as setter calls.

## Use When

- The hook has an independent reusable contract.
- Async lifecycle is complex.
- Race or stale-response behavior matters.
- Cancellation is part of the contract.
- Retry/reset behavior matters.
- The hook performs optimistic state transitions.
- Cleanup or subscription lifecycle matters.
- Dependency injection needs direct verification.
- A server-state wrapper exposes a stable feature-semantic API.
- A regression occurred inside hook-level behavior and component tests would be unnecessarily broad.

## Do Not Use When

- The hook is trivial and only hides one `useState`.
- The behavior is pure and should be tested as a plain function or reducer.
- The behavior belongs to a Domain or Application Use Case.
- The behavior is adapter mapping.
- The same contract is more naturally proven through a component test.
- The task is to plan the overall test strategy.
- The task is to design the hook rather than test it.
- The behavior requires real-browser layout, visual, route, or E2E fidelity.

## Inputs

- Accepted custom-hook design record.
- Accepted frontend test strategy.
- Hook implementation.
- Dependency-injection contract.
- Async lifecycle and race policy.
- Cancellation policy.
- Optimistic update policy, if applicable.
- Server-state strategy, if applicable.
- Existing hook test tooling and render harness.
- Existing test doubles, InMemory implementations, fake timers, and mock server setup.
- Repository-local `AGENTS.md`.

## Outputs

- Focused hook test file(s).
- Minimal fixtures and test doubles.
- Deterministic async/race controls.
- Regression tests.
- Hook test implementation record.
- Passing focused-test evidence.

## Readiness Gate

Use one:

```text
READY_TO_TEST_REACT_HOOK
READY_WITH_CONDITIONS
HOOK_NOT_WORTH_INDEPENDENT_TEST
RETURN_TO_HOOK_DESIGN
RETURN_TO_TEST_STRATEGY
DEPENDENCY_BOUNDARY_REQUIRED
ASYNC_POLICY_REQUIRED
REAL_BROWSER_REQUIRED
BLOCKED
```

Stop when:

- the public hook API is unstable or undefined;
- accepted race/cancellation semantics are missing;
- the test would need to assert internals because no observable contract exists;
- server-state ownership is unresolved.

## Core Workflow

```text
accepted hook contract
→ identify observable states and commands
→ select minimal dependencies and doubles
→ render hook through approved harness
→ invoke semantic command
→ control async completion deterministically
→ assert public state/result
→ test races, retry, cleanup, or rollback when applicable
→ remove implementation coupling
→ run focused tests
```

## Independent-Test Justification

A hook SHOULD have its own suite when at least one applies:

- state machine has several meaningful transitions;
- async behavior is non-trivial;
- several consumers reuse the hook;
- race/cancellation policy is important;
- cleanup is non-trivial;
- optimistic updates exist;
- dependency orchestration is reusable;
- testing through a component would add unrelated noise.

Use:

```text
INDEPENDENT_HOOK_TEST_JUSTIFIED
COMPONENT_TEST_SUFFICIENT
PURE_FUNCTION_TEST_PREFERRED
USE_CASE_TEST_PREFERRED
ADAPTER_TEST_PREFERRED
```

Do not create a hook suite merely because a file begins with `use`.

## Public Contract

Test only the public hook surface.

Examples:

```text
state
data
error
isSubmitting
canRetry
load()
applyPromotion()
retry()
cancel()
reset()
dismissError()
```

Do not reach into:

- internal `useState`;
- reducer dispatch;
- private helper functions;
- refs;
- Effect callbacks;
- request sequence counters;
- AbortController instance;
- internal cache client.

## State Model

Map each accepted public state.

Example:

```text
idle
→ loading
→ success

idle
→ loading
→ error
→ retrying
→ success
```

If the hook uses a discriminated union publicly, assert the semantic variant.

If it exposes booleans publicly by accepted design, assert only valid public combinations.

Do not assert internal grouped state shape if consumers cannot see it.

## Commands

Drive the hook through named commands.

Examples:

```text
load()
applyPromotion(code)
retry()
cancel()
reset()
```

Do not:

- call internal setters;
- call reducer dispatch directly;
- simulate Effect dependencies manually;
- mutate refs.

The test should behave like a real consumer.

## Initial State

Verify only meaningful initial semantics:

- state;
- available commands;
- initial data;
- disabled/enabled state;
- error absence;
- lazy versus immediate behavior.

Do not assert all implementation fields.

## Async Success

Typical sequence:

```text
render
→ invoke command
→ observe pending state
→ resolve dependency
→ observe success state/result
```

Assert:

- command input;
- pending semantics;
- successful result;
- previous data retention when accepted;
- error clearing when accepted.

Do not wait for arbitrary time.

## Async Failure

Verify stable semantic outcomes:

```text
VALIDATION_ERROR
SEMANTIC_ERROR
FORBIDDEN
UNAVAILABLE
UNKNOWN
```

according to the accepted hook API.

Do not assert provider or HTTP error objects when the hook exposes stable semantics.

Verify recovery options such as retry or dismiss when accepted.

## Deterministic Async Control

Use deterministic controllable dependencies.

Possible approaches:

- explicit deferred promise;
- fake dependency with externally controlled resolve/reject;
- mock server handler with controlled response;
- virtual clock for timer behavior;
- controlled AbortSignal.

The test must decide exactly when each async operation completes.

Do not use sleeps to “let the hook update.”

## Retry

Retry tests should prove the semantic contract.

Example:

```text
first attempt
→ unavailable

retry()
→ second dependency call
→ success
```

Verify:

- retry is available only when accepted;
- previous error clears at the accepted time;
- correct input is reused or requested again according to contract;
- duplicate retries are handled correctly;
- retry does not bypass cancellation policy.

Do not assert internal retry counters unless exposed publicly.

## Reset

When `reset()` is public, verify:

- resulting public state;
- retained or cleared data;
- error clearing;
- pending operation behavior;
- whether reset cancels active work.

Do not assume reset means “return every field to original constructor value” unless specified.

## Cancellation

When cancellation is public or lifecycle-owned, test:

- pending operation exists;
- cancellation occurs;
- dependency receives cancellation when that boundary is observable;
- public state becomes accepted cancelled/idle state;
- cancellation is not exposed as system failure unless designed that way;
- late completion cannot overwrite accepted state.

Do not require access to the internal AbortController.

## Unmount Cancellation

If unmount cleanup must cancel active work:

```text
start operation
→ unmount hook
→ complete dependency late
→ no visible post-unmount effect / resource is cleaned
```

Test cleanup through observable dependency/resource effects.

Do not assert `useEffect` cleanup was called directly.

## Race Conditions

Build races deliberately.

Example:

```text
A starts
B starts
B resolves
A resolves later
```

Then assert the accepted policy:

```text
LATEST_REQUEST_WINS
FIRST_REQUEST_WINS
CONCURRENT_BY_KEY
DUPLICATE_REJECTED
QUEUE
LIBRARY_OWNS
```

For latest-wins:

- B result becomes public;
- A resolving later does not replace B.

Do not inspect request sequence refs to prove this.

## Stale Responses

A stale-response test must control completion order.

Bad:

```text
await load A
await load B
```

This never creates a race.

Good conceptual flow:

```text
promise A unresolved
promise B unresolved

start A
start B
resolve B
assert B
resolve A
assert still B
```

The public state is the evidence.

## Duplicate Commands

If duplicate submission is prohibited, test:

```text
first command starts
second command invoked while pending
```

Then assert accepted behavior:

- ignored;
- rejected;
- same promise reused;
- queued;
- disabled via public state.

Do not infer duplicate protection only from call counts when public behavior exists.

## Optimistic Updates

Only test optimistic behavior when explicitly accepted.

Verify:

```text
command
→ optimistic state
→ authoritative success
```

and failure:

```text
command
→ optimistic state
→ rejection
→ rollback or reconciliation
```

Define:

- previous value;
- optimistic value;
- pending indicator;
- authoritative result;
- rollback;
- error;
- concurrency behavior.

Do not add optimistic tests to a hook that has no optimistic contract.

## Optimistic Concurrency

When two optimistic operations can overlap, test the accepted ordering/reconciliation rule.

Do not invent a rule.

If the server-state library owns optimistic concurrency, test only the feature-semantic outcome exposed by the wrapper.

## Cleanup

Test cleanup when the hook owns:

- subscriptions;
- timers;
- event listeners;
- observers;
- external widgets;
- streams;
- in-flight work.

Evidence should be observable:

- unsubscribe called on the fake external source;
- listener removed;
- timer cancelled;
- stream closed;
- late event no longer updates public state.

Do not assert Effect invocation count.

## Subscription Hooks

For reusable subscriptions, test:

```text
subscribe on accepted lifecycle
receive event
update public state
change semantic key
unsubscribe old
subscribe new
unmount
unsubscribe
```

When a value should remain latest without resubscription, test behavior rather than internal ref strategy.

## Dependency Injection

Hooks should receive replaceable dependencies through the accepted composition mechanism.

Test with:

- explicit fake Use Case;
- InMemory repository when the hook legitimately depends on a port by accepted architecture;
- feature provider override;
- composed hook factory override.

Do not import or patch concrete production adapters inside hook tests.

Do not call a global Factory.

## Dependency Call Assertions

A dependency spy may verify:

- semantic command;
- parameters;
- accepted number of calls;
- cancellation;
- retry.

Only assert call order when the contract depends on it.

Avoid asserting incidental helpers or transport calls that belong to adapter tests.

## Use Case Boundary

If the hook wraps a Use Case:

```text
hook command
→ Use Case
→ semantic result
→ hook state
```

Hook tests may fake/stub the Use Case.

They should not reproduce Use Case business-rule scenarios exhaustively.

Use Case tests own those rules.

The hook test owns UI-state adaptation.

## Repository Boundary

If architecture intentionally injects a repository directly into a hook, follow the accepted design.

Prefer an InMemory implementation when it meaningfully exercises the port.

Do not mock repository internals.

However, do not introduce a repository into hook tests if the accepted hook depends on a Use Case.

## Server-State Wrapper

A wrapper around SWR, React Query, Apollo, Relay, RTK Query, or framework data APIs should be tested only when it adds feature semantics.

Test:

- semantic data/result;
- mapped status;
- semantic commands;
- feature key/input behavior if externally significant;
- mutation outcome;
- retry/refetch behavior exposed publicly;
- retained/optimistic state if part of the feature contract.

Do not test:

- cache object internals;
- query observer count;
- retry algorithm of the library;
- deduplication implementation;
- internal status field mapping if not public;
- library hook invocation count.

## Direct Library Hook Preferred

If the wrapper simply renames library fields one-to-one, an independent hook suite may not add value.

Use:

```text
FEATURE_WRAPPER_TEST_JUSTIFIED
DIRECT_LIBRARY_USAGE_SUFFICIENT
COMPONENT_TEST_SUFFICIENT
```

Do not create ceremony around a zero-semantics wrapper.

## Server-State Test Isolation

Create isolated library/cache state per test or accepted suite scope.

Ensure:

- cache is empty or intentionally seeded;
- retries do not leak;
- handlers are scenario-scoped;
- pending requests are cleaned;
- tests do not depend on order.

Do not share mutable query/SWR caches across unrelated hook tests.

## Mock Server Versus Dependency Fake

Use a dependency fake when the hook public contract begins at a semantic dependency such as a Use Case.

Use MSW or repository-approved mock server when the hook itself intentionally wraps the HTTP/server-state integration and that boundary is part of the test.

Do not add MSW merely to make a unit-level state-machine test slower.

## Timers and Debounce

Use fake/virtual timers only when timer behavior is part of the hook contract.

Test:

- delay;
- latest value;
- cancellation;
- reset;
- unmount cleanup;
- leading/trailing semantics when accepted.

Do not use timer flushing as a generic async-testing technique.

## `act` and Test Harness

Use the repository-approved React hook-testing harness correctly.

Any operation that causes React state changes must follow the test tool's expected interaction model.

Prefer user/public commands and supported utilities rather than manually invoking React internals.

Do not create custom render machinery if the repository already provides an accepted harness.

## Rerender

Use rerender only when hook behavior depends on changing public inputs.

Examples:

- resource ID changes;
- enabled flag changes;
- dependency identity changes;
- initial config changes according to contract.

Assert resulting public behavior.

Do not rerender to poke internal Effects.

## Props / Input Changes

For a hook with inputs:

```text
usePromotion(subscriptionId)
```

test:

- initial ID;
- change ID;
- accepted loading/retained state;
- new result;
- stale old result cannot overwrite new result.

This is a strong stale-response case.

## Callback Identity

Do not test function identity by default.

Only test stable identity when it is explicitly part of an integration contract.

Example:

- external subscription requires callback identity stability;
- provider contract requires stable value.

Do not assert `command === previousCommand` merely because `useCallback` is used.

## Memoization

Do not test `useMemo` or `useCallback`.

Test:

- result correctness;
- externally required identity only when semantically accepted;
- measured performance elsewhere if needed.

React Compiler may remove the need for manual memoization; hook tests should remain valid.

## Refs

Do not test internal refs.

Test the behavior the ref enables:

- stale callback reads latest accepted value;
- focus target exposed publicly;
- external instance cleaned;
- request ordering preserved.

## Reducers

If the hook uses a reducer internally:

- hook tests assert public hook behavior;
- pure reducer tests may separately assert transition logic if the reducer itself is a meaningful pure boundary.

Do not assert dispatched action sequence from the hook.

## Errors

Test stable error semantics.

Examples:

```text
invalid
expired
forbidden
unavailable
cancelled
unknown
```

Do not assert:

- raw HTTP status;
- Axios error;
- provider SDK object;
- stack trace.

If translation belongs to the adapter or Use Case, test only the hook-facing semantic result.

## Error Clearing

Test when the public contract defines it:

- new command clears prior error;
- retry clears at start or success;
- dismiss command clears;
- reset clears;
- input change clears only if designed.

Do not assume every change clears errors.

## Error Recovery

For recoverable states test the full hook-level transition:

```text
error
→ retry/dismiss/reset/new command
→ accepted next state
```

The recovery path often matters more than exact error implementation.

## Mount-Time Behavior

If the hook intentionally loads on mount, test:

- initial pending state if observable;
- dependency invoked with current identity;
- result;
- rerender identity changes;
- unmount cleanup.

If server-state library owns mount fetching, test feature semantics rather than library lifecycle.

## Strict Mode

Do not assert exact effect or dependency call counts when development Strict Mode may replay lifecycle unless the production contract requires exact external semantics and the implementation handles replay.

Test:

- no duplicated irreversible outcome;
- proper cleanup;
- stable final public state.

Do not disable Strict Mode merely to make a brittle test pass unless repository test policy explicitly differs.

## Hook Test Data

Use minimal data.

Prefer:

- small semantic values;
- stable IDs;
- fixed timestamps;
- controlled errors;
- explicit previous/current values.

Avoid full production payloads unless the hook contract actually exposes them.

## Async Assertions

Wait for public state.

Good:

```text
wait until state is success
wait until data equals expected result
wait until canRetry becomes true
```

Bad:

```text
sleep
flush all promises five times
wait for internal setState
```

## Test Naming

Name tests by contract.

Good:

```text
keeps the newest promotion when an older request resolves later
rolls back the optimistic promotion when the command fails
unsubscribes from the previous room when subscriptionId changes
exposes retry after an unavailable result
```

Weak:

```text
works
calls effect
sets state
```

## Test Isolation

Each test owns:

- hook render;
- dependency doubles;
- deferred promises;
- timers;
- provider/cache instance;
- mock-server handlers;
- storage;
- subscription source.

Cleanup after each test.

Do not let unresolved promises or timers leak.

## Flakiness

Prevent:

- sleeps;
- shared cache;
- uncontrolled retries;
- real network in focused hook tests;
- shared mutable fakes;
- test-order dependence;
- unresolved async work;
- timing races that are not deliberately controlled.

Race tests should be deterministic by construction.

## Regression Tests

For a hook-level defect:

```text
bug: old request overwrote newer result
```

add:

```text
start A
start B
resolve B
resolve A
assert B remains
```

This is better than adding a broad E2E test when the bug is isolated to the hook.

## Escalation

Escalate when the behavior is not a hook concern.

Use:

```text
HOOK_TEST_SUFFICIENT
COMPONENT_TEST_REQUIRED
ADAPTER_TEST_REQUIRED
USE_CASE_TEST_REQUIRED
ROUTE_OR_E2E_REQUIRED
REAL_BROWSER_REQUIRED
MANUAL_AT_REQUIRED
```

Examples:

- visible focus restoration → component/browser;
- HTTP schema mapping → adapter;
- eligibility rule → Domain/Use Case;
- route hydration → route integration;
- visual layout → browser visual.

## Completion Status

Use:

```text
REACT_HOOK_TESTS_COMPLETE
REACT_HOOK_TESTS_COMPLETE_WITH_CONDITIONS
HOOK_NOT_WORTH_INDEPENDENT_TEST
RETURN_TO_TEST_STRATEGY
TEST_ENVIRONMENT_BLOCKED
REAL_BROWSER_EVIDENCE_REQUIRED
BLOCKED
```

## Output

Use `assets/react-hook-test-implementation-record.md`.

## Completion Criteria

- [ ] Independent hook testing is justified.
- [ ] Public states, commands, inputs, and outputs are explicit.
- [ ] Initial state is tested only where meaningful.
- [ ] Async success and stable failure semantics are tested.
- [ ] Retry/reset behavior is tested when public.
- [ ] Cancellation behavior is tested without reaching into AbortController internals.
- [ ] Race and stale-response tests control completion order deterministically.
- [ ] Duplicate-command behavior is tested when applicable.
- [ ] Optimistic update and rollback are tested only when accepted.
- [ ] Cleanup is tested through observable resource behavior.
- [ ] Dependencies are injected through the accepted boundary.
- [ ] Use Case or adapter business/mapping branches are not duplicated.
- [ ] Server-state wrappers are tested for feature semantics, not library internals.
- [ ] Cache/provider state is isolated.
- [ ] Internal setters, reducer actions, Effects, refs, memoization, and private helpers are not asserted.
- [ ] Callback identity is tested only when semantically required.
- [ ] Async waits target public state rather than sleeps.
- [ ] Regression tests target the smallest hook-level defect.
- [ ] Behavior outside hook scope is escalated to the correct boundary.
- [ ] Focused hook tests pass.
- [ ] No new test library or unrelated architecture change was introduced.

## References

- Read `references/hook-contract-and-observable-state.md` first.
- Read `references/async-retry-cancellation-races-and-stale-responses.md`.
- Read `references/optimistic-updates-cleanup-and-subscriptions.md`.
- Read `references/dependency-injection-and-boundary-selection.md`.
- Read `references/server-state-wrappers-and-test-isolation.md`.
- Read `references/anti-brittleness-regressions-and-escalation.md`.
- Read `references/react-hook-test-audit.md` before completion.
