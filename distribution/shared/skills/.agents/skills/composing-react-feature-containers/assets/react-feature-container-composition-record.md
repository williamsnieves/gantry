# React Feature Container Composition Record

## Context

- Change/capability:
- Repository/application:
- Architecture profile:
- Route/screen:
- Composition root/Factory:
- Use Cases/dependencies:
- Feature hook:
- Server-state profile:
- Presentational view:
- Routing framework:
- Server/client runtime:
- Test strategy:
- Applicable `AGENTS.md`:
- Composed by/date:

## Readiness

- Route/feature boundary known:
- Composition root known:
- Hook contract known:
- View contract known:
- Server/client boundary known:
- Loader/action policy known:
- Initial decision:
- Conditions/blockers:

## Container Justification

- Decision: CONTAINER_JUSTIFIED / CONTAINER_AND_VIEW_COLOCATED / ROUTE_IS_COMPOSITION_BOUNDARY / HOOK_IS_EXPLICIT_COMPOSITION_BOUNDARY / NO_CONTAINER_REQUIRED / CEREMONIAL_CONTAINER
- Why:
- Dependency composition value:
- Routing/framework value:
- Testability value:
- Reusable view value:
- Wrapper-only ceremony:

## Composition Flow

```text

```

- Outer boundary:
- Dependency source:
- Hook:
- View:
- Navigation:
- Error/loading owner:

## Dependencies

| Dependency | Type | Created by | Lifetime |
|---|---|---|---|
| | Use Case / port / semantic service | | |

- Concrete adapters created in container:
- Global Factory called from hook/view:
- Service locator:
- Per-request/user state safety:

## Route / Framework Inputs

| Raw framework input | Semantic feature input | Validation/normalization |
|---|---|---|
| route param | | |
| search param | | |
| loader data | | |
| server data | | |

- Router object passed deep:
- URLSearchParams leaked inward:

## Hook Binding

- Hook:
- Dependencies passed:
- Semantic state:
- Commands:
- Server-state owner:
- State copied locally:
- Duplicate Effects:

## View Contract

```text

```

- Data props:
- Semantic status:
- Commands:
- Accessibility content:
- React/router/server-state library objects excluded:
- Use Case/repository instances excluded:

## Container/View Placement

- Same file:
- Separate files:
- Why:
- Presentational view independently testable:
- Extraction improves clarity:
- Line count not used as hard rule:

## Navigation

- Trigger:
- Semantic result:
- Container routing action:
- Use Case routing excluded:
- Raw HTTP/provider status excluded:

## Permissions / Metadata

- Frontend capability/permission:
- Backend remains authoritative:
- Page metadata:
- Route-level concerns only:

## Loading / Error Boundaries

- Initial loading owner:
- Background refresh owner:
- Local recoverable errors:
- Route-level errors:
- Auth/session errors:
- React render errors:
- Duplicate states avoided:

## Modal Feature

- Applicable:
- Composition justified:
- Dependencies:
- Async state:
- Open/close owner:
- Submit/retry owner:
- Focus-return behavior:
- Pure presentational modal alternative:

## Tiny Component Check

- Applicable:
- Props-only:
- External dependencies:
- Routing:
- Hook:
- Decision:
- Ceremonial wrapper avoided:

## Next.js Server / Client Split

- Applicable:
- Server component/route:
- Server-only dependencies:
- Server data:
- Serialized client props:
- Client container:
- Interactive hook:
- `use client` boundary:
- Server secrets/functions/instances excluded:
- Request-scope safety:
- Duplicate server/client fetch avoided:

## React Router Loader / Action

- Applicable:
- Loader/action:
- Route input parsing:
- Application/repository call:
- Serializable output:
- Provider mapping excluded:
- Route error policy:
- Initial data reuse:
- Client duplicate load avoided:

## Server-State Integration

- Query/cache owner:
- Loader hydration/prefetch:
- Same semantic resource identity:
- Query library response hidden from view:
- No duplicate local remote-state cache:

## Test Container

- Required:
- Providers:
- Router:
- Server-state cache:
- Dependencies overrideable:
- InMemory/fakes:
- Cache isolated:
- Global Factory mutation avoided:
- Whole-app boot avoided:

## Container Test Matrix

| Scenario | Composition behavior |
|---|---|
| route param mapping | |
| dependency binding | |
| hook → view props | |
| navigation after semantic result | |
| modal retry/close | |
| server/client boundary | |
| loader initial-data reuse | |
| dependency override | |

## Ceremonial Wrapper Audit

- Wrapper only forwards props:
- Container per component:
- Deep container chain:
- Generic container HOC/framework:
- Giant services context:
- Route merely renames loader props:
- View has no independent value:
- Decision: PROPORTIONATE_CONTAINER / UNDERCOMPOSED_FEATURE / CEREMONIAL_CONTAINER / NO_CONTAINER_REQUIRED

## Under-Composition Audit

- Component imports concrete repository:
- Hook calls global Factory unexpectedly:
- Route maps provider DTO:
- View depends on full router for one ID:
- Client imports server-only dependency:
- Tests mutate singleton services:

## Public Surface

- Feature entrypoint:
- Internal view:
- Internal hook:
- Narrow exports:
- Broad barrel avoided:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
