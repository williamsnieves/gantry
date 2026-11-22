---
name: composing-react-feature-containers
description: Portable engineering capability `composing-react-feature-containers`.
  Use when the harness or a specialist agent explicitly requires this named capability.
---
# Composing React Feature Containers

## Purpose

Compose React features at the outer Presentation/routing boundary.

A feature container answers:

```text
Which dependencies and route/framework inputs does this feature need?
How are they connected to the hook/view?
```

It does not answer:

```text
What is the business rule?
How does HTTP work?
How is the provider payload mapped?
```

A container may:

- obtain Use Cases from the composition root;
- connect routing;
- bind feature dependencies;
- invoke approved feature/server-state hooks;
- pass stable data and commands to a presentational component;
- coordinate page-level composition.

A container is optional.

Do not create one mechanically.

## Governing Standard

Dependency creation belongs at an explicit outer boundary.

A Factory or composition root MAY:

- create HTTP clients;
- create adapters;
- create Use Cases;
- apply configuration;
- cache safe shared instances;
- construct route containers.

Components and hooks MUST NOT instantiate infrastructure dependencies globally.

A container may:

- obtain Use Cases from the composition root;
- connect routing;
- bind feature dependencies;
- pass stable dependencies into hooks or components.

A presentational component SHOULD receive explicit data and behavior through props or a feature hook.

The container and component MAY live in the same file for small cohesive screens.

Do not create a container wrapper mechanically for every component.

Routes are outer composition boundaries.

Framework-specific server/client boundaries MUST be explicit.

## Use When

- A route/screen must obtain dependencies and bind a feature.
- A feature hook needs injected Use Cases or replaceable capabilities.
- Route params/search params must become feature inputs.
- A modal has meaningful dependency/behavior composition.
- Server/client boundaries need explicit placement.
- A React Router loader/action must connect to Application behavior.
- A feature has a reusable presentational view that benefits from separation.
- Tests need a focused container boundary.
- Composition currently leaks into hooks/components.

## Do Not Use When

- The component is tiny and has no meaningful dependency composition.
- A component only receives props and renders.
- A hook already is the intentional explicit composition boundary.
- The wrapper would merely rename props.
- The task is to construct infrastructure dependencies themselves.
- The task is to design a Use Case, hook, or server-state strategy.
- The proposed container exists only because “every feature needs one”.

## Inputs

- Architecture profile.
- Route/screen ownership.
- Composition-root/Factory policy.
- Use Case and port dependencies.
- Custom hook design.
- Server-state integration strategy.
- Presentational component design.
- Routing framework.
- Server/client runtime.
- Error/loading boundary strategy.
- Permission/metadata requirements.
- Test strategy.
- Existing feature conventions.
- Repository-local `AGENTS.md`.

## Outputs

- Container justification decision.
- Composition boundary.
- Dependency acquisition strategy.
- Route/framework input mapping.
- Hook invocation contract.
- View props contract.
- Server/client split.
- Loader/action integration when applicable.
- Modal/container ownership decision.
- Test-container strategy.
- Anti-ceremony decision.
- React feature container composition record.

## Core Workflow

```text
identify route/feature boundary
→ decide whether a container adds value
→ obtain dependencies from approved composition root
→ map route/framework inputs
→ invoke feature behavior
→ derive stable view props
→ render view
→ keep business/infrastructure concerns outside
```

## Readiness Gate

Use one:

```text
READY_TO_COMPOSE_REACT_FEATURE_CONTAINER
READY_WITH_CONDITIONS
NO_CONTAINER_REQUIRED
COMPOSITION_ROOT_REQUIRED
ROUTE_BOUNDARY_REQUIRED
SERVER_CLIENT_BOUNDARY_REQUIRED
HOOK_CONTRACT_REQUIRED
VIEW_CONTRACT_REQUIRED
LOADER_POLICY_REQUIRED
BLOCKED
```

A successful outcome may be:

```text
NO_CONTAINER_REQUIRED
```

# Container Justification

Use:

```text
CONTAINER_JUSTIFIED
CONTAINER_AND_VIEW_COLOCATED
ROUTE_IS_COMPOSITION_BOUNDARY
HOOK_IS_EXPLICIT_COMPOSITION_BOUNDARY
NO_CONTAINER_REQUIRED
CEREMONIAL_CONTAINER
```

A container is justified when it provides one or more:

- dependency acquisition;
- route/framework adaptation;
- server/client boundary;
- feature-hook binding;
- permission/page-level composition;
- reusable view separation;
- testable composition seam.

It is not justified when it only does:

```tsx
return <View {...props} />
```

with no transformation, dependency, routing, or ownership value.

# Container Responsibilities

A container may own:

- dependency lookup from approved outer mechanism;
- route params/search params;
- framework loader data;
- server-state/feature-hook invocation;
- mapping semantic hook state into view props;
- page-level command wiring;
- page-level error/loading boundary selection;
- modal lifecycle binding;
- navigation command wiring when Presentation owns navigation.

A container MUST NOT own:

- Domain invariants;
- Use Case business orchestration;
- provider response mapping;
- raw HTTP;
- repository implementation;
- business calculations;
- arbitrary global state;
- design-system internals unrelated to composition.

# Composition Root Integration

Preferred:

```text
composition root / Factory
→ Use Cases / semantic dependencies
→ route/container
→ hook
→ view
```

Do not instantiate concrete adapters in arbitrary containers:

```ts
const repo = new HttpPromotionRepository(new HttpClient(...))
```

unless that route/container is explicitly the approved composition root.

Normally, concrete dependency creation remains in the Factory/composition module.

# Dependency Acquisition

Allowed patterns may include:

```text
explicit props from route composition
approved context/provider
Factory function at outer boundary
framework dependency mechanism
package entrypoint composition
```

Do not use service-location calls throughout feature code.

If DI container exists, its service resolution should remain at explicit composition boundaries.

# Stable Dependencies

Dependencies passed into hooks should have stable lifecycle according to their semantics.

Avoid:

```ts
const useCase = createUseCase()
```

on every render when creation is not intentionally cheap/stateless and identity matters.

Prefer composition-root construction or safe memoized/stable provider lifecycle.

Do not add memoization mechanically; dependency lifetime should be explicit.

# Container and View Separation

Separate when:

- presentational view is reusable/testable independently;
- container has route/dependency/framework concerns;
- server/client boundary requires it;
- view can remain framework-light;
- feature behavior is complex enough to benefit from an explicit seam.

Keep together when:

- screen is small/cohesive;
- no meaningful dependency/routing distinction exists;
- splitting creates prop-forwarding ceremony;
- testing is not improved.

The standard explicitly allows container and component in the same file.

# Presentational View

A presentational view should focus on:

```text
what the user sees
how the user interacts
```

It should receive:

- explicit data;
- semantic status;
- semantic commands/callbacks;
- accessible content;
- presentation variants.

It should not obtain repositories or concrete adapters.

# Container-to-View Props

Prefer semantic props:

```ts
<PromotionView
  promotion={promotion}
  status={status}
  onApply={apply}
  onRetry={retry}
/>
```

Avoid leaking:

```text
UseQueryResult
SWRResponse
AxiosError
Use Case instances
repository instances
router object
raw loader context
```

unless the view is intentionally framework-specific.

# Hooks in Containers

A container may call:

```text
feature hook
server-state hook
routing hook
permission hook
```

according to architecture.

The hook should expose semantic state/commands.

Do not duplicate hook state inside container `useState`.

Do not move Use Case logic into the container because the hook is “too thin”.

# Route Containers

Routes are natural outer composition boundaries.

A route may:

- obtain dependencies;
- parse route params;
- load data through approved framework mechanisms;
- bind Use Cases;
- coordinate feature containers;
- enforce permissions;
- define page metadata.

Route files SHOULD NOT become large business-logic modules.

If route code grows substantially, extract feature composition without moving business rules into Presentation.

# Route Params

Map raw route parameters into stable feature inputs.

Example:

```text
params.subscriptionId
→ validate/normalize route input
→ SubscriptionFeatureContainer
```

Do not pass entire router objects deep into the feature when only one semantic ID is needed.

# Search Params

Search/query params belong to routing Presentation boundary.

Map them into semantic filter/input objects.

Avoid leaking:

```text
URLSearchParams
router location object
framework search-param object
```

into Application/Domain unless explicitly part of accepted boundary.

# Navigation

Navigation is usually Presentation-owned.

A container may wire:

```text
onCompleted
→ navigate(...)
```

when accepted UX says navigation follows a semantic result.

The Use Case should return semantic outcomes, not call the router.

Do not hide navigation inside Application.

# Permissions

A route/container may use frontend permission/capability state to decide:

- render;
- redirect;
- disable;
- show unauthorized view.

Frontend permission checks do not replace backend authorization.

Do not treat container-level hiding as security enforcement.

# Metadata

Route/page-level metadata may be composed at the route boundary.

Avoid making feature Domain/Application code depend on metadata APIs.

# Loading Boundaries

Decide where loading belongs:

```text
framework route boundary
server-state hook
container conditional
view
Suspense boundary
```

Avoid duplicate loading states.

If framework/Suspense owns initial loading, the container should not recreate it.

# Error Boundaries

Decide whether failures are:

```text
feature-local recoverable
route-level blocking
auth/session-level
render crash
```

The container may select the presentation/error boundary.

Do not send operational API errors to React Error Boundary by default.

# Modal Features

A modal feature may justify a container when it needs:

- Use Cases;
- server-state;
- route/search-param binding;
- async command state;
- dependency composition.

A purely presentational confirmation modal often does not.

# Modal Container

Good separation:

```text
DeleteAccountModalContainer
→ useDeleteAccount(...)
→ DeleteAccountModal
```

when behavior/dependencies are meaningful.

Ceremonial:

```text
InfoModalContainer
→ <InfoModal {...props} />
```

with no composition value.

# Modal Lifecycle

Container may bind:

```text
open/close
submit
cancel
success close
error retry
```

but should not duplicate state owned by modal primitive or server-state hook.

# Tiny Components

Tiny leaf components should usually remain presentational.

Do not create:

```text
BadgeContainer
ButtonContainer
AvatarContainer
```

unless they genuinely compose external dependencies or routing.

# Feature Root

A feature root/container may coordinate several child presentational components.

Example:

```text
SubscriptionFeatureContainer
├── SubscriptionHeader
├── PromotionPanel
└── BillingSummary
```

This does not mean every child needs its own container.

# Nested Containers

Nested containers are acceptable when they correspond to real feature composition boundaries.

Avoid deep chains:

```text
RouteContainer
→ PageContainer
→ FeatureContainer
→ SectionContainer
→ WidgetContainer
→ View
```

if each layer only forwards props.

Use the smallest number of meaningful boundaries.

# Next.js Server/Client Split

In React Server Component environments, server-only and client-only boundaries must be explicit.

Potential split:

```text
Server route/page
→ obtain server-safe dependencies/data
→ serialize safe props
→ Client feature container
→ interactive hook/view
```

or:

```text
Server component
→ Application query
→ presentational server view
```

when no client interactivity is required.

# Server Components

Server components may:

- call server-safe Application/Infrastructure composition according to project architecture;
- load data;
- render server-safe presentation;
- pass serializable data to client components.

They MUST NOT pass:

- server secrets;
- non-serializable Use Case instances;
- database clients;
- provider SDK handles;
- functions to arbitrary client boundaries unless framework-supported server actions policy explicitly applies.

# Client Components

A client feature container may:

- consume serializable initial data;
- use browser/server-state hooks;
- wire interactive commands;
- bind navigation.

It must not import server-only dependencies.

# `use client`

Place client boundaries as low as practical while preserving coherent feature composition.

Do not mark a whole route/client subtree as client merely because one leaf needs interactivity if server rendering can remain useful.

Also do not fragment the tree excessively into artificial boundaries.

# Server Actions

If the framework uses server actions, treat them as an explicit framework boundary.

Do not bypass existing Application/Use Case rules automatically.

A server action may adapt form/framework input to an Application Use Case.

Do not put business rules directly into the action because it executes on the server.

# Next.js Route Example

Possible:

```text
page.tsx (server)
→ load accepted route data
→ PromotionFeatureClient initialData=...
```

Then client container owns interactive SWR/mutation composition.

If SWR is hydrated, ensure server and client semantic resource identity match.

# React Router Loader

A loader is an outer routing boundary.

It may:

- parse route params;
- obtain dependencies;
- call Use Cases/repositories;
- return serializable Application-safe data;
- throw/return framework route responses according to accepted policy.

It should not contain provider mapping or substantial business rules.

# Loader and Component

Possible pattern:

```text
loader
→ Application data
→ route component/container
→ feature view
```

If loader owns initial load, avoid immediately duplicating it with a second fetch unless revalidation policy requires it.

# React Router Action

An action may adapt form/route input to a Use Case.

It should not become a replacement Application layer.

Keep validation ownership clear:

```text
route/form shape
→ action
→ Use Case
→ Domain/server
```

# Framework Loader + Server State

If loader and selected query cache coexist, establish one source of truth.

Possible:

```text
loader prefetches query cache
→ route uses same cache
```

or:

```text
loader data is authoritative initial result
→ server-state layer revalidates according to policy
```

Do not perform two unrelated fetches by default.

# Test Containers

A test container may be useful to provide:

- composition dependencies;
- router context;
- server-state cache client;
- design-system providers;
- translations;
- feature flags.

It should mirror production composition enough to exercise behavior.

Do not create a giant universal test app for every component test.

# Test Container Scope

Prefer the smallest realistic wrapper.

Examples:

```text
renderFeature()
renderWithRouter()
renderWithServerState()
```

according to repository conventions.

Do not hide all test setup behind opaque helpers that make dependencies impossible to override.

# Dependency Overrides in Tests

Test composition should allow explicit replacement of:

- Use Cases;
- repositories/ports when container directly consumes them;
- clock;
- analytics;
- server-state client.

Use InMemory/fakes where appropriate.

Do not reach into a global Factory and mutate singleton state between tests.

# Container Testing

Test containers for composition behaviors such as:

- correct route input mapping;
- dependency binding;
- navigation after semantic result;
- server/client handoff;
- loader integration;
- modal close/retry behavior.

Do not retest all presentational rendering and all Use Case branches through the container.

# Presentational Testing

View/component tests should test rendering and user interaction independent of infrastructure when practical.

Container tests verify composition.

Use Case tests verify Application behavior.

This preserves boundary-focused testing.

# Dependency Creation

Concrete dependencies belong to:

```text
Factory
composition root
route outer boundary explicitly designated as composition root
```

Do not construct HTTP clients/repositories in leaf containers.

# Safe Shared Instances

Composition may reuse safe stateless instances.

Avoid accidental singleton scope for:

- per-request auth;
- per-user mutable state;
- request-scoped server services.

Container composition must honor lifecycle established by `composing-frontend-dependencies`.

# Context Providers

Use Context when it represents a real shared Presentation/composition dependency.

Examples:

- app-level semantic dependencies;
- theme;
- i18n;
- auth/session presentation context;
- approved dependency provider.

Do not put every Use Case into a giant untyped “services context” by default.

# Service Locator Anti-Pattern

Avoid:

```ts
const services = useServices()
services.resolve("applyPromotion")
```

through arbitrary feature code.

Prefer typed explicit dependencies or narrowly scoped approved context.

# Prop Drilling

Do not introduce Context solely because a dependency passes through one or two levels.

Likewise, do not insist on prop drilling through an entire app when a stable composition provider is clearly justified.

Apply proportionality.

# Container Props

Container props should normally be semantic route/feature inputs:

```text
subscriptionId
organizationId
initialData
mode
```

not concrete infrastructure instances from arbitrary callers unless the container itself is deliberately reusable at a composition boundary.

# View Props

View props should remain rendering-oriented.

Container converts:

```text
framework + hook state
→ view contract
```

This helps keep route/library types out of presentational components.

# Derived View State

Container may derive simple presentation semantics:

```text
canRetry
showRefreshingIndicator
isSubmitDisabled
```

when these are direct feature/UI derivations.

Do not move substantial business calculations into the container.

If derivation is reusable/pure presentation logic, a view-data mapper may be cleaner.

# Event Wiring

Container may bind semantic commands:

```ts
onApply={() => apply(code)}
onRetry={retry}
onClose={close}
```

Avoid anonymous handlers containing business orchestration:

```ts
onClick={async () => {
  const data = await repo.get(...)
  if (...) ...
  await analytics...
}}
```

That belongs in hook/Application.

# Effects in Containers

Containers may use Effects only for genuine synchronization/lifecycle integration.

Do not use Effects to:

- copy hook state to local state;
- trigger normal user command flows;
- derive props.

Apply `designing-react-effects`.

# Server-State Hooks

Container may use selected server-state hooks directly or through a feature hook according to architecture.

Do not expose query-library response objects directly to the view unless the view is intentionally coupled.

Prefer stable semantic props.

# Async State

Container should consume the accepted async-state model.

Do not invent another status model.

Example:

```text
hook/server-state
→ semantic feature state
→ view props
```

# Accessibility

Container may coordinate accessibility behaviors that depend on application flow, such as:

- returning focus after modal close;
- choosing page title/heading data;
- announcing completion/error through a presentation mechanism.

Keep actual semantic markup/focus primitives in Presentation/accessibility layer.

Do not hide accessibility decisions in Infrastructure/Application.

# Error Recovery

Container may wire:

```text
Retry button
→ retry command
```

or:

```text
Session expired
→ auth/session boundary
```

according to stable semantic errors.

Do not inspect raw HTTP status in container if adapter/Application already translated it.

# Analytics

Presentation/container may emit analytics only if project ownership says UI interaction analytics belongs there.

Business/application analytics may instead be a Use Case port.

Do not duplicate the same event in container and Use Case.

# Feature Flags

Container may read a Presentation-level feature flag to choose composition.

If flag changes business behavior, Application ownership may be more appropriate.

Do not import provider SDK directly if an approved flag abstraction exists.

# Container File Naming

Use repository conventions.

Possible:

```text
PromotionFeature.tsx
PromotionContainer.tsx
PromotionRoute.tsx
PromotionScreen.tsx
```

Do not introduce `Container.tsx` suffix universally if project naming differs.

# Folder Placement

Container belongs with the route/feature that owns composition.

Avoid central:

```text
src/containers
```

dumping ground unless project architecture explicitly uses it.

Feature/vertical-slice ownership should remain visible.

# Public Surface

Expose the feature entrypoint intentionally.

A package/feature public API may expose:

```text
PromotionFeature
```

while keeping internal view/hook modules private.

Do not export every internal container/view/helper through broad barrels.

# Container and View Same File

Valid:

```tsx
export function PromotionFeature(...) {
  const state = usePromotion(...)
  return <PromotionView ... />
}

function PromotionView(...) {
  ...
}
```

for a small cohesive feature.

File separation is not an architecture requirement.

# Extract When Valuable

Extract the view when:

- props are stable and meaningful;
- separate component tests are useful;
- route/framework code obscures rendering;
- multiple containers reuse the same view;
- server/client split requires it.

Do not extract based on line count alone.

# Ceremonial Wrapper Audit

Flag:

```text
wrapper only forwards props
wrapper only renames component
container has no dependency/routing/hook role
multiple one-line container layers
container exists solely for folder symmetry
```

Use:

```text
PROPORTIONATE_CONTAINER
UNDERCOMPOSED_FEATURE
CEREMONIAL_CONTAINER
NO_CONTAINER_REQUIRED
```

# Under-Composition Signals

A container/composition boundary may be missing when:

- component imports concrete repository;
- hook calls global Factory unexpectedly;
- route parses provider DTOs;
- view imports router object for one ID;
- server-only dependency leaks into client component;
- every test mutates global dependency singletons.

Fix the composition boundary rather than hiding imports.

# Route Container Evaluation

Verify:

- route is outer composition boundary;
- route params become semantic inputs;
- dependencies come from approved composition;
- route file does not become business module;
- view does not receive router/library objects unnecessarily.

# Modal Feature Evaluation

Verify:

- meaningful async/dependency behavior justifies container;
- pure modal stays presentational;
- open/close/submit ownership is clear;
- focus and error recovery are preserved;
- no duplicate server-state/local async ownership.

# Tiny Component Evaluation

Given a tiny component with props only:

```text
NO_CONTAINER_REQUIRED
```

should be preferred.

Do not create wrappers for architectural aesthetics.

# Next.js Server/Client Evaluation

Verify:

- server-only dependencies remain server-side;
- client boundary is explicit;
- only serializable safe data crosses;
- client does not import server module;
- route cache/server-state hydration avoids duplicate load;
- request/user scope is safe.

# React Router Loader Evaluation

Verify:

- loader parses route inputs;
- calls accepted Application/repository boundary;
- returns serializable Application-safe data;
- provider/HTTP mapping stays Infrastructure;
- route errors follow accepted framework policy;
- client does not duplicate initial load accidentally.

# Test Container Evaluation

Verify:

- wrapper contains only required providers;
- dependencies are overrideable;
- server-state cache is isolated;
- router state is explicit;
- no mutable global Factory hacking;
- tests focus on composition behavior.

# Testing Matrix

Test only meaningful composition behavior.

Potential cases:

```text
route param mapping
dependency injection
hook/view binding
navigation after success
modal retry/close
server/client serialization boundary
loader initial-data reuse
test dependency override
```

Do not repeat Domain/Use Case/provider tests.

# Overmodeling Audit

Flag:

- container per component;
- container + view + presenter + connector for a trivial screen;
- universal `withContainer` HOC;
- generic container framework;
- giant app services context;
- route container that only forwards loader data;
- test container that boots the whole app for leaf tests.

# Final Decision

Use:

```text
REACT_FEATURE_CONTAINER_READY
REACT_FEATURE_CONTAINER_READY_WITH_CONDITIONS
NO_CONTAINER_REQUIRED
ROUTE_IS_COMPOSITION_BOUNDARY
CONTAINER_AND_VIEW_COLOCATED
RETURN_TO_COMPOSITION_OR_HOOK_DESIGN
SERVER_CLIENT_BOUNDARY_REQUIRED
LOADER_INTEGRATION_REQUIRED
TEST_COMPOSITION_REQUIRED
BLOCKED
```

## Output

Use `assets/react-feature-container-composition-record.md`.

## Completion Criteria

- [ ] Container justification is explicit.
- [ ] `NO_CONTAINER_REQUIRED` is accepted as valid.
- [ ] Dependency creation remains at approved outer composition boundary.
- [ ] Container obtains semantic dependencies rather than concrete Infrastructure ad hoc.
- [ ] Route/framework inputs are mapped into stable feature inputs.
- [ ] Router objects are not passed deep when semantic values suffice.
- [ ] Hooks receive explicit/approved dependencies.
- [ ] Container consumes existing async/server-state ownership rather than duplicating it.
- [ ] View receives rendering-oriented semantic props.
- [ ] UseQuery/SWR/router/provider types do not leak into presentational view without intentional coupling.
- [ ] Business rules remain Domain/Application-owned.
- [ ] Provider/HTTP mapping remains Infrastructure-owned.
- [ ] Navigation remains Presentation-owned.
- [ ] Permission checks are not treated as backend security.
- [ ] Container/view separation is proportional and may remain in one file.
- [ ] Tiny components do not receive ceremonial containers.
- [ ] Modal containers exist only for meaningful composition.
- [ ] Next.js server/client boundaries are explicit and serializable.
- [ ] React Router loaders/actions remain routing adapters, not Application replacements.
- [ ] Loader + server-state duplicate fetching is avoided.
- [ ] Test containers are small, realistic, isolated, and overrideable.
- [ ] Global mutable service-locator patterns are avoided.
- [ ] Feature public surface remains narrow.
- [ ] Roadmap evaluations are covered: route container, modal feature, tiny component, Next.js server/client split, React Router loader, test container.
- [ ] No generic container framework, new DI system, or wrapper ceremony is introduced.
- [ ] Final composition decision is explicit.

## References

- Read `references/container-justification-and-composition-boundary.md` first.
- Read `references/route-modal-and-view-composition.md`.
- Read `references/nextjs-server-client-and-framework-boundaries.md`.
- Read `references/react-router-loaders-actions-and-prefetch.md`.
- Read `references/test-containers-and-dependency-overrides.md`.
- Read `references/ceremonial-containers-service-location-and-overmodeling.md`.
- Read `references/react-feature-container-composition-audit.md` before completion.
