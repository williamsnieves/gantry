---
name: designing-react-custom-hooks
description: Designs reusable React custom-hook contracts, dependency injection, state transitions, async behavior, cancellation, race protection, and stable return APIs for one frontend slice. Use when deciding whether behavior belongs in a hook, choosing multiple useState calls versus grouped state or useReducer, exposing commands instead of raw setters, placing Effects inside reusable hooks, preventing stale responses, and integrating approved server-state libraries without rebuilding them. Do not implement code, turn hooks into a second Application layer, import concrete adapters or global factories, add memoization mechanically, introduce state libraries, or invent behavior.
...
---

# Designing React Custom Hooks

## Purpose

Design one custom hook that answers:

```text
How does this reusable React behavior work?
```

A hook design should define:

- responsibility;
- consumers;
- dependency injection;
- state ownership;
- valid transitions;
- async lifecycle;
- cancellation and race handling;
- Effect ownership;
- commands and events;
- stable return API;
- server-state integration;
- test boundary.

The skill produces a design record, not production code.

## Governing Rules

Custom hooks encapsulate reusable React behavior, state, and integration.

They SHOULD NOT become a second Application layer.

Use Cases and replaceable dependencies SHOULD be passed explicitly or obtained through an approved composition mechanism.

Hooks MUST NOT:

- import concrete adapters;
- call a global Factory internally;
- locate services dynamically;
- rebuild a server-state library;
- expose raw setters by default;
- suppress dependency rules without semantic justification.

Effects MAY live inside a hook when synchronization belongs to the reusable hook responsibility.

Use `useMemo` and `useCallback` only for:

- semantic identity;
- measured performance;
- integration requirements.

When React Compiler or equivalent optimization is enabled, avoid redundant manual memoization.

## Use When

- Reusable React behavior needs an independent contract.
- Several components share stateful interaction logic.
- A component is mixing orchestration, async behavior, and rendering.
- One versus several `useState` calls is uncertain.
- A `useReducer` decision is needed.
- A hook exposes raw setters or implementation details.
- Async responses may arrive out of order.
- Cancellation or unmount safety matters.
- An Effect may belong inside a reusable hook.
- A hook wraps SWR, React Query, framework loaders, Apollo, Relay, RTK Query, or another approved strategy.
- The hook return shape—object or tuple—is unclear.
- A hook is incorrectly acting as a service container.

## Do Not Use When

- The task is to implement the hook.
- The behavior is pure and React-independent.
- The task is only Effect design.
- The task is only component design.
- The architecture profile or slice is unresolved.
- The behavior has one trivial consumer and no stable hook responsibility.
- A new state or server-state library is being selected.
- The task is backend-only.

## Inputs

- Accepted frontend slice.
- Component design record.
- Frontend profile decision.
- Existing hooks and consumers.
- State and server-state ownership.
- Approved Use Cases, adapters, and composition mechanisms.
- Async/error/cancellation requirements.
- Existing server-state library and conventions.
- React version and compiler configuration.
- Repository-local `AGENTS.md`.
- Testing conventions.

## Outputs

- Hook responsibility and consumer map.
- Hook necessity decision.
- Dependency-injection design.
- State model and transition table.
- Async, cancellation, and race strategy.
- Effect ownership decision.
- Commands and events.
- Return API shape.
- Stability and memoization decisions.
- Server-state integration boundary.
- Hook test proposal.
- React custom-hook design record.

## Core Workflow

```text
accepted behavior
→ identify reusable React responsibility
→ separate React behavior from Application/business logic
→ define dependencies and composition
→ choose state representation
→ model transitions and async races
→ place Effects only where synchronization belongs
→ design commands and return API
→ define server-state and test boundaries
```

## Readiness Gate

Use one:

```text
READY_TO_DESIGN_REACT_HOOK
READY_WITH_CONDITIONS
HOOK_NOT_JUSTIFIED
RETURN_TO_COMPONENT_DESIGN
RETURN_TO_APPLICATION_DESIGN
EFFECT_DECISION_REQUIRED
SERVER_STATE_POLICY_REQUIRED
DEPENDENCY_OWNERSHIP_REQUIRED
BLOCKED
```

Stop when:

- hook ownership is unclear;
- behavior is actually pure Application/Domain logic;
- server-state policy is unresolved;
- dependencies can only be obtained through forbidden global lookup;
- accepted transitions or error behavior are undefined.

## Hook Necessity

A custom hook is justified when it owns one coherent reusable React behavior.

Strong indicators:

- several components consume the same React behavior;
- a component has complex state transitions;
- browser/framework synchronization is reusable;
- approved server-state integration needs a stable feature contract;
- cancellation and race handling should be centralized;
- a UI workflow has a stable commands/state API.

Weak indicators:

- code is merely long;
- one component has one `useState`;
- a function begins with `use`;
- one API call needs a wrapper;
- logic is pure and could be a normal function;
- a hook would only rename an existing library hook.

Use:

```text
CUSTOM_HOOK_REQUIRED
CUSTOM_HOOK_JUSTIFIED
COLOCATED_COMPONENT_STATE_PREFERRED
PLAIN_FUNCTION_PREFERRED
APPLICATION_USE_CASE_PREFERRED
EXISTING_HOOK_REUSED
```

## Responsibility Boundary

A hook may own:

- React state;
- event-to-state transitions;
- integration with an approved server-state hook;
- synchronization with browser/framework systems;
- cancellation and request identity;
- reusable status/error mapping for UI;
- stable commands for components.

A hook should not own:

- substantial business invariants;
- repository implementation;
- transport decoding when an adapter owns it;
- concrete HTTP/SDK details;
- application-wide dependency selection;
- product policy invented from UI behavior.

## React Versus Application Logic

Ask whether the behavior can exist without React.

If yes and it represents a user intention or business workflow, prefer:

```text
Application Use Case
```

The hook may adapt the Use Case into React state.

Example:

```text
ApplyPromotion Use Case
→ useApplyPromotion hook
→ component
```

The hook owns:

- submitting state;
- cancellation;
- stale response protection;
- UI error/status mapping;
- command exposure.

The Use Case owns:

- orchestration and semantic outcome.

## Dependency Injection

Dependencies may be:

- passed as hook parameters;
- provided by an approved feature-level context;
- closed over by an explicit composition factory;
- obtained from an approved library provider;
- passed through a configured server-state hook.

Do not:

- import a concrete repository;
- instantiate an adapter in the hook;
- call a global factory;
- use a Service Locator;
- read hidden mutable globals.

Use one:

```text
EXPLICIT_PARAMETER_INJECTION
FEATURE_CONTEXT_INJECTION
COMPOSED_HOOK_FACTORY
APPROVED_LIBRARY_PROVIDER
NO_REPLACEABLE_DEPENDENCY
```

## Hook Parameters

Parameters should represent:

- stable identity;
- initial state;
- feature configuration;
- semantic dependencies when explicitly injected;
- enabled/disabled conditions.

Avoid:

- large dependency bags;
- transport-specific options;
- arbitrary config objects;
- raw state setters;
- hidden defaults that change behavior significantly.

Document whether parameter identity matters.

## State Inventory

Classify hook state:

```text
EPHEMERAL_UI_STATE
FORM_STATE
ASYNC_OPERATION_STATE
SERVER_STATE_DERIVATION
OPTIMISTIC_STATE
BROWSER_SYNCHRONIZATION_STATE
SELECTION_STATE
TRANSITION_STATE
ERROR_STATE
```

Do not duplicate state already owned by the server-state library.

Derived values should remain derived when possible.

## Choosing State Representation

Use one or several `useState` calls when values evolve independently.

Use grouped state when:

- several fields transition together;
- atomic updates matter;
- invalid combinations should be prevented;
- one operation owns the lifecycle.

Use `useReducer` when:

- transitions are numerous or explicit;
- several events lead to shared transitions;
- state evolution benefits from a transition table;
- undo/redo or workflow behavior exists;
- reducer tests provide value.

No universal rule requires:

- exactly one `useState`;
- never using `useReducer`;
- always using a reducer for complex state.

## Multiple `useState`

Prefer separate state when:

- values are independent;
- updates do not need atomic coordination;
- one value changing should not conceptually change the others;
- state remains simple and local.

Potential smell:

```text
isLoading
isSuccess
error
data
```

when they permit impossible combinations.

## Grouped State

Use a state object or discriminated union when one operation has coherent phases.

Conceptual example:

```text
idle
submitting(previousData?)
success(data)
error(previousData?, reason)
```

Record intentional retained data and background refresh states.

## `useReducer`

A reducer design should define:

- state;
- events/actions;
- transition table;
- invalid-event behavior;
- initialization;
- reset;
- side-effect boundary.

Reducers MUST remain pure.

Effects and async commands should occur outside the reducer.

Do not use Redux-style ceremony for a trivial local toggle.

## Transition Table

For each event define:

| Current state | Event | Next state | Side effect | Invalid? |
|---|---|---|---|---|

Examples:

```text
idle
→ submit
→ submitting
→ invoke dependency

submitting
→ resolved
→ success
→ update cache

submitting
→ rejected
→ error
→ announce status

submitting
→ submit
→ unchanged or rejected
→ no duplicate request
```

The hook contract must define duplicate command behavior.

## Updates

Use functional state updates when next state depends on previous state.

Direct updates are valid when they do not.

The design should identify transitions that require previous state:

- append/remove;
- toggle;
- retry count;
- optimistic rollback;
- selection changes;
- undo/redo.

Do not require functional updates mechanically.

## Commands Versus Raw Setters

Prefer named commands:

```text
applyPromotion(code)
retry()
dismissError()
reset()
selectItem(id)
cancel()
```

Avoid:

```text
setLoading
setError
setData
setState
```

unless setter semantics are intentionally the public API.

A public setter exposes internal representation and weakens future evolution.

## Hook Return Shape

Use an object for larger or evolving APIs.

Example conceptual shape:

```text
{
  state,
  applyPromotion,
  retry,
  dismissError,
  canSubmit
}
```

Use a tuple when:

- the API is small;
- positional semantics are conventional and stable;
- there is little evolution risk.

Examples:

```text
[value, setValue]
[isOpen, open, close]
```

Do not prohibit destructuring.

Use one:

```text
OBJECT_API
TUPLE_API
SINGLE_VALUE
COMMAND_ONLY
```

## Return API Principles

The return API should be:

- minimal;
- semantic;
- stable;
- free from concrete dependencies;
- free from raw transport responses;
- explicit about states and commands.

Avoid returning:

- internal dispatch;
- AbortController;
- raw SDK error;
- cache client;
- repository;
- unstable helper functions with no consumer need.

## Async Lifecycle

For every async command define:

```text
start
pending
success
semantic failure
system failure
cancellation
stale response
retry
unmount
```

Record:

- duplicate-submission policy;
- whether previous data remains visible;
- cache update ownership;
- retry ownership;
- cancellation ownership;
- error clearing;
- command result contract.

## Race Conditions

Common race:

```text
request A starts
request B starts
request B resolves
request A resolves later
```

The hook must define whether A may overwrite B.

Possible strategies:

- AbortController cancellation;
- request sequence/version;
- stable request key;
- library-provided deduplication;
- latest-wins guard;
- first-wins lock;
- queue;
- reject concurrent command.

Choose according to accepted behavior.

Do not add race machinery when concurrency is impossible by contract.

## Stale Response Protection

Use one:

```text
LATEST_REQUEST_WINS
FIRST_REQUEST_WINS
CONCURRENT_REQUESTS_ALLOWED_BY_KEY
DUPLICATE_COMMAND_REJECTED
QUEUE_COMMANDS
LIBRARY_OWNS_RACE_HANDLING
NOT_APPLICABLE
```

Record evidence for the selected strategy.

A mounted flag alone is not sufficient for ordering between multiple active requests.

## Cancellation

Distinguish:

- user cancellation;
- navigation/unmount cancellation;
- superseded request;
- timeout;
- library-managed cancellation.

Cancellation should not normally appear as an error to the user unless product behavior requires it.

Do not assume aborting a client request means a server-side mutation did not happen.

## Effect Ownership

An Effect belongs in a hook when the hook owns reusable synchronization with an external system.

Examples:

- subscription;
- timer;
- browser storage;
- media query;
- document event;
- third-party API;
- lifecycle-triggered I/O required by framework;
- cleanup.

An Effect should not be used for:

- pure derivation;
- command execution that belongs in an event handler;
- copying props into state without a synchronization contract;
- invoking a callback solely because state changed after an event;
- rebuilding server-state fetching manually.

Route detailed effect reasoning to:

```text
designing-react-effects
```

## Effect Dependencies

The hook design must identify:

- external values read;
- stable or unstable dependency identity;
- cleanup;
- resubscription behavior;
- stale closure risk;
- lint compliance.

Do not suppress exhaustive dependency rules without an explicit semantic decision.

## Server-State Integration

Remote state should use the selected project strategy when caching, deduplication, invalidation, retries, or synchronization are required.

Examples:

```text
SWR
React Query
framework loaders/actions
Apollo
Relay
RTK Query
```

The custom hook may:

- wrap the approved library for a feature-semantic API;
- map library state to feature state;
- expose semantic commands;
- configure keys and invalidation according to project policy;
- translate stable errors if that boundary belongs here.

It must not reimplement:

- cache;
- deduplication;
- retry engine;
- invalidation graph;
- background synchronization;
- global request registry.

## Hook Wrapping a Server-State Library

A wrapper is justified when it adds a stable feature contract.

Good value:

- semantic name;
- feature-owned key construction;
- error/state mapping;
- mutation/cache coordination;
- multiple library calls combined coherently;
- hiding library details from components.

Weak value:

- one-to-one rename;
- forwarding all library fields unchanged;
- no feature semantics;
- creating another generic data hook.

Use:

```text
FEATURE_HOOK_JUSTIFIED
DIRECT_LIBRARY_HOOK_PREFERRED
APPLICATION_ADAPTER_REQUIRED
```

## Error Model

Separate:

```text
VALIDATION_ERROR
SEMANTIC_ERROR
FORBIDDEN
NOT_FOUND
UNAVAILABLE
CANCELLED
UNKNOWN
```

The hook should expose stable UI-facing errors.

It should not expose:

- HTTP status as primary semantics;
- SDK error objects;
- stack traces;
- provider codes unless accepted as feature semantics.

Record when error mapping belongs to the HTTP adapter instead.

## Error Clearing

Define when errors clear:

- new submit;
- input change;
- explicit dismiss;
- retry;
- navigation;
- successful result.

Do not clear an error merely because an unrelated render occurred.

## Optimistic State

Use only when accepted.

Define:

- optimistic state;
- authoritative confirmation;
- rollback;
- concurrent updates;
- error presentation;
- cache ownership;
- reconciliation.

Do not add optimistic behavior solely for responsiveness.

## Context

A hook may consume feature context for stable dependencies or shared feature state.

The context must have:

- explicit provider scope;
- stable value contract;
- missing-provider behavior;
- test setup;
- render-performance consideration.

Do not consume a global “services” context containing arbitrary adapters.

## Memoization and Identity

Use `useCallback` when:

- consumer effect/subscription semantics require stable function identity;
- memoized child behavior is measured and relevant;
- an external integration requires identity stability;
- the repository policy requires it for a specific boundary.

Use `useMemo` when:

- object identity is semantically significant;
- computation is measured as expensive;
- provider/context value stability requires it;
- integration contracts require stable identity.

Do not add memoization mechanically.

When React Compiler is enabled:

- follow compiler constraints;
- avoid redundant manual memoization;
- preserve semantic identities explicitly required by integrations.

## Nested Functions

Local functions are allowed.

Extract when:

- nesting hides the hook contract;
- function is reused;
- testability improves;
- accidental recreation has measured impact;
- the function is pure and belongs outside React.

Do not forbid nested functions universally.

## Composition Boundary

If the hook itself is the explicit composition boundary, document:

- why;
- which dependencies are selected;
- lifecycle;
- testing overrides;
- why selection is not hidden.

Otherwise, dependency selection belongs outside the hook.

The default is not to import a global factory.

## Hook Naming

Use `use*` and intent-revealing capability language.

Good:

```text
useApplyPromotion
usePromotionApplication
useSubscriptionPromotion
```

Weak:

```text
useData
useService
useApi
useStuff
```

The name should describe the reusable React behavior, not the technology.

## Consumers

Record:

- current consumers;
- expected stable consumers;
- whether behavior is truly reusable;
- whether one consumer still justifies isolation due to complexity.

A hook may be justified with one consumer when:

- behavior is complex;
- it creates a clear test boundary;
- it isolates synchronization;
- it separates container and presentation.

Do not extract trivial state only for file count.

## Testing Boundary

Test a custom hook independently when its behavior is reusable or complex enough to deserve a contract.

Hook tests should cover:

- initial state;
- commands;
- valid transitions;
- functional updates;
- async success;
- semantic/system failure;
- cancellation;
- stale response;
- duplicate command;
- retry/reset;
- cleanup;
- dependency invocation;
- server-state integration contract.

Do not retest server-state library internals.

Pure reducers/functions should be tested without rendering hooks.

## Hook Design Decisions

Use:

```text
HOOK_DESIGN_READY
HOOK_DESIGN_READY_WITH_CONDITIONS
HOOK_NOT_JUSTIFIED
STATE_MODEL_DECISION_REQUIRED
DEPENDENCY_INJECTION_DECISION_REQUIRED
ASYNC_RACE_DECISION_REQUIRED
EFFECT_DESIGN_REQUIRED
SERVER_STATE_BOUNDARY_REQUIRED
RETURN_TO_COMPONENT_DESIGN
RETURN_TO_APPLICATION_DESIGN
BLOCKED
```

## Output

Use `assets/react-custom-hook-design-record.md`.

## Completion Criteria

- [ ] Accepted slice and hook scope are explicit.
- [ ] Hook necessity is justified.
- [ ] React behavior is separated from pure Application/Domain logic.
- [ ] Dependencies are explicit or obtained through an approved mechanism.
- [ ] No concrete adapter, global Factory, or Service Locator is hidden inside the hook.
- [ ] State ownership is classified.
- [ ] Multiple `useState`, grouped state, or `useReducer` is selected by behavior.
- [ ] Valid transitions and invalid combinations are explicit.
- [ ] Commands are semantic and raw setters are excluded unless intentional.
- [ ] Object or tuple return shape is justified.
- [ ] Async success, failure, cancellation, retry, and unmount behavior are explicit.
- [ ] Race and stale-response strategy is explicit where applicable.
- [ ] Effects are included only for reusable synchronization.
- [ ] Effect dependencies and cleanup are explicit.
- [ ] Approved server-state strategy is reused rather than rebuilt.
- [ ] Error model is stable and technical details are excluded.
- [ ] Memoization is evidence-driven or semantically required.
- [ ] Test boundary proves hook behavior without retesting library internals.
- [ ] No implementation code or new library selection was produced.
