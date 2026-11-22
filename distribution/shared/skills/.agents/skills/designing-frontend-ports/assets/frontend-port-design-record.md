# Frontend Port Design Record

## Context

- Change/capability:
- Repository/application:
- Architecture profile:
- User/system intention:
- Domain model:
- Use Case:
- DTO/result contract:
- External provider/browser capability:
- Offline/cache requirements:
- Security/privacy requirements:
- Server/client runtime:
- Applicable `AGENTS.md`:
- Designed by/date:

## Readiness

- Capability semantics known:
- Port needed:
- Owner known:
- Failure semantics:
- Cancellation policy:
- Cache/sync policy:
- Security/privacy policy:
- Initial decision:
- Conditions/blockers:

## Port Justification

- Capability:
- Why inward abstraction is needed:
- Provider replacement value:
- Testability value:
- Package/public-boundary value:
- Decision: PORT_JUSTIFIED / PORT_BOUNDARY_VALUE_ONLY / PORT_OVERMODELED / NO_PORT_REQUIRED

## Ownership

- Owner: DOMAIN_PORT / APPLICATION_PORT / NO_PORT_REQUIRED / OWNERSHIP_REQUIRES_DECISION
- Why Domain/Application:
- Would Domain need it without current Use Case:
- Folder/module:

## Category

- Category: REPOSITORY / EXTERNAL_SERVICE / BROWSER_CAPABILITY / TIME / IDENTITY / ANALYTICS / CACHE / SYNC / CONNECTIVITY / SUBSCRIPTION / FILE_ACCESS / NOTIFICATION / OTHER_SEMANTIC_CAPABILITY
- Runtime: SERVER_ONLY / CLIENT_ONLY / ISOMORPHIC / SPLIT_IMPLEMENTATION

## Contract

```text

```

### Methods

| Method | Semantic intention | Input | Output |
|---|---|---|---|
| | | | |

- Product language:
- Narrow interface:
- CRUD completeness avoided:
- Endpoint/provider naming excluded:

## Input Boundary

| Input | Type | Owner | Serializable |
|---|---|---|---|
| | Domain/Application/primitive | | |

- Request/Response excluded:
- React/browser event excluded:
- Provider SDK excluded:
- Transport config excluded:

## Output Boundary

| Output | Type | Semantic meaning |
|---|---|---|
| | Domain/Application/result/primitive/void | |

- Raw payload excluded:
- SDK object excluded:
- Browser handle excluded:
- Cache object excluded:

## Not-Found Semantics

- Relevant:
- Representation:
- Valid absence vs failure:
- Command not-found behavior:
- Repository lookup behavior:

## Failure Contract

| Failure | Stable port semantic | Caller behavior differs |
|---|---|---|
| unavailable | | |
| unauthenticated | | |
| forbidden | | |
| not found | | |
| conflict | | |
| timeout | | |
| cancelled | | |
| contract mismatch | | |
| rate limited | | |
| unknown | | |

- Raw provider/HTTP/browser errors excluded:
- Result/typed-error convention:

## Cancellation and Races

- Operation can become obsolete:
- Cancellation contract:
- AbortSignal policy:
- Vendor cancellation excluded:
- Cancellation outcome:
- Port supports cancellation:
- Latest-wins owner:
- Adapter dedup owner:

## Repository Semantics

- Applicable:
- Collection/persistence language:
- `findById` semantics:
- `save` semantics:
- `remove` semantics:
- Ordering:
- Pagination:
- Search/filter semantics:
- Endpoint mirroring excluded:

## Browser Storage

- Applicable:
- Semantic store/repository:
- localStorage details hidden:
- IndexedDB details hidden:
- Migration/version handling kept Infrastructure:
- Storage failure semantics:

## Analytics

- Applicable:
- Semantic events:
- Allowed fields:
- PII excluded:
- Failure policy: BEST_EFFORT / REQUIRED_FOR_INTENTION / OUTER_LAYER_ONLY
- Vendor event names excluded:

## Clipboard / Files / Geolocation / Notifications

| Capability | Application need | Port method | Stable failures |
|---|---|---|---|
| Clipboard | | | |
| Files | | | |
| Geolocation | | | |
| Notifications | | | |

- Browser APIs excluded:
- Permission semantics:
- Presentation-owned permission prompt decisions:

## Time / Identity / Connectivity

- Clock needed:
- `now()` semantic:
- ID generator needed:
- ID semantics:
- Connectivity needed:
- Connectivity semantics:
- `navigator.onLine` not treated as contract:

## Cache Semantics

- Classification: CACHE_TRANSPARENT / CACHE_POLICY_APPLICATION_VISIBLE / STALE_WHILE_REVALIDATE_VISIBLE / OFFLINE_CACHE_VISIBLE
- Freshness visible to caller:
- Cache metadata returned:
- Query/cache library types excluded:
- Invalidation ownership:
- Cache key details excluded:

## Sync

- Applicable:
- Sync intention:
- Input:
- Result:
- Conflict semantics:
- Partial success:
- Retry ownership:
- Provider protocol hidden:

## Subscription / Lifecycle

- Applicable:
- Subscription key:
- Event semantics:
- Unsubscribe:
- Error semantics:
- Reconnect ownership:
- Ordering:
- Duplicate events:
- Adapter lifecycle:

## Security / Privacy

- Sensitive inputs:
- Sensitive outputs:
- Secrets excluded:
- Token/header exposure excluded:
- Consent:
- Redaction:
- Third-party sharing:
- Retention assumptions:
- Frontend authorization not treated as authority:

## Server / Client Boundary

- Server implementation:
- Client implementation:
- Semantic equivalence:
- Browser-only adapter excluded from server:
- Request/user mutable state lifecycle:

## Adapter Candidates

| Adapter | Provider/runtime | Replaceable behind port |
|---|---|---|
| | | |

- No adapter implementation designed here:

## Test Doubles

| Port type | Double | Required semantics |
|---|---|---|
| Repository | IN_MEMORY_IMPLEMENTATION | |
| External service | FAKE/STUB/SPY | |
| Clock | VIRTUAL_CLOCK | |
| Subscription | CONTROLLED_SUBSCRIPTION_SOURCE | |

- Mock-framework-driven API avoided:
- Shared contract tests justified:

## Overmodeling Audit

- Generic getJson/request:
- Endpoint-shaped method:
- Generic StorageService:
- God BrowserCapabilitiesPort:
- `execute(action, payload)`:
- Provider-specific names:
- CRUD completeness:
- Port used by one Infrastructure implementation only:
- Abstraction justified beyond mocking:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
