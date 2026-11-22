# React Hook Test Implementation Record

## Context

- Change/hook:
- Repository/application:
- Hook design record:
- Test strategy record:
- Test stack/harness:
- Server-state strategy:
- Applicable `AGENTS.md`:
- Implemented by/date:

## Readiness

- Public hook contract:
- Independent-test justification:
- Dependencies:
- Async policy:
- Race policy:
- Cancellation policy:
- Optimistic policy:
- Initial decision:
- Conditions/blockers:

## Public Contract

| Surface | Type/shape | Meaning |
|---|---|---|
| Input | | |
| State/data | | |
| Error | | |
| Command | | |
| Derived flag | | |

- Internal details intentionally excluded:

## State Transition Matrix

| Current state | Command/event | Controlled dependency outcome | Expected public state |
|---|---|---|---|
| | | | |

## Test Doubles

| Dependency | Double | Scope | Why |
|---|---|---|---|
| | fake/stub/spy/InMemory/MSW/virtual clock | per test/suite | |

- Concrete adapters excluded:
- Global Factory excluded:
- Shared mutable fake excluded:

## Async Success

- Command:
- Pending assertion:
- Controlled resolve:
- Success assertion:
- Previous data retention:
- Error clearing:

## Failure and Recovery

| Failure | Public state/error | Recovery command | Expected next state |
|---|---|---|---|
| | | | |

## Retry / Reset

- Retry availability:
- Retry input:
- Call count semantics:
- Error clearing:
- Reset semantics:
- Active operation behavior:

## Cancellation

- Trigger:
- Observable dependency evidence:
- Public cancelled/idle state:
- Late completion behavior:
- System-error distinction:
- Unmount behavior:

## Race / Stale Response

### Scenario

```text
A starts
B starts
B resolves
A resolves
```

- Accepted policy:
- Public assertion after B:
- Public assertion after A:
- Internal sequence/ref assertions excluded:

## Duplicate Commands

- Scenario:
- Accepted behavior:
- Observable evidence:
- Dependency-call evidence:

## Optimistic Update

- Accepted:
- Previous state:
- Optimistic state:
- Authoritative success:
- Failure rollback:
- Concurrent optimistic behavior:
- Library ownership:

## Cleanup / Subscription

| Resource | Setup trigger | Observable cleanup | Rerender behavior |
|---|---|---|---|
| | | | |

- Effect-count assertion excluded:
- Late-event behavior:

## Dependency Injection

- Injection mechanism:
- Semantic dependency:
- Inputs asserted:
- Call order required:
- Use Case branches intentionally excluded:
- Adapter branches intentionally excluded:

## Server-State Wrapper

- Wrapper value:
- Public feature semantics:
- Cache/provider isolation:
- Representative handler/data:
- Library internals intentionally excluded:
- Direct library usage would be sufficient:

## Timer / Debounce

- Timer behavior:
- Virtual timer:
- Delay:
- Leading/trailing:
- Latest value:
- Cancel/unmount:
- Generic async timer flushing excluded:

## Rerender / Input Changes

| Input change | Expected transition | Race implication |
|---|---|---|
| | | |

## Anti-Brittleness Review

- Setter assertions:
- Reducer action assertions:
- Effect-count assertions:
- Ref assertions:
- `useMemo`/`useCallback` assertions:
- Callback identity assertions:
- Internal server-state fields:
- Raw HTTP/provider error assertions:
- Sleeps:

## Isolation

- Render cleanup:
- Deferred promises:
- Timers:
- Cache/provider:
- MSW handlers:
- Storage/subscriptions:
- Pending work:

## Regression Coverage

| Defect/risk | Smallest deterministic hook test |
|---|---|
| | |

## Escalation

| Behavior | Correct boundary |
|---|---|
| | HOOK_TEST_SUFFICIENT/COMPONENT_TEST_REQUIRED/ADAPTER_TEST_REQUIRED/USE_CASE_TEST_REQUIRED/ROUTE_OR_E2E_REQUIRED/REAL_BROWSER_REQUIRED/MANUAL_AT_REQUIRED |

## Test Evidence

| Test/check | Result |
|---|---|
| Focused hook suite | |
| Typecheck/lint if applicable | |
| Cleanup/open handles | |

## Residual Risks

| Risk/gap | Status | Owner |
|---|---|---|
| | | |

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
