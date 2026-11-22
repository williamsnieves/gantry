# Frontend Async State Modeling Record

## Context

- Change/capability:
- Repository/application:
- Architecture profile:
- Accepted behavior:
- Hook/component:
- Use Case/result:
- Server-state strategy:
- Optional-value convention:
- Error semantics:
- Retry policy:
- Cancellation policy:
- Optimistic policy:
- Partial-data behavior:
- Applicable `AGENTS.md`:
- Modeled by/date:

## Readiness

- Async behavior known:
- State owner known:
- Optionality convention known:
- Error semantics known:
- Retry policy known:
- Cancellation policy known:
- Optimistic policy known:
- Partial-data policy known:
- Initial decision:
- Conditions/blockers:

## State Ownership

- Primary owner: LOCAL_UI_STATE / HOOK_ASYNC_STATE / SERVER_STATE_LIBRARY / APPLICATION_RESULT / ROUTE_LOADER_STATE / EXTERNAL_STORE / MIXED_WITH_EXPLICIT_BOUNDARY
- Why:
- Remote state copied locally:
- Duplicate source of truth:
- Decision: PROPORTIONATE_ASYNC_STATE / UNDERMODELED_ASYNC_STATE / OVERMODELED_ASYNC_STATE / SERVER_STATE_DUPLICATION / ASYNC_STATE_NOT_REQUIRED

## Optional Value Convention

- Convention: undefined / null / Maybe<T> / discriminated union / library status
- Meaning of absence:
- Mixed conventions:
- Why coherent:

## Observable State Inventory

| State | User-visible difference | Commands differ | Data retained |
|---|---|---|---|
| idle | | | |
| loading | | | |
| success | | | |
| empty | | | |
| error | | | |
| refreshing | | | |
| stale | | | |
| retrying | | | |
| cancelled | | | |
| optimistic | | | |
| rollingBack | | | |
| partial | | | |

- Removed redundant states:

## Representation

```text

```

- Representation type: primitives / Maybe / discriminated union / server-state status / reducer state
- Discriminant:
- Invalid combinations prevented:
- Optional fields inside success/error avoided:

## Initial / Idle

- Initial state:
- Idle observable:
- Auto-start:
- Hydrated/server-provided initial data:
- Loading flash avoided:

## Loading / Success / Empty

- Initial loading meaning:
- Success data guarantee:
- Empty representation:
- Empty commands/rendering differ:

## Error

- Stable error type:
- Initial error clears data:
- Refresh error preserves data:
- Retryability:
- Forbidden/not-found/empty distinctions:

## Transition Table

| From | Event | To | Data retention | Error retention |
|---|---|---|---|---|
| | | | | |

- Invalid transitions:
- Command guards:
- Functional/atomic update requirement:

## Background Refresh

- Applicable:
- Previous data remains:
- Refresh indicator:
- Refresh success:
- Refresh failure:
- Full loading avoided:
- Server-state library owns refresh:

## Stale

- Applicable:
- Classification: CACHE_STALE_INTERNAL / PRODUCT_STALE_VISIBLE
- User-visible stale meaning:
- Freshness source:
- Library staleTime not leaked:
- Offline cached behavior:

## Retry

- Applicable:
- Valid source states:
- Input preserved:
- Previous data preserved:
- Old error clearing:
- Dedicated retrying state justified:
- Duplicate retry behavior:

## Cancellation

- Applicable:
- Meaning:
- Outcome: idle / previous success / retained data / explicit cancelled / silent
- Generic error avoided:
- Late completion ignored:
- Public state does not expose AbortController/request counter:

## Resource Identity Change

- Key:
- Policy: CLEAR_ON_KEY_CHANGE / KEEP_PREVIOUS_DATA / STALE_WHILE_REVALIDATE / SERVER_STATE_LIBRARY_OWNS
- Old data behavior:
- Race/stale-response policy:

## Optimistic Update

- Applicable:
- Owner: SERVER_STATE_LIBRARY / HOOK_LOCAL_WORKFLOW / DOMAIN / APPLICATION
- Optimistic state:
- Previous state source:
- Success reconciliation:
- Failure rollback:
- Concurrent policy: SERIALIZE / LATEST_WINS / QUEUE / KEYED_CONCURRENT / LIBRARY_OWNS
- Duplicate optimistic state excluded:

## Partial Data

- Applicable:
- Atomic vs independent sections:
- Application partial result:
- Server-state independent queries:
- Section state type:
- Giant optional bag avoided:
- Aggregate page condition derived:

## Multiple Operations

| Operation | Owner | State |
|---|---|---|
| query/load | | |
| mutation/save | | |
| upload | | |
| secondary action | | |

- One global busy status avoided:

## Server-State Integration

- Library/profile:
- Strategy: DIRECT_LIBRARY_STATE / THIN_FEATURE_SEMANTIC_WRAPPER / APPLICATION_RESULT_PLUS_LIBRARY_STATE
- Library-owned data:
- Library-owned loading/error:
- Library-owned refresh/stale:
- Local semantic additions:
- Data copied to local state:
- Sync Effect avoided:

## State Update Mechanism

- Multiple `useState`:
- Grouped state:
- `useReducer`:
- Why:
- Atomic transitions:
- Reducer events semantic:
- Raw setter public API avoided:

## Accessibility Mapping

- Loading announcement:
- Refresh announcement:
- Error recovery:
- Optimistic rollback communication:
- Focus behavior delegated to Presentation:

## Test Matrix

| Scenario | Initial | Event | Expected state |
|---|---|---|---|
| initial load | | | |
| success | | | |
| error | | | |
| background refresh | | | |
| refresh failure | | | |
| retry | | | |
| cancellation | | | |
| optimistic apply | | | |
| optimistic rollback | | | |
| partial data | | | |
| key change | | | |
| stale response | | | |

- Internal setters not asserted:
- Abort/request counters not asserted:
- Pure reducer test justified:
- Hook/component test boundary:

## Overmodeling Audit

- Unobservable idle:
- Stale mirrors library internals:
- Retrying identical to loading:
- Cancelled never rendered:
- Optimistic duplicates cache:
- Generic AsyncState forced globally:
- Giant page status:
- Derived booleans stored:
- Server state copied through Effect:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
