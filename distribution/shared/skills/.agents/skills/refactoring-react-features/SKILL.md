---
name: refactoring-react-features
description: Portable engineering capability `refactoring-react-features`. Use when
  the harness or a specialist agent explicitly requires this named capability.
---
# Refactoring React Features

## Purpose

Improve an existing React feature without changing its accepted user-visible behavior.

Core workflow:

```text
protect behavior
→ inventory responsibilities
→ identify boundary violations
→ choose smallest coherent extraction
→ refactor one responsibility at a time
→ preserve contracts
→ validate behavior + architecture + accessibility
```

This skill is for brownfield feature internals.

It does not migrate an entire repository into vertical slices.

Use:

```text
migrating-to-frontend-vertical-slices
```

for repository/capability ownership migration.

## Roadmap Purpose

This skill MUST:

- reduce mixed responsibilities;
- improve boundaries;
- extract behavior, mapping, or UI primitives safely;
- preserve tests and user-visible behavior.

## Roadmap Evaluations

This skill MUST cover:

```text
oversized component
god hook
direct fetch
shared abstraction overreach
duplicated async state
inaccessible custom widget
```

## Governing Rules

### Components

Components SHOULD NOT:

- contain substantial business rules;
- instantiate concrete adapters;
- call `fetch` directly;
- duplicate server-state lifecycle;
- hide inaccessible custom interactions.

### Hooks

Custom hooks SHOULD encapsulate coherent reusable React behavior.

They SHOULD NOT become a second Application layer or a service locator.

### Effects

Effects are for synchronization with external systems, not pure derivation or ordinary event commands.

### Async State

Each async concern should have one primary owner.

Do not copy server-state library state into duplicate local loading/error/data booleans unless product behavior requires a distinct local state.

### Accessibility

Prefer semantic HTML and established accessible primitives over bespoke interactive widgets.

### HTTP/Data

Use the project's accepted HTTP/repository/server-state boundaries.

### Behavior Preservation

Refactor architecture by default without changing:

- route behavior;
- visible content;
- interaction semantics;
- accessibility contract;
- network/business outcome;
- accepted error behavior.

## Use When

- A feature component mixes rendering, fetching, mapping, business rules, navigation, analytics, and async state.
- A custom hook controls unrelated flows or exposes too many setters/flags.
- A component calls `fetch`, Axios, SDKs, or concrete adapters directly.
- A shared component/hook contains feature-specific business semantics.
- Local React state duplicates React Query/SWR/Apollo/Relay/framework server-state.
- An Effect synchronizes derived state unnecessarily.
- An inaccessible custom select/dialog/menu/tab/widget should be replaced or redesigned.
- A feature needs smaller responsibility boundaries before architecture validation.
- A brownfield feature has acceptable behavior but poor internal structure.

## Do Not Use When

- The feature behavior is still being designed.
- The task is greenfield component/hook design.
- The repository needs vertical-slice migration first.
- The user wants unrelated product/UI changes bundled into the refactor.
- The task is only performance/security/privacy review.
- The component is large only because it renders a large static/semantic structure with one coherent responsibility.
- The hook is long only because one state machine is inherently complex and cohesive.

## Inputs

- Existing feature code.
- Selected architecture profile.
- Current tests.
- Accepted user-visible behavior.
- Existing component/hook design conventions.
- Server-state strategy.
- HTTP/repository boundaries.
- Accessibility standard.
- Existing architecture review findings.
- Applicable `AGENTS.md`.

## Outputs

- Responsibility inventory.
- Refactor seam.
- Behavior-preservation plan.
- Component/hook/extraction decisions.
- Async-state ownership decision.
- Direct-fetch remediation plan.
- Shared abstraction ownership decision.
- Accessibility replacement contract.
- Incremental refactor sequence.
- Validation plan.
- React feature refactoring record.

# Core Principle

Refactor by responsibility, not line count.

Bad rule:

```text
> 300 lines
→ split
```

Better:

```text
multiple independent reasons to change
→ split along stable responsibility boundaries
```

# Behavior Gate

Before refactoring, define:

```text
what users can see/do
what requests/business outcomes occur
what loading/error/retry states exist
what focus/keyboard semantics exist
what tests already prove
```

If important behavior is not protected:

```text
CHARACTERIZATION_REQUIRED
```

# Characterization Tests

Use the lowest useful boundary.

Examples:

```text
component interaction test
hook test
route integration test
adapter test
critical E2E
```

Do not add E2E for every refactor path.

# Responsibility Inventory

Classify current code into:

```text
rendering
interaction wiring
React-local state
server-state integration
Application orchestration
business/domain rule
DTO/view mapping
HTTP/provider access
navigation
analytics
effects/external synchronization
accessibility semantics
styling
```

Then decide where each belongs.

# Extraction Rule

Extract only when a responsibility has:

- distinct semantics;
- independent reason to change;
- useful test boundary;
- reusable behavior or meaningful isolation;
- clearer ownership after extraction.

Do not extract every JSX block into a component.

# Roadmap Evaluation — Oversized Component

An oversized component is a problem when it mixes several responsibilities, not merely because it is long.

Common symptoms:

```text
fetching
mapping
permissions
business decisions
multiple async workflows
navigation
analytics
complex focus behavior
large presentation tree
```

# Oversized Component Refactor

Potential target:

```text
FeatureRoute / FeatureContainer
→ data/orchestration hook
→ view data
→ presentational sections
```

But a small cohesive feature may keep container + presentation together.

Do not create wrapper components mechanically.

# Component Extraction Candidates

Extract subcomponents when they have their own:

- semantic region;
- interaction state;
- accessibility pattern;
- stable props contract;
- visual primitive reuse.

Avoid:

```text
HeaderSection
BodySection
FooterSection
```

if they only rename arbitrary markup.

# Business Rule Extraction

If JSX contains:

```text
eligibility
pricing
permission semantics
state transition rules
```

move to Domain/Application when selected profile justifies it.

Do not move simple view formatting into Domain.

# Mapping Extraction

DTO/provider data SHOULD be mapped before it reaches deep presentational UI.

Potential:

```text
adapter mapper
view-data mapper
feature hook
Application result mapping
```

depending on ownership.

Do not make presentational components understand provider DTO quirks.

# Navigation Extraction

Navigation triggered by feature/application outcome may remain in route/container/hook depending on architecture.

Do not put router calls inside Domain/Application.

# Analytics Extraction

Provider-specific analytics stays behind approved adapter.

Feature code may emit application-owned analytics events.

Do not leave direct provider SDK calls inside presentational components.

# Roadmap Evaluation — God Hook

A god hook is a custom hook with too many unrelated responsibilities.

Symptoms:

```text
fetches multiple unrelated resources
owns several independent forms
navigates
shows toast
tracks analytics
contains business rules
manages modal state
builds DTOs
instantiates adapters
returns dozens of flags/setters
```

# Hook Cohesion Test

Ask:

```text
What one reusable React behavior does this hook own?
```

If the answer needs several unrelated sentences, it may be over-scoped.

# Split God Hook by Responsibility

Potential:

```text
useSubscriptionData
useSubscriptionUpgrade
useUpgradeDialog
```

only if these are coherent boundaries.

Do not fragment one cohesive state machine into many hooks merely to reduce file size.

# Hook vs Application

Application orchestration that is framework-independent belongs in Application Use Cases where the architecture profile supports it.

React hook adapts Application behavior into React state/events.

Avoid:

```text
hook = hidden service layer
```

# Hook Dependencies

Prefer accepted injection/composition.

Do not instantiate:

```text
new ApiClient()
new Repository()
providerSdk
```

inside reusable hooks if composition root exists.

# Hook Return API

Prefer stable commands/state over raw setters.

Bad:

```ts
{
  setLoading,
  setError,
  setData,
  setStep,
  setModalOpen,
}
```

Better:

```ts
{
  state,
  upgrade,
  retry,
  openConfirmation,
}
```

when those are real feature commands.

# God Hook Split Risk

Splitting can create hidden coordination problems.

If two hooks must mutate the same state machine continuously, they may actually be one cohesive hook.

Do not split blindly.

# Roadmap Evaluation — Direct Fetch

Components/hooks SHOULD NOT scatter raw `fetch` or vendor clients when the project has an accepted HTTP/repository/server-state boundary.

Bad:

```ts
useEffect(() => {
  fetch("/api/subscriptions")
    .then(...)
}, [])
```

inside component when React Query/repository abstraction is selected.

# Direct Fetch Classification

Direct fetch may be acceptable inside:

```text
approved HTTP client
repository adapter
intentionally isolated infrastructure adapter
framework loader
```

according to project policy.

Do not ban native `fetch` globally.

# Direct Fetch Refactor

Potential:

```text
component
→ feature hook
→ server-state/repository
→ HTTP client
```

or:

```text
route loader
→ repository/HTTP boundary
```

according to profile/framework.

# Fetch-on-Mount Effect

If a server-state library owns remote state:

```text
remove manual Effect state machine
→ use selected server-state strategy
```

Do not rebuild caching/retry/invalidation inside custom hook.

# HTTP Mapping

Keep:

```text
transport
DTO decode
runtime validation
stable transport errors
```

at infrastructure boundary.

Do not move provider DTO semantics into JSX during refactor.

# Roadmap Evaluation — Shared Abstraction Overreach

A shared abstraction has overreached when it contains business semantics from one or a few capabilities.

Examples:

```text
shared/DataTable knows subscription status
shared/usePermissions knows billing roles
shared/Modal triggers checkout flow
shared/api handles feature-specific validation
```

# Shared Ownership Test

A module belongs in shared only when:

```text
multiple genuine consumers
neutral semantics
stable contract
central ownership beneficial
```

If one capability drives its evolution, move it back to feature ownership.

# Shared Abstraction Smell

Common signs:

- prop list full of feature flags;
- `type` union grows with feature names;
- conditional imports of feature modules;
- shared module imports feature code;
- one consumer needs most branches;
- business terminology appears in supposedly generic primitive.

# Refactor Overreached Shared Component

Potential:

```text
shared generic primitive
+
feature wrapper/composition
```

Example:

```text
shared/DataTable
subscriptions/SubscriptionTable
```

Keep business columns/actions/permissions in feature layer.

# Do Not Over-Generalize

Sometimes duplication is cheaper and clearer than a speculative abstraction.

Do not create:

```text
UniversalFeatureRenderer<TConfig>
```

to avoid two 20-line feature components.

# Roadmap Evaluation — Duplicated Async State

Common anti-pattern:

```ts
const query = useQuery(...)
const [data, setData] = useState()
const [loading, setLoading] = useState(false)
const [error, setError] = useState(null)

useEffect(() => {
  setData(query.data)
  setLoading(query.isLoading)
  setError(query.error)
}, [query...])
```

This creates two owners.

# Single Owner Principle

If React Query/SWR/Apollo/Relay/framework loader owns remote lifecycle:

```text
server-state library
→ primary async owner
```

Feature may derive semantic state without copying raw lifecycle.

# Thin Semantic Wrapper

Acceptable:

```text
query.isError + specific error code
→ feature semantic "upgradeUnavailable"
```

when product semantics differ.

Do not mirror every library flag.

# Local Draft vs Server State

Local editable form draft may coexist with server state intentionally.

Record ownership:

```text
server canonical data
local unsaved draft
```

This is not automatically duplicated state.

# Hydration

Do not copy server-provided/hydrated data into new local loading state and create loading flashes.

Use existing data as initial/server-state owner.

# Optimistic State

Use server-state library's accepted optimistic mechanisms where available.

Do not create parallel local shadow caches casually.

# Async Boolean Explosion

Symptoms:

```text
isLoading
isSaving
isSuccess
isError
isRetrying
hasData
```

with impossible combinations.

Use explicit state model when product behavior is genuinely complex.

Do not build a custom state machine for a simple query.

# Derived State

Compute cheap derived values during render.

Avoid Effect:

```text
props/data
→ setDerivedState
```

unless synchronization semantics truly require it.

# Roadmap Evaluation — Inaccessible Custom Widget

A custom interactive widget is a refactor target when it lacks accepted semantics/keyboard/focus/name-role-value behavior.

Examples:

```text
div dropdown
custom dialog
clickable span
DIY tabs
custom combobox
drag-only control
```

# Accessibility Refactor Priority

Prefer:

```text
native semantic element
→ existing accessible design-system primitive
→ established headless primitive
→ custom implementation only when necessary
```

# Custom Select Example

Bad:

```jsx
<div onClick={toggle}>
  Choose plan
</div>
```

Potential replacements:

```text
native <select>
accessible design-system Select
headless combobox/listbox
```

depending on interaction requirements.

# Accessible Dialog

Must address:

```text
semantic role/name
focus entry
focus trap/containment as appropriate
Escape
focus restoration
background interaction
```

Use existing primitive if available.

# Keyboard Behavior

Do not “fix accessibility” by adding:

```text
tabIndex=0
onKeyDown Enter
```

to every `div`.

Use the correct native/ARIA pattern.

# Accessible Primitive Contract

When replacing widget preserve:

- accepted visual behavior;
- product interaction;
- labels;
- focus;
- errors/status;
- mobile behavior.

Architecture refactor must not regress UX.

# Testing Inaccessible Widget Refactor

Use:

```text
role/name queries
keyboard interaction
focus assertions
accessible status
automated accessibility checks
manual/browser verification for complex widget
```

Do not rely only on snapshots.

# Component + Hook Boundary

A common target:

```text
Route/Container
├── useFeatureController()
├── PresentationalView
└── Accessible primitives
```

But do not mandate this structure for every feature.

# Controller Hook

A feature controller hook may coordinate:

- approved server-state hooks;
- local interaction state;
- Application commands;
- navigation result;
- semantic view state.

It should not own every possible sub-feature.

# Feature Container

Container can:

- connect dependencies;
- invoke hook;
- map to view props;
- wire commands.

It should not duplicate Domain/Application behavior.

# View Data

Presentational component SHOULD receive frontend-friendly view data rather than API DTOs where mapping complexity is meaningful.

# Refactor Sequence

Recommended:

```text
1. characterize behavior
2. inventory responsibilities
3. isolate direct infrastructure access
4. establish async-state owner
5. extract business/application behavior
6. simplify hook contract
7. split semantic UI regions
8. repair shared ownership
9. replace inaccessible widget
10. validate
```

Sequence may vary.

# Incremental PRs

Prefer reviewable steps.

Potential:

```text
PR 1
→ tests + direct-fetch boundary

PR 2
→ async ownership + hook simplification

PR 3
→ component extraction + accessibility primitive

PR 4
→ remove obsolete shared abstraction
```

Do not create a long-lived rewrite branch when small changes are possible.

# Contract Preservation

Preserve public:

```text
component props
feature public API
route params
query keys where externalized
event names
storage keys
server contracts
```

unless change is explicitly accepted.

# Internal API Change

Internal hook/component signatures may change freely if all consumers are controlled and tests prove behavior.

Do not preserve bad internals for compatibility without reason.

# Test Preservation

Tests should continue to assert user-observable behavior.

Do not rewrite tests to mirror new internals.

# Test Smell During Refactor

If tests break because they call private hook setters or component internals, improve test boundary rather than recreating private API.

# Snapshot Tests

Do not preserve giant snapshots solely to prevent change.

Use semantic interaction/accessible queries where behavior matters.

# Effect Refactor

For every Effect ask:

```text
external synchronization?
```

If no:

- derive during render;
- move to event handler;
- use server-state library;
- use external-store API.

Do not move bad Effect into a custom hook just to hide it.

# Analytics Effect

Analytics triggered by user action may belong in event path rather than Effect over derived state.

Follow privacy/analytics policy.

# Race Conditions

When splitting async logic preserve:

- stale-response behavior;
- cancellation;
- retry;
- duplicate command semantics;
- optimistic rollback.

Do not simplify structure by losing concurrency correctness.

# Error Semantics

Preserve distinguishable errors where UI behavior depends on them.

Do not collapse:

```text
unauthorized
conflict
validation
network
cancel
```

into one generic error if product semantics differ.

# Loading Semantics

Preserve:

```text
initial loading
background refresh
mutation pending
retry
```

only when product behavior actually distinguishes them.

# Performance

Refactoring can accidentally increase rerenders or bundles.

Do not add memoization mechanically.

If measurable performance concern exists, use:

```text
reviewing-frontend-performance
```

# React Compiler

If React Compiler is enabled:

```text
trust compiler first
```

before adding manual memoization.

This skill should not introduce `useMemo`, `useCallback`, or `React.memo` merely because code was extracted.

# Security

Refactor must not:

- move authorization to client;
- expose secrets;
- weaken sanitization;
- broaden third-party access.

Use `reviewing-frontend-security` when affected.

# Privacy

Moving analytics into adapters should preserve consent/data-minimization policy.

Use `reviewing-frontend-privacy-and-analytics` when affected.

# Architecture Validation

After meaningful boundary changes run:

```text
validating-frontend-architecture
```

Check:

- dependency direction;
- feature ownership;
- no concrete adapter leak;
- no cross-feature internal import;
- shared boundaries.

# Accessibility Review

For complex custom widgets, use:

```text
designing-accessible-web-interfaces
reviewing-web-accessibility
```

as needed.

# Existing Primitive Reuse

Before implementing custom replacement search existing:

```text
design system
headless primitive
shared accessible component
```

Do not build duplicate widget.

# Deletion

After refactor remove:

- obsolete wrapper;
- duplicate local async state;
- unused Effect;
- dead service method;
- abandoned shared abstraction;
- compatibility alias with no consumers.

Do not leave two implementations indefinitely.

# Dead Code Handoff

Use:

```text
analyzing-dead-code
```

for uncertain broad cleanup outside refactor scope.

# Refactor Finding Structure

Record:

```text
current responsibility
problem
target owner
extraction
behavior evidence
risk
validation
```

# Refactor Decision Types

Use:

```text
KEEP_COHESIVE
SPLIT_COMPONENT
SPLIT_HOOK
MOVE_TO_APPLICATION
MOVE_TO_INFRASTRUCTURE
MOVE_TO_FEATURE
REDUCE_SHARED_ABSTRACTION
REMOVE_DUPLICATE_ASYNC_STATE
REPLACE_WITH_ACCESSIBLE_PRIMITIVE
CHARACTERIZATION_REQUIRED
```

# Roadmap Evaluation — Oversized Component

Passing:

- responsibilities identified;
- extraction based on semantics;
- user behavior preserved;
- component does not call infrastructure directly after refactor.

# Roadmap Evaluation — God Hook

Passing:

- hook has coherent responsibility;
- Application behavior moved inward where justified;
- concrete adapters not instantiated;
- return API is stable/semantic;
- async/race behavior preserved.

# Roadmap Evaluation — Direct Fetch

Passing:

- raw fetch/vendor usage moves to accepted infrastructure/loader boundary;
- selected server-state strategy owns request lifecycle;
- component/hook no longer rebuilds request machinery.

# Roadmap Evaluation — Shared Abstraction Overreach

Passing:

- business semantics leave shared;
- shared primitive remains neutral;
- duplication is accepted if abstraction would be speculative.

# Roadmap Evaluation — Duplicated Async State

Passing:

- one primary async owner remains;
- semantic derived state is not a copied mirror;
- loading/error/data states cannot drift between owners.

# Roadmap Evaluation — Inaccessible Custom Widget

Passing:

- native/existing accessible primitive considered first;
- semantic/keyboard/focus/name-role-value behavior is explicit;
- verification uses user/AT-relevant evidence.

# Over-Refactoring Audit

Flag:

- split by line count;
- every JSX block extracted;
- one cohesive hook fragmented;
- new generic abstraction for two weakly related consumers;
- manual memoization added during cleanup;
- unrelated architecture migration bundled in;
- UI redesign mixed with behavior-preserving refactor.

Use:

```text
PROPORTIONATE_REFACTOR
OVER_REFACTORED
PREMATURE_ABSTRACTION
BEHAVIOR_CHANGE_MIXED_IN
```

# Under-Refactoring Audit

Flag:

- direct fetch remains in component;
- duplicated async state remains;
- god hook merely renamed;
- shared abstraction still imports feature semantics;
- inaccessible widget gets only `tabIndex`;
- obsolete implementation remains active.

# Final Decision

Use:

```text
REACT_FEATURE_REFACTOR_READY
REACT_FEATURE_REFACTOR_READY_WITH_CONDITIONS
CHARACTERIZATION_REQUIRED
COMPONENT_BOUNDARY_REFACTOR_REQUIRED
HOOK_BOUNDARY_REFACTOR_REQUIRED
ASYNC_STATE_OWNERSHIP_REQUIRED
INFRASTRUCTURE_BOUNDARY_REQUIRED
SHARED_ABSTRACTION_REQUIRES_REOWNERSHIP
ACCESSIBILITY_REFACTOR_REQUIRED
ARCHITECTURE_VALIDATION_REQUIRED
BLOCKED
```

## Output

Use `assets/react-feature-refactoring-record.md`.

## Completion Criteria

- [ ] Accepted user-visible behavior is explicit.
- [ ] Existing tests/characterization protect critical behavior.
- [ ] Responsibilities are inventoried before extraction.
- [ ] Refactor decisions use semantic boundaries rather than line count.
- [ ] Oversized components are split only where responsibilities differ.
- [ ] Presentational components do not own substantial business/infrastructure logic.
- [ ] God hooks are reduced to coherent React behavior.
- [ ] Application behavior is not hidden inside hooks when framework-independent.
- [ ] Concrete adapters are not instantiated in reusable hooks.
- [ ] Hook APIs expose semantic commands/state rather than raw setters by default.
- [ ] Direct `fetch`/vendor usage follows accepted HTTP/repository/server-state boundary.
- [ ] Fetch-on-mount Effects do not rebuild selected server-state strategy.
- [ ] DTO/provider quirks do not leak into deep presentation unnecessarily.
- [ ] Shared abstractions remain semantically neutral.
- [ ] Feature-specific semantics move back to feature ownership.
- [ ] Shared is not generalized speculatively.
- [ ] Async server-state has one primary owner.
- [ ] Local draft state is distinguished from canonical server state.
- [ ] Duplicated loading/error/data mirrors are removed.
- [ ] Effects for pure derivation are removed.
- [ ] Race/cancellation/retry semantics are preserved during async refactor.
- [ ] Custom widgets prefer native/design-system/headless accessible primitives.
- [ ] Keyboard/focus/name-role-value behavior is verified.
- [ ] Accessibility is not “fixed” with generic `tabIndex` alone.
- [ ] Tests remain user-observable rather than private implementation-coupled.
- [ ] Manual memoization is not added without semantic/measured need.
- [ ] Security/privacy boundaries remain intact.
- [ ] Obsolete duplicate code is removed when consumers are migrated.
- [ ] `validating-frontend-architecture` runs after meaningful boundary changes.
- [ ] Roadmap evaluations are covered: oversized component, god hook, direct fetch, shared abstraction overreach, duplicated async state, inaccessible custom widget.
- [ ] Final refactor status is explicit.

## References

- Read `references/responsibility-inventory-and-behavior-preservation.md` first.
- Read `references/oversized-components-and-semantic-extraction.md`.
- Read `references/god-hooks-application-boundaries-and-effects.md`.
- Read `references/direct-fetch-server-state-and-infrastructure-boundaries.md`.
- Read `references/shared-abstraction-overreach-and-feature-reownership.md`.
- Read `references/duplicated-async-state-and-single-owner-model.md`.
- Read `references/inaccessible-custom-widgets-and-accessible-primitives.md`.
- Read `references/react-feature-refactoring-audit.md` before completion.
