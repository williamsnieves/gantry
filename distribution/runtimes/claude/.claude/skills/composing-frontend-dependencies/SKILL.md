---
name: composing-frontend-dependencies
description: Implements or designs the frontend composition root that selects concrete adapters, constructs stable Use Cases, controls shared, per-user, per-request, route, and component lifecycles, and injects dependencies at application, route, screen, container, or package boundaries. Use after ports and adapters exist and React components/hooks must receive semantic dependencies without importing concrete Infrastructure. Reuse deliberate shared clients, prevent accidental singleton user state, respect framework server/client boundaries, support deterministic test injection, and follow the repository's accepted explicit Factory or DI-container policy. Do not create a Service Locator, let Domain/Application import composition, hide environment or user context, construct expensive clients per render, cache mutable Use Cases globally, or introduce a DI library without an accepted decision.
---

# Composing Frontend Dependencies

## Purpose

Create or evolve the frontend composition boundary that connects:

```text
UI / framework entry point
→ Application Use Cases
→ ports
→ concrete Infrastructure adapters
```

The composition design must make explicit:

- which concrete implementation satisfies each port;
- where dependencies are created;
- which instances are shared;
- which instances are user-, request-, route-, or component-scoped;
- how configuration and trusted context enter;
- how React components and hooks receive semantic dependencies;
- how tests replace dependencies deterministically;
- how server and client runtimes remain separated.

Composition belongs to Infrastructure or the executable application boundary.

It does not belong to Domain or Application.

## Roadmap Purpose

This skill covers:

- implementing a Factory or composition root;
- creating stable Use Cases and adapters;
- controlling lifecycle and caching;
- binding dependencies at routes, screens, or containers.

It explicitly evaluates:

- cached `HttpClient`;
- per-user adapter;
- test dependency injection;
- accidental singleton state;
- framework server/client boundary;
- projects using a DI container.

## Use When

- Accepted ports and concrete adapters must be wired.
- A route, screen, container, hook, or package consumer needs Use Cases.
- Components or hooks currently import concrete adapters.
- A global Factory is being called from arbitrary feature code.
- An `HttpClient` or SDK is created repeatedly.
- User-specific state is accidentally cached globally.
- Tests cannot replace dependencies cleanly.
- SSR, React Server Components, hydration, or serverless requests require scope decisions.
- A monorepo package needs app-specific composition.
- The project uses an explicit Factory and needs consistent lifecycle.
- The project already uses an accepted DI container and needs safe registration boundaries.

## Do Not Use When

- Ports or adapters are not accepted.
- Application behavior is unresolved.
- The task is to design or implement a repository adapter.
- The task is component or hook design only.
- The task is selecting a DI library.
- A direct feature helper is sufficient under the accepted Profile A design.
- The task is backend-only.
- The proposal would expose generic runtime dependency lookup to feature code.

## Inputs

- Architecture-profile decision.
- Frontend vertical-slice plan.
- Accepted Domain/Application implementation.
- Ports and concrete adapters.
- Component and hook designs.
- Framework rendering model.
- Authentication and tenant/user context model.
- Configuration and environment policy.
- Server-state and HTTP-client policy.
- Existing Factory, providers, context, bootstrap, or DI container.
- Test setup and reset conventions.
- Repository-local `AGENTS.md`.

## Outputs

- Composition-root implementation or design.
- Dependency graph.
- Lifecycle classification.
- Concrete adapter-selection decisions.
- Route/screen/container binding.
- Server/client split.
- Trusted user/request context binding.
- Test override strategy.
- Reset/disposal strategy where applicable.
- Focused composition tests.
- Frontend composition record.

## Core Architecture

```text
app / route / screen / package consumer
→ composition boundary
→ concrete Infrastructure
→ Application Use Cases
→ Domain
```

Only the composition boundary should normally know both:

- inward ports and Use Cases;
- outward concrete implementations.

## Governing Rules

Domain MUST NOT import composition.

Application MUST NOT import composition or concrete Infrastructure.

Components and hooks MUST NOT import concrete repository or HTTP adapters.

Feature code MUST NOT call a generic:

```text
resolve(token)
getService(name)
container.get(anything)
```

unless the accepted framework/DI policy explicitly limits that lookup to the composition boundary.

Composition MUST NOT become a Service Locator.

## Workflow

1. Confirm ports, adapters, Use Cases, and policy are ready.
2. Map the complete dependency graph.
3. Classify each dependency lifecycle.
4. Identify server-only, client-only, and isomorphic dependencies.
5. Centralize configuration and trusted context.
6. Select concrete adapters explicitly.
7. Construct deliberate shared clients.
8. Construct scoped adapters and Use Cases.
9. Bind dependencies at app, route, screen, container, or package boundaries.
10. Define React provider/context use only where justified.
11. Define test overrides and deterministic reset/disposal.
12. Verify no hidden global mutable state.
13. Test selection, identity, isolation, server/client boundaries, and overrides.
14. Record the composition decision.

## Readiness Gate

Use one:

```text
READY_TO_COMPOSE_FRONTEND_DEPENDENCIES
READY_WITH_CONDITIONS
RETURN_TO_PORT_OR_ADAPTER_IMPLEMENTATION
ADAPTER_SELECTION_REQUIRED
LIFECYCLE_DECISION_REQUIRED
USER_CONTEXT_DECISION_REQUIRED
SERVER_CLIENT_BOUNDARY_REQUIRED
CONFIGURATION_DECISION_REQUIRED
DI_POLICY_DECISION_REQUIRED
BLOCKED
```

Stop when:

- an inward port has no accepted implementation;
- adapter selection is ambiguous;
- user/request scope is unresolved;
- server and browser code would be bundled together accidentally;
- secrets would cross to the client;
- tests cannot isolate mutable global state;
- the repository's Factory versus DI-container policy is unknown.

## Dependency Graph

For each node record:

- abstraction or concrete type;
- direct dependencies;
- creation owner;
- lifecycle;
- runtime;
- configuration;
- disposal;
- test override.

Example:

```text
HttpClient
→ PromotionHttpRepository
→ ApplyPromotionUseCase
→ useApplyPromotion
→ PromotionPanel
```

Avoid hidden edges created by module imports, global registries, or ambient mutable state.

## Lifecycle Classification

Use:

```text
BUILD_TIME
APP_SINGLETON
SERVER_PROCESS_SINGLETON
REQUEST_SCOPED
USER_SCOPED
SESSION_SCOPED
ROUTE_SCOPED
SCREEN_SCOPED
COMPONENT_SCOPED
TRANSIENT
EXTERNAL_LIBRARY_MANAGED
```

The lifetime must not outlive the context it captures.

## Shared Infrastructure

Reasonable shared dependencies may include:

- stateless configured HTTP clients;
- telemetry clients;
- runtime validators;
- immutable configuration;
- browser capability wrappers with no user-specific mutable state;
- SDK clients documented as safe to share.

Requirements:

- construction is deliberate;
- configuration is stable;
- no request/user token is captured unsafely;
- tests can replace or reset it;
- server and client instances are not confused;
- disposal is defined if necessary.

## Cached `HttpClient`

A cached client is acceptable when:

- it is safe for the selected runtime;
- credentials are resolved per request or through an approved token provider;
- it does not capture one user's token forever;
- interceptors/listeners are not registered repeatedly;
- base URL and policy are immutable or correctly scoped;
- server requests remain isolated.

Bad:

```text
global client created after first login
→ Authorization header permanently captures user A
```

Preferred:

```text
shared transport engine
+ request-scoped or current-session credential provider
```

or:

```text
request-scoped server HttpClient
```

according to framework policy.

## Mutable Singleton Risk

Do not cache globally:

- current user;
- current tenant;
- mutable cart/editor/workflow state;
- request headers;
- per-request cookies;
- route parameters;
- abort controllers;
- transient Use Case state;
- server-state cache unless the library/runtime explicitly owns it safely.

Use:

```text
SAFE_SHARED
SCOPED_REQUIRED
MUTABLE_SINGLETON_BLOCKER
EXTERNAL_LIBRARY_MANAGED
```

## Use Case Lifecycle

Use Cases are usually:

```text
TRANSIENT
ROUTE_SCOPED
SCREEN_SCOPED
```

depending on the accepted implementation.

A stateless Use Case may be reusable, but global caching is not automatically beneficial.

Do not cache a Use Case that captures:

- user context;
- request-specific adapters;
- cancellation state;
- mutable workflow state;
- feature flags evaluated per request.

Prefer fresh construction when lifecycle is cheap and ambiguity exists.

## Adapter Lifecycle

Classify adapters based on captured dependencies.

Examples:

```text
HttpPromotionRepository over safe shared HttpClient
→ may be app/session scoped

Server repository with cookies/request headers
→ request scoped

IndexedDB repository
→ app or browser-session scoped with explicit connection lifecycle

InMemory repository in test
→ test scoped

User-specific local cache
→ user/session scoped
```

Do not infer scope from class name.

## Configuration

Configuration should enter near the composition boundary.

Separate:

```text
PUBLIC_CLIENT_CONFIGURATION
SERVER_ONLY_CONFIGURATION
BUILD_TIME_CONFIGURATION
RUNTIME_CONFIGURATION
USER_OR_REQUEST_CONTEXT
```

Do not expose server secrets to client bundles.

Do not read environment variables throughout Domain, Application, hooks, or components.

Validate required configuration according to project policy.

## User, Tenant, and Request Context

Trusted context may include:

- authenticated user ID;
- tenant/organization ID;
- locale;
- request headers;
- cookies;
- feature flags;
- correlation ID;
- region/account selection.

Define:

- trusted source;
- scope;
- refresh/change behavior;
- whether it belongs in adapter, Use Case input, or provider context;
- test override.

Do not obtain authority from arbitrary component form values.

Do not cache context beyond its valid scope.

## Server and Client Boundary

Classify every dependency:

```text
SERVER_ONLY
CLIENT_ONLY
ISOMORPHIC
SERIALIZABLE_CONFIGURATION
NON_SERIALIZABLE_RUNTIME_OBJECT
```

Server-only examples:

- secrets;
- server cookies API;
- privileged BFF client;
- filesystem;
- Node-only SDK.

Client-only examples:

- IndexedDB;
- localStorage;
- DOM;
- browser analytics SDK;
- notification APIs.

Do not import server-only modules into client components or client bundles.

Do not pass repository instances, functions, class instances, or clients through a serialized server/client boundary.

Pass serializable data or configure the client-side composition separately.

## React Server Components / SSR

Possible patterns:

### Server Composition

```text
server route/component
→ request-scoped server adapter
→ Use Case
→ serializable result
→ client component
```

### Client Composition

```text
client route/container
→ client composition module/provider
→ browser/HTTP adapter
→ hook/component
```

### Hybrid

Use separate server and client composition roots.

Do not create one universal module that imports both server secrets and browser APIs.

## Serverless and Edge

In serverless or edge runtimes:

- process-level reuse is opportunistic, not guaranteed;
- request data must remain request scoped;
- APIs and SDK support may differ;
- connection/resource reuse must follow platform guidance;
- global mutable state must not contain user data;
- disposal assumptions may differ.

Do not rely on one process singleton for correctness.

## Binding Location

Select the narrowest stable composition boundary.

Use:

```text
APPLICATION_BOOTSTRAP
ROUTE_BOUNDARY
SERVER_ROUTE_HANDLER
SCREEN_CONTAINER
FEATURE_CONTAINER
FEATURE_PROVIDER
PACKAGE_CONSUMER
TEST_HARNESS
```

### Application Bootstrap

Use for stable application-wide infrastructure.

### Route Boundary

Use when dependencies depend on route, request, auth, or tenant context.

### Screen/Feature Container

Use when a feature needs a small semantic dependency set.

### Feature Provider

Use when several descendants need one stable feature-scoped contract and props composition is inadequate.

### Package Consumer

Use when Profile C packages require app-specific adapters.

Do not bind concrete dependencies in a presentational component.

## Props Injection

Use props when:

- the dependency reaches one or few consumers;
- the contract is explicit;
- composition depth is small;
- tests benefit from direct replacement.

Pass semantic Use Cases or commands rather than broad dependency bags.

Good:

```text
applyPromotion
loadPromotion
```

Potentially acceptable:

```text
applyPromotionUseCase
```

Avoid:

```text
services
dependencies
container
repository
httpClient
```

in presentational props.

## Hook Factory

A composed hook factory may close over accepted dependencies:

```text
createUseApplyPromotion({ applyPromotionUseCase })
```

Use when:

- it creates a stable feature-semantic hook;
- construction occurs at an explicit boundary;
- dependencies remain testable;
- framework constraints support it.

Do not create factories that hide global lookup.

## React Context / Provider

Use a feature provider when:

- several descendants need the same feature-scoped dependency or API;
- prop composition is genuinely inadequate;
- provider scope and lifetime are clear;
- value identity is controlled;
- missing-provider behavior is explicit.

Context must expose a narrow semantic contract.

Bad:

```text
ServicesContext = { every repository, every client, every use case }
```

Do not use context as a Service Locator.

## Provider Value Stability

Provider values should avoid unnecessary identity changes when that causes meaningful consumer work.

Use memoization only when:

- object identity is a real provider contract;
- React Compiler/project behavior does not already handle it;
- dependencies are correct;
- stability is useful.

Do not memoize merely for stylistic reasons.

## Factory Policy

When explicit Factory composition is accepted, prefer named functions.

Examples:

```text
getHttpClient()
getPromotionRepository()
createApplyPromotionUseCase()
createPromotionScreenDependencies()
```

Names should reveal lifecycle:

```text
get*
→ deliberately cached/shared

create*
→ fresh/scoped
```

This convention is a project policy and must match repository rules.

Avoid generic runtime lookup.

## Factory Caching

A cached factory must define:

- exact cache key;
- lifecycle;
- captured context;
- reset/disposal;
- server/client runtime;
- test isolation.

Possible keyed caches:

```text
per user
per tenant
per request
per configuration
```

Use keyed caching only when lifecycle and eviction are explicit.

Do not create unbounded user-keyed module caches.

## Per-User Adapter

A per-user adapter may be required when it captures:

- user token;
- tenant;
- region/account;
- user-specific local storage namespace;
- encryption key;
- server-state cache.

Define:

- creation trigger;
- identity key;
- logout/user-switch behavior;
- disposal/eviction;
- cross-tab behavior;
- test isolation.

A global cached adapter that captures the first user is a blocker.

## Authentication Changes

When login/logout/token refresh occurs:

- avoid stale credentials;
- define whether clients read current credentials dynamically;
- recreate scoped adapters when identity changes;
- clear user-specific caches where required;
- prevent data leakage between users;
- cancel or isolate in-flight work when necessary.

Do not assume a cached Authorization header updates automatically.

## Server-State Providers

Server-state libraries may own:

- client/cache instance;
- deduplication;
- retries;
- invalidation;
- hydration/dehydration.

Composition should:

- create them at the accepted scope;
- avoid cross-user server cache leakage;
- bind adapters/hooks consistently;
- provide test instances;
- follow SSR hydration policy.

Do not create one global server-side cache shared across users unless explicitly safe and accepted.

## Analytics and Browser Services

Browser services may be composed:

- at client bootstrap;
- behind semantic adapters;
- through a feature/app provider.

Define:

- consent;
- initialization;
- user identity changes;
- teardown;
- SSR exclusion;
- test fake.

Do not initialize them during render.

## DI Container Projects

If the repository already has an accepted DI container:

- use it only at composition boundaries;
- register concrete implementations centrally;
- use typed tokens where supported;
- classify scope explicitly;
- avoid direct `container.resolve()` inside Domain, Application, components, and hooks;
- define child/request/user scopes where needed;
- reset/dispose test containers;
- avoid reflection-heavy magic crossing package boundaries without policy.

Use one:

```text
EXPLICIT_FACTORY_POLICY
ACCEPTED_DI_CONTAINER_POLICY
FRAMEWORK_MANAGED_INJECTION
POLICY_DECISION_REQUIRED
```

Do not replace an accepted DI container merely because explicit factories are preferred elsewhere.

Do not introduce a container into a project that does not already accept one.

## Framework-Managed Injection

Frameworks may provide:

- route loaders/actions;
- request context;
- server dependency context;
- plugin injection;
- application providers.

Use framework mechanisms only when:

- lifecycle semantics are understood;
- types remain explicit;
- Domain/Application remain framework-independent;
- tests can inject alternatives;
- server/client boundaries are safe.

## Package-Scale Composition

For Profile C:

```text
capability package
→ exports ports / Use Cases / public UI contracts
app
→ supplies concrete adapters and composition
```

The package should not import app-specific adapters.

Each app may use a different implementation.

Avoid deep imports into package internals.

## Circular Dependencies

Composition modules are prone to cycles.

Prevent:

- feature public surface importing app composition;
- adapter importing container that imports adapter;
- provider importing component barrel that reexports provider;
- broad index barrels hiding cycles.

Composition should sit at an outer edge.

Use direct imports for wiring when broad barrels create ambiguity.

## Lazy Dependencies and Code Splitting

A route may lazily load:

- feature UI;
- adapter SDK;
- Use Case graph.

Define:

- chunk boundary;
- construction timing;
- failure fallback;
- preload;
- lifecycle after navigation;
- server/client compatibility.

Do not use lazy composition to hide unresolved lifecycle.

## Disposal

Dependencies may require:

- unsubscribe;
- close;
- abort;
- destroy;
- flush;
- clear cache;
- remove listener.

Define disposal owner:

```text
APPLICATION_SHUTDOWN
REQUEST_END
USER_LOGOUT
ROUTE_UNMOUNT
PROVIDER_UNMOUNT
TEST_TEARDOWN
EXTERNAL_LIBRARY_MANAGED
```

Do not dispose a shared client from one component consumer.

## Test Injection

Tests should replace dependencies without mutating production global state unpredictably.

Preferred strategies:

- pass dependency props;
- create test-specific composition root;
- use provider override with scoped value;
- construct factory with explicit overrides;
- use child/test DI container;
- inject InMemory ports or spies.

Avoid:

- patching module globals across concurrent tests;
- mocking every internal import;
- exposing production Service Locator reset methods to feature code.

## Deterministic Reset

If module caching is used, tests need:

- explicit reset;
- disposal before reset;
- isolated config;
- no cross-test user state;
- no open listeners or timers.

Reset belongs to test/bootstrap utilities, not Domain/Application.

## Composition Tests

Test:

- correct adapter selected;
- shared client identity;
- transient/scoped Use Case identity;
- per-user isolation;
- user switch/logout;
- server request isolation;
- no server module in client bundle path;
- provider missing behavior;
- test override;
- disposal/reset;
- configuration failure;
- DI scope where applicable.

Do not retest business behavior through composition tests.

## Identity Assertions

Examples:

```text
getHttpClient() === getHttpClient()
```

when safe sharing is policy.

```text
createApplyPromotionUseCase() !== createApplyPromotionUseCase()
```

when transient creation is policy.

```text
getRepository(userA) !== getRepository(userB)
```

when user scope is required.

Identity expectations must derive from the accepted lifecycle, not naming alone.

## Security and Privacy

Verify:

- no server secret enters client code;
- no user data survives logout into another user session;
- no cross-request server cache leakage;
- auth/tenant context is trusted;
- logs and debug graphs redact sensitive configuration;
- test fakes do not accidentally use production services.

## Anti-Patterns

Reject:

- Service Locator;
- global `dependencies` object imported everywhere;
- global Factory called inside hooks/components;
- one singleton repository capturing first-user credentials;
- concrete adapter passed through many presentation layers;
- expensive client recreated on every render;
- provider containing every application service;
- server and client adapters in one universal module;
- process-global server-state cache containing user data;
- DI container resolution inside business or presentation code;
- hidden module side effects that initialize services on import;
- unbounded per-user cache.

## Composition Decisions

Use:

```text
FRONTEND_COMPOSITION_READY
FRONTEND_COMPOSITION_READY_WITH_CONDITIONS
FACTORY_POLICY_APPLIED
DI_CONTAINER_POLICY_APPLIED
ROUTE_OR_REQUEST_SCOPE_REQUIRED
USER_SCOPE_REQUIRED
SERVER_CLIENT_SPLIT_REQUIRED
LIFECYCLE_DECISION_REQUIRED
RETURN_TO_ADAPTER_OR_USE_CASE_IMPLEMENTATION
BLOCKED
```

## Output

Use `assets/frontend-dependency-composition-record.md`.

## Completion Criteria

- [ ] Ports, adapters, Use Cases, and policy are accepted.
- [ ] Complete dependency graph is explicit.
- [ ] Every dependency has a lifecycle and runtime classification.
- [ ] Concrete adapters are selected only in composition.
- [ ] Shared clients are cached only when safe.
- [ ] User/request/route context does not leak into longer-lived instances.
- [ ] Use Case lifecycle is explicit.
- [ ] Configuration is centralized and server secrets remain server-only.
- [ ] Components and hooks receive semantic dependencies without importing concrete adapters.
- [ ] Props, hook factories, or focused providers are used proportionately.
- [ ] Context is not a Service Locator.
- [ ] Server and client composition roots are separated where required.
- [ ] SSR/serverless/server-state caches cannot leak across users.
- [ ] Explicit Factory or accepted DI-container policy is followed.
- [ ] No new DI library is introduced silently.
- [ ] Test overrides are deterministic and scoped.
- [ ] Reset/disposal behavior is defined where required.
- [ ] Composition tests verify selection, identity, isolation, boundaries, and cleanup.
- [ ] Domain/Application do not import composition.
- [ ] No hidden global mutable user state remains.

## References

- Read `references/composition-root-and-dependency-graph.md` first.
- Read `references/lifecycle-caching-and-user-isolation.md` for scope decisions.
- Read `references/react-binding-props-providers-and-hook-factories.md` for UI binding.
- Read `references/server-client-ssr-and-framework-boundaries.md` for runtime separation.
- Read `references/factory-di-container-testing-and-disposal.md` for policy and tests.
- Read `references/frontend-composition-audit.md` before completion.
