# Frontend Server State Integration Record

## Context

- Change/capability:
- Repository/application:
- Architecture profile:
- Selected server-state profile:
- Accepted behavior:
- Use Cases/repositories:
- Adapter boundary:
- Async-state model:
- Route/framework:
- SSR/client runtime:
- Retry policy:
- Security/privacy scope:
- Applicable `AGENTS.md`:
- Designed/implemented by/date:

## Readiness

- Server-state profile selected:
- Architecture boundary known:
- Resource identities known:
- Invalidation policy known:
- Optimistic policy known:
- Route prefetch policy known:
- SSR/hydration policy known:
- Initial decision:
- Conditions/blockers:

## Profile

- Profile: REACT_QUERY / SWR / RTK_QUERY / APOLLO / RELAY / FRAMEWORK_LOADERS / CUSTOM_APPROVED_SERVER_STATE
- Existing project conventions:
- New library introduced:
- Library-private abstractions avoided:

## Architecture Integration

- Pattern: PRESENTATION_DIRECT_TO_SERVER_STATE / SERVER_STATE_TO_USE_CASE / SERVER_STATE_TO_REPOSITORY / SERVER_STATE_TO_ADAPTER / FRAMEWORK_LOADER_TO_APPLICATION / ARCHITECTURE_REQUIRES_DECISION
- Why:
- Query/mutation function calls:
- Concrete adapter creation location:
- Raw fetch bypass:
- Provider mapping remains Infrastructure:
- Library types stay out of Domain/Application:

## Resource Inventory

| Resource | Semantic identity | Read owner | Mutation owner |
|---|---|---|---|
| | | | |

## Query Keys / Resource Identity

| Resource | Key/identity | Inputs included | Presentation-only values excluded |
|---|---|---|---|
| | | | |

- Deterministic:
- Complete:
- URL/version transport details excluded:
- Tenant/user scope included:
- Key factory justified:

## Cache Ownership

- Library owns remote cache:
- Duplicate local/store cache:
- Editable draft is separate owner:
- Data shape cached:
- View formatting excluded:
- Sensitive data considerations:

## Freshness

| Resource | Policy | Product-visible stale | Library mapping |
|---|---|---|---|
| | ALWAYS_REVALIDATE/SHORT_LIVED/SESSION_STABLE/IMMUTABLE/EVENT_INVALIDATED/USER_INVALIDATED/ROUTE_INVALIDATED/OFFLINE_STALE_ALLOWED | | |

- Arbitrary staleTime avoided:
- Cache stale vs product stale distinguished:

## Deduplication

- Same-resource consumers:
- Shared semantic key:
- Route + component duplicate:
- Prefetch + mount duplicate:
- Retry/polling/focus refetch distinguished from duplicate:
- Native library dedup used:

## Invalidation Matrix

| Mutation/event | Detail | Lists | Aggregates | Prefetched routes | Normalized records |
|---|---|---|---|---|---|
| | | | | | |

- Global invalidate avoided:
- Derived caches covered:
- Timing:
- Mutation result reused:
- Refetch required:

## Mutation Integration

| Mutation | Semantic command | Function boundary | Result |
|---|---|---|---|
| | | Use Case/repository/adapter | |

- Business rules excluded from mutation config:
- HTTP verb not used as query/mutation semantic:

## Optimistic Update

- Applicable:
- Owner: SERVER_STATE_LIBRARY / DOMAIN / APPLICATION / LOCAL_WORKFLOW
- Affected resources:
- Snapshot:
- Optimistic patch:
- Authoritative success reconciliation:
- Rollback:
- Related cache consistency:
- Concurrent policy: SERIALIZE / KEYED_CONCURRENT / LATEST_WINS / QUEUE / LIBRARY_NATIVE_POLICY
- High-risk operation check:

## Retry

- Primary owner: SERVER_STATE_LIBRARY / HTTP_CLIENT / ADAPTER / USE_CASE / NO_RETRY
- Query retries:
- Mutation retries:
- Idempotency:
- Forbidden/contract/cancelled retry:
- Hidden retry stacking checked:

## Cancellation

- Library cancellation capability:
- Signal propagation:
- Use Case/repository support:
- Adapter/HTTP propagation:
- Cancelled not treated as generic error:
- Stale response protection:

## Dependent Queries

| Parent | Dependency | Child | Enabled/conditional rule |
|---|---|---|---|
| | | | |

- Fake placeholder IDs avoided:
- Dependency enters child key:
- Parent error prevents bogus child request:
- Waterfall unavoidable:
- Aggregation/prefetch alternative:

## Parallel Queries

- Independent resources:
- Parallelized:
- Effect serialization avoided:

## Route Prefetch

| Route/intent | Resource | Prefetch trigger | Destination uses same identity |
|---|---|---|---|
| | | | |

- Prefetch cost:
- Freshness:
- Immediate duplicate refetch avoided:
- Abandoned navigation safe:

## Framework Loader Integration

- Loader owns server state:
- Combined with query cache:
- Source of truth:
- Loader fetch + component fetch duplication:
- Cache seeded intentionally:

## SSR / Hydration

- Server cache/client lifecycle:
- Request scoped:
- Server auth/request context:
- Dehydration:
- Client hydration:
- Resource identity matches:
- Loading flicker avoided:
- Unsafe errors/functions/provider objects excluded:
- Server secrets excluded:

## Error Boundaries

- Local feature errors:
- Route errors:
- React Error Boundary:
- Auth/session boundary:
- Retry/reset behavior:
- Recoverable errors not over-escalated:

## Pagination / Search / Polling

- Pagination identity:
- Next-page state:
- Search filters:
- Debounce excluded from key:
- Polling:
- Focus/reconnect revalidation:
- Feature deviations:

## Normalization / Profile-Specific Mechanisms

- React Query query options:
- SWR key/mutate:
- RTK Query tags:
- Apollo normalized cache:
- Relay records/fragments:
- Framework revalidation:
- Profile-specific details remain Integration-layer only:

## Security Scope

- User identity in keys:
- Tenant/org identity in keys:
- Tokens/secrets excluded from keys:
- PII minimized:
- Logout/user-switch cache reset:
- Cross-user cache leakage prevented:
- Persisted cache:
- Dehydrated state reviewed:

## Adapter Integration

- QueryFn/mutationFn dependency:
- Use Case/repository boundary:
- Provider DTO mapping:
- Runtime validation:
- Stable errors:
- Cancellation:
- No direct raw fetch where architecture forbids:

## Test Matrix

| Roadmap case | Setup | Expected semantic behavior |
|---|---|---|
| duplicate requests | two same-resource consumers | one accepted underlying load |
| stale invalidation | mutation affects detail/list/aggregate | all required resources become current |
| optimistic rollback | controlled mutation failure | previous semantic cache restored |
| dependent queries | parent identity unresolved/resolved | child waits then loads correct key |
| route prefetch | prefetch then destination | cache reused according to policy |
| adapter integration | semantic dependency fake | correct boundary invoked/results exposed |

## Test Isolation

- Query/cache client per test:
- Timers reset:
- Requests reset:
- Subscriptions reset:
- Auth/context reset:
- Library internals not asserted:

## Duplicate Request Audit

- Different key for same resource:
- Loader + query:
- Prefetch + query:
- StrictMode/dev behavior:
- Retry:
- polling:
- focus revalidation:

## Overmodeling Audit

- Query library wrapped generically:
- Global query-key framework:
- Local cache duplicate:
- Hook rebuilding retries/dedup:
- Server-state used for modal/UI state:
- Library cache metadata leaked inward:
- Cache persistence introduced without requirement:
- Query abstraction hides selected library with no value:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
