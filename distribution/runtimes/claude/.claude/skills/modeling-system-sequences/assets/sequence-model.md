# Sequence Model

## Document Control

- Product/system:
- Initiative:
- Model version:
- Status:
- Source C4 model:
- Source ADR(s):
- Source use cases/process/state:
- Owner:
- Date:
- Applicable `AGENTS.md`:

## Scenario Inventory

| Sequence ID | Scenario | Status | Why sequence modeling is useful |
|---|---|---|---|
| SEQ-001 | | | |

## Participant Catalog

| Participant | Type | Architecture source | Responsibility in scenario |
|---|---|---|---|
| | actor/client/container/component/store/provider | | |

# SEQ-001 — [Scenario]

- Status:
- Quality status:
- Trigger:
- Success outcome:
- Source use case:
- Source FRs:
- Source process flow:
- Source state transition:
- Source quality scenario:
- Source ADR/C4:
- Open questions:

## Happy Path

```mermaid
sequenceDiagram
    actor Actor
    participant System
    Actor->>System: Initiating interaction
    System-->>Actor: Observable success outcome
```

## Important Alternatives

### Alternative A — [Condition]

- Guard/condition:
- Interaction difference:
- Outcome:
- Source:

```mermaid
sequenceDiagram
    ...
```

## Failure / Degraded Paths

### Failure F1 — [Failure]

- Trigger/failure:
- Who observes it:
- Response/fallback:
- Terminal/rejoin outcome:
- Source/gap:

## Authorization

| Protected interaction | Authoritative authorization point | Tenant/resource scope | Source |
|---|---|---|---|
| | | | |

## Retry Semantics

| Interaction | Retry owner | Condition | Limit/deadline | Terminal outcome | Source/gap |
|---|---|---|---|---|---|
| | | | | | RETRY_POLICY_REQUIRED / defined |

## Timeout Semantics

| Interaction | Observer | Timeout | Outcome/fallback | Source/gap |
|---|---|---|---|---|
| | | | | TIMEOUT_POLICY_REQUIRED / defined |

## Concurrency / Race Scenarios

| Scenario | Concurrent interactions | Required semantic result | Gap |
|---|---|---|---|
| | | | CONCURRENCY_POLICY_REQUIRED / defined |

## Idempotency / Duplicate / Ordering

| Interaction/event | Duplicate behavior | Out-of-order behavior | Late behavior | Source/gap |
|---|---|---|---|---|
| | | | | IDEMPOTENCY_POLICY_REQUIRED / EVENT_ORDERING_POLICY_REQUIRED / defined |

## Interaction Ordering Decisions

| Order-sensitive step | Why order matters | Accepted order | Gap |
|---|---|---|---|
| | | | INTERACTION_ORDER_DECISION_REQUIRED / defined |

## Coverage Matrix

| Use Case / FR / QA | Sequence | Coverage |
|---|---|---|
| | | COVERED / PARTIALLY_COVERED / NO_SEQUENCE_NEEDED / MISSING_SEQUENCE / BLOCKED_BY_INTERACTION_DECISION |

## Traceability

| Sequence element | FR | UC | Process | State | QA | ADR/C4 |
|---|---|---|---|---|---|---|
| | | | | | | |

## Alignment Audits

### Architecture / C4
- Unmodeled participants:
- Abstraction mismatches:
- ADR/C4 conflicts:

### Process / Business Rules
- Ordering conflicts:
- Branch/rule conflicts:

### State Machine
- Illegal transition implied:
- Missing state precondition:

### Authorization
- Frontend-only authorization:
- Missing tenant/resource scope:
- Missing authoritative authorization:

### Failure / Retry / Timeout
- Unsupported retry:
- Unsupported timeout:
- Undefined failure:
- Hidden infinite retry:

### Idempotency / Concurrency
- Unproven idempotency:
- Duplicate semantics unknown:
- Concurrency policy gaps:
- Ordering policy gaps:

## Downstream Handoffs

### Data Flow / STRIDE
- Sensitive relationships:
- Third-party transfers:
- Trust-boundary interactions:

### Event Flow
- Events needing detailed producer/consumer/delivery modeling:

### Deployment
- Latency/failure/topology questions deferred:

### Architecture Validation
- Sequence scenarios to validate:

## Gap Ledger

| ID | Sequence | Gap | Type | Owner |
|---|---|---|---|---|
| | | | PARTICIPANT_DECISION_REQUIRED / INTERACTION_ORDER_DECISION_REQUIRED / FAILURE_SEMANTICS_REQUIRED / RETRY_POLICY_REQUIRED / TIMEOUT_POLICY_REQUIRED / AUTHORIZATION_CLARIFICATION_REQUIRED / IDEMPOTENCY_POLICY_REQUIRED / CONCURRENCY_POLICY_REQUIRED / EVENT_ORDERING_POLICY_REQUIRED / C4_ALIGNMENT_REQUIRED | |

## Final Decision

- Decision: SEQUENCE_MODEL_READY / SEQUENCE_MODEL_READY_WITH_OPEN_QUESTIONS / SEQUENCE_MODEL_REQUIRES_PARTICIPANT_DECISION / SEQUENCE_MODEL_REQUIRES_INTERACTION_ORDER / SEQUENCE_MODEL_REQUIRES_FAILURE_SEMANTICS / SEQUENCE_MODEL_REQUIRES_RETRY_POLICY / SEQUENCE_MODEL_REQUIRES_TIMEOUT_POLICY / SEQUENCE_MODEL_REQUIRES_AUTHORIZATION_CLARIFICATION / SEQUENCE_MODEL_REQUIRES_IDEMPOTENCY_POLICY / SEQUENCE_MODEL_REQUIRES_CONCURRENCY_POLICY / SEQUENCE_MODEL_REQUIRES_ARCHITECTURE_ALIGNMENT / SEQUENCE_MODEL_CONFLICTED / BLOCKED
- Blocking interaction decisions:
- Failure/retry/timeout gaps:
- Authorization gaps:
- Idempotency/concurrency gaps:
- Architecture alignment gaps:
- Ready for downstream models:
