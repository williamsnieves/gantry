# React Custom Hook Design Record

## Context

- Change/slice:
- Hook candidate:
- Repository/application:
- Owning capability:
- Architecture profile:
- Component design record:
- Approved server-state strategy:
- React/compiler configuration:
- Applicable `AGENTS.md`:
- Designed by/date:

## Readiness

- Accepted behavior:
- Consumers:
- State owner:
- Dependencies:
- Async behavior:
- Effect need:
- Initial decision:
- Conditions/blockers:

## Hook Necessity

- Decision:
- Reusable React responsibility:
- Why component-local state is insufficient or preferable:
- Why plain function is insufficient or preferable:
- Why Application Use Case is insufficient or preferable:
- Existing hook reuse:
- One-consumer justification:

## Responsibility Boundary

| Responsibility | Hook owns | Other owner |
|---|---|---|
| React state | | |
| User command wiring | | |
| Application orchestration | | |
| Business rules | | |
| Data mapping | | |
| Server-state integration | | |
| Browser synchronization | | |
| Error mapping | | |
| Cache invalidation | | |
| Dependency composition | | |

## Dependency Injection

| Dependency | Abstraction | Injection mechanism | Lifecycle/identity |
|---|---|---|---|
| | | EXPLICIT_PARAMETER_INJECTION/FEATURE_CONTEXT_INJECTION/COMPOSED_HOOK_FACTORY/APPROVED_LIBRARY_PROVIDER/NO_REPLACEABLE_DEPENDENCY | |

- Concrete adapters excluded:
- Global Factory excluded:
- Service Locator excluded:
- Hidden globals excluded:
- Composition owner:

## Hook Parameters

| Parameter | Type/shape | Meaning | Identity significance |
|---|---|---|---|
| | | | |

- Large option bags rejected:
- Defaults:
- Enabled/disabled behavior:

## State Inventory

| State/value | Classification | Source of truth | Derived/owned |
|---|---|---|---|
| | EPHEMERAL_UI_STATE/FORM_STATE/ASYNC_OPERATION_STATE/SERVER_STATE_DERIVATION/OPTIMISTIC_STATE/BROWSER_SYNCHRONIZATION_STATE/SELECTION_STATE/TRANSITION_STATE/ERROR_STATE | | |

## State Representation Decision

- Selection: multiple useState / grouped state / discriminated union / useReducer / library-owned state
- Rationale:
- Values evolving independently:
- Fields transitioning atomically:
- Invalid combinations prevented:
- Functional updates required:
- Reducer purity:

## State Model

```text

```

## Transition Table

| Current state | Event/command | Next state | Side effect owner | Invalid behavior |
|---|---|---|---|---|
| | | | | |

## Commands

| Command | Parameters | Preconditions | Duplicate behavior | Result/error ownership |
|---|---|---|---|---|
| | | | | |

- Raw setters exposed:
- Reset behavior:
- Error-clearing behavior:
- Cancellation command:

## Return API

- Shape: OBJECT_API / TUPLE_API / SINGLE_VALUE / COMMAND_ONLY
- Contract:

```text

```

- Stable semantics:
- Internal details excluded:
- Destructuring:
- Evolution considerations:

## Async Lifecycle

- Start:
- Pending:
- Success:
- Semantic failure:
- System failure:
- Cancellation:
- Retry:
- Unmount:
- Previous data retention:
- Cache update/invalidation:
- Command result:

## Race and Stale-Response Strategy

- Concurrency possible:
- Strategy: LATEST_REQUEST_WINS / FIRST_REQUEST_WINS / CONCURRENT_REQUESTS_ALLOWED_BY_KEY / DUPLICATE_COMMAND_REJECTED / QUEUE_COMMANDS / LIBRARY_OWNS_RACE_HANDLING / NOT_APPLICABLE
- Request identity:
- Abort behavior:
- Out-of-order response handling:
- Mounted/unmounted behavior:
- Ambiguous server mutation risk:

## Effect Design

| Synchronization | Effect required | Owner | Dependencies | Cleanup |
|---|---|---|---|---|
| | | hook/component/library/adapter | | |

- Pure derivations excluded:
- Event-driven operations excluded from Effects:
- Exhaustive-deps status:
- Detailed effect skill required:

## Server-State Integration

- Library/strategy:
- Query/mutation key ownership:
- Feature-semantic wrapper value:
- Library state mapped:
- Cache behavior:
- Deduplication:
- Retry:
- Cancellation:
- Invalidation:
- Library internals not rebuilt:
- Wrapper decision:

## Error Model

| Error | Source | Hook-exposed meaning | Clear condition |
|---|---|---|---|
| | | VALIDATION_ERROR/SEMANTIC_ERROR/FORBIDDEN/NOT_FOUND/UNAVAILABLE/CANCELLED/UNKNOWN | |

- HTTP/SDK details excluded:
- Mapping owner:
- Announcement owner:

## Context and Composition

- Context consumed:
- Provider scope:
- Value stability:
- Missing-provider behavior:
- Broad services context rejected:
- Hook composition boundary status:

## Memoization and Identity

| Value/function | Stable identity required | Reason | Mechanism |
|---|---|---|---|
| | | semantic/performance/integration/compiler | |

- Mechanical memoization excluded:
- React Compiler considerations:
- Nested functions retained/extracted:

## Consumer Contract

| Consumer | Uses state | Uses commands | Coupling risk |
|---|---|---|---|
| | | | |

## Test Boundary

| Behavior | Hook test | Pure function/reducer test | Component/E2E evidence |
|---|---|---|---|
| Initial state | | | |
| Commands/transitions | | | |
| Async success | | | |
| Semantic/system failure | | | |
| Cancellation | | | |
| Stale response/race | | | |
| Duplicate command | | | |
| Retry/reset | | | |
| Cleanup | | | |
| Server-state integration | | | |

- Library internals excluded:
- Fake timers/network control:
- Determinism:

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
