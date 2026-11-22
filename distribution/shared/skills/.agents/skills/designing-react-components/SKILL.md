---
name: designing-react-components
description: Designs React component boundaries, typed props, rendering states, presentational/container roles, composition, and semantic accessible markup for one frontend slice. Use when a component or screen mixes concerns, calls data dependencies directly, has contradictory async booleans, suffers prop drilling, needs reusable versus feature-local classification, or requires a render-prop/children composition decision. Keep rendering and interaction wiring in components while moving substantial business rules, repository access, concrete adapters, and hidden side effects outward. Do not implement code, split by line count alone, create container wrappers mechanically, introduce global state or new libraries, promote one-off UI to shared, or invent interaction behavior.
...
---

# Designing React Components

## Purpose

Design one React component boundary so it clearly answers:

```text
What should the user see?
How can the user interact with it?
```

A component design should define:

- responsibility;
- public props;
- event contract;
- rendering-state model;
- presentational versus container role;
- composition and ownership;
- accessible semantic structure;
- feature-local versus shared placement;
- testable behavior.

This skill produces a design record, not production code.

## Governing Rules

Components SHOULD focus on:

- rendering;
- event wiring;
- accessible semantics;
- lifecycle integration.

Components MUST NOT:

- call repositories;
- call `fetch`;
- import concrete adapters;
- contain substantial business rules;
- hide important side effects in render logic.

Props MUST be typed explicitly.

Component line count is diagnostic, not a hard limit.

Split by responsibility, interaction region, or reusable substructure—not by arbitrary size.

## Use When

- Designing a new feature component or screen.
- A large component mixes data, business decisions, effects, and presentation.
- A component calls a repository, HTTP client, SDK, or concrete adapter.
- Loading/error/data booleans can contradict each other.
- Prop drilling is creating unclear ownership.
- Reuse versus feature-local placement is uncertain.
- A container/presentational split may improve testability.
- A render-prop, children-as-function, slot, compound, or composition API decision is needed.
- Semantic HTML and accessibility behavior must be designed before implementation.
- A component interface needs typed props and event contracts.

## Do Not Use When

- The task is to implement JSX/CSS.
- The task is only to design a hook or effect.
- The architecture profile or vertical slice is unresolved.
- The component behavior is not accepted.
- The user asks to introduce a component/state library.
- The task is backend-only.
- The issue is purely styling-profile selection.
- The component is generated code or third-party internals.

## Inputs

- Accepted frontend slice.
- Frontend standard application record.
- Architecture-profile decision.
- Vertical-slice plan.
- Existing component tree.
- Design-system and styling rules.
- Accessibility requirements.
- Data/state ownership.
- Existing hooks, Use Cases, adapters, and composition roots.
- Repository-local `AGENTS.md`.
- Testing conventions.

## Outputs

- Component responsibility map.
- Component tree proposal.
- Container/presentational decision.
- Typed props and event contracts.
- Rendering-state model.
- Composition API decision.
- Feature-local/shared ownership decision.
- Semantic HTML and accessibility structure.
- Error/loading/empty/permission behavior.
- Test boundary proposal.
- React component design record.

## Core Workflow

```text
accepted slice
→ identify visible responsibilities and interaction regions
→ identify data and dependency ownership
→ choose container/presentational boundary
→ design explicit props and events
→ model rendering states
→ design semantic accessible structure
→ challenge splitting and reuse
→ define test boundary
```

## Readiness Gate

Use one:

```text
READY_TO_DESIGN_REACT_COMPONENTS
READY_WITH_CONDITIONS
RETURN_TO_VERTICAL_SLICE_PLAN
DATA_OR_STATE_OWNERSHIP_REQUIRED
DESIGN_SYSTEM_DECISION_REQUIRED
ACCESSIBILITY_DECISION_REQUIRED
BLOCKED
```

Stop when:

- accepted states are unclear;
- the interaction pattern has no accessible semantics;
- dependency ownership is unresolved;
- component responsibilities cannot be separated from undefined business behavior.

## Responsibility Inventory

For the selected UI, list:

- visible regions;
- interaction regions;
- data displayed;
- user events;
- status and errors;
- routing responsibilities;
- browser/framework integration;
- composition responsibilities;
- reusable substructures.

Classify each responsibility:

```text
PRESENTATION
INTERACTION_WIRING
DATA_ORCHESTRATION
BUSINESS_DECISION
EXTERNAL_SYNCHRONIZATION
ROUTING
DEPENDENCY_COMPOSITION
STYLING
ACCESSIBILITY
```

Target placement:

- presentation and interaction wiring → component;
- orchestration → hook, container, or Application Use Case;
- business decision → Domain/Application;
- external synchronization → effect or adapter;
- routing/dependency selection → container/composition root.

## Component Roles

Use one or more:

```text
ROUTE_OR_SCREEN_CONTAINER
FEATURE_CONTAINER
FEATURE_COMPONENT
PRESENTATIONAL_COMPONENT
DESIGN_SYSTEM_COMPONENT
LAYOUT_COMPONENT
ERROR_OR_LOADING_BOUNDARY
```

Do not use role names as ceremony.

A component may combine container and presentation when the screen is small and cohesive.

## Container Decision

A container may:

- obtain Use Cases from the composition root;
- connect routing;
- bind feature dependencies;
- invoke a feature hook;
- pass stable data and callbacks to presentation.

Create a container only when it improves:

- dependency isolation;
- testability;
- reuse;
- rendering clarity;
- server/client boundary clarity.

Do not create a wrapper that only forwards all props unchanged.

Use:

```text
CONTAINER_REQUIRED
COLOCATED_CONTAINER_AND_VIEW
CONTAINER_NOT_JUSTIFIED
EXISTING_CONTAINER_REUSED
```

## Presentational Component

A presentational component should receive:

- explicit view data;
- explicit state;
- explicit callbacks;
- stable semantic props;
- child content or slots where justified.

It should not know:

- repository interfaces;
- concrete adapters;
- transport DTOs unless local policy explicitly treats them as view data;
- cache invalidation mechanics;
- provider errors;
- global service lookup.

## Props Design

Props MUST be typed explicitly.

Prefer:

```text
type Props = {
  ...
}
```

for reusable or non-trivial components.

Destructuring is allowed when it improves readability.

Avoid:

- `any`;
- catch-all `options`;
- catch-all `data`;
- spreading arbitrary unknown props across feature components;
- dependency bags mixing data, callbacks, and infrastructure;
- booleans that encode contradictory state combinations;
- passing concrete services when semantic callbacks suffice.

## Prop Categories

Classify props:

```text
VIEW_DATA
RENDER_STATE
USER_EVENT
ACCESSIBILITY
COMPOSITION_SLOT
VISUAL_VARIANT
DEPENDENCY
ROUTING
```

Dependencies should normally remain in containers/hooks, not presentational components.

## Event Contracts

Event props should express user intent:

Good:

```text
onApply(code)
onRetry()
onDismissError()
onOpenDetails()
```

Weak:

```text
onClick()
setData()
setLoading()
handleResponse(response)
```

Use semantic events that do not expose implementation mechanics.

Record:

- parameters;
- sync/async expectation;
- duplicate-submission behavior;
- disabled/busy behavior;
- error ownership;
- cancellation behavior.

Do not pass state setters as a default component API.

## Controlled and Uncontrolled State

Decide explicitly:

```text
CONTROLLED
UNCONTROLLED
HYBRID_WITH_CLEAR_CONTRACT
NOT_APPLICABLE
```

Controlled state is preferred when:

- owner needs validation or synchronization;
- several components coordinate;
- state must persist or route;
- deterministic tests require explicit control.

Uncontrolled state may be appropriate for:

- isolated native input behavior;
- low-value ephemeral state;
- design-system primitives already owning it safely.

Avoid hybrid contracts with unclear source of truth.

## Rendering-State Model

Use clear states for applicable behavior:

```text
INITIAL
LOADING
EMPTY
READY
SUBMITTING
SUCCESS
PARTIAL
STALE
VALIDATION_ERROR
SEMANTIC_ERROR
FORBIDDEN
NOT_FOUND
UNAVAILABLE
RETRYING
DISABLED
```

For complex state prefer:

- discriminated unions;
- explicit state machines;
- another model that prevents invalid combinations.

Avoid unrelated booleans such as:

```text
isLoading
hasError
hasData
isSuccess
```

when they permit contradictory combinations.

## Example State Shape

Conceptual design:

```text
idle
loading
ready(data)
submitting(data)
error(data?, reason)
success(data)
```

The exact implementation belongs to hook/Application design.

The component design must state which states can coexist, such as:

```text
ready data + background refresh
```

when intentionally supported.

## Rendering Branches

For every state define:

- visible content;
- retained data;
- enabled actions;
- focus behavior;
- status/error announcement;
- retry/dismiss behavior;
- skeleton/spinner semantics;
- empty-state action;
- permission-safe content.

Do not render mutually contradictory status messages.

## Business Logic Boundary

A component may contain:

- small view formatting;
- local presentation branching;
- simple derived display values;
- event wiring.

Move outward:

- eligibility;
- pricing;
- lifecycle transitions;
- conflict resolution;
- authorization decisions;
- cache/retry policy;
- data merging with business meaning;
- provider error interpretation.

Do not mistake a pure display formatter for a Domain rule.

## Data Boundary

A component should consume feature-owned view data.

Prefer:

```text
external response
→ adapter/hook/application mapping
→ component props
```

Avoid components interpreting:

- HTTP status;
- raw backend enums with unstable meaning;
- provider-specific errors;
- nullable transport quirks;
- SDK objects.

When a transport DTO is accepted directly under Profile A, document that it is stable feature-owned data and not a leaking external type.

## Component Splitting

Split when the component has:

- multiple responsibilities;
- independent interaction regions;
- independently testable behavior;
- reusable substructure;
- distinct accessibility patterns;
- different data/update cadence;
- different loading/error boundaries.

Do not split merely because:

- line count exceeds a number;
- JSX appears long;
- every `div` could be a component;
- one subcomponent would only rename markup;
- props must be forwarded through a meaningless wrapper.

## Interaction Regions

Examples of independent regions:

- promotion form;
- current promotion summary;
- error/retry panel;
- audit/history list;
- modal confirmation.

Independent regions may justify subcomponents when they have their own:

- state;
- events;
- semantic landmark;
- loading/error behavior;
- tests;
- reuse.

## Prop Drilling

First determine whether prop drilling reflects legitimate composition.

Acceptable:

- explicit data/callbacks through one or two meaningful levels;
- layout passing a slot;
- container passing feature props to view.

Potential problem:

- unrelated intermediaries forward many props;
- dependency services cross presentation layers;
- several branches need the same feature state;
- component API mirrors internal state setters.

Possible solutions:

```text
compose children closer to owner
introduce feature container
introduce feature-scoped context
move orchestration to hook/Application
reduce component responsibility
```

Do not introduce global state by default.

## Context

Use React context for a stable feature-local cross-tree dependency or state contract when prop composition is genuinely inadequate.

Context should define:

- provider owner;
- scope;
- value stability;
- consumer contract;
- missing-provider behavior;
- test strategy.

Do not use context as a Service Locator or dumping ground.

Do not put frequently changing broad state into one context without considering render impact and ownership.

## Reuse Classification

Use:

```text
FEATURE_LOCAL
CAPABILITY_SHARED
APPLICATION_SHARED
DESIGN_SYSTEM
PACKAGE_PUBLIC
NOT_REUSABLE
```

Promote only with evidence.

Feature-specific behavior stays feature-local even when visually generic.

A design-system component must have:

- semantic stability;
- multiple consumers or platform mandate;
- ownership;
- accessibility contract;
- styling/token contract;
- versioning/change policy.

Do not promote a one-off campaign form to shared UI.

## Composition Patterns

Potential patterns:

```text
plain props
children
named slots
compound components
render prop
context-backed compound component
```

Select the simplest contract that preserves flexibility.

### Plain Props

Default for explicit data, variants, and events.

### Children

Use for natural content composition.

### Named Slots

Use when several regions are independently supplied.

### Compound Components

Use for related components with a coherent shared semantic contract.

### Render Prop

Use when the parent owns behavior/state but consumers need flexible rendering.

Do not use render props where ordinary props or children are clearer.

## Render-Prop Decision

A render prop may be justified when:

- behavior is reusable;
- rendering varies substantially;
- consumers need state/actions;
- hook-only access is insufficient due to ownership or framework constraints.

Reject when:

- it hides simple markup;
- only one consumer exists;
- it increases nested complexity;
- a custom hook provides the same boundary more clearly.

## Semantic HTML

Use native semantics first:

- `button` for actions;
- `a` for navigation;
- `form`, `label`, and form controls;
- headings in logical order;
- `section`, `nav`, `main`, `aside` where appropriate;
- lists for list content;
- tables for tabular relationships;
- `dialog` or proven accessible primitive for dialogs.

Do not recreate button behavior on `div` or `span`.

ARIA must supplement, not replace, correct native semantics.

## Accessibility Contract

For each interactive component define:

- semantic role/element;
- accessible name;
- label/description;
- keyboard interaction;
- focus order;
- focus placement and return;
- disabled versus `aria-disabled`;
- invalid/error association;
- busy state;
- live-region announcement;
- reduced motion;
- zoom/reflow;
- contrast/theme;
- touch target.

Complex widgets should use approved accessible primitives.

## Loading and Busy Semantics

Define:

- whether existing content remains;
- whether action is disabled;
- `aria-busy` placement;
- progress label;
- focus preservation;
- duplicate-action prevention;
- skeleton semantics.

Do not move focus to a spinner by default.

## Error Semantics

Distinguish:

- validation;
- semantic rejection;
- permission;
- not found;
- unavailable/network;
- unknown system error;
- cancellation.

Define:

- inline field error;
- form-level alert;
- persistent versus dismissible;
- focus on invalid field or summary;
- retry action;
- technical-detail exclusion.

## Empty States

An empty state should communicate:

- what is absent;
- whether this is expected;
- next valid action;
- permission limitations;
- no false error language.

Do not show a generic blank region.

## Server and Client Components

When applicable, classify:

```text
SERVER_COMPONENT
CLIENT_COMPONENT
SERVER_CONTAINER_CLIENT_INTERACTION
CLIENT_ONLY
```

Browser APIs, hooks, state, and effects require a client boundary.

Do not mark an entire route client-only if a smaller interactive boundary suffices.

Do not pass non-serializable dependencies across server/client boundaries.

## Suspense and Error Boundaries

Use only when supported by the project's rendering/data strategy.

Define:

- boundary scope;
- fallback ownership;
- retained surrounding UI;
- retry/reset;
- error logging boundary;
- accessibility of fallback.

Do not add Suspense mechanically around every component.

## Dependency Composition

Concrete dependencies should be selected in:

- route/screen container;
- composition root;
- app/package adapter boundary;
- approved provider.

Presentational components should receive semantic props or use a focused feature hook.

A component must not call a global runtime container to locate services.

## Styling Contract

The component design should identify:

- styling profile;
- variants;
- tokens;
- responsive behavior;
- theme behavior;
- focus-visible state;
- pending/disabled/error state;
- class-name extension policy;
- visual regression need.

Do not embed a new styling architecture in component design.

## Public Component API

For reusable components define:

- minimal stable props;
- defaults;
- variants;
- events;
- slots/children;
- accessibility requirements;
- forbidden prop combinations;
- controlled/uncontrolled behavior;
- forward-ref need;
- escape hatches;
- deprecation/change policy when public.

Do not expose internal DOM structure unnecessarily.

## Ref and Imperative APIs

Use refs for:

- focus;
- measurement;
- integration with imperative systems;
- approved primitive composition.

Avoid public imperative handles unless:

- semantic operations cannot be expressed declaratively;
- lifecycle ownership is clear;
- tests and accessibility require it.

Do not expose arbitrary internal DOM nodes by default.

## Performance

Do not add memoization by default.

First design:

- stable ownership;
- small render surface;
- localized state;
- clear context boundaries;
- appropriate list keys;
- virtualization only when data size requires it.

React version/compiler may influence optimization strategy.

Performance optimization belongs to evidence-driven follow-up.

## Test Boundary

Component tests should cover observable behavior:

- rendering state;
- user interaction;
- semantic elements;
- callback intent;
- error/status announcement;
- focus and disabled behavior;
- conditional regions;
- composition contract.

Do not test private implementation details or exact internal component structure.

Map pure rules, orchestration, and adapter behavior to their lower test levels.

## Component Design Decisions

Use:

```text
COMPONENT_DESIGN_READY
COMPONENT_DESIGN_READY_WITH_CONDITIONS
RESPONSIBILITY_SPLIT_REQUIRED
CONTAINER_DECISION_REQUIRED
STATE_MODEL_DECISION_REQUIRED
ACCESSIBILITY_DECISION_REQUIRED
DESIGN_SYSTEM_DECISION_REQUIRED
RETURN_TO_VERTICAL_SLICE_PLAN
BLOCKED
```

## Output

Use `assets/react-component-design-record.md`.

## Completion Criteria

- [ ] Selected slice and component scope are explicit.
- [ ] Visible and interaction responsibilities are inventoried.
- [ ] Data orchestration, business logic, effects, routing, and composition are assigned outside presentation where appropriate.
- [ ] Container/presentational decision is justified without mechanical wrappers.
- [ ] Props are explicit, typed, semantic, and minimal.
- [ ] User event contracts express intent rather than implementation.
- [ ] Controlled/uncontrolled ownership is explicit.
- [ ] Rendering states prevent invalid combinations.
- [ ] Loading, empty, success, error, permission, stale, and partial states are addressed when applicable.
- [ ] Component splitting follows responsibilities and interaction regions, not line count.
- [ ] Prop drilling and context decisions preserve ownership.
- [ ] Reuse remains feature-local unless evidence supports promotion.
- [ ] Composition pattern is the simplest sufficient option.
- [ ] Native semantic HTML and accessibility behavior are explicit.
- [ ] Server/client boundaries are explicit when applicable.
- [ ] Styling and design-system constraints are preserved.
- [ ] Test boundary covers observable behavior at the right level.
- [ ] No repository/fetch/concrete-adapter access or substantial business rule remains in presentation.
- [ ] No implementation code or new library selection was produced.
