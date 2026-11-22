---
name: wiring-backend-composition
description: Portable engineering capability `wiring-backend-composition`. Use when
  the harness or a specialist agent explicitly requires this named capability.
---
# Wiring Backend Composition

## Purpose

Create or evolve the backend composition root so the complete dependency graph is explicit, deterministic, and testable.

The composition root must:

- be the only general location that selects concrete adapters;
- validate configuration near startup;
- cache deliberate shared Infrastructure dependencies;
- create Use Cases as fresh transient objects;
- expose narrow delivery-facing factories;
- avoid runtime dependency-injection containers;
- avoid Service Locator behavior;
- prevent Domain and Application from importing composition;
- provide deterministic reset behavior for tests;
- manage startup and shutdown lifecycle safely.

Current project policy:

```text
get*    → cached shared dependency
create* → fresh transient dependency
```

## Use When

- A new Use Case, repository adapter, provider adapter, controller, or module must be wired.
- Concrete adapters are selected in several unrelated files.
- Database or provider clients are constructed per request accidentally.
- Environment variables are read throughout business code.
- Use Cases are cached despite being intended as transient.
- Tests share stale module-level clients or configuration.
- A framework container is being introduced despite the explicit factory policy.
- The dependency graph or lifecycle ownership is unclear.
- Startup validation and graceful shutdown must be made explicit.

## Do Not Use When

- Domain or Application behavior is still unresolved.
- Required repository or provider ports/adapters do not exist.
- The task is to design a repository, Use Case, DTO, controller, or adapter.
- A runtime DI container has been accepted centrally as a different project policy.
- The request is merely to create arbitrary global singletons.
- The proposed factory would expose a generic `resolve(token)` API.
- Application or Domain would import Infrastructure composition.
- Configuration defaults or adapter choices are speculative.

## Inputs

- Accepted Domain and Application implementation.
- Repository and external-service ports.
- Concrete repository and provider adapters.
- Controllers or delivery entry points.
- Configuration and environment requirements.
- Shared/transient lifecycle policy.
- Startup and shutdown conventions.
- Existing factory/composition modules and tests.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the relevant vertical slice and completed implementation records.
3. Inspect all required ports and concrete adapters.
4. Inspect current entry points, factories, bootstrap code, and lifecycle hooks.
5. Confirm the project policy:
   - explicit factory composition;
   - no runtime DI container;
   - cached shared Infrastructure;
   - transient Use Cases.
6. Identify every configuration key and validation rule.
7. Identify shared resource lifecycle:
   - database clients;
   - SDK clients;
   - connection pools;
   - telemetry;
   - caches;
   - message clients.
8. Identify delivery-facing construction needs.
9. Inspect test setup/reset conventions.
10. Do not infer adapter selection or environment policy silently.

## Outputs

- Explicit composition-root module.
- Central configuration loader and validator integration.
- Cached `get*` factories for shared Infrastructure.
- Fresh `create*` factories for Use Cases and controllers where appropriate.
- Adapter selection decisions.
- Startup readiness and shutdown behavior.
- Deterministic test reset function.
- Composition tests.
- Composition implementation record.

## Core Architecture

```text
entry point / delivery
→ composition root
→ concrete Infrastructure adapters
→ Application ports and Use Cases
→ Domain
```

Dependency direction remains inward.

Only the composition root knows both:

- inward abstractions;
- outward implementations.

## Workflow

1. **Confirm composition readiness:** Required ports, adapters, Use Cases, and policy exist.
2. **Inventory the graph:** List nodes, dependencies, owners, and lifecycle.
3. **Classify lifecycle:** Shared, transient, request-scoped, startup-only, or shutdown-managed.
4. **Centralize configuration:** Read and validate required settings near the root.
5. **Select concrete adapters:** Make environment/project choices explicit.
6. **Implement shared factories:** Cache deliberate Infrastructure resources through `get*`.
7. **Implement transient factories:** Build fresh Use Cases through `create*`.
8. **Wire delivery factories:** Controllers receive Use Cases, not repositories or adapters.
9. **Implement startup validation:** Fail early before serving traffic.
10. **Implement shutdown:** Close resources once and in safe order.
11. **Implement deterministic reset:** Clear caches and close resources for tests.
12. **Test graph and lifecycle:** Selection, caching, transience, config failure, reset, and shutdown.
13. **Audit boundaries:** No factory import in Domain/Application and no Service Locator.
14. **Report:** Use the composition implementation record.

## Readiness Gate

Use one:

```text
READY_TO_WIRE_COMPOSITION
READY_WITH_CONDITIONS
RETURN_TO_PORT_OR_ADAPTER_IMPLEMENTATION
CONFIGURATION_DECISION_REQUIRED
LIFECYCLE_DECISION_REQUIRED
ADAPTER_SELECTION_REQUIRED
BLOCKED
```

Stop when:

- an inward port has no accepted implementation;
- several adapters exist but selection policy is unresolved;
- required environment variables are unknown;
- resource sharing or shutdown ownership is unresolved;
- test reset cannot safely close resources;
- Domain or Application currently imports composition.

## Composition Root Ownership

Composition belongs in Infrastructure or the executable entry-point layer according to repository topology.

It must not live in:

- Domain;
- Application;
- shared Domain modules;
- reusable business packages.

The executable entry point may import the composition root.

The composition root may import both ports and implementations.

## Explicit Factory Policy

Use explicit named factory functions.

Example:

```ts
export function getDatabaseClient(): DatabaseClient
export function getPromotionRepository(): PromotionRepository
export function getCampaignProvider(): CampaignProvider
export function createApplyPromotionUseCase(): ApplyPromotionUseCase
export function createApplyPromotionController(): ApplyPromotionController
```

Names reveal lifecycle and responsibility.

Avoid:

```ts
container.resolve(...)
serviceLocator.get(...)
dependencies["promotionRepository"]
buildEverything()
```

unless `buildEverything` is a narrow bootstrap function with an explicit typed result and no runtime lookup behavior.

## Shared Dependencies

Shared Infrastructure usually includes expensive or stateful resources:

- database connection pools;
- ORM clients;
- provider SDK clients;
- HTTP connection pools;
- telemetry exporters;
- message-broker clients;
- long-lived caches.

Use module-level caching only deliberately.

Example concept:

```ts
let databaseClient: DatabaseClient | undefined

export function getDatabaseClient(): DatabaseClient {
  databaseClient ??= createDatabaseClient(getConfig())
  return databaseClient
}
```

Requirements:

- construction is centralized;
- configuration is already validated;
- repeated calls return the same instance;
- shutdown closes it once;
- tests can reset it deterministically.

## Transient Dependencies

Use Cases are fresh transient objects under current policy.

```ts
export function createApplyPromotionUseCase(): ApplyPromotionUseCase {
  return new ApplyPromotionUseCase(
    getPromotionRepository(),
    getSubscriptionRepository(),
    getCampaignProvider(),
    getClock(),
  )
}
```

Repeated calls should return different Use Case instances while sharing accepted Infrastructure.

Do not cache Use Cases merely because they are stateless today. Current policy is explicit.

## Controllers

Controllers or route handlers may be:

- created once by framework bootstrap when stateless;
- created through explicit factories;
- recreated per request only when framework policy requires it.

Regardless of controller lifecycle, each receives Application Use Cases rather than repositories, provider adapters, or clients.

Do not let controllers call composition functions during each handler invocation unless framework architecture explicitly requires that pattern.

Prefer wiring at registration/bootstrap.

## Configuration

Configuration and environment variables must be read and validated near composition.

Recommended flow:

```text
raw environment
→ configuration parser
→ validation
→ typed immutable config
→ adapter construction
```

Do not read `process.env` throughout:

- Use Cases;
- Domain;
- repositories;
- controllers;
- provider operation methods.

Adapters may receive typed configuration through constructors or dedicated Infrastructure config objects.

## Configuration Validation

Validate at startup:

- required values;
- enum choices;
- URLs;
- numeric ranges;
- timeout values;
- credentials references;
- region;
- environment;
- feature/adapter selection;
- mutually exclusive options.

Fail early with a safe configuration error.

Do not log secret values.

Do not silently invent production defaults for critical configuration.

## Adapter Selection

The composition root is the only general place that chooses concrete adapters.

Examples:

```text
PromotionRepository → PrismaPromotionRepository
CampaignProvider → AcmeCampaignProvider
Clock → SystemClock
```

Selection may depend on:

- environment;
- explicit configuration;
- executable target;
- test composition;
- accepted feature switch.

Do not use business code conditionals such as:

```ts
if (process.env.CAMPAIGN_PROVIDER === "acme") ...
```

inside Use Cases.

## Multiple Implementations

When multiple adapters exist, define an explicit selector.

The selector must:

- be exhaustive;
- fail on unsupported values;
- return the inward port type;
- remain inside composition;
- avoid provider-specific types in consumers.

Do not silently fall back to another provider unless that fallback is accepted architecture.

## Manual Composition

Current policy rejects runtime DI containers.

Do not introduce:

- decorators for automatic injection;
- runtime reflection;
- token registries;
- provider arrays;
- global `container`;
- hidden auto-discovery.

Manual construction should remain readable and typed.

If the graph becomes large, split composition by capability while keeping one explicit top-level entry.

## Capability Composition

A large backend may use focused modules:

```text
composition/
  config.ts
  database.ts
  campaigns.ts
  promotions.ts
  http.ts
  index.ts
```

Rules:

- each module exposes named factories;
- concrete selection remains in composition;
- no inward layer imports these modules;
- shared resources have one lifecycle owner;
- top-level bootstrap remains understandable.

Do not create circular factory modules.

## Service Locator Anti-Pattern

A factory becomes a Service Locator when business or delivery code pulls arbitrary dependencies at runtime.

Forbidden patterns:

```ts
locator.get("repository")
container.resolve(Symbol.for("CampaignProvider"))
context.services.paymentGateway
```

Prefer constructor injection performed once at composition.

The composition root pushes dependencies into objects; objects do not pull them from a global registry.

## Factory Import Boundaries

Allowed:

```text
main/bootstrap
→ composition root

route registration
→ explicit controller factory
```

Forbidden:

```text
Domain → factory
Application Use Case → factory
Entity → getRepository()
Domain Service → container
```

Tests may import reset/test composition functions explicitly.

## Circular Dependencies

Detect graph cycles before implementation.

Common causes:

- composition module imports controller;
- controller imports composition;
- Use Case imports factory;
- two capability composition modules create each other.

Resolve by:

- constructor injection;
- moving shared port inward;
- top-level orchestration;
- separating creation from registration;
- eliminating runtime lookup.

Do not use lazy dynamic `require()` as a hidden cycle fix.

## Startup

A bootstrap function should:

1. load and validate configuration;
2. initialize required shared resources;
3. verify critical connectivity only when accepted;
4. register controllers/routes/consumers;
5. start delivery server;
6. install shutdown hooks;
7. expose readiness according to policy.

Do not accept traffic before critical startup requirements are satisfied.

Differentiate:

- construction;
- startup initialization;
- readiness;
- liveness.

## Eager Versus Lazy Initialization

### Lazy Shared Initialization

Useful when:

- resource is optional;
- startup cost should be deferred;
- factory access is controlled.

### Eager Initialization

Useful when:

- failure must block startup;
- readiness requires connectivity;
- migrations/schema/version must be checked;
- provider configuration must be verified.

Choose explicitly.

Do not allow accidental first-request initialization for critical resources without accepted policy.

## Readiness and Health

Composition coordinates health contributors but business code should not know them.

Define:

- liveness;
- readiness;
- startup state;
- degraded dependencies;
- optional dependency behavior.

Health endpoints should use dedicated health ports/services rather than exposing raw clients.

## Shutdown

Install shutdown handling in the executable/bootstrap layer.

Close resources in a safe, deterministic order:

```text
stop accepting new work
→ drain in-flight work
→ stop consumers/jobs
→ flush telemetry
→ close provider/message clients
→ close database
```

Exact order follows architecture.

Requirements:

- each resource closes once;
- shutdown is idempotent;
- partial-startup cleanup is handled;
- time-bounded shutdown is explicit;
- errors are logged safely.

## Test Reset

Module-level cached state requires an explicit reset strategy.

Example:

```ts
export async function resetCompositionForTests(): Promise<void> {
  await closeProviderClientIfCreated()
  await closeDatabaseClientIfCreated()
  clearCachedConfig()
  clearAllCachedFactories()
}
```

Requirements:

- only test code should call it;
- close resources before clearing references;
- reset all deliberate caches;
- restore environment/config isolation;
- be safe when resources were never initialized;
- be safe after partial construction;
- avoid leaking handles across test files.

## Test Composition

Tests may provide separate explicit composition:

```text
createTestApplyPromotionUseCase({
  promotionRepository,
  campaignProvider,
  clock
})
```

Prefer direct constructor construction for focused tests.

Use the production composition root only for integration/HTTP tests that aim to validate real wiring.

Do not overload production factories with many optional test-only parameters unless project convention explicitly supports override factories.

## Overrides

When integration tests need overrides, use a typed, narrow test composition builder.

Example concept:

```ts
createTestComposition({
  campaignProvider: fakeCampaignProvider,
})
```

Guardrails:

- unavailable in production runtime;
- typed by port;
- explicit default behavior;
- no string-token lookup;
- resettable.

Do not turn overrides into a global mutable Service Locator.

## Environment Isolation in Tests

Tests that alter environment/config must:

- save original state;
- reset composition caches;
- restore state;
- avoid parallel collision;
- use isolated processes when necessary.

A cached config object can make environment changes appear ignored unless reset deliberately.

## Composition Tests

### Shared Lifecycle

Verify:

```text
getDatabaseClient() === getDatabaseClient()
getCampaignProvider() === getCampaignProvider()
```

when those dependencies are shared.

### Transient Lifecycle

Verify:

```text
createApplyPromotionUseCase() !== createApplyPromotionUseCase()
```

while their shared dependencies match.

### Adapter Selection

Test every accepted configuration option and unsupported values.

### Configuration Failure

Missing or invalid configuration should fail before operation handling.

### Reset

Verify:

- resources close;
- references clear;
- next access creates fresh shared resources;
- reset is idempotent.

### Boundary Test

Use static architecture checks when available to ensure:

- Domain does not import composition/Infrastructure;
- Application does not import composition/concrete adapters;
- only composition selects concrete implementations.

## Avoid Over-Mocking

Composition tests can use construction spies or lightweight fake constructors when necessary.

Do not reproduce the entire object graph with brittle mocks.

Prefer checking:

- instance type;
- identity/lifecycle;
- resolved port implementation;
- configuration propagation;
- reset behavior.

## Factories and Errors

Factory construction errors should:

- identify the dependency/capability safely;
- avoid secrets;
- fail deterministically;
- preserve technical cause in protected telemetry;
- not be translated into Domain errors.

Configuration/bootstrap failures are operational failures.

## Generated Clients and Schema

Composition may construct generated clients but must not generate or modify them.

Generation belongs to source-schema tooling.

The root selects and configures the generated client adapter.

## Observability Wiring

Composition may construct:

- logger;
- tracer;
- metrics exporter;
- audit publisher.

Provide them only through accepted inward ports or Infrastructure constructors.

Do not inject Infrastructure loggers into every Use Case by habit.

Initialize telemetry early enough to capture startup failures and close it during shutdown.

## Security

Composition owns critical operational boundaries:

- secrets retrieval;
- credential selection;
- TLS configuration;
- regional endpoints;
- production versus sandbox mode;
- tenant/account mapping;
- startup validation.

Do not print complete configuration objects.

Avoid accidentally selecting sandbox adapters in production.

Environment-to-adapter selection should be explicit and exhaustively tested.

## Existing Composition Refactoring

Warning signs:

- `new PrismaClient()` in controllers;
- provider SDK constructed per request;
- `process.env` inside Use Cases;
- global container;
- Application imports Infrastructure factory;
- cached Use Cases;
- no shutdown;
- tests require process restart to clear state.

Incremental recovery:

```text
inventory graph
→ centralize one shared client
→ create one adapter factory
→ create one transient Use Case factory
→ wire one controller
→ add reset and lifecycle tests
→ migrate next slice
```

Avoid rewriting the entire bootstrap unless required.

## Boundary Guardrails

Composition may import:

- Application Use Cases and ports;
- concrete Infrastructure adapters;
- controllers/delivery registrations;
- typed configuration;
- resource lifecycle utilities.

Domain and Application must not import:

- composition root;
- concrete adapters;
- runtime container;
- configuration/environment readers.

## Output

Use `assets/backend-composition-implementation-record.md`.

## Completion Criteria

- [ ] Required ports, adapters, Use Cases, controllers, and policies are ready.
- [ ] Complete dependency graph and lifecycle classification are explicit.
- [ ] Configuration is loaded and validated near the composition root.
- [ ] Concrete adapter selection exists in one general location.
- [ ] Shared Infrastructure uses cached `get*` factories.
- [ ] Use Cases use fresh `create*` factories.
- [ ] Controllers receive Use Cases rather than repositories/adapters.
- [ ] No runtime DI container or Service Locator exists.
- [ ] Domain and Application do not import composition.
- [ ] Startup/readiness and shutdown lifecycle are explicit.
- [ ] Module-level caches have deterministic test reset behavior.
- [ ] Adapter selection, lifecycle, config failure, reset, and boundary tests pass.
- [ ] Secrets and configuration are not exposed.
- [ ] No speculative adapter, fallback, lifecycle, or environment default was introduced.

## References

- Read `references/composition-readiness-and-graph.md` first.
- Read `references/factory-lifecycle-and-adapter-selection.md` for `get*`/`create*` behavior.
- Read `references/configuration-startup-and-shutdown.md` for operational lifecycle.
- Read `references/test-reset-and-composition-testing.md` before completion.
- Read `references/service-locator-and-boundary-guardrails.md` for anti-patterns.
- Read `references/refactoring-existing-composition.md` only for brownfield composition.
