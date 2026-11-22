---
name: modeling-event-flows
description: Portable engineering capability `modeling-event-flows`. Use when the
  harness or a specialist agent explicitly requires this named capability.
---
# Modeling Event Flows

## Purpose

Model event-driven/asynchronous interactions explicitly and safely.

Canonical structure:

```text
producer
→ event
→ consumer
```

with explicit semantics for:

```text
ownership
delivery
ordering
retries
deduplication
dead-letter behavior
schema/versioning
failure handling
```

Output:

```text
event-flow-model.md
```

# Core Principle

An event-flow model answers:

```text
who produces the event?
what business/system fact does the event represent?
who consumes it?
who owns the contract?
what delivery semantics are required?
what ordering matters?
what happens on retry/duplicate/failure?
how is the contract versioned?
```

It does not automatically imply:

```text
Kafka
RabbitMQ
SNS/SQS
Pub/Sub
exactly-once delivery
dead-letter queue
event sourcing
CQRS
schema registry
```

# Use When

- Accepted architecture contains asynchronous/event-driven interaction.
- A provider emits events/callbacks whose semantics matter.
- Internal architectural events decouple capabilities.
- Consumers may process the same event independently.
- Delivery, ordering, duplicate, retry, replay, or failure behavior matters.
- Domain/state transitions produce events that other components react to.
- Architecture validation needs explicit event contracts and ownership.
- DFD/sequence models identify an asynchronous flow that needs deeper semantics.

# Do Not Use When

- Architecture does not actually include events/asynchronous behavior.
- The flow is simply synchronous request/response.
- The task is message order in one scenario; use `modeling-system-sequences`.
- The task is lifecycle/state modeling; use `modeling-state-machines`.
- The task is data movement/trust boundaries; use `modeling-data-flows`.
- The task is infrastructure selection/configuration for a broker.
- The task is API schema design rather than event semantics.

# Inputs

Preferred:

- ADRs;
- C4 architecture model;
- sequence models;
- state-machine model;
- domain-data model;
- DFD;
- functional requirements;
- NFR/quality scenarios;
- accepted provider/event contracts;
- accepted delivery/retry/idempotency semantics;
- applicable `AGENTS.md`.

Optional:

- existing event catalog;
- event schemas;
- provider docs;
- runtime traces;
- dead-letter/runbook docs;
- event version history;
- brownfield messaging topology.

# Outputs

- Event Flow Model.
- Event catalog.
- Producer/consumer catalog.
- Ownership matrix.
- Delivery-semantics matrix.
- Ordering requirements.
- Retry/deduplication/dead-letter policy ledger.
- Schema/versioning record.
- Failure/recovery/replay notes.
- Traceability to FRs/state/sequence/C4/ADR.
- Gaps and downstream validation/deployment handoffs.

# Event Identity

Use stable IDs:

```text
EVT-001
EVT-002
```

# Flow Identity

Use:

```text
EF-001
EF-002
```

# Event Status

Use:

```text
PROPOSED
REVIEW_REQUIRED
ACCEPTED
DEPRECATED
SUPERSEDED
```

# Step 1 — Establish Event-Flow Scope

Record:

```text
system/scenario
architecture version / ADR basis
why asynchronous modeling is required
which events/flows are in scope
which are out of scope
```

Do not introduce events just because they could be useful.

# Step 2 — Verify Event-Driven Architecture Evidence

Before creating a flow ask:

```text
Is asynchronous/event interaction accepted?
```

Evidence may be:

```text
ADR
C4 relationship
provider contract
sequence model
state transition contract
existing architecture
```

If no:

```text
EVENT_INTERACTION_DECISION_REQUIRED
```

Do not invent a broker/event.

# Step 3 — Define the Producer

Producer is the party that emits/publishes the event.

Examples:

```text
Support Application
Email Provider
Payment Provider
Order capability
Deployment pipeline
```

Producer should be an accepted architectural/external participant.

# Step 4 — Define the Event

Event should describe a fact that happened.

Good:

```text
ConversationResolved
InboundMessageAccepted
PrivilegedReassignmentRecorded
PaymentCaptured
```

Bad:

```text
ResolveConversationCommand
DoTheThing
UpdateMessage
```

unless command/event distinction is intentionally in scope.

# Step 5 — Event Fact Semantics

An event should be phrased as:

```text
past-tense fact
```

when it represents something that has occurred.

Do not call a request/command an event by default.

# Step 6 — Define Consumers

Consumers react to the event.

Examples:

```text
Audit/Operations capability
Notification capability
Analytics consumer
External partner
```

Only model accepted consumers.

# Step 7 — Consumer Independence

If several consumers are independent:

```text
record each separately
```

Do not imply ordering among consumers unless required.

# Step 8 — Event Ownership

Roadmap-required.

Record:

```text
semantic owner
contract owner
producer owner
consumer owner(s)
```

where known.

Do not assume broker/platform team owns business semantics.

# Step 9 — Contract Ownership

A useful default distinction:

```text
domain/business capability owns event meaning
platform/infrastructure may own transport
```

only if organization architecture supports it.

If unclear:

```text
EVENT_OWNERSHIP_REQUIRED
```

# Step 10 — Event Purpose

Every event needs a clear reason to exist.

Examples:

```text
allow audit consumer to record privileged action
notify downstream capability that conversation is resolved
notify ingestion diagnostics of accepted provider message
```

Avoid “for decoupling” as the only purpose.

# Step 11 — Delivery Semantics

Roadmap-required.

Possible requirements:

```text
at-most-once
at-least-once
exactly-once effect
best effort
provider-defined
TBD
```

Important distinction:

```text
exactly-once delivery
≠
exactly-once business effect
```

Do not claim either without evidence.

# Step 12 — Delivery Semantics Gap

If not accepted:

```text
DELIVERY_SEMANTICS_REQUIRED
```

# Step 13 — Acknowledgement Semantics

Only model:

```text
ack
nack
visibility timeout
commit
```

if transport/contract explicitly requires it.

Do not invent broker semantics.

# Step 14 — Ordering

Roadmap-required.

Ask:

```text
Does event order matter globally?
per aggregate/entity?
per tenant?
per external key?
not at all?
```

Do not invent partition-key strategy.

# Step 15 — Ordering Scope

Possible:

```text
GLOBAL
PER_ENTITY
PER_TENANT
PER_STREAM
NONE
UNKNOWN
```

Use only supported semantics.

# Step 16 — Ordering Gap

Use:

```text
ORDERING_REQUIREMENT_REQUIRED
```

# Step 17 — Late Events

If event may arrive after newer state:

```text
define accepted semantic response
```

Otherwise:

```text
LATE_EVENT_POLICY_REQUIRED
```

# Step 18 — Out-of-Order Events

Do not assume reordering buffer.

If behavior unknown:

```text
OUT_OF_ORDER_POLICY_REQUIRED
```

# Step 19 — Retries

Roadmap-required.

Retries must specify, when known:

```text
retry owner
failure condition
retry eligibility
attempt/deadline
backoff
terminal outcome
```

Do not invent counts/timing.

# Step 20 — Retry Ownership

Distinguish:

```text
producer retry
transport retry
consumer retry
provider retry
```

Do not blur responsibilities.

# Step 21 — Retry Gap

Use:

```text
RETRY_POLICY_REQUIRED
```

# Step 22 — Poison Messages / Permanent Failure

If consumer permanently cannot process an event:

```text
define accepted terminal handling
```

if known.

Do not assume DLQ.

# Step 23 — Dead-Letter Behavior

Roadmap-required.

Possible:

```text
dead-letter queue
manual review
drop/reject
quarantine
provider-defined
TBD
```

Only choose if accepted.

If unresolved:

```text
DEAD_LETTER_BEHAVIOR_REQUIRED
```

# Step 24 — Dead Letter != Required Queue

The roadmap asks for dead-letter behavior, not necessarily a DLQ.

Behavior can be:

```text
manual intervention
quarantine
rejection
provider recovery
```

depending on architecture.

# Step 25 — Deduplication

Roadmap-required.

Ask:

```text
Can duplicate delivery occur?
Does duplicate processing cause harmful effect?
Where should semantic deduplication happen?
What identity supports detection?
```

Do not invent dedup keys.

# Step 26 — Deduplication vs Idempotency

Distinguish:

```text
deduplication
→ identify/reject repeated event

idempotent consumer/business effect
→ repeated handling has same business outcome
```

Either may be used, both, or neither.

Do not assume.

# Step 27 — Deduplication Gap

Use:

```text
DEDUPLICATION_POLICY_REQUIRED
```

# Step 28 — Idempotency Gap

Use:

```text
IDEMPOTENCY_POLICY_REQUIRED
```

# Step 29 — Event Identity

An event may need:

```text
event ID
business/entity ID
provider event ID
correlation ID
causation ID
```

Only record semantics if required/evidenced.

Do not invent UUIDs.

# Step 30 — Correlation / Causation

Use when tracing workflows matters.

Do not force every event to have both.

# Step 31 — Event Schema

Roadmap-required.

Model semantic contract fields/categories only when known.

Do not invent exact payload.

At minimum:

```text
event name
event meaning
required semantic data
optional semantic data
metadata needs
```

# Step 32 — Schema Detail

Avoid:

```text
JSON Schema
Avro
Protobuf
```

unless selected.

Keep:

```text
schema technology: TBD
```

# Step 33 — Schema Versioning

Roadmap-required.

Record accepted strategy when known:

```text
backward compatible evolution
new event version
parallel versions
provider-defined
TBD
```

Do not invent semver.

# Step 34 — Version Compatibility

Ask:

```text
Can older consumers continue?
Can producer deploy independently?
Can fields be added?
Can meaning change?
```

Do not answer without policy/evidence.

# Step 35 — Schema Versioning Gap

Use:

```text
EVENT_VERSIONING_POLICY_REQUIRED
```

# Step 36 — Breaking Change

A semantic breaking change should not silently reuse the same event contract.

Flag:

```text
BREAKING_EVENT_CHANGE_REQUIRES_DECISION
```

# Step 37 — Event Immutability

Events generally represent historical facts, but do not assume event-store immutability or event sourcing.

# Step 38 — Event Sourcing Boundary

Event-driven architecture does NOT imply event sourcing.

Do not create:

```text
event store
aggregate replay
event-sourced persistence
```

unless accepted.

# Step 39 — CQRS Boundary

Events do not imply CQRS.

# Step 40 — Broker Boundary

Events do not imply a broker.

Possible mechanisms:

```text
provider callback
webhook
message broker
internal event bus
change feed
stream
```

Only accepted architecture decides.

# Step 41 — Topic / Queue Names

Do not invent.

# Step 42 — Producer Transaction Boundary

A key architectural question:

```text
When is event considered valid relative to authoritative state change?
```

Examples:

```text
after transaction commit
after external provider acceptance
after business operation succeeds
```

Only state accepted semantics.

If unclear:

```text
EVENT_EMISSION_ORDER_REQUIRED
```

# Step 43 — Dual-Write Risk

If system must update state and emit event:

```text
record atomicity/consistency concern
```

Do not prescribe outbox/transactional messaging unless accepted.

# Step 44 — Consumer Transaction Boundary

Record whether consumer side effect and acknowledgement need consistency if known.

Do not invent transaction strategy.

# Step 45 — State Machine Alignment

Event may correspond to state transition.

Example:

```text
ConversationResolved
→ after OPEN → RESOLVED accepted transition
```

Do not create event for unaccepted states.

# Step 46 — Domain Data Alignment

Event semantic data should reference accepted domain concepts/identifiers.

Do not introduce new canonical entities in event schema.

# Step 47 — DFD Alignment

Event flow may carry sensitive data.

Reference:

```text
classification
third-party transfer
trust boundary
```

from DFD.

Do not duplicate privacy analysis.

# Step 48 — Sequence Alignment

Sequence models may show one event publication/consumption scenario.

Event flow owns delivery/order/retry/version semantics.

# Step 49 — C4 Alignment

Producer/consumer must map to accepted C4 participants.

If not:

```text
EVENT_C4_ALIGNMENT_REQUIRED
```

# Step 50 — Provider Events

External provider events may have provider-defined semantics.

Record:

```text
provider ownership
delivery/order guarantees if documented
event identity
version policy if documented
```

Do not overwrite provider contract.

# Step 51 — Internal Events

Internal event ownership must be explicit enough for maintenance.

# Step 52 — Integration Events vs Domain Events

Where useful distinguish:

```text
domain event
→ internal business fact

integration event
→ contract intended for cross-boundary consumption
```

Do not force distinction if architecture does not use it.

# Step 53 — Privacy / Sensitive Data

Events may duplicate sensitive data.

Ask:

```text
does event need full content?
can it reference ID instead?
what classification applies?
```

Do not decide minimization fields without evidence.

# Step 54 — Secrets in Events

Secrets should not appear unless explicit requirement says so.

If proposed:

```text
SECURITY_REVIEW_REQUIRED
```

Do not place credentials in event examples.

# Step 55 — Retention

Broker/event retention is infrastructure/policy-specific.

Do not invent.

If architecture requires replay/history and retention is unspecified:

```text
EVENT_RETENTION_POLICY_REQUIRED
```

# Step 56 — Replay

Replay semantics must be explicit if supported.

Questions:

```text
who can replay?
which consumers?
what business effects occur?
how duplicates are handled?
```

Do not assume replay.

# Step 57 — Replay Gap

Use:

```text
REPLAY_POLICY_REQUIRED
```

# Step 58 — Backpressure

If high-volume event flow may overwhelm consumers:

```text
record backpressure concern
```

when supported by scale/quality drivers.

Do not invent strategy.

# Step 59 — Consumer Lag

If latency/lag matters:

```text
record accepted lag target
```

or:

```text
CONSUMER_LAG_TARGET_REQUIRED
```

# Step 60 — Failure Isolation

Event flow can clarify:

```text
producer succeeds even if consumer temporarily fails?
```

Only if delivery semantics support it.

# Step 61 — Consumer Independence

One consumer failure should not be assumed to block another.

Record actual architecture semantics.

# Step 62 — Fan-Out

If event has many consumers:

```text
record consumers independently
```

Do not invent pub/sub technology.

# Step 63 — Fan-In

If one consumer combines several events:

```text
ordering/correlation implications
```

may matter.

# Step 64 — Choreography

If multiple event reactions form a workflow, model the flow but flag complexity.

Do not assume choreography over orchestration by preference.

# Step 65 — Event Cycle Audit

Detect cycles:

```text
A event → B event → A event
```

that may create feedback loops.

Flag:

```text
EVENT_CYCLE_REVIEW_REQUIRED
```

# Step 66 — Retry Storm Audit

If retries can amplify failures:

```text
record risk
```

without inventing mitigation.

# Step 67 — Duplicate Side-Effect Audit

Check consumers with non-idempotent business effects.

# Step 68 — Ordering Conflict Audit

Check when consumer logic assumes order not guaranteed by source.

# Step 69 — Ownership Gap Audit

Every accepted event should have clear contract owner or gap.

# Step 70 — Schema Drift Audit

Check producer/consumer expectations for version mismatch.

# Step 71 — Consumer Compatibility Audit

For each consumer:

```text
which event version/semantic contract expected?
```

when known.

# Step 72 — Orphan Event Audit

An event with no consumer may still be valid for future/external use, but needs explicit reason.

# Step 73 — Orphan Consumer Audit

Every consumer expectation must point to an event/source.

# Step 74 — Event Naming

Prefer business facts.

Avoid transport names:

```text
topic1-message
queue-item
notification-event
```

# Step 75 — Event Flow Diagram

Prefer version-control-friendly syntax:

```text
Mermaid flowchart
PlantUML
repository event-diagram convention
```

# Step 76 — Diagram Semantics

Diagram should show:

```text
producer
event
consumer(s)
```

plus annotations for:

```text
delivery/order/failure
```

not runtime infrastructure unless accepted.

# Step 77 — Event Flow vs Sequence

Event Flow:

```text
contract and asynchronous semantics
```

Sequence:

```text
one temporal scenario
```

# Step 78 — Event Flow vs State Machine

State Machine:

```text
legal lifecycle transitions
```

Event Flow:

```text
facts emitted/consumed around those transitions
```

# Step 79 — Event Flow vs DFD

DFD:

```text
data classes + trust movement
```

Event Flow:

```text
event contracts + delivery/order/retry/version semantics
```

# Step 80 — Event Flow vs Deployment

Broker/cluster/partition infrastructure belongs to deployment/infra design.

# Step 81 — Deployment Handoff

Flag:

```text
broker placement
multi-zone/multi-region
capacity
consumer scaling
network boundaries
```

if/when messaging infrastructure is selected.

# Step 82 — Validation Handoff

Accepted event semantics become validation criteria:

```text
duplicate behavior
ordering
retry
dead-letter handling
version compatibility
consumer independence
```

# Model Quality Status

Use:

```text
READY
READY_WITH_OPEN_QUESTIONS
REQUIRES_EVENT_INTERACTION_DECISION
REQUIRES_DELIVERY_SEMANTICS
REQUIRES_ORDERING_REQUIREMENT
REQUIRES_RETRY_POLICY
REQUIRES_DEDUPLICATION_POLICY
REQUIRES_DEAD_LETTER_BEHAVIOR
REQUIRES_VERSIONING_POLICY
REQUIRES_EVENT_OWNERSHIP
REQUIRES_ARCHITECTURE_ALIGNMENT
CONFLICTED
```

# Final Decision

Use:

```text
EVENT_FLOW_MODEL_READY
EVENT_FLOW_MODEL_READY_WITH_OPEN_QUESTIONS
EVENT_FLOW_MODEL_REQUIRES_EVENT_INTERACTION_DECISION
EVENT_FLOW_MODEL_REQUIRES_DELIVERY_SEMANTICS
EVENT_FLOW_MODEL_REQUIRES_ORDERING_REQUIREMENT
EVENT_FLOW_MODEL_REQUIRES_RETRY_POLICY
EVENT_FLOW_MODEL_REQUIRES_DEDUPLICATION_POLICY
EVENT_FLOW_MODEL_REQUIRES_DEAD_LETTER_BEHAVIOR
EVENT_FLOW_MODEL_REQUIRES_VERSIONING_POLICY
EVENT_FLOW_MODEL_REQUIRES_EVENT_OWNERSHIP
EVENT_FLOW_MODEL_REQUIRES_ARCHITECTURE_ALIGNMENT
EVENT_FLOW_MODEL_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/event-flow-model.md
```

## Completion Criteria

- [ ] Event-driven/asynchronous behavior is evidenced.
- [ ] Scope and architecture basis are explicit.
- [ ] Producers are accepted participants.
- [ ] Events represent meaningful facts/contracts.
- [ ] Consumers are accepted participants.
- [ ] Event purpose is explicit.
- [ ] Semantic/contract ownership is explicit or gap flagged.
- [ ] Delivery semantics are evidence-backed or TBD.
- [ ] Exactly-once delivery/business effect are not conflated.
- [ ] Ordering scope is explicit or gap flagged.
- [ ] Late/out-of-order behavior is not invented.
- [ ] Retry ownership/eligibility/terminal behavior is evidence-backed.
- [ ] Retry counts/backoff/deadlines are not invented.
- [ ] Dead-letter behavior is explicit without assuming a DLQ.
- [ ] Deduplication and idempotency are distinguished.
- [ ] Dedup/idempotency semantics are not invented.
- [ ] Event identity/correlation/causation are not invented.
- [ ] Schema semantics are explicit without invented payload fields.
- [ ] Schema technology is not invented.
- [ ] Versioning/compatibility policy is explicit or gap flagged.
- [ ] Breaking changes do not silently reuse contracts.
- [ ] Event-driven design is not confused with event sourcing/CQRS/broker use.
- [ ] Topic/queue names are not invented.
- [ ] Event emission order relative to authoritative state is explicit or gap flagged.
- [ ] Dual-write/consumer consistency risks are visible without premature tactics.
- [ ] State/domain/DFD/sequence/C4 alignment is audited.
- [ ] Provider contract semantics are preserved.
- [ ] Sensitive-data duplication is visible without invented minimization.
- [ ] Secrets are not placed in event examples.
- [ ] Retention/replay/backpressure/lag are only modeled when supported.
- [ ] Fan-out/fan-in/choreography semantics are explicit when relevant.
- [ ] Event cycles/retry storms/duplicate effects/order conflicts are audited.
- [ ] Ownership/schema compatibility/orphan events/consumers are audited.
- [ ] Diagram is transport-neutral unless infrastructure is accepted.
- [ ] Sequence/state/DFD/deployment responsibilities remain separate.
- [ ] Deployment and validation handoffs are explicit.
- [ ] Final readiness is explicit.

## References

- Read `references/event-flow-purpose-producer-event-consumer-and-ownership.md` first.
- Read `references/delivery-ordering-retries-deduplication-and-dead-letter.md`.
- Read `references/schema-versioning-compatibility-and-breaking-changes.md`.
- Read `references/event-identity-correlation-idempotency-and-replay.md`.
- Read `references/state-domain-dfd-sequence-and-c4-alignment.md`.
- Read `references/event-sourcing-cqrs-broker-and-infrastructure-boundaries.md`.
- Read `references/fanout-fanin-choreography-backpressure-and-failure-risks.md`.
- Read `references/event-flow-model-audit.md` before completion.
