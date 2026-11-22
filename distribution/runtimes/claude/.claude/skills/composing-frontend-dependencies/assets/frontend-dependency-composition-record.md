# Frontend Dependency Composition Record

## Context

- Change/slice:
- Repository/application:
- Owning capability:
- Architecture profile:
- Framework/rendering model:
- Composition policy:
- Existing composition modules:
- Applicable `AGENTS.md`:
- Implemented/designed by:
- Date:

## Readiness

- Ports accepted:
- Adapters implemented:
- Use Cases implemented:
- Adapter selection resolved:
- User/request context resolved:
- Server/client boundary resolved:
- Configuration resolved:
- Initial decision:
- Conditions/blockers:

## Dependency Graph

```text

```

| Node | Abstraction/concrete | Dependencies | Creation owner |
|---|---|---|---|
| | | | |

## Lifecycle Classification

| Dependency | Lifecycle | Runtime | Captured context | Disposal |
|---|---|---|---|---|
| | BUILD_TIME/APP_SINGLETON/SERVER_PROCESS_SINGLETON/REQUEST_SCOPED/USER_SCOPED/SESSION_SCOPED/ROUTE_SCOPED/SCREEN_SCOPED/COMPONENT_SCOPED/TRANSIENT/EXTERNAL_LIBRARY_MANAGED | SERVER_ONLY/CLIENT_ONLY/ISOMORPHIC | | |

## Configuration

| Value | Classification | Validation | Consumer |
|---|---|---|---|
| | PUBLIC_CLIENT_CONFIGURATION/SERVER_ONLY_CONFIGURATION/BUILD_TIME_CONFIGURATION/RUNTIME_CONFIGURATION/USER_OR_REQUEST_CONTEXT | | |

- Environment reads centralized:
- Client-exposed values:
- Server secrets protected:
- Configuration failure behavior:

## Shared Dependencies

| Dependency | Shared | Cache owner/key | Safety evidence |
|---|---|---|---|
| | | | |

- Cached HttpClient decision:
- Credential behavior:
- Interceptor/listener duplication:
- Server request isolation:
- Accidental mutable singleton risks:

## User / Tenant / Request Scope

- Trusted context source:
- User identity:
- Tenant identity:
- Token/credential refresh:
- User switch/logout:
- Per-user adapters:
- Cache eviction:
- Cross-tab:
- In-flight request behavior:
- Cross-user leakage protection:

## Use Cases and Adapters

| Use Case/adapter | Lifecycle | Concrete dependencies | Reason |
|---|---|---|---|
| | | | |

- Mutable state captured:
- Fresh versus cached decision:
- Port implementation selection:
- Environment-specific selection:

## Server / Client Composition

### Server

- Composition root:
- Request context:
- Request-scoped dependencies:
- Server-only modules:
- Cache scope:
- Serializable result:

### Client

- Composition root:
- Browser-only dependencies:
- Session/user scope:
- Provider scope:
- Hydration inputs:

### Boundary

- Non-serializable objects excluded:
- Universal-module risk:
- Serverless/edge considerations:
- Client bundle checks:

## Binding Location

- Selected boundary:
- Route/screen/container/package:
- Why this is the narrowest stable boundary:
- Presentational construction excluded:
- Lazy-loading/code-splitting:

## React Binding

### Props Injection

- Semantic dependencies passed:
- Broad dependency bags excluded:
- Depth:

### Hook Factory

- Factory:
- Closed-over dependencies:
- Test override:
- Global lookup excluded:

### Context / Provider

- Provider:
- Scope:
- Exposed contract:
- Value stability:
- Missing-provider behavior:
- Broad services context excluded:

## Factory or DI Policy

- Policy: EXPLICIT_FACTORY_POLICY / ACCEPTED_DI_CONTAINER_POLICY / FRAMEWORK_MANAGED_INJECTION
- Named factories or registrations:
- `get*` cached semantics:
- `create*` fresh semantics:
- DI scopes/tokens:
- Generic resolve exposure:
- New library introduced:

## Server-State and External Libraries

- Cache/client owner:
- Client scope:
- Server request isolation:
- Hydration/dehydration:
- Test instance:
- Analytics/widget lifecycle:

## Disposal and Reset

| Resource | Disposal trigger | Action | Owner |
|---|---|---|---|
| | APPLICATION_SHUTDOWN/REQUEST_END/USER_LOGOUT/ROUTE_UNMOUNT/PROVIDER_UNMOUNT/TEST_TEARDOWN/EXTERNAL_LIBRARY_MANAGED | | |

- Reset function:
- Disposal before reset:
- Open handles:
- Cross-test isolation:

## Test Injection

- Strategy:
- InMemory/fakes:
- Provider/factory override:
- Test container:
- Module-global mutation excluded:
- Production service protection:

## Composition Test Evidence

| Case | Expected | Result |
|---|---|---|
| Concrete adapter selection | | |
| Shared client identity | | |
| Use Case/scoped identity | | |
| Per-user isolation | | |
| User switch/logout | | |
| Server request isolation | | |
| Server/client import boundary | | |
| Provider missing behavior | | |
| Test override | | |
| Disposal/reset | | |
| Configuration failure | | |
| DI scope | | |

## Security and Privacy

- Secret leakage:
- Cross-user data:
- Cross-request cache:
- Trusted context:
- Logging/redaction:
- Production service use in tests:

## Architecture Checks

- Domain imports composition:
- Application imports composition:
- Components/hooks import concrete adapters:
- Deep feature/package imports:
- Circular dependencies:
- Broad barrels:
- Service Locator:
- Hidden module initialization:

## Residual Risks

| Risk/question | Owner | Blocking |
|---|---|---|
| | | |

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
