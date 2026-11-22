---
name: designing-react-effects
description: Portable engineering capability `designing-react-effects`. Use when the
  harness or a specialist agent explicitly requires this named capability.
---
# Designing React Effects

## Purpose

Design lifecycle synchronization between React and an external system.

The first question is always:

```text
Is an Effect necessary?
```

An Effect is appropriate when React must synchronize with something outside React, such as:

- a subscription;
- a timer;
- a browser API;
- an imperative widget;
- analytics lifecycle;
- external storage;
- a DOM integration;
- a network process not already owned by the selected data strategy.

Effects are not the default mechanism for computing values or reacting to user events.

This skill produces a design record, not production code.

## Governing Rules

Effects synchronize React with external systems.

Use an Effect for:

- subscriptions and unsubscriptions;
- timers and cancellation;
- imperative third-party integrations;
- browser or DOM synchronization;
- external resource lifecycle;
- lifecycle analytics when that event is truly lifecycle-based.

Do not use an Effect merely to:

- derive values available during render;
- copy props into state without a synchronization contract;
- invoke an operation that belongs directly in an event handler;
- chain local state changes;
- notify a parent of an event React already knows;
- rebuild fetching, cache, retries, or invalidation already owned by a server-state library.

Effect dependencies MUST be correct.

Effects MAY live in a custom hook when synchronization belongs to the reusable hook responsibility.

## Use When

- Evaluating an existing or proposed `useEffect`.
- A fetch-on-mount Effect may duplicate SWR, React Query, or framework loading.
- A filtered/sorted value is stored through an Effect.
- A component subscribes to an external source.
- Analytics are emitted from state changes or lifecycle.
- A debounced action uses timers.
- A third-party widget has initialize/update/destroy phases.
- A prop is copied into local state.
- An Effect produces stale closures or race conditions.
- `exhaustive-deps` is ignored or suppressed.
- The Effect placement between component and custom hook is unclear.
- Cleanup, Strict Mode, SSR, or hydration behavior matters.

## Do Not Use When

- The task is to implement the Effect.
- The task is general custom-hook design.
- The behavior and external system are undefined.
- The task is server-state library selection.
- The request is only component semantics or styling.
- A pure function can answer the problem without lifecycle synchronization.
- The task is backend-only.

## Inputs

- Accepted frontend slice.
- Component and hook design records.
- Effect candidate or current Effect.
- External-system contract.
- React version, Strict Mode, and rendering model.
- Approved server-state strategy.
- Event and state ownership.
- Dependency identity and composition design.
- Cleanup and cancellation requirements.
- Repository-local `AGENTS.md`.
- Testing conventions.

## Outputs

- Effect necessity decision.
- External system and synchronization contract.
- Correct owner and placement.
- Setup/update/cleanup lifecycle.
- Dependency inventory.
- Stale-closure and identity analysis.
- Race/cancellation strategy.
- Strict Mode and SSR/hydration considerations.
- Test strategy.
- React Effect design record.

## Core Workflow

```text
candidate Effect
→ identify the external system
→ challenge whether render/event/library can own it
→ select owner and trigger semantics
→ define setup/update/cleanup
→ enumerate dependencies
→ design races, cancellation, and idempotency
→ define test evidence
```

## Readiness Gate

Use one:

```text
READY_TO_DESIGN_EFFECT
READY_WITH_CONDITIONS
EFFECT_NOT_REQUIRED
EVENT_HANDLER_REQUIRED
RENDER_DERIVATION_REQUIRED
SERVER_STATE_LIBRARY_REQUIRED
EXTERNAL_STORE_API_REQUIRED
OWNERSHIP_DECISION_REQUIRED
BLOCKED
```

Stop when:

- the external system is not identifiable;
- trigger semantics are ambiguous;
- dependency ownership is unresolved;
- the proposed Effect hides an undefined product behavior.

## Effect Necessity Test

Ask:

1. What external system is synchronized?
2. What starts synchronization?
3. What changes require resynchronization?
4. What cleanup reverses setup?
5. Could the value be derived during render?
6. Could the operation run directly from an event?
7. Does an approved library already own this lifecycle?
8. Is this actually external-store subscription behavior?
9. Is the Effect safe under remount and replay?

If there is no external system, an Effect is usually not required.

## Alternatives to Effects

### Render-Time Derivation

Use render-time calculation for:

- filtered lists;
- sorted lists;
- totals;
- validation summaries;
- display labels;
- booleans derived from props/state;
- view models that are cheap and pure.

Do not store derived values through an Effect.

Memoization may be considered only for measured cost or semantic identity.

### Event Handlers

Use event handlers for:

- submit;
- save;
- delete;
- analytics tied to a specific user action;
- starting a mutation;
- navigation caused by an action;
- updating related local state from the same event.

Do not set state and then use an Effect merely to notice that event.

### Approved Server-State Strategy

Use the project's selected strategy for:

- fetch lifecycle;
- cache;
- deduplication;
- invalidation;
- retries;
- dependent requests;
- background refresh;
- mutation status.

A custom Effect should not recreate this behavior.

### External Store APIs

For store-like subscriptions, consider the project-approved external-store API, such as a React-compatible subscription abstraction, rather than ad hoc Effect state synchronization.

## Synchronization Classification

Use:

```text
SUBSCRIPTION
TIMER
BROWSER_API
DOM_SYNCHRONIZATION
THIRD_PARTY_WIDGET
EXTERNAL_STORAGE
NETWORK_RESOURCE
LIFECYCLE_ANALYTICS
EXTERNAL_STORE
NOT_EXTERNAL_SYNCHRONIZATION
```

## Trigger Semantics

Classify why synchronization begins:

```text
MOUNT_LIFECYCLE
DEPENDENCY_CHANGE
VISIBILITY_CHANGE
ROUTE_CHANGE
RESOURCE_IDENTITY_CHANGE
USER_EVENT
LIBRARY_MANAGED
```

A user event normally belongs in an event handler.

Do not use mount semantics as a substitute for explicit resource identity.

## Placement

Use:

```text
COMPONENT_EFFECT
CUSTOM_HOOK_EFFECT
APP_OR_ROUTE_BOUNDARY_EFFECT
LIBRARY_OWNED
ADAPTER_OWNED
EFFECT_NOT_REQUIRED
```

### Component Effect

Use when synchronization is unique to one component and closely tied to its rendered lifecycle.

### Custom-Hook Effect

Use when synchronization is reusable or deserves an isolated contract.

### App or Route Boundary

Use when lifecycle belongs to navigation, document-level integration, or application composition.

### Library Owned

Use when an approved library already manages synchronization.

### Adapter Owned

Use when technical lifecycle can be encapsulated below React and React only subscribes to a semantic interface.

Do not move an Effect into a hook merely to hide complexity.

## Effect Lifecycle

Define:

```text
setup
→ active synchronization
→ update/resubscribe when semantic identity changes
→ cleanup
```

For each phase record:

- external call;
- resource identity;
- retained handle;
- cleanup;
- failure behavior;
- retry responsibility;
- idempotency.

Setup and cleanup should be symmetrical where the external API permits.

## Dependencies

List every reactive value read by the Effect:

- props;
- state;
- context;
- functions;
- objects;
- resource IDs;
- configuration;
- refs whose current value is intentionally non-reactive.

Then classify:

```text
REACTIVE_DEPENDENCY
STABLE_BY_CONTRACT
NON_REACTIVE_REF
MODULE_CONSTANT
EXTERNAL_MUTABLE_SOURCE
```

Do not omit a dependency merely to reduce executions.

Do not add a dependency blindly without checking whether the Effect has mixed responsibilities.

## Exhaustive Dependencies

An `exhaustive-deps` warning is diagnostic.

Resolve by:

- including the dependency;
- moving event logic to an event handler;
- moving pure derivation to render;
- splitting unrelated synchronization;
- stabilizing identity only when semantically required;
- using a ref for intentionally non-reactive latest data when the contract supports it;
- redesigning ownership.

Do not:

- disable the rule;
- add an empty dependency array to force mount-only behavior;
- wrap every function in `useCallback` only to silence the warning.

## Stale Closures

A stale closure occurs when an Effect callback observes outdated reactive values.

Determine whether the synchronization should use:

- the values that created the subscription;
- the latest values without resubscribing;
- a new subscription whenever values change.

Use:

```text
RESUBSCRIBE_ON_CHANGE
LATEST_VALUE_VIA_REF
EVENT_CALLBACK_BOUNDARY
STABLE_VALUE_BY_CONTRACT
NOT_APPLICABLE
```

A ref is appropriate only when the latest value is intentionally non-reactive and changing it must not recreate synchronization.

Do not use refs to hide real dependencies.

## Splitting Effects

Split an Effect when it synchronizes unrelated systems or has different dependency lifecycles.

Example:

```text
subscription to chat room
and
document title update
```

should usually be separate.

Keep setup and cleanup together for one external resource.

Do not split one coherent subscription across several Effects in a way that breaks symmetry.

## Cleanup

Cleanup is required for applicable:

- subscriptions;
- event listeners;
- timers;
- observers;
- widgets;
- streams;
- pending client requests;
- object URLs;
- locks or external handles.

Cleanup should be:

- safe if called more than once when possible;
- scoped to the exact resource created;
- ordered correctly;
- free from unrelated state mutation.

Do not update state during cleanup merely to avoid a warning.

## Strict Mode

Development Strict Mode may perform an extra setup/cleanup cycle to reveal unsafe Effects.

The design should remain correct when:

```text
setup
→ cleanup
→ setup
```

This requires:

- symmetric cleanup;
- no leaked listeners/timers/widgets;
- idempotent or reversible initialization;
- no duplicate irreversible side effect from mount-only assumptions.

Do not “fix” Strict Mode by adding a ref that suppresses the second setup if the real lifecycle remains unsafe.

## SSR and Hydration

Effects do not run during server rendering.

Consider:

- server-safe initial markup;
- hydration consistency;
- browser API access only after client boundary;
- layout shift;
- client-only widget placeholders;
- persisted-state reconciliation;
- route transitions.

Do not rely on an Effect to correct markup that must match during hydration.

Browser-only integration should live in the smallest client boundary.

## Fetch on Mount

Default questions:

1. Does the framework or server-state library already own fetching?
2. Is caching/deduplication/retry required?
3. Can the request start before mount?
4. Is the component responsible for resource identity?
5. What happens on route changes?
6. How are stale responses and cancellation handled?

Usually prefer the approved data strategy.

A raw Effect fetch may be acceptable only when:

- the request is truly lifecycle synchronization;
- caching is unnecessary;
- ownership is local and explicit;
- cancellation/races are designed;
- repository policy permits it.

Do not use an empty dependency array while reading changing resource identity.

## Derived Filtered Lists

Bad conceptual flow:

```text
items/filter
→ Effect
→ setFilteredItems
```

Preferred:

```text
filteredItems = derive(items, filter)
```

Use memoization only if computation is expensive or identity matters.

Do not create duplicate sources of truth.

## Subscriptions

For a subscription define:

- subscription key/resource identity;
- callback semantics;
- initial snapshot;
- update ordering;
- resubscription;
- cleanup/unsubscribe;
- reconnect behavior;
- error behavior;
- external-store suitability.

Do not subscribe in render.

Do not resubscribe on every render due to unstable dependency identity.

## Analytics

Classify analytics:

```text
USER_ACTION_ANALYTICS
VIEW_OR_IMPRESSION_ANALYTICS
LIFECYCLE_ANALYTICS
STATE_TRANSITION_ANALYTICS
```

User-action analytics normally belongs in the event handler that caused the action.

View/impression analytics may require an Effect when visibility or mounted lifecycle is the actual event.

Define:

- event name;
- exactly-once or at-least-once expectation;
- Strict Mode/dev behavior;
- route identity;
- consent/privacy;
- deduplication owner;
- payload redaction.

Do not emit analytics from every render or from broad state watchers.

## Debounced Actions

Distinguish:

```text
DEBOUNCED_DERIVED_VALUE
DEBOUNCED_USER_COMMAND
DEBOUNCED_EXTERNAL_SYNCHRONIZATION
```

A debounced command may be designed in an event-driven hook with a timer lifecycle.

Define:

- delay;
- leading/trailing behavior;
- cancellation;
- flush;
- dependency identity;
- latest input;
- unmount;
- race with network completion.

Do not use an Effect debounce when a direct event-owned debouncer is clearer.

## Timers

For timers define:

- interval/timeout;
- start trigger;
- reset conditions;
- pause/resume;
- cleanup;
- latest callback semantics;
- background-tab behavior;
- fake-timer testing.

Avoid including a changing callback directly if it recreates an interval unintentionally; choose a clear latest-callback or resubscription contract.

## Third-Party Widgets

For an imperative widget define:

```text
create
→ configure
→ update
→ destroy
```

Record:

- host DOM ownership;
- instance ref;
- configuration identity;
- update versus recreate behavior;
- event callbacks;
- cleanup;
- Strict Mode;
- SSR/client boundary;
- widget errors;
- accessibility ownership;
- memory/resource leaks.

Do not instantiate the widget during render.

Do not recreate it for every cosmetic prop when an update API exists.

## Browser Storage

For storage synchronization distinguish:

- initial read;
- ongoing write;
- cross-tab subscription;
- schema/version;
- parse failure;
- privacy;
- SSR fallback;
- source-of-truth ownership.

Do not copy every state change to storage through a broad Effect without throttling, schema, and failure semantics.

## DOM Synchronization

Use Effects for imperative DOM behavior only when declarative props are insufficient.

Examples:

- focus after a defined transition;
- measurement;
- observer registration;
- scrolling;
- media control.

For visual measurement before paint, the project may require the layout-effect variant, but this must be justified because it blocks painting.

Do not use imperative DOM mutation for behavior React can render declaratively.

## Focus Effects

Define:

- exact transition causing focus;
- target;
- whether target exists;
- focus restoration;
- user-initiated versus automatic behavior;
- accessibility impact;
- retries when rendering is conditional.

Avoid moving focus on every render or every validation change.

## Race Conditions

For async Effects define:

```text
LATEST_RESOURCE_WINS
EACH_RESOURCE_INDEPENDENT
CANCEL_PREVIOUS
IGNORE_STALE_RESULT
LIBRARY_OWNS
```

Use request identity or cancellation as appropriate.

A mounted flag only prevents updates after unmount; it does not solve ordering among active requests.

## Cancellation

Cancellation may stop client work but not necessarily reverse external side effects.

Record:

- abort mechanism;
- cleanup timing;
- stale-result behavior;
- user-visible cancellation;
- server ambiguity;
- retry.

Do not treat cancellation as a product failure unless accepted behavior says so.

## Error Handling

Define whether synchronization errors are:

- rendered;
- retried;
- logged;
- ignored under a documented policy;
- escalated to an error boundary;
- returned through a hook contract.

Do not throw technical errors from asynchronous Effect callbacks expecting an error boundary to catch them automatically.

Do not expose secrets or provider payloads.

## Idempotency and Duplicate Side Effects

Effects that create irreversible side effects require special scrutiny.

Examples:

- purchase;
- mutation;
- email;
- analytics with strict billing impact;
- external command.

Prefer event handlers or explicit Application commands.

Mount-driven irreversible commands are normally unsafe.

If lifecycle execution is required, define deduplication and authoritative ownership explicitly.

## Dependency Identity

Unstable functions/objects can recreate synchronization.

Possible responses:

- move object/function creation inside the Effect;
- pass primitives or stable semantic IDs;
- move ownership upward/downward;
- use memoization when identity is a real contract;
- split the Effect.

Do not memoize indiscriminately.

## Refs

Refs may hold:

- external instance;
- timer handle;
- latest non-reactive callback;
- previous value for synchronization logic;
- DOM node;
- request sequence.

Refs must not become hidden mutable state that should trigger rendering.

Document why ref updates are intentionally non-reactive.

## Effect Events or Equivalent APIs

When the React version/project provides an approved mechanism for reading latest values inside an Effect without making them reactive, it may be used for non-reactive event-like logic.

The design must still identify:

- which values are reactive;
- which values are latest-only;
- why resubscription is not intended.

Do not use emerging APIs without repository approval and version support.

## Testing

Test observable synchronization behavior:

- setup;
- update/resubscribe;
- cleanup;
- dependency changes;
- unmount;
- Strict Mode-compatible lifecycle;
- timer advance;
- external event;
- stale response;
- cancellation;
- widget creation/update/destroy;
- analytics trigger semantics.

Prefer fake adapters, event targets, timers, or widget spies.

Do not assert merely that `useEffect` was called.

Do not test React internals.

## Effect Design Decisions

Use:

```text
EFFECT_DESIGN_READY
EFFECT_DESIGN_READY_WITH_CONDITIONS
EFFECT_NOT_REQUIRED
MOVE_TO_RENDER_DERIVATION
MOVE_TO_EVENT_HANDLER
DELEGATE_TO_SERVER_STATE_LIBRARY
DELEGATE_TO_EXTERNAL_STORE
SPLIT_EFFECT_REQUIRED
DEPENDENCY_OR_IDENTITY_DECISION_REQUIRED
CLEANUP_OR_RACE_DECISION_REQUIRED
RETURN_TO_HOOK_OR_COMPONENT_DESIGN
BLOCKED
```

## Output

Use `assets/react-effect-design-record.md`.

## Completion Criteria

- [ ] The external system is explicitly identified.
- [ ] Render derivation, event handling, server-state ownership, and external-store alternatives were considered first.
- [ ] Effect necessity is justified.
- [ ] Owner and placement are explicit.
- [ ] Trigger and resource identity are explicit.
- [ ] Setup, update/resubscribe, and cleanup are symmetrical.
- [ ] Every reactive dependency is classified.
- [ ] No `exhaustive-deps` suppression is used as a design solution.
- [ ] Stale closure behavior is explicit.
- [ ] Unrelated synchronization is split.
- [ ] Strict Mode remount behavior is safe.
- [ ] SSR/hydration and client boundaries are considered.
- [ ] Races and cancellation are explicit where applicable.
- [ ] Fetching, caching, retry, and invalidation are not rebuilt when a library owns them.
- [ ] Analytics and mutations use event ownership when appropriate.
- [ ] Third-party widget lifecycle is complete when applicable.
- [ ] Memoization or refs are used only with semantic justification.
- [ ] Tests verify observable synchronization and cleanup.
- [ ] No implementation code or new library selection was produced.

## References

- Read `references/effect-necessity-and-alternatives.md` first.
- Read `references/dependencies-stale-closures-and-identity.md` for dependency design.
- Read `references/setup-cleanup-strict-mode-and-ssr.md` for lifecycle.
- Read `references/fetch-subscriptions-analytics-and-debounce.md` for common cases.
- Read `references/third-party-widgets-dom-and-storage.md` for imperative systems.
- Read `references/react-effect-design-audit.md` before completion.
