# Event Flow Model

## Document Control

- Product/system:
- Initiative:
- Model version:
- Status:
- Source ADR(s):
- Source C4:
- Source sequence model:
- Source state/domain/DFD:
- Owner:
- Date:
- Applicable `AGENTS.md`:

## Event-Flow Scope

- System/scenario:
- Why event/asynchronous modeling is required:
- Accepted event interaction evidence:
- Included:
- Excluded:

## Producer / Consumer Catalog

| ID | Participant | Role | C4 mapping | Owner | Source |
|---|---|---|---|---|---|
| P-001 | | PRODUCER / CONSUMER / BOTH | | | |

## Event Catalog

| Event ID | Event | Meaning/fact | Producer | Consumer(s) | Purpose | Status | Contract owner |
|---|---|---|---|---|---|---|---|
| EVT-001 | | | | | | | |

## Event Semantic Contract

### EVT-001 — [Event]

- Meaning:
- Trigger/business fact:
- Producer:
- Consumers:
- Semantic owner:
- Contract owner:
- Required semantic data:
- Optional semantic data:
- Data classification reference:
- External/provider identifiers:
- Correlation/causation needs:
- Schema technology:
- Version:
- Source:

## Delivery Semantics

| Event | Requirement | Evidence | Gap |
|---|---|---|---|
| | at-most-once / at-least-once / exactly-once-effect / best-effort / provider-defined / TBD | | DELIVERY_SEMANTICS_REQUIRED / defined |

## Ordering

| Event | Ordering scope | Why order matters | Late behavior | Out-of-order behavior | Source/gap |
|---|---|---|---|---|---|
| | GLOBAL / PER_ENTITY / PER_TENANT / PER_STREAM / NONE / UNKNOWN | | | | |

## Retry Policy

| Event/consumer | Retry owner | Eligible failure | Attempts/deadline | Backoff | Terminal outcome | Source/gap |
|---|---|---|---|---|---|---|
| | producer/transport/consumer/provider | | | | | RETRY_POLICY_REQUIRED / defined |

## Deduplication / Idempotency

| Event/consumer | Duplicate possible? | Dedup needed? | Idempotent effect required? | Identity basis | Source/gap |
|---|---|---|---|---|---|
| | | | | | DEDUPLICATION_POLICY_REQUIRED / IDEMPOTENCY_POLICY_REQUIRED / defined |

## Dead-Letter / Permanent Failure

| Event/consumer | Permanent-failure behavior | Manual intervention | Reprocess/replay | Source/gap |
|---|---|---|---|---|
| | | | | DEAD_LETTER_BEHAVIOR_REQUIRED / defined |

## Schema / Versioning

| Event | Current contract/version | Evolution policy | Backward compatibility | Breaking-change policy | Source/gap |
|---|---|---|---|---|---|
| | | | | | EVENT_VERSIONING_POLICY_REQUIRED / defined |

## Event Emission / State Consistency

| Event | Authoritative state/action | When event becomes valid | Atomicity/dual-write concern | Source/gap |
|---|---|---|---|---|
| | | | | EVENT_EMISSION_ORDER_REQUIRED / defined |

## Event Flow Diagram

```text
[Version-controlled event-flow diagram source]
```

## Fan-Out / Fan-In / Choreography

### Fan-Out
- Events with multiple independent consumers:
- Consumer independence assumptions:

### Fan-In
- Consumers correlating multiple events:
- Ordering/correlation questions:

### Choreography
- Multi-event workflow:
- Cycle/feedback-loop risk:

## Replay / Retention / Lag / Backpressure

- Replay required:
- Replay authority:
- Event retention:
- Consumer lag target:
- Backpressure concern:
- Policy gaps:

## Alignment Audits

### C4 / ADR
- Unmodeled producers:
- Unmodeled consumers:
- Architecture conflict:

### State Machine
- Event from illegal/unaccepted state transition:
- Missing state precondition:

### Domain Data
- Unknown/new canonical concept introduced:
- Identifier mismatch:
- Ownership mismatch:

### DFD / Privacy
- Sensitive data copied into events:
- Third-party trust crossing:
- Classification mismatch:
- Secret exposure:

### Sequence
- Interaction pattern conflict:
- Timing/order contradiction:

## Risk Audits

- Event cycles:
- Retry amplification/storm:
- Poison/permanent-failure path:
- Duplicate side-effect risk:
- Ordering assumption conflict:
- Schema drift:
- Consumer compatibility:
- Orphan events:
- Orphan consumers:

## Traceability

| Event/flow | FR | UC/process | State transition | Domain concept | QA/NFR | ADR/C4 |
|---|---|---|---|---|---|---|
| | | | | | | |

## Downstream Handoffs

### Deployment Architecture
- Messaging infrastructure placement:
- Capacity/consumer scaling:
- Multi-zone/region questions:
- Network/trust topology:

### Security / STRIDE
- External event entry points:
- Trust-boundary events:
- Sensitive event data:
- Spoofing/tampering/replay concerns to assess:

### Architecture Validation
- Delivery guarantees to verify:
- Ordering/idempotency tests:
- Retry/dead-letter tests:
- Version-compatibility tests:
- Consumer-independence tests:

## Gap Ledger

| ID | Event/flow | Gap | Type | Owner |
|---|---|---|---|---|
| | | | EVENT_INTERACTION_DECISION_REQUIRED / DELIVERY_SEMANTICS_REQUIRED / ORDERING_REQUIREMENT_REQUIRED / RETRY_POLICY_REQUIRED / DEDUPLICATION_POLICY_REQUIRED / IDEMPOTENCY_POLICY_REQUIRED / DEAD_LETTER_BEHAVIOR_REQUIRED / EVENT_VERSIONING_POLICY_REQUIRED / EVENT_OWNERSHIP_REQUIRED / EVENT_EMISSION_ORDER_REQUIRED / EVENT_C4_ALIGNMENT_REQUIRED | |

## Final Decision

- Decision: EVENT_FLOW_MODEL_READY / EVENT_FLOW_MODEL_READY_WITH_OPEN_QUESTIONS / EVENT_FLOW_MODEL_REQUIRES_EVENT_INTERACTION_DECISION / EVENT_FLOW_MODEL_REQUIRES_DELIVERY_SEMANTICS / EVENT_FLOW_MODEL_REQUIRES_ORDERING_REQUIREMENT / EVENT_FLOW_MODEL_REQUIRES_RETRY_POLICY / EVENT_FLOW_MODEL_REQUIRES_DEDUPLICATION_POLICY / EVENT_FLOW_MODEL_REQUIRES_DEAD_LETTER_BEHAVIOR / EVENT_FLOW_MODEL_REQUIRES_VERSIONING_POLICY / EVENT_FLOW_MODEL_REQUIRES_EVENT_OWNERSHIP / EVENT_FLOW_MODEL_REQUIRES_ARCHITECTURE_ALIGNMENT / EVENT_FLOW_MODEL_CONFLICTED / BLOCKED
- Blocking delivery/order gaps:
- Retry/dedup/dead-letter gaps:
- Versioning/ownership gaps:
- Architecture/alignment conflicts:
- Ready for `modeling-deployment-architecture`:
