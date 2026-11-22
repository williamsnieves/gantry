---
name: modeling-frontend-async-state
description: Models frontend optional and asynchronous state around valid UI states. Use when a React feature must represent idle, loading, success, error, refreshing, stale, partial-data, optimistic, retry, or cancellation semantics without impossible boolean combinations. Decide when undefined/null/Maybe<T> is enough, when a discriminated union is justified, and when the project's selected server-state library should remain the state owner instead of copying remote state into local React state. Do not rebuild React Query/SWR/Apollo/Relay/RTK Query/framework status machines inside custom hooks, add refreshing/stale/optimistic states without product behavior, or collapse cancellation and meaningful failures into one generic error.
---

# Modeling Frontend Async State

## Purpose

Choose an async-state representation that makes valid UI states explicit and invalid combinations difficult or impossible.

The skill answers:

```text
What states can this UI actually be in?
```

and:

```text
Who owns those states?
```

before deciding:

```text
useState
useReducer
discriminated union
Maybe<T>
server-state library status
```

The goal is not to create the biggest state machine.

The goal is to model only the states the accepted behavior requires.

## Governing Standard

The project MUST choose a coherent representation for optional and asynchronous values.

Allowed approaches include:

- `undefined`;
- `null`;
- `Maybe<T>`;
- discriminated unions;
- server-state library status objects.

`Maybe<T>` is a valid project policy, not a universal requirement.

Do not mix multiple absence conventions within the same boundary without reason.

For complex async behavior, prefer explicit states:

```ts
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: AppError };
```

Add refreshing or stale states only when behavior requires them.

Remote server state SHOULD use the project's selected server-state strategy when caching, deduplication, invalidation, retries, or synchronization are required.

Do not rebuild a server-state library inside a custom hook.

## Use When

- Async UI has more than simple loading/success.
- Several booleans can contradict one another.
- Background refresh needs different rendering from initial load.
- Existing data should remain visible during refresh or retry.
- Partial success exists.
- Optimistic state needs explicit ownership.
- Cancellation has user-visible semantics.
- Retry behavior changes the state transition.
- Optional/absence conventions are inconsistent.
- Server-state status and local React state are duplicated.
- A hook/component needs a stable public state contract.

## Do Not Use When

- Data is synchronous.
- One optional value is adequately represented by the accepted boundary convention.
- The task is server-state query-key/cache/invalidation design.
- The task is implementing a custom hook.
- The task is designing a Use Case.
- The feature already uses an approved server-state status model and no feature-specific state is added.
- The proposal creates explicit states that product behavior cannot distinguish.

## Inputs

- Accepted UI behavior.
- Architecture profile.
- Selected optional-value convention.
- Selected server-state strategy, if any.
- Hook/component design.
- Use Case/result contract.
- Error semantics.
- Cancellation policy.
- Retry policy.
- Optimistic-update policy.
- Partial-data behavior.
- Background-refresh behavior.
- Existing state shape.
- Test strategy.
- Repository-local `AGENTS.md`.

## Outputs

- Async-state ownership decision.
- Optional-value convention.
- State inventory.
- State representation decision.
- Discriminated union when justified.
- Transition table.
- Data-retention semantics.
- Background-refresh/stale semantics.
- Retry/cancellation semantics.
- Optimistic/rollback ownership.
- Partial-data model.
- Server-state integration policy.
- Async-state test matrix.
- Frontend async-state modeling record.

## Core Workflow

```text
accepted behavior
→ identify state owner
→ enumerate observable states
→ remove impossible/redundant states
→ choose optional-value convention
→ choose representation
→ define transitions
→ define data retention
→ integrate server-state owner
→ define tests
```

## Readiness Gate

Use one:

```text
READY_TO_MODEL_FRONTEND_ASYNC_STATE
READY_WITH_CONDITIONS
ASYNC_STATE_NOT_REQUIRED
STATE_OWNER_REQUIRED
OPTIONAL_VALUE_POLICY_REQUIRED
ERROR_SEMANTICS_REQUIRED
RETRY_POLICY_REQUIRED
CANCELLATION_POLICY_REQUIRED
OPTIMISTIC_POLICY_REQUIRED
PARTIAL_DATA_POLICY_REQUIRED
BLOCKED
```

A valid result may be:

```text
ASYNC_STATE_NOT_REQUIRED
```

Do not create a state machine for a single optional value.

# State Ownership

Classify the owner first:

```text
LOCAL_UI_STATE
HOOK_ASYNC_STATE
SERVER_STATE_LIBRARY
APPLICATION_RESULT
ROUTE_LOADER_STATE
EXTERNAL_STORE
MIXED_WITH_EXPLICIT_BOUNDARY
```

The owner determines which layer should represent:

- loading;
- error;
- retry;
- freshness;
- optimistic state;
- cancellation.

Do not copy state merely to make it convenient.

## Single Owner Principle

Each async concern should have one primary owner.

Examples:

```text
SWR owns:
data
error
isLoading
isValidating
cache freshness

feature hook may own:
selectedItem
modal state
semantic command pending state not represented by SWR
```

Avoid:

```text
SWR data
→ copied to local data state
SWR error
→ copied to local error state
SWR loading
→ copied to isLoading
```

without explicit product semantics.

# Observable State Inventory

Enumerate states in product/UI language.

Possible states:

```text
idle
loading
success
empty
error
refreshing
stale
retrying
cancelled
optimistic
rollingBack
partial
permissionDenied
```

Do not include every possible label automatically.

A state belongs only if:

- behavior differs;
- rendering differs;
- allowed commands differ;
- data retention differs;
- recovery differs;
- accessibility announcement differs.

# Initial State

Choose intentionally.

Possible initial semantics:

```text
idle
loading immediately
hydrated success
cached stale
server-provided success
```

Do not assume every async flow starts at `idle`.

Server/route data may start already loaded.

# Idle

Use `idle` when the operation has not started and that distinction matters.

Examples:

- search waits for minimum query length;
- user has not submitted;
- optional lazy panel not opened.

Do not add `idle` if the operation always starts immediately and no caller can observe it.

# Loading

Initial loading usually means:

```text
no usable data yet
+
operation in flight
```

This differs from background refresh when prior data remains usable.

Avoid one `isLoading` flag for both semantics if the UI behaves differently.

# Success

Success should contain the data required by that state.

Good:

```ts
{ status: 'success'; data: T }
```

Avoid:

```ts
{
  status: 'success',
  data?: T
}
```

unless success legitimately permits absence.

# Empty

Empty may be:

```text
success with []
```

or a distinct state:

```text
{ status: 'empty' }
```

Choose based on UI semantics.

Use a distinct `empty` state when:

- rendering is materially different;
- available commands differ;
- empty has semantic meaning beyond zero items.

Do not create `empty` just because an array can be empty.

# Error

Error state should contain a stable semantic error.

Do not expose raw:

```text
AxiosError
Response
provider SDK error
stack trace
```

Async state should consume Application/port-safe errors.

## Error Data Retention

Decide whether an error retains prior data.

Possible:

```text
INITIAL_ERROR_NO_DATA
REFRESH_ERROR_WITH_STALE_DATA
MUTATION_ERROR_WITH_ROLLBACK
```

Do not assume every error must clear data.

# Impossible Boolean Combinations

Avoid state such as:

```ts
{
  isLoading: boolean
  isError: boolean
  isSuccess: boolean
  isRefreshing: boolean
  data?: T
  error?: Error
}
```

unless the library itself owns a coherent tested status model.

Potential impossible combinations:

```text
isLoading=true + isSuccess=true
isError=true + error=undefined
isSuccess=true + data=undefined
isRefreshing=true + no previous data
```

Prefer a union when transitions are coupled.

# Multiple useState Versus One State Object

Separate state is fine when values evolve independently.

Example:

```text
query text
selected tab
isHelpOpen
```

Grouped/reduced state is preferable when multiple fields must transition atomically.

Example:

```text
status
data
error
previousData
```

Do not follow “only one useState” or “never useReducer” rules.

# useReducer

Use a reducer when:

- transitions are numerous;
- events matter;
- several fields update atomically;
- transition logic benefits from centralization.

Do not use a reducer merely because async state exists.

A discriminated union can be managed by `useState`.

# Optional Values

Choose a coherent convention:

```text
undefined
null
Maybe<T>
discriminated union
```

Use the boundary's established policy.

Do not mix:

```text
undefined
null
Maybe.none
```

for the same meaning.

# Maybe<T>

`Maybe<T>` can be appropriate for:

```text
optional data
lookup absence
optional selection
```

It does not automatically model:

```text
loading
error
refreshing
retry
```

Example:

```text
Maybe<Profile>
```

cannot tell:

```text
not loaded
not found
failed
cancelled
```

unless those distinctions are intentionally irrelevant.

# Maybe Versus Discriminated Union

Use `Maybe<T>` when the meaningful question is:

```text
value exists
or
value does not exist
```

Use a discriminated union when the meaningful question is:

```text
which async state are we in?
```

Example:

```ts
type SearchState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: AppError };
```

Do not wrap every union payload inside `Maybe`.

# Null Versus Undefined

Choose according to project policy and boundary semantics.

Possible interpretation:

```text
undefined → absent/not provided
null → explicitly no value
```

Do not impose this universally if the project has another coherent policy.

# Discriminated Unions

Prefer a stable discriminant:

```text
status
type
kind
```

Use one convention consistently.

Each variant should contain only valid fields.

Good:

```ts
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: AppError };
```

# Exhaustive Handling

Presentation may use exhaustive switching when valuable.

Do not require verbose switch statements if a simple rendering expression remains clear.

The key is that invalid states cannot exist, not that syntax is ceremonial.

# Background Refresh

Background refresh means:

```text
usable data remains visible
+
new request in flight
```

If UI distinguishes it, model it.

Options:

```ts
{ status: 'refreshing'; data: T }
```

or use selected server-state library semantics:

```text
data + isValidating
data + fetchStatus
```

according to project strategy.

Do not copy server-state flags into a local union merely to rename them.

# Refresh Failure

Decide:

```text
retain prior data + show non-blocking error
```

or:

```text
transition to blocking error
```

according to accepted behavior.

Common model:

```text
success/stale data remains
+
refreshError
```

or a discriminated state that preserves data.

Do not erase usable data automatically.

# Stale State

Add `stale` only when the product cares about freshness.

Examples:

- offline cached data;
- visibly outdated quote;
- cached dashboard with “updated 10m ago”;
- explicit stale-warning behavior.

Do not add stale state just because the server-state library has a staleTime concept.

Library cache staleness is not automatically product-visible staleness.

# Server-State Staleness Versus Product Staleness

Distinguish:

```text
CACHE_STALE_INTERNAL
PRODUCT_STALE_VISIBLE
```

React Query/SWR may consider data stale for refetching while the UI still treats it as normal success.

Do not expose cache implementation semantics as product state without reason.

# Retry

Retry can mean:

```text
error → loading
```

or:

```text
error-with-data → refreshing
```

depending on retained data.

Define:

- whether input is preserved;
- whether previous data is preserved;
- whether old error clears immediately;
- duplicate retry behavior.

Do not invent a separate `retrying` state unless UI/commands differ.

# Retrying

A distinct `retrying` state is useful when:

- copy changes;
- user can cancel;
- previous error remains visible;
- retry count/progress matters.

Otherwise reuse loading/refreshing semantics.

# Cancellation

Cancellation semantics must be explicit.

Potential outcomes:

```text
return to idle
return to previous success
remain with prior data
explicit cancelled state
silent no-op
```

Do not automatically model:

```text
{ status: 'error'; error: cancelled }
```

if cancellation is not an error to the user.

# Explicit Cancelled State

Use only when the UI cares:

- user sees “cancelled”;
- resume/restart differs;
- audit/workflow semantics require it.

For obsolete search requests, cancellation may simply prevent state update.

# Stale Responses

State transitions MUST prevent an older response from overwriting a newer one.

Ownership may be:

```text
server-state library
hook/request controller
Use Case cancellation
adapter cancellation support
```

The state model should reflect accepted latest-wins semantics but does not need to encode request sequence internals.

Do not expose:

```text
requestIdCounter
AbortController
generationRef
```

in public UI state.

# Optimistic Updates

First decide owner:

```text
SERVER_STATE_LIBRARY
HOOK_LOCAL_WORKFLOW
DOMAIN
APPLICATION
```

Do not duplicate optimistic state across owners.

## Optimistic State

A distinct optimistic state may be justified when UI behavior differs.

Example:

```ts
{ status: 'optimistic'; data: T; previous: T }
```

But if React Query/SWR mutation cache already owns optimistic data and rollback, reuse its semantics.

Do not copy optimistic cache into local state.

# Optimistic Rollback

Define:

```text
optimistic apply
→ success reconcile
OR
→ rollback on accepted failure
```

Specify:

- previous state source;
- concurrent mutation policy;
- error display;
- retry.

Do not invent rollback if product behavior says optimistic update is irreversible locally until reload.

# Concurrent Optimistic Mutations

If concurrent mutations are allowed, define ordering/reconciliation.

Possible:

```text
SERIALIZE
LATEST_WINS
QUEUE
KEYED_CONCURRENT
LIBRARY_OWNS
```

Do not implement ad hoc state merging without accepted policy.

# Partial Data

Partial data exists when some meaningful sections are available while others are not.

Avoid:

```ts
{
  profile?: Profile
  stats?: Stats
  recommendations?: Recommendation[]
  error?: Error
}
```

when sections have independent states.

Prefer:

```ts
type SectionState<T> =
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: AppError };
```

or application-level partial result semantics.

# Partial Data Ownership

If partial success is decided by the Use Case/Application result, Presentation should consume that semantic result.

If independent queries load separately through a server-state library, keep state in each query rather than merging into one local mega-state.

# Aggregate Page State

A page may derive an aggregate display condition:

```text
show full-page skeleton
show partial dashboard
show global blocking error
```

Derive it from section states when possible.

Do not duplicate section states into another independently mutable page-state object.

# Permission States

Permission denial may be:

- an Application result;
- an async error category;
- a separate UI state.

Choose based on accepted behavior.

Do not treat forbidden as empty data.

# Loading and Empty

Do not collapse:

```text
loading
empty
```

An empty successful list is not loading.

Likewise:

```text
not found
empty list
forbidden
```

are not interchangeable unless product explicitly treats them the same.

# Hydration / Server-Provided Data

If server-rendered data is supplied:

```text
initial state may be success
```

or the server-state library may hydrate its cache.

Do not flash `loading` unnecessarily by copying hydrated data into new local async state.

# Route Loaders

Framework route loaders/actions may own async status.

If their status object already provides required semantics, do not rebuild it locally.

Only add feature state for behavior the route framework does not represent.

# Server-State Library Integration

When caching/dedup/invalidation/retry/synchronization is required, use the selected server-state library.

Possible profiles:

```text
React Query
SWR
RTK Query
Apollo
Relay
framework loaders/actions
```

This skill models feature semantics around the library; it does not configure query keys or cache policy.

That belongs to `integrating-frontend-server-state`.

# Server-State State Mapping

Three acceptable strategies:

```text
DIRECT_LIBRARY_STATE
THIN_FEATURE_SEMANTIC_WRAPPER
APPLICATION_RESULT_PLUS_LIBRARY_STATE
```

## DIRECT_LIBRARY_STATE

Use when library semantics map cleanly to UI needs.

Example:

```text
data
error
isLoading
isValidating
```

No local duplication.

## THIN_FEATURE_SEMANTIC_WRAPPER

Use when UI benefits from stable semantic naming.

Example:

```text
isApplying
canRetry
promotion
```

The wrapper derives from library state.

Do not copy the data into independent local state.

## APPLICATION_RESULT_PLUS_LIBRARY_STATE

Use when server-state fetch/mutation returns a meaningful Application result while library owns cache/request lifecycle.

Keep responsibilities explicit.

# Duplicate Local State Anti-Pattern

Reject:

```ts
const query = useQuery(...)

const [data, setData] = useState(query.data)
const [loading, setLoading] = useState(query.isLoading)
const [error, setError] = useState(query.error)

useEffect(() => {
  setData(query.data)
  setLoading(query.isLoading)
  setError(query.error)
}, [query.data, query.isLoading, query.error])
```

This creates:

- two sources of truth;
- synchronization Effects;
- transient contradictions;
- stale state risk.

Derive instead.

# Derived State

If state can be computed from:

```text
props
server-state status
Application result
other local state
```

derive it during render unless a stateful transition is genuinely needed.

Do not store:

```text
hasData
isEmpty
canRetry
```

if these are pure derivations.

# State Machine Libraries

Do not introduce XState or another state-machine library merely because explicit states are useful.

Plain TypeScript unions/useReducer are often sufficient.

Use an existing state-machine library only when the project has selected it or the workflow complexity clearly justifies an approved change.

# Reducer Events

If reducer is used, name events semantically:

```text
loadStarted
loadSucceeded
loadFailed
refreshStarted
refreshFailed
cancelled
```

Avoid setter-like reducer events:

```text
setLoading
setError
setData
```

when transitions have coupled invariants.

# Transition Table

Define allowed transitions.

Example:

| From | Event | To |
|---|---|---|
| idle | load | loading |
| loading | success | success |
| loading | failure | error |
| success | refresh | refreshing |
| refreshing | success | success |
| refreshing | failure | success-with-refresh-error |
| error | retry | loading |

Do not permit transitions product behavior cannot trigger.

# Transition Guards

When a command is invalid in a state, define:

```text
disabled
ignored
rejected
queued
```

Example:

```text
retry
```

only valid from retryable error.

Do not rely on component disabling alone if the state API itself is reusable.

# Data Retention Matrix

For every transition decide whether data survives.

Example:

| Transition | Keep existing data |
|---|---|
| initial load | no |
| background refresh | yes |
| refresh failure | yes |
| resource ID changed | maybe/no |
| retry after initial error | no |
| retry after refresh error | yes |
| cancellation | previous state |

This prevents accidental flicker and stale presentation.

# Error Retention

Likewise decide whether old error survives when retry starts.

Often:

```text
retry starts
→ clear blocking error
```

but non-blocking refresh error may remain until next success depending on UX.

Do not assume.

# Resource Identity Changes

When key input changes:

```text
userId
subscriptionId
search query
route param
```

decide whether old data remains visible.

Policies:

```text
CLEAR_ON_KEY_CHANGE
KEEP_PREVIOUS_DATA
STALE_WHILE_REVALIDATE
SERVER_STATE_LIBRARY_OWNS
```

This is a product/UX decision, not merely a library option.

# Search State

Search commonly needs:

```text
idle (query too short)
loading
success results
empty
error
```

Potential latest-wins behavior.

Do not show prior query results as current unless keep-previous semantics are intentional.

# Pagination / Infinite Loading

For pagination, distinguish:

```text
initial loading
loaded page
loading next page
next-page error
refreshing all
```

Avoid one global `loading` flag that hides existing pages while loading more.

If server-state library owns infinite-query status, derive UI from it.

# Mutation State

Mutation state may be separate from query state.

Example:

```text
profile query success
+
save mutation pending
```

Do not merge them into one status:

```text
status: loading
```

which loses whether data is still visible.

# Multiple Concurrent Operations

When a feature can perform independent operations:

```text
load profile
upload avatar
save settings
```

do not force one global async status.

Each operation may need its own state owner.

Use aggregate state only for truly coupled transitions.

# Command Pending State

A command may expose:

```text
pending
success result
error
```

while resource query remains success.

Keep command lifecycle separate unless they are one atomic workflow.

# Optimistic Form Submission

If submission optimistically updates server-state cache, avoid also storing a separate local “optimistic resource” unless component-specific draft behavior requires it.

Form input state and server resource state are different owners.

# Error Boundary

React error boundaries handle render failures.

They do not replace operation-level async error state.

Do not model network/API errors by throwing everything into an Error Boundary unless the framework strategy explicitly owns them that way.

# Suspense

If project uses Suspense/server components/framework loaders, some loading/error representation may move to framework boundaries.

Do not duplicate suspense loading state inside the component.

Model only feature semantics not already handled by the framework.

# Accessibility

Async state should support accessible behavior.

Examples:

- loading status announcement when needed;
- non-blocking refresh should not repeatedly steal focus;
- error recovery should remain discoverable;
- optimistic failure should communicate rollback when user impact exists.

Do not encode accessibility copy in generic async-state types unless it is semantic content.

Presentation maps state to accessible UI.

# Error Semantics

Use stable Application errors or semantic result variants.

Do not model:

```text
error: unknown
```

at the public feature API when callers need meaningful recovery.

Internal lower-level unknown may be translated before state exposure.

# Retryability

Not every error is retryable.

Possible:

```text
retryable: true
```

derived from error type,

or state variant:

```text
{ status: 'error'; error: AppError; canRetry: true }
```

only if that property is stable semantic behavior.

Prefer derivation from error policy when possible.

# Cancelability

Likewise:

```text
canCancel
```

may be derived from operation/state.

Do not store it independently if it follows directly from status.

# Progress

Long operations may add:

```text
progress
```

only when product behavior requires it.

Possible:

```ts
{ status: 'loading'; progress: number }
```

or a separate progress stream.

Do not add fake progress.

# Unknown Duration

Use indeterminate loading semantics when duration/progress is unknown.

Do not manufacture percentage state.

# Timeouts

Timeout is usually an error semantic:

```text
TIMEOUT
```

not a distinct top-level state unless UI behaves differently.

# Rate Limit

Rate-limit errors may retain:

```text
retryAfter
```

if Application error semantics expose it.

State does not need a `rateLimited` variant unless behavior differs materially.

# Offline State

Offline may be:

```text
connectivity context
+
cached resource state
```

or explicit:

```text
{ status: 'stale'; data; source: 'offline-cache' }
```

when user-visible.

Do not treat `navigator.onLine` directly as async state authority.

# State Naming

Use names reflecting behavior.

Good:

```text
loading
refreshing
optimistic
partial
```

Avoid vague:

```text
processing
working
busy
done
```

unless project semantics define them.

# Hook Public Contract

A reusable hook may expose:

```text
state
data
error
commands
```

or a semantic object.

Do not expose internal setters/reducer dispatch.

Prefer named commands.

# State Type Location

Place state types where ownership belongs:

```text
feature hook/presentation
Application result
shared server-state wrapper
```

Do not put React-specific async state into Domain.

# Shared Async Types

A generic:

```text
AsyncState<T>
```

may be shared only when multiple features truly have identical semantics.

Be cautious: `loading/success/error` looks generic, but features often diverge on:

- refreshing;
- retained data;
- retryability;
- cancellation;
- partial state.

Avoid premature global state abstractions.

# Testing

Test observable transitions and public behavior.

Do not test internal setter sequences.

For pure reducer/state-machine logic, pure tests may be appropriate.

For hooks, use `testing-react-hooks`.

For server-state library integration, use the library-aware integration skill/test boundary.

# State Model Tests

Test only applicable transitions:

- initial;
- load success;
- load error;
- background refresh;
- refresh failure;
- retry;
- cancellation;
- optimistic apply/rollback;
- partial data;
- key change;
- stale response protection.

Do not test impossible internal states by manually constructing them unless validating the type/reducer guard itself.

# Background Refresh Evaluation

Must verify:

```text
existing data remains usable
refresh indicator is non-blocking if accepted
success replaces data
failure follows accepted retention behavior
```

Do not turn refresh into full loading unless product behavior says so.

# Optimistic Update Evaluation

Must verify:

```text
owner explicit
optimistic state visible if needed
success reconciles
failure rolls back if accepted
concurrent policy defined
```

No duplicate local/cache owner.

# Partial Data Evaluation

Must verify independent section state or accepted Application partial result.

Avoid giant optional bags.

# Retry Evaluation

Must verify:

```text
retry only where valid
input preserved as accepted
old error cleared/retained intentionally
state transition correct
```

# Cancellation Evaluation

Must verify cancellation:

- is distinguishable from failure when needed;
- returns to accepted state;
- prevents late obsolete success from overwriting current state.

Do not assert AbortController internals.

# Maybe Versus Union Evaluation

Given:

```text
Maybe<T>
```

ask whether callers need to distinguish:

```text
not loaded
not found
error
cancelled
```

If yes, `Maybe` alone is insufficient.

# Overmodeling Audit

Flag:

- idle state that cannot be observed;
- stale state copied from cache internals with no UX;
- retrying state identical to loading;
- cancelled state never rendered;
- optimistic state duplicated from React Query/SWR cache;
- shared `AsyncState<T>` forced across unrelated features;
- one giant page status for independent operations.

Use:

```text
PROPORTIONATE_ASYNC_STATE
UNDERMODELED_ASYNC_STATE
OVERMODELED_ASYNC_STATE
SERVER_STATE_DUPLICATION
ASYNC_STATE_NOT_REQUIRED
```

# Final Decision

Use:

```text
FRONTEND_ASYNC_STATE_READY
FRONTEND_ASYNC_STATE_READY_WITH_CONDITIONS
ASYNC_STATE_NOT_REQUIRED
SERVER_STATE_LIBRARY_OWNS_STATE
RETURN_TO_BEHAVIOR_OR_ERROR_DESIGN
STATE_OWNER_REQUIRED
OPTIMISTIC_POLICY_REQUIRED
PARTIAL_DATA_POLICY_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-async-state-modeling-record.md`.

## Completion Criteria

- [ ] State owner is explicit.
- [ ] Optional-value convention is coherent.
- [ ] Observable states come from accepted behavior.
- [ ] Unobservable/redundant states are removed.
- [ ] Impossible boolean combinations are prevented.
- [ ] `Maybe<T>` is used only for optionality, not as a hidden async state machine.
- [ ] Discriminated union is used when async distinctions matter.
- [ ] Initial/idle/loading/success/error semantics are explicit.
- [ ] Empty is distinct only when behavior requires it.
- [ ] Background refresh preserves data according to policy.
- [ ] Cache-internal stale semantics are not exposed as product stale state without reason.
- [ ] Retry transitions and data/error retention are explicit.
- [ ] Cancellation semantics are explicit and not automatically treated as generic error.
- [ ] Stale responses cannot overwrite newer state.
- [ ] Optimistic state has one owner and rollback/reconciliation semantics.
- [ ] Partial data is represented explicitly rather than through a giant nullable bag.
- [ ] Independent async operations are not forced into one global status.
- [ ] Server-state library state is derived/wrapped rather than copied locally.
- [ ] Hydrated/route/framework state is not duplicated.
- [ ] `useState` vs grouped state vs `useReducer` is selected according to transition coupling.
- [ ] Public hooks expose semantic state/commands rather than raw setters.
- [ ] Shared generic async types are not introduced speculatively.
- [ ] Tests target observable transitions and applicable roadmap cases.
- [ ] No new state-machine/server-state library is introduced without approval.
- [ ] Final async-state decision is explicit.

## References

- Read `references/async-state-ownership-and-representation.md` first.
- Read `references/maybe-unions-and-impossible-states.md`.
- Read `references/refresh-stale-retry-and-cancellation.md`.
- Read `references/optimistic-partial-and-concurrent-state.md`.
- Read `references/server-state-integration-without-duplication.md`.
- Read `references/transitions-testing-and-overmodeling.md`.
- Read `references/frontend-async-state-modeling-audit.md` before completion.
