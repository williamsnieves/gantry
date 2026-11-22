# React Effect Design Record

## Context

- Change/slice:
- Effect candidate:
- Repository/application:
- Owning capability:
- Component/hook:
- React/Strict Mode:
- Rendering model:
- Approved server-state strategy:
- Applicable `AGENTS.md`:
- Designed by/date:

## Readiness

- Proposed behavior:
- External system:
- Trigger:
- Resource identity:
- Owner:
- Initial decision:
- Conditions/blockers:

## Effect Necessity Analysis

| Question | Answer/evidence |
|---|---|
| External system exists | |
| Can derive during render | |
| Can run from event handler | |
| Server-state library owns it | |
| External-store API fits | |
| Lifecycle synchronization required | |

- Decision:
- Alternative selected/rejected:
- Why an Effect is or is not required:

## Synchronization Classification

- Type:
- Trigger semantics:
- Placement:
- Current owner:
- Proposed owner:
- Why component/hook/library/adapter owns it:

## Lifecycle Contract

### Setup

- External call:
- Inputs:
- Resource/handle created:
- Failure behavior:
- Idempotency:

### Update or Resubscribe

- Changes requiring update:
- Recreate versus update:
- Ordering:
- Previous resource handling:

### Cleanup

- Unsubscribe/destroy/cancel:
- Exact resource:
- Multiple-call safety:
- State updates excluded:
- Leak risk:

## Dependency Inventory

| Value | Read by Effect | Classification | Change semantics |
|---|---|---|---|
| | | REACTIVE_DEPENDENCY/STABLE_BY_CONTRACT/NON_REACTIVE_REF/MODULE_CONSTANT/EXTERNAL_MUTABLE_SOURCE | resubscribe/update/latest-only/not-applicable |

- Exhaustive-deps status:
- Suppression removed:
- Effect split required:
- Object/function identity decision:

## Stale Closure Design

- Values requiring latest version:
- Values defining subscription identity:
- Strategy: RESUBSCRIBE_ON_CHANGE / LATEST_VALUE_VIA_REF / EVENT_CALLBACK_BOUNDARY / STABLE_VALUE_BY_CONTRACT / NOT_APPLICABLE
- Why refs do or do not fit:
- Hidden dependency risk:

## Strict Mode and Idempotency

- Setup → cleanup → setup safe:
- Duplicate listener/timer/widget risk:
- Irreversible side effect:
- Deduplication owner:
- Development analytics behavior:

## SSR and Hydration

- Runs on server:
- Browser-only API:
- Client boundary:
- Initial markup:
- Hydration consistency:
- Layout shift:
- Client-only placeholder:

## Async, Races, and Cancellation

- Async work:
- Concurrency possible:
- Strategy: LATEST_RESOURCE_WINS / EACH_RESOURCE_INDEPENDENT / CANCEL_PREVIOUS / IGNORE_STALE_RESULT / LIBRARY_OWNS / NOT_APPLICABLE
- Request/resource identity:
- Abort/cancel:
- Stale result:
- Unmount:
- External side-effect ambiguity:
- Retry owner:

## Common-Case Classification

### Fetching

- Raw Effect fetch:
- Approved library alternative:
- Cache/deduplication/retry:
- Route/resource change:
- Decision:

### Subscription

- Key:
- Initial snapshot:
- Unsubscribe:
- Reconnect/error:
- External-store alternative:

### Analytics

- Type:
- Event/lifecycle owner:
- Once semantics:
- Consent/redaction:
- Strict Mode behavior:

### Debounce or Timer

- Type:
- Delay/interval:
- Leading/trailing:
- Reset/cancel/flush:
- Latest callback:
- Fake-timer test:

## Third-Party or DOM Integration

- Widget/DOM API:
- Host node:
- Create:
- Update:
- Destroy:
- Instance ref:
- Accessibility:
- SSR:
- Memory leak risk:

## Storage Synchronization

- Initial read:
- Writes:
- Cross-tab:
- Schema/version:
- Parse/error:
- Privacy:
- Source of truth:

## Error Handling

| Failure | User-visible | Retry/log/escalation | Owner |
|---|---|---|---|
| | | | |

- Error-boundary assumptions:
- Technical details/redaction:

## Memoization and Refs

| Value | Mechanism | Semantic reason |
|---|---|---|
| | useMemo/useCallback/ref/none | |

- Mechanical memoization excluded:
- Non-reactive mutable state justified:

## Test Strategy

| Behavior | Test/evidence |
|---|---|
| Setup | |
| Dependency update/resubscribe | |
| Cleanup/unmount | |
| Strict Mode lifecycle | |
| External event | |
| Timer/debounce | |
| Race/stale result | |
| Cancellation | |
| Analytics trigger | |
| Widget create/update/destroy | |

- React internals excluded:
- Deterministic fakes:
- Leak/open-handle evidence:

## Decisions and Risks

| Question/risk | Owner | Blocking |
|---|---|---|
| | | |

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
