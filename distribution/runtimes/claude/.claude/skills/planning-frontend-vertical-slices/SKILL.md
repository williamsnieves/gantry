---
name: planning-frontend-vertical-slices
description: Converts one ready frontend change into the smallest user-visible, end-to-end vertical slices. Use after applying the frontend standard and classifying the architecture profile. Build a behavior inventory, assign capability ownership, map each slice across only the justified Domain, Application, adapter, server-state, hook, component, styling, accessibility, and test boundaries, order dependencies safely, and define completion evidence. Preserve screaming architecture and existing project conventions. Do not plan by technical layer alone, create speculative shared abstractions, invent requirements, create ceremonial folders, duplicate every test at every level, or implement code.
---

# Planning Frontend Vertical Slices

## Purpose

Turn a ready frontend change into a sequence of small, user-visible behaviors that can be implemented and validated independently.

A vertical slice should connect the necessary boundaries for one observable outcome:

```text
user intent
→ UI interaction
→ state/orchestration
→ data or browser boundary
→ visible result
→ focused evidence
```

Depending on the selected architecture profile, a slice may include:

- Domain models and pure rules;
- Application Use Cases and DTOs;
- repository or browser adapters;
- server-state integration;
- route/screen composition;
- components;
- custom hooks;
- effects;
- styling;
- accessibility behavior;
- tests.

Do not create every layer mechanically.

## Relationship to Other Skills

Use before:

```text
applying-frontend-engineering-standard
classifying-frontend-architecture-profile
```

Use after planning:

```text
designing-react-components
designing-react-custom-hooks
designing-react-effects
implementing-frontend-repository-adapters
composing-frontend-dependencies
selecting-frontend-styling-profile
designing-accessible-react-ui
planning-frontend-test-strategy
```

Use shared Domain/Application skills only when Profile B or C justifies them.

## Use When

- A frontend change is accepted and ready to break down.
- The architecture profile and local rules are known.
- The team needs the smallest end-to-end delivery sequence.
- The feature crosses UI, state, data, styling, accessibility, and tests.
- A large story must be decomposed without losing user-visible value.
- A brownfield change must remain capability-local.
- Several UI states or acceptance paths need sequencing.
- A package-scale capability needs consumer-safe slices.

## Do Not Use When

- The change is not ready or acceptance behavior is unresolved.
- The architecture profile is still blocked.
- The request is only to design one component, hook, effect, or adapter.
- The task is implementation.
- The user asks for a purely technical migration plan unrelated to user behavior.
- The change is backend-only.
- Product, design, accessibility, or data contracts are too incomplete to define behavior.

## Inputs

- Accepted specification and acceptance criteria.
- Frontend standard application record.
- Frontend architecture profile record.
- Repository-local `AGENTS.md`.
- Current feature/capability structure.
- API and browser dependency contracts.
- Existing design-system and styling rules.
- Accessibility target and interaction pattern.
- Test and CI conventions.
- Rollout, compatibility, and migration constraints.

## Outputs

- Behavior inventory.
- Slice ownership.
- Slice boundaries and dependency map.
- Implementation sequence.
- Data and mapping boundaries.
- UI state matrix per slice.
- Accessibility checkpoints.
- Test matrix.
- Completion evidence.
- Explicit exclusions and deferred work.
- Frontend vertical-slice plan.

## Core Workflow

```text
accepted behavior
→ inventory user-visible outcomes
→ identify capability ownership
→ choose smallest executable slices
→ map only required boundaries
→ sequence dependencies and risk
→ attach accessibility and test evidence
→ define completion gate per slice
```

## Readiness Gate

Use one:

```text
READY_TO_PLAN_FRONTEND_SLICES
READY_WITH_CONDITIONS
RETURN_TO_SPECIFICATION
FRONTEND_PROFILE_DECISION_REQUIRED
DATA_CONTRACT_DECISION_REQUIRED
DESIGN_DECISION_REQUIRED
ACCESSIBILITY_DECISION_REQUIRED
ROLLBACK_OR_MIGRATION_DECISION_REQUIRED
BLOCKED
```

Stop when a missing decision changes the slice boundaries materially.

## Planning Principle

Plan by user-visible behavior, not technical layer.

Bad:

```text
1. create all components
2. create all hooks
3. create API services
4. add styles
5. add tests
```

Preferred:

```text
1. render current promotion state accessibly
2. submit a valid campaign code and show pending/success state
3. handle semantic rejection states
4. handle unavailable/retry behavior
```

Each slice may touch several technical areas, but it should complete one coherent user outcome.

## Behavior Inventory

Describe every accepted behavior as:

```text
actor/context
→ trigger
→ visible or semantic outcome
→ state/data effect
→ failure outcomes
```

Classify behaviors:

```text
PRIMARY_SUCCESS
ALTERNATIVE_SUCCESS
VALIDATION_FAILURE
SEMANTIC_FAILURE
AUTHORIZATION_FAILURE
SYSTEM_FAILURE
EMPTY_STATE
LOADING_STATE
RETRY_OR_RECOVERY
NAVIGATION_OR_COMPOSITION
MIGRATION_OR_COMPATIBILITY
```

Do not invent states not present in the accepted behavior.

## Slice Quality

A good slice is:

- user-visible or externally observable;
- independently implementable;
- independently testable;
- small enough to review;
- owned by one capability;
- vertically complete;
- safe to release or hide;
- explicit about failure and accessibility.

A slice is too large when it contains several independent intentions or several unrelated interaction regions.

A slice is too small when it delivers only a technical artifact with no independent behavioral evidence.

## Capability Ownership

Every slice must identify:

- owning capability;
- route/screen or public package entry;
- feature-local files;
- shared dependencies reused;
- other capabilities consulted;
- owner of any public contract.

Preserve screaming architecture.

Preferred:

```text
src/subscriptions/promotion-application/
```

Avoid spreading one slice across generic roots such as:

```text
src/components
src/hooks
src/services
src/utils
```

unless repository policy already defines those as owned public boundaries.

## Shared Abstractions

A slice may reuse an existing shared abstraction.

A plan must not create a new shared abstraction unless:

- two real consumers exist;
- semantics are stable;
- ownership is explicit;
- the current slice genuinely requires the public contract.

Keep unique behavior feature-local.

Do not plan speculative design-system, hook, utility, repository, or package extraction.

## Profile-A Slice Shape

A typical Profile A slice may include:

```text
feature component
→ feature hook or event handler
→ approved server-state/HTTP abstraction
→ CSS Modules/design-system composition
→ component/accessibility test
→ critical E2E only when needed
```

Do not introduce Domain/Application layers solely to make the plan appear complete.

## Profile-B Slice Shape

A typical Profile B slice may include:

```text
Domain rule or transition
→ Application Use Case
→ semantic port
→ adapter
→ composition/container
→ hook/component
→ accessibility/styling
→ layered tests
```

Use inside-out sequencing when rich client-owned behavior exists.

Do not require every slice to touch every layer.

## Profile-C Slice Shape

A typical Profile C slice may include:

```text
public capability contract
→ package internals
→ app-specific adapter/composition
→ consumer UI
→ package/consumer validation
```

Plan compatibility and release order explicitly.

Do not expose package internals through deep imports.

## Slice Boundary Map

For each slice classify applicable areas:

```text
FRONTEND_DOMAIN
FRONTEND_APPLICATION
PORT
ADAPTER
SERVER_STATE
LOCAL_STATE
ROUTER_STATE
FORM_STATE
BROWSER_STATE
COMPOSITION
COMPONENT
CUSTOM_HOOK
EFFECT
STYLING
DESIGN_SYSTEM
ACCESSIBILITY
COMPONENT_TEST
HOOK_TEST
ADAPTER_TEST
DOMAIN_TEST
USE_CASE_TEST
E2E
ARCHITECTURE_CHECK
PACKAGE_CONTRACT
```

Use:

```text
REQUIRED
REUSED
NOT_APPLICABLE
DEFERRED_WITH_TRIGGER
DECISION_REQUIRED
```

## Mapping Boundaries

Identify where external data becomes feature-owned data.

Potential mappings:

```text
transport response
→ runtime decoding
→ feature/application DTO
→ Domain type when justified
→ view model or component props
```

Record:

- request mapping;
- response mapping;
- date/enum/null conversion;
- stable error translation;
- pagination or cursor mapping;
- cancellation;
- optimistic update shape;
- rollback/reconciliation data.

Do not pass raw API or SDK types through all slices without an accepted local convention.

## Server-State Planning

For server-authoritative behavior, plan:

- query or mutation key;
- cache update or invalidation;
- pending state;
- duplicate submission prevention;
- cancellation;
- stale data;
- optimistic behavior only if accepted;
- retry policy;
- semantic error mapping.

Reuse the approved server-state strategy.

Do not introduce a new library.

## Local and Form State

Plan only state that is necessary.

Classify:

```text
EPHEMERAL_UI
FORM_DRAFT
DERIVED_VIEW
URL_STATE
SHARED_CLIENT_STATE
PERSISTED_BROWSER_STATE
OPTIMISTIC_STATE
OFFLINE_STATE
```

Do not promote local state globally without ownership evidence.

Derived values should remain derived rather than duplicated as state.

## Components

For each slice identify:

- route/screen container;
- feature component;
- presentational subcomponents;
- existing design-system primitives;
- interaction regions;
- loading/error boundaries;
- public props contracts.

Do not pre-plan excessive component fragmentation.

Route detailed design to:

```text
designing-react-components
```

## Hooks

Identify hooks only when the slice needs:

- reusable React stateful behavior;
- server-state integration;
- browser synchronization;
- stable interaction contract.

Do not use a hook as a generic dumping ground for orchestration.

Route detailed design to:

```text
designing-react-custom-hooks
```

## Effects

Plan an effect only for synchronization with an external system.

Examples:

- focus after state transition;
- browser storage;
- analytics;
- third-party widget;
- event subscription;
- timer;
- document title.

Do not plan effects for pure derivation or event-driven state updates.

Route detailed design to:

```text
designing-react-effects
```

## Composition

Identify where concrete dependencies are selected:

- route;
- screen container;
- feature factory;
- app composition root;
- package consumer adapter.

Components and hooks should not instantiate concrete infrastructure globally unless that location is the explicit composition boundary.

Route to:

```text
composing-frontend-dependencies
```

## Styling

For each slice record:

- existing styling profile;
- tokens and variants;
- responsive behavior;
- theme support;
- focus-visible state;
- disabled/pending/error styling;
- motion and reduced-motion behavior;
- visual regression need.

Do not decide a new styling strategy.

## Accessibility Checkpoints

Accessibility checkpoints belong to each slice, not a final cleanup phase.

Potential checkpoints:

- semantic element;
- accessible name and description;
- label and error association;
- keyboard interaction;
- focus order and focus return;
- focus visibility;
- live-region announcement;
- loading/busy semantics;
- disabled behavior;
- modal/menu/listbox/combobox pattern;
- zoom/reflow;
- reduced motion;
- contrast and theme;
- touch target and pointer-independent behavior.

Define both implementation and test evidence.

## UI State Matrix

For each slice consider only applicable states:

```text
INITIAL
LOADING
EMPTY
READY
EDITING
SUBMITTING
SUCCESS
DUPLICATE_OR_IDEMPOTENT_SUCCESS
VALIDATION_ERROR
SEMANTIC_ERROR
FORBIDDEN
UNAVAILABLE
RETRYING
STALE
PARTIAL
OFFLINE
DISABLED
```

A state may belong to a later slice when that keeps earlier slices smaller and still coherent.

Do not defer critical accessibility behavior from an earlier slice.

## Slice Sequencing

Preferred sequencing principles:

1. establish a visible baseline;
2. protect or map the external boundary;
3. implement the simplest accepted success path;
4. add semantic failure paths;
5. add system failure and recovery;
6. add advanced optimistic/offline behavior;
7. extract sharing only after reuse evidence;
8. remove compatibility paths only after migration evidence.

For Profile B with rich behavior:

```text
Domain
→ Application
→ adapter
→ composition
→ UI
```

may be the implementation order inside one slice.

The slice itself remains one user-visible outcome.

## Dependency Ordering

Record dependencies as:

```text
HARD_DEPENDENCY
SOFT_DEPENDENCY
PARALLELIZABLE
BLOCKED_BY_DECISION
```

Examples:

- API contract before adapter mapping;
- interaction semantics before component design;
- Domain transition before Use Case;
- design-system primitive before feature composition;
- package public contract before consumers.

Do not create circular slice dependencies.

## Risk-First Planning

Prioritize early evidence for:

- uncertain API mapping;
- inaccessible interaction pattern;
- browser/provider compatibility;
- offline conflict semantics;
- public package contract;
- migration/feature-flag routing;
- complex state transition;
- third-party widget behavior.

A thin technical spike may be included only when it resolves a concrete risk and has an explicit exit into a user-visible slice.

Do not let spikes become unbounded architecture work.

## Brownfield Planning

For existing features:

```text
characterize current UI behavior
→ introduce a feature-local seam
→ deliver one new/changed behavior
→ validate compatibility
→ migrate the next interaction
```

Preserve:

- route;
- public props;
- URL state;
- analytics contract;
- design-system behavior;
- accessibility behavior;
- test selectors only when contractually required.

Do not reorganize unrelated components.

## Migration Slices

When the architecture profile changes:

- keep migration change-local;
- define current and target ownership;
- preserve one authoritative state/data path;
- use compatibility mapping only when necessary;
- define feature-flag or routing ownership;
- define removal condition;
- avoid old/new duplicate side effects.

A migration-only slice should still have observable evidence and clear consumer impact.

## Test Matrix

Map each behavior to the cheapest reliable test level.

Typical order:

```text
Domain rule
→ Domain test

React-independent intention
→ Use Case test

transport/browser mapping
→ adapter test

reusable React behavior
→ hook test

user interaction and semantics
→ component test

critical cross-route/package flow
→ E2E
```

Include:

- positive path;
- active failure;
- state preservation;
- accessibility assertion;
- mapping/failure semantics;
- package compatibility where applicable.

Do not repeat every scenario at every level.

## Completion Evidence Per Slice

Every slice should define:

- acceptance cases covered;
- visible behavior;
- focused tests;
- accessibility evidence;
- typecheck/lint/build scope;
- integration or E2E evidence when required;
- architecture/package checks when affected;
- manual verification only where automation is not sufficient;
- blocked or unavailable evidence.

Use:

```text
SLICE_READY
SLICE_READY_WITH_CONDITIONS
SLICE_BLOCKED
SLICE_NEEDS_REFINEMENT
```

## Slice Size

A slice should normally fit one reviewable change.

Split when:

- several independent user intentions exist;
- several public contracts change;
- migration and feature behavior cannot be reviewed safely together;
- advanced recovery can follow a basic safe behavior;
- multiple consumers require staged rollout.

Keep together when splitting would create:

- unusable UI;
- untestable intermediate state;
- duplicated mapping;
- inaccessible temporary interaction;
- incompatible public contract.

## Definition of Done

A slice is done when:

- accepted behavior is visible;
- all required states in the slice work;
- data mappings are explicit;
- accessibility checkpoint passes;
- focused tests pass;
- required architecture/build checks pass;
- no speculative abstraction was introduced;
- documentation/story/spec is synchronized where required;
- rollout and compatibility conditions are satisfied.

## Explicit Exclusions

Each plan must state:

- behavior not in this change;
- states deferred;
- abstractions not justified;
- shared/package work excluded;
- visual polish deferred;
- unsupported browser/offline behavior;
- backend changes outside frontend ownership.

Deferred work needs a trigger, not a vague future note.

## Final Decision

Use one:

```text
FRONTEND_VERTICAL_SLICES_READY
FRONTEND_VERTICAL_SLICES_READY_WITH_CONDITIONS
RETURN_TO_SPECIFICATION
PROFILE_OR_OWNERSHIP_DECISION_REQUIRED
DESIGN_OR_ACCESSIBILITY_DECISION_REQUIRED
DATA_CONTRACT_DECISION_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-vertical-slice-plan.md`.

## Completion Criteria

- [ ] Accepted behavior and architecture profile are explicit.
- [ ] User-visible behavior inventory is complete.
- [ ] Every slice has one coherent outcome and one capability owner.
- [ ] The plan is vertical rather than grouped by technical layer.
- [ ] Only justified Domain, Application, ports, adapters, hooks, effects, and components are included.
- [ ] Screaming architecture is preserved.
- [ ] External data and error mapping boundaries are explicit.
- [ ] State ownership and server-state behavior are explicit.
- [ ] Styling and design-system rules are preserved.
- [ ] Accessibility checkpoints exist per slice.
- [ ] Tests map to the cheapest reliable levels.
- [ ] Implementation and dependency sequence is explicit.
- [ ] Brownfield or package migration conditions are explicit when applicable.
- [ ] No speculative shared abstraction or package is planned.
- [ ] No requirements or UI states were invented.
- [ ] Every slice has completion evidence and a readiness status.
- [ ] No implementation code was produced.

## References

- Read `references/behavior-inventory-and-slice-quality.md` first.
- Read `references/profile-aware-slice-mapping.md` for Profile A/B/C plans.
- Read `references/state-data-and-mapping-boundaries.md` for state and adapters.
- Read `references/accessibility-and-ui-state-checkpoints.md` for interaction coverage.
- Read `references/test-matrix-sequencing-and-completion.md` before finalizing.
- Read `references/frontend-vertical-slice-audit.md` before completion.
