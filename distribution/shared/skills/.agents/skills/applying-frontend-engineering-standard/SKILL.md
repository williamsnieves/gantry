---
name: applying-frontend-engineering-standard
description: Portable engineering capability `applying-frontend-engineering-standard`.
  Use when the harness or a specialist agent explicitly requires this named capability.
---
# Applying Frontend Engineering Standard

## Purpose

Prepare one frontend change for safe implementation by determining:

- which rules apply;
- which capability and files own the change;
- which architecture profile is currently in use;
- which layers and UI boundaries are affected;
- which implementation path is proportionate;
- which validations will be required;
- which decisions or deviations must be resolved first.

This is the frontend entry skill.

It does not implement code.

## Precedence

Apply rules in this order:

```text
Explicit accepted specification
→ repository-local AGENTS.md
→ definitive frontend standard
→ scoped frontend rules
→ framework and design-system constraints
→ existing local conventions
→ general engineering judgment
```

A lower-level rule must not silently contradict a higher-level rule.

When a conflict cannot be resolved safely:

1. stop the affected implementation;
2. describe the conflict;
3. identify the smallest required decision;
4. avoid inventing a new architecture or UI convention.

## Use When

- A frontend change or user story is ready for implementation planning.
- A PR/task needs frontend rule selection before coding.
- The repository has local conventions, nested `AGENTS.md`, or mixed frontend profiles.
- The change may affect React components, hooks, data adapters, styling, accessibility, or tests.
- The team needs to know whether Domain/Application boundaries are justified.
- A brownfield feature must follow local architecture without a broad rewrite.
- Several possible frontend paths exist and the smallest valid one must be selected.

## Do Not Use When

- The task is to implement or refactor code.
- The task is only to classify the architecture profile in depth.
- The task is only to plan vertical slices.
- The specification is not accepted enough to classify the change.
- The user asks for a generic frontend tutorial.
- The repository context cannot be inspected.
- The task is backend-only.

## Inputs

- Accepted change or specification.
- Repository structure.
- Root and nested `AGENTS.md`.
- Definitive frontend engineering standard.
- Framework and build configuration.
- Existing feature/capability structure.
- State-management and server-state conventions.
- Styling and design-system profile.
- Testing configuration and CI.
- Existing accessibility conventions.
- Relevant architecture decisions and accepted deviations.

## Required Context

1. Read the accepted specification.
2. Read the nearest applicable `AGENTS.md`.
3. Inspect repository and workspace structure.
4. Identify the owning application, package, and capability.
5. Inspect current feature organization.
6. Inspect framework/runtime version and rendering model.
7. Inspect state, server-state, data-access, and composition conventions.
8. Inspect styling and UI primitive conventions.
9. Inspect test tooling and CI.
10. Inspect accepted local deviations.
11. Do not infer a new project policy from personal preference.

## Outputs

- Applicable frontend rules.
- Rule precedence and conflicts.
- Current architecture-profile indication.
- Affected capability, slices, and layers.
- Affected UI/data/styling/test boundaries.
- Selected implementation path.
- Required focused skills.
- Required validation matrix.
- Unresolved decisions and deviations.
- Frontend standard application record.

## Core Workflow

```text
accepted change
→ discover local rules and repository profile
→ classify affected capability and boundaries
→ select proportionate implementation path
→ select focused skills
→ define required validation
→ stop on unresolved conflicts
```

## Stage 1 — Confirm the Change Is Ready

Confirm:

- user-visible behavior;
- actor and permission context;
- loading, empty, success, error, and disabled states;
- acceptance criteria;
- API/data dependencies;
- accessibility expectations;
- responsive and theme expectations;
- compatibility constraints;
- rollout or feature-flag constraints.

Use one:

```text
READY_TO_APPLY_FRONTEND_STANDARD
READY_WITH_CONDITIONS
RETURN_TO_SPECIFICATION
PRODUCT_DECISION_REQUIRED
DESIGN_DECISION_REQUIRED
ACCESSIBILITY_DECISION_REQUIRED
BLOCKED
```

Do not proceed under a blocking status.

## Stage 2 — Discover Repository-Local Rules

Inspect:

- root `AGENTS.md`;
- nested `AGENTS.md`;
- package-level README or architecture docs;
- lint/import-boundary configuration;
- TypeScript project references or package exports;
- framework conventions;
- design-system documentation;
- test conventions;
- CI workflows.

Record each applicable rule as:

```text
MANDATORY_INVARIANT
DEFAULT_CONVENTION
PROJECT_POLICY
ACCEPTED_LOCAL_OVERRIDE
NOT_APPLICABLE
INCONCLUSIVE
```

Do not treat an existing pattern as policy unless repository evidence supports it.

## Stage 3 — Identify the Current Architecture Profile

The definitive standard defines:

### Profile A — Small feature or small application

```text
feature/
├── components/
├── hooks/
├── api/
└── tests/
```

Use when:

- business logic is limited;
- Domain modeling adds little value;
- the feature is unlikely to evolve independently.

### Profile B — Modular frontend

```text
feature/
├── domain/
├── application/
├── infrastructure/
└── tests/
```

Use when:

- business rules exist;
- external dependencies require ports;
- testability and independent evolution matter.

### Profile C — Large product or monorepo

```text
apps/
packages/
features/
shared/
```

Use when:

- multiple applications consume capabilities;
- ownership boundaries are explicit;
- public package contracts are required;
- independent delivery or versioning matters.

At this stage, identify the current or likely profile.

Do not replace the profile silently.

Route deeper evaluation to:

```text
classifying-frontend-architecture-profile
```

Use profile status:

```text
PROFILE_A_INDICATED
PROFILE_B_INDICATED
PROFILE_C_INDICATED
MIXED_PROFILE
PROFILE_DECISION_REQUIRED
```

## Architecture Proportionality

The project must select the lightest profile that preserves required boundaries.

Do not:

- create Domain/Application folders for a purely presentational feature;
- place complex business/offline behavior in a flat components folder;
- create packages for a capability used by one feature without scaling evidence;
- force every feature to contain every layer.

Complexity must be earned.

## Stage 4 — Identify Capability and Ownership

Determine:

- owning product capability;
- application or package owner;
- current feature boundary;
- public entry points;
- affected routes/screens;
- shared dependencies;
- whether the change crosses capability boundaries.

Prefer screaming architecture:

```text
src/
├── orders/
├── subscriptions/
├── billing/
└── authentication/
```

Avoid adding new behavior to generic root folders such as:

```text
components/
hooks/
services/
utils/
models/
```

unless repository policy explicitly uses them and the change is truly shared.

## Shared Versus Feature-Owned

A dependency should remain feature-owned unless there is evidence for sharing.

A shared abstraction requires:

- more than one real consumer or an explicit platform boundary;
- stable semantics;
- clear owner;
- public contract;
- no leakage of one feature's implementation details.

Do not create speculative shared helpers.

## Stage 5 — Classify Affected Layers

Use:

```text
FRONTEND_DOMAIN
FRONTEND_APPLICATION
FRONTEND_PORT
FRONTEND_ADAPTER
HTTP_CLIENT
SERVER_STATE
LOCAL_STATE
ROUTING_COMPOSITION
REACT_COMPONENT
CUSTOM_HOOK
REACT_EFFECT
ACCESSIBILITY
STYLING
DESIGN_SYSTEM
TESTING
PUBLIC_PACKAGE_CONTRACT
BUILD_CONFIGURATION
```

A simple change may affect only components, styling, and tests.

A complex change may cross Domain, Application, adapters, hooks, components, and E2E.

Do not classify by filename alone.

## Domain and Application Justification

Frontend Domain/Application layers are justified when they protect:

- client-owned business rules;
- rich editor or workflow state;
- deterministic offline behavior;
- optimistic transitions;
- independent capability evolution;
- browser-port boundaries;
- complex orchestration.

They are usually not justified for:

- pure rendering transformations;
- one-off API display screens;
- basic form wiring with no meaningful rules;
- duplicated backend validation that is not client-authoritative.

Do not duplicate backend business authority blindly.

## Stage 6 — Classify Data and State Boundaries

Identify:

- remote server state;
- local component state;
- shared client state;
- URL/router state;
- form state;
- persisted browser state;
- optimistic state;
- offline state;
- derived view data.

Inspect current approved strategy before selecting tools.

Do not silently introduce:

- Redux;
- Zustand;
- React Query/TanStack Query;
- SWR;
- XState;
- a custom event bus;
- a new context layer.

Route server-state decisions to specialized skills when created.

## Data Mapping Boundary

External payloads should be mapped explicitly where they enter the application boundary.

Identify whether the change requires:

- runtime validation;
- transport-to-domain mapping;
- transport-to-application DTO mapping;
- enum/date/nullable conversion;
- pagination mapping;
- error translation.

Raw provider or API response types should not leak through the feature without an accepted local convention.

## Stage 7 — Classify React Boundaries

Identify likely work in:

- route/screen container;
- presentational component;
- feature component;
- custom hook;
- effect;
- event handler;
- composition root/provider;
- error/loading boundary.

Route focused work to:

```text
designing-react-components
designing-react-custom-hooks
designing-react-effects
composing-frontend-dependencies
```

Do not decide implementation details that belong to those skills.

## Component Boundary Indicators

A component likely needs decomposition when it mixes several of:

- data orchestration;
- business decisions;
- complex effects;
- presentation;
- several independent interaction regions;
- unrelated loading/error states.

Do not split solely by line count.

## Hook Boundary Indicators

A custom hook may be justified when it owns:

- reusable React-specific stateful behavior;
- synchronization with browser/framework APIs;
- reusable server-state integration;
- a stable event/state contract.

Do not hide generic business logic in hooks when it can remain React-independent.

## Effect Indicators

An effect should synchronize React with an external system.

Potential external systems:

- DOM APIs;
- timers;
- browser storage;
- network subscriptions;
- analytics;
- media queries;
- third-party widgets.

Do not use effects for pure derivation or event-driven state updates when they can happen directly.

## Stage 8 — Identify Styling and UI-System Profile

Inspect the current project use of:

- CSS Modules;
- Tailwind;
- CSS-in-JS;
- global CSS;
- design tokens;
- component library;
- headless primitives;
- vendor design system;
- theme and responsive conventions.

Use one:

```text
CSS_MODULES_PROFILE
TAILWIND_PROFILE
DESIGN_SYSTEM_PROFILE
CSS_IN_JS_PROFILE
MIXED_STYLING_PROFILE
STYLING_PROFILE_DECISION_REQUIRED
```

Do not introduce or replace the styling strategy.

Route deeper work to:

```text
selecting-frontend-styling-profile
```

or specialized styling skills.

## Design-System Boundary

Identify whether the change should:

- use an existing shared component;
- extend a shared component;
- compose headless primitives;
- remain feature-local;
- add or reuse design tokens.

Do not bypass a project policy that forbids direct vendor primitive imports outside shared UI.

Do not promote a one-off feature component to the design system without reuse evidence.

## Stage 9 — Accessibility Classification

Determine applicable needs:

- semantic HTML;
- accessible name;
- label and description;
- keyboard interaction;
- focus management;
- focus visibility;
- error announcement;
- live region;
- modal/dialog behavior;
- menu/listbox/combobox behavior;
- disabled versus aria-disabled semantics;
- responsive zoom/reflow;
- reduced motion;
- color contrast.

Accessibility is part of correctness.

Route implementation to:

```text
designing-accessible-react-ui
```

Stop if the interaction pattern is unresolved and no accessible behavior can be selected safely.

## Stage 10 — Testing Boundary Classification

Identify required test levels:

```text
DOMAIN_TEST
USE_CASE_TEST
ADAPTER_TEST
HOOK_TEST
COMPONENT_TEST
ACCESSIBILITY_TEST
VISUAL_REGRESSION
E2E_TEST
ARCHITECTURE_CHECK
```

Map accepted behavior to the cheapest reliable level.

Examples:

```text
pure client rule
→ Domain test

React-independent orchestration
→ Use Case test

API/browser mapping
→ adapter test

React state behavior
→ hook test

user interaction and semantics
→ component test

critical cross-page flow
→ E2E
```

Do not duplicate every case at every level.

Route deeper selection to:

```text
planning-frontend-test-strategy
```

## Stage 11 — Select Focused Skills

Potential routing:

```text
profile ambiguity
→ classifying-frontend-architecture-profile

vertical behavior planning
→ planning-frontend-vertical-slices

components
→ designing-react-components

hooks
→ designing-react-custom-hooks

effects
→ designing-react-effects

repository/browser adapters
→ implementing-frontend-repository-adapters

composition
→ composing-frontend-dependencies

styling
→ selecting-frontend-styling-profile

accessibility
→ designing-accessible-react-ui

test planning
→ planning-frontend-test-strategy

component tests
→ testing-react-components

hook tests
→ testing-react-hooks

architecture validation
→ validating-frontend-architecture

architecture review
→ reviewing-frontend-architecture
```

Use shared Domain/Application skills only when the selected profile justifies them.

## Stage 12 — Define Required Validation

Always consider repository-native:

```text
format/check
lint
typecheck
focused tests
build
```

Depending on the change, include:

- Domain or Use Case tests;
- adapter integration tests;
- hook tests;
- component tests;
- accessibility checks;
- visual regression;
- E2E;
- architecture checks;
- package/public-contract checks;
- responsive and theme verification.

Every required validation should include:

- why it applies;
- expected scope;
- repository-native command if known;
- environment requirement;
- blocked/unavailable risk.

Do not invent commands.

## UI State Matrix

For user-facing changes, consider:

```text
loading
empty
success
error
permission/unauthorized
disabled
retrying
partial/stale
offline
```

Only include states applicable to the accepted behavior.

Do not invent product states.

## Responsive and Theme Matrix

Consider:

- small viewport;
- large viewport;
- zoom/reflow;
- light/dark theme;
- reduced motion;
- long text/localization;
- high-content-density data;
- touch and pointer interaction.

Use the project's accepted support matrix.

## Browser and Rendering Model

Identify whether the project uses:

- client-side rendering;
- SSR;
- SSG;
- React Server Components;
- hydration;
- streaming;
- client-only islands;
- monorepo package rendering.

This affects:

- browser API placement;
- effects;
- data fetching;
- serialization;
- hydration safety;
- test environment.

Do not use browser-only APIs in server-executed code.

## Conflicts

Record conflicts such as:

- specification asks for a new library but repository policy forbids it;
- local feature is flat but the change introduces substantial business/offline rules;
- design asks for an inaccessible interaction;
- shared component contract cannot support the required behavior;
- project uses CSS Modules but task assumes Tailwind;
- SSR code path requires browser-only APIs;
- test requirement cannot run in current environment.

Use:

```text
RESOLVED_BY_PRECEDENCE
LOCAL_OVERRIDE_REQUIRED
PRODUCT_DECISION_REQUIRED
ARCHITECTURE_DECISION_REQUIRED
DESIGN_SYSTEM_DECISION_REQUIRED
ACCESSIBILITY_DECISION_REQUIRED
TOOLING_OR_ENVIRONMENT_BLOCKED
```

## Deviations

A deviation must include:

- rule;
- exact scope;
- reason;
- risk;
- owner;
- decision reference;
- expiry or removal condition when temporary;
- required validation.

Do not create silent exceptions.

## Selected Implementation Path

Produce a concise path such as:

### Simple UI feature

```text
feature component
→ local hook if needed
→ approved API/data helper
→ styling profile
→ component/accessibility tests
```

### Modular behavior

```text
frontend Domain/Application
→ repository port/adapter
→ container hook/component
→ UI components
→ focused tests and architecture validation
```

### Package-scale capability

```text
public package contract
→ capability internals
→ adapters/composition per app
→ package and consumer validation
```

Do not make the path more complex than the accepted change requires.

## Final Decision

Use one:

```text
FRONTEND_STANDARD_APPLIED
FRONTEND_STANDARD_APPLIED_WITH_CONDITIONS
FRONTEND_PROFILE_CLASSIFICATION_REQUIRED
RETURN_TO_SPECIFICATION
DECISION_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-standard-application-record.md`.

## Completion Criteria

- [ ] Accepted specification and applicable `AGENTS.md` were read.
- [ ] Rule precedence is explicit.
- [ ] Repository, framework, rendering, state, styling, test, and UI-system conventions were inspected.
- [ ] Owning capability and feature boundary are identified.
- [ ] Current architecture profile is indicated without forcing a replacement.
- [ ] Affected layers and boundaries are classified.
- [ ] Domain/Application work is included only when justified.
- [ ] No new state, server-state, styling, UI, or architecture library was selected silently.
- [ ] Accessibility implications are identified.
- [ ] Testing boundaries map behavior to the cheapest reliable levels.
- [ ] Required validations are proportionate and repository-native where known.
- [ ] Conflicts and deviations are explicit.
- [ ] The selected implementation path is the smallest valid one.
- [ ] No implementation code was produced.
- [ ] Final decision and focused-skill routing are explicit.

## References

- Read `references/rule-precedence-and-repository-discovery.md` first.
- Read `references/frontend-profile-indicators.md` for profile indication.
- Read `references/layer-state-and-data-classification.md` for affected boundaries.
- Read `references/ui-styling-and-accessibility-profile.md` for UI-system classification.
- Read `references/test-and-validation-selection.md` before finalizing.
- Read `references/frontend-standard-application-audit.md` before completion.
