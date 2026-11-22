---
name: modeling-system-sequences
description: Models time-ordered interactions across actors, UI/frontends, APIs, applications/services, data stores, queues, and external providers for architecturally important scenarios. Use after use cases/process flows/state machines and accepted architecture/C4 boundaries exist, when runtime interaction order matters. Include happy paths, important alternatives, failures, retries, timeouts, authorization, and concurrency/idempotency only when supported by requirements or architecture decisions. Produce sequence models with explicit participants, messages, conditions, responses, failure semantics, and traceability. Do not invent protocols, endpoints, retry policies, timeout values, idempotency behavior, or architectural participants; do not use sequence diagrams as process flows, state machines, DFDs, or deployment diagrams.
...
---

# Modeling System Sequences

## Purpose

Model architecturally important runtime interactions in temporal order.

Core workflow:

```text
use case / process / state transition
+ accepted architecture / C4
→ choose scenario
→ select participants
→ define initiating event
→ model happy path
→ model important alternatives/failures
→ model auth / timeout / retry when supported
→ model concurrency/idempotency when material
→ audit participant/order/semantics
→ produce sequence model
```

Output:

```text
sequence-model.md
```

## Core Principle

A sequence diagram answers:

```text
who interacts with whom
in what order
under what condition
with what response or failure
```

It does not primarily answer:

```text
who may perform a capability?        → use cases
what branch happens next?            → process flows
what lifecycle transition is legal?  → state machines
what structural elements exist?      → C4
how sensitive data crosses trust?    → DFD
where instances run?                 → deployment
```

## Use When

- A critical use case crosses multiple architectural participants.
- External providers participate in runtime behavior.
- Authorization placement/order matters.
- Callback/request-response order matters.
- Failure propagation matters.
- Retry/timeout behavior is accepted and architecturally relevant.
- Concurrency/idempotency semantics matter.
- Architecture validation needs a concrete runtime interaction probe.

## Do Not Use When

- Only static structure is needed.
- The main issue is workflow branching.
- The main issue is lifecycle transitions.
- The main issue is data lineage/trust boundaries.
- Participants are not yet decided.
- The task is to invent API contracts or protocols.
- The task is source-code call tracing without architecture purpose.

## Inputs

Preferred:

- accepted/proposed C4 model;
- use-case catalog;
- process-flow model;
- state-machine model;
- ADRs;
- functional requirements;
- NFR/quality scenarios;
- business rules;
- authorization rules;
- external provider behavior;
- accepted retry/timeout/idempotency semantics;
- applicable `AGENTS.md`.

Optional:

- existing sequence diagrams;
- API contracts;
- event contracts;
- provider documentation;
- runtime traces;
- brownfield interaction behavior.

## Outputs

- Sequence model document.
- Scenario inventory.
- Participant catalog.
- Happy-path sequence.
- Important alternative/failure sequences.
- Authorization sequence notes.
- Retry/timeout semantics when supported.
- Concurrency/idempotency notes when material.
- Traceability.
- Gaps/unknowns.
- Downstream DFD/event/deployment/validation handoffs.

# Sequence Identity

Use stable IDs:

```text
SEQ-001
SEQ-002
```

# Scenario Status

Use:

```text
PROPOSED
REVIEW_REQUIRED
ACCEPTED
DEFERRED
SUPERSEDED
```

# Sequence Quality Status

Use:

```text
READY
READY_WITH_OPEN_QUESTIONS
REQUIRES_PARTICIPANT_DECISION
REQUIRES_FAILURE_SEMANTICS
REQUIRES_RETRY_POLICY
REQUIRES_TIMEOUT_POLICY
REQUIRES_AUTHORIZATION_CLARIFICATION
REQUIRES_IDEMPOTENCY_POLICY
REQUIRES_CONCURRENCY_POLICY
CONFLICTED
```

# Step 1 — Define the Scenario

State one bounded runtime question.

Good:

```text
How does an inbound email become an accepted conversation message?
```

Good:

```text
How does an agent request an AI suggestion and fall back to manual reply?
```

Bad:

```text
How does the whole support platform work?
```

# Step 2 — Select Participants from Accepted Architecture

Participants may include:

```text
actor
frontend/client
accepted application/container
accepted component
data store
queue/broker if accepted
external provider
```

Do not invent new runtime units.

# Participant Naming

Prefer architecture names from C4/ADR.

Bad:

```text
Service A
Helper
Utils
```

Good:

```text
Support Agent
Support Web Client
Support Application
Persistent Store
Email Provider
AI Provider
```

# Step 3 — Participant Abstraction Level

Keep participants at a consistent/useful level.

Do not mix:

```text
Support Application
ConversationController
PostgreSQL table
Kubernetes pod
```

unless the scenario specifically requires a lower accepted level.

# Step 4 — Initiating Event

Explicitly identify the first trigger.

Examples:

```text
Agent submits reply
Email Provider delivers inbound message
Manager requests reassignment
AI Provider callback arrives
```

# Step 5 — Happy Path

Roadmap-required.

Model the normal successful interaction in order.

Each message should communicate:

```text
intent
not implementation noise
```

Bad:

```text
call method()
map DTO
serialize JSON
```

unless the exact contract is the subject.

# Step 6 — Request / Response

Show response only when it matters to understanding.

Do not clutter the diagram with every return value.

# Step 7 — Synchronous Interactions

Use synchronous semantics only if accepted.

Do not infer HTTP/REST from “calls API”.

If protocol is unknown:

```text
interaction protocol: TBD
```

# Step 8 — Asynchronous Interactions

Use async/event/message arrows only when architecture or contract accepts asynchronous behavior.

Do not invent queues or events.

# Step 9 — Important Alternatives

Roadmap-required.

Use alternatives when runtime participants/order differ materially.

Examples:

```text
AI available vs unavailable
authorized vs unauthorized
provider accepted vs rejected
```

Do not repeat every business branch already clear in a process flow unless it affects system interactions.

# Step 10 — Failure Paths

Roadmap-required.

Examples:

```text
dependency unavailable
storage write fails
authorization denied
provider rejects request
callback invalid
```

Only model known behavior.

If failure outcome is undefined:

```text
FAILURE_SEMANTICS_REQUIRED
```

# Step 11 — Retry Semantics

Roadmap-required when relevant.

Represent retries only if accepted.

Record:

```text
who retries
what operation
under what condition
attempt/deadline if known
terminal outcome
```

If unknown:

```text
RETRY_POLICY_REQUIRED
```

Never invent “retry 3 times”.

# Step 12 — Timeout Semantics

Roadmap-required when relevant.

Record:

```text
which interaction may time out
who observes timeout
timeout value if authoritative
result/fallback
```

If timing undefined but materially needed:

```text
TIMEOUT_POLICY_REQUIRED
```

Do not invent 30s/5s/etc.

# Step 13 — Authorization

Roadmap-required.

For protected operations show the authoritative authorization decision at an appropriate level.

Example:

```text
Agent
→ Support Application: request conversation
Support Application
→ Tenant Access capability: authorize tenant-scoped access
```

only if those internal components are accepted at L3.

At L2-only architecture:

```text
Support Application: validates tenant-scoped authorization
```

is enough.

# Authorization UI Warning

Do not model frontend hiding a button as authoritative authorization.

# Step 14 — Authentication vs Authorization

Keep separate when material.

```text
authentication
→ who are you?

authorization
→ may you perform this action on this resource?
```

Do not add identity-provider interactions if not relevant/accepted.

# Step 15 — Tenant Scope

For multi-tenant interactions, model tenant context at the authorization/resource boundary when materially relevant.

Do not invent tenancy implementation.

# Step 16 — Concurrency

Roadmap-required when material.

Use sequence diagrams to expose:

```text
two actors/events race
ordering matters
conflicting updates
```

If semantic outcome is undefined:

```text
CONCURRENCY_POLICY_REQUIRED
```

Do not choose locking/versioning.

# Step 17 — Idempotency

Roadmap-required when material.

Examples:

```text
duplicate provider callback
repeated payment request
retry of accepted message
```

Record expected semantic behavior only if accepted.

If undefined:

```text
IDEMPOTENCY_POLICY_REQUIRED
```

# Step 18 — Duplicate Messages

Do not automatically assume deduplication.

# Step 19 — Out-of-Order Events

If async external events may arrive out of order, model only accepted semantics.

Otherwise:

```text
EVENT_ORDERING_POLICY_REQUIRED
```

# Step 20 — Parallel Work

Use parallel fragments only when interactions truly happen independently/concurrently.

Do not use parallel notation for visual convenience.

# Step 21 — Loop Fragments

Use loop notation only for accepted repeated behavior.

The loop condition must be explicit.

# Step 22 — Optional Fragments

Use optional fragments when behavior can occur without changing the base successful scenario.

# Step 23 — Alternative Fragments

Use alternative fragments for mutually exclusive branches with clear guards.

# Step 24 — Critical Fragments

Use critical/atomic notation sparingly and only if architecture semantics support it.

Do not imply transactionality accidentally.

# Step 25 — Storage Interaction

Show data store interaction when needed to explain:

```text
authoritative acceptance
read-before-write
persistence before provider call
audit recording
transaction boundary
```

Do not show SQL/table details.

# Step 26 — Write Ordering

Ordering can be architecture-significant.

Example question:

```text
Does the platform persist an outbound reply before or after provider acceptance?
```

If undecided:

```text
INTERACTION_ORDER_DECISION_REQUIRED
```

Do not choose silently.

# Step 27 — Audit Interaction

If auditability is an accepted requirement and ordering matters, model it.

Do not invent an audit service if architecture models audit inside the application.

# Step 28 — Provider Interaction

Show provider at the accepted abstraction level.

Do not invent:

```text
webhook endpoint
SDK method
queue topic
HTTP status code
```

unless contract evidence exists.

# Step 29 — Callback Model

If a provider callback is accepted:

```text
request
→ provider processing
→ callback/event
```

can be modeled.

If callback vs polling is undecided:

```text
INTEGRATION_PATTERN_REQUIRED
```

# Step 30 — Degraded Mode

Use sequence variants to show accepted degraded behavior.

Example:

```text
AI provider unavailable
→ no AI suggestion
→ agent manual reply remains available
```

# Step 31 — Readability During Provider Outage

For accepted degraded read behavior, model provider absence only if it is relevant to prove the read path does not depend on the provider.

Do not invent caches/replicas.

# Step 32 — Error Propagation

Show who receives/handles a failure.

Avoid vague:

```text
error happens
```

# Step 33 — User-Visible Outcome

For user-facing scenarios, end with an observable outcome.

Examples:

```text
conversation displayed
reply accepted
reassignment rejected
manual reply remains available
```

# Step 34 — Sequence vs Process Flow

If the diagram is mostly:

```text
decision diamond
approval
loop/rework
```

use `modeling-process-flows`.

Sequence focuses on participants/messages over time.

# Step 35 — Sequence vs State Machine

A sequence may trigger a transition.

Example:

```text
resolve request
→ state transition OPEN → RESOLVED
```

But legal lifecycle rules remain in the state machine.

# Step 36 — Sequence vs C4

Participants must align with C4.

If sequence needs an unmodeled participant:

```text
C4_ALIGNMENT_REQUIRED
```

Do not silently add architecture.

# Step 37 — Sequence vs DFD

A sequence can mention payload intent.

Detailed:

```text
PII fields
data classification
trust boundary
retention
third-party transfer
```

belongs to DFD/privacy/security modeling.

# Step 38 — Sequence vs Event Flow

A sequence can show one event interaction.

Detailed producer/event/consumer semantics, schema, delivery guarantees, ordering, replay belong to `modeling-event-flows`.

# Step 39 — Sequence vs Deployment

Do not show pods/nodes/zones.

# Step 40 — Diagram Syntax

Prefer version-control-friendly formats:

```text
Mermaid sequenceDiagram
PlantUML sequence diagram
```

Follow repository convention.

# Step 41 — Mermaid Example

```text
sequenceDiagram
    actor Agent
    participant App as Support Application
    participant AI as AI Provider

    Agent->>App: Request AI suggestion
    App->>AI: Request suggestion
    alt AI available
        AI-->>App: Suggestion
        App-->>Agent: Show optional suggestion
    else AI unavailable
        App-->>Agent: Manual reply remains available
    end
```

Only use interactions supported by evidence.

# Step 42 — Message Labels

Prefer semantic labels.

Good:

```text
Request conversation reply suggestion
Authorize tenant-scoped access
Persist accepted inbound message
```

Bad:

```text
POST /x
callService()
```

unless contract detail is intentionally in scope.

# Step 43 — Response Labels

Show important semantics:

```text
authorized
denied
accepted
rejected
timeout
unavailable
```

# Step 44 — Notes

Use notes sparingly for:

```text
constraint
unknown policy
state invariant
architecture decision
```

Do not hide half the model in notes.

# Step 45 — Sequence Splitting

If one sequence becomes unreadable:

```text
split happy path
failure/degraded variant
concurrency variant
```

while preserving one scenario family.

# Step 46 — Traceability

Each sequence should trace to:

```text
use case
FR
process flow
state transition
quality scenario
ADR/C4 relationship
```

# Step 47 — Scenario Coverage

Use:

```text
COVERED
PARTIALLY_COVERED
NO_SEQUENCE_NEEDED
MISSING_SEQUENCE
BLOCKED_BY_INTERACTION_DECISION
```

Not every use case needs a sequence.

# Step 48 — Participant Audit

Check:

```text
participant exists in accepted architecture?
participant level consistent?
internal/external boundary correct?
```

# Step 49 — Ordering Audit

Check:

```text
does ordering contradict process/state/business rules?
```

# Step 50 — Authorization Audit

Check:

```text
protected operation lacks authoritative auth step?
frontend-only auth implied?
tenant/resource scope missing?
```

# Step 51 — Failure Coverage Audit

For critical interaction ask:

```text
dependency unavailable?
authorization denied?
timeout?
write failure?
provider rejection?
duplicate/retry?
```

only where materially relevant.

# Step 52 — Retry/Timeout Audit

No retry/timeout without evidence.

# Step 53 — Idempotency Audit

Do not mark repeat behavior safe without accepted semantics.

# Step 54 — Architecture Alignment Audit

Sequence must not contradict ADR/C4.

Use:

```text
SEQUENCE_ARCHITECTURE_CONFLICT
```

# Step 55 — State Alignment Audit

Sequence must not perform illegal state transition.

Use:

```text
SEQUENCE_STATE_CONFLICT
```

# Step 56 — Process Alignment Audit

Sequence must not violate accepted business branch/rule.

Use:

```text
SEQUENCE_PROCESS_CONFLICT
```

# Step 57 — Undecided Participant

Use:

```text
PARTICIPANT_DECISION_REQUIRED
```

# Step 58 — Undecided Order

Use:

```text
INTERACTION_ORDER_DECISION_REQUIRED
```

# Step 59 — Failure Gap

Use:

```text
FAILURE_SEMANTICS_REQUIRED
```

# Step 60 — Integration Gap

Use:

```text
INTEGRATION_PATTERN_REQUIRED
```

when callback/polling/sync/async architecture is undecided and needed for the sequence.

# Final Decision

Use:

```text
SEQUENCE_MODEL_READY
SEQUENCE_MODEL_READY_WITH_OPEN_QUESTIONS
SEQUENCE_MODEL_REQUIRES_PARTICIPANT_DECISION
SEQUENCE_MODEL_REQUIRES_INTERACTION_ORDER
SEQUENCE_MODEL_REQUIRES_FAILURE_SEMANTICS
SEQUENCE_MODEL_REQUIRES_RETRY_POLICY
SEQUENCE_MODEL_REQUIRES_TIMEOUT_POLICY
SEQUENCE_MODEL_REQUIRES_AUTHORIZATION_CLARIFICATION
SEQUENCE_MODEL_REQUIRES_IDEMPOTENCY_POLICY
SEQUENCE_MODEL_REQUIRES_CONCURRENCY_POLICY
SEQUENCE_MODEL_REQUIRES_ARCHITECTURE_ALIGNMENT
SEQUENCE_MODEL_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/sequence-model.md
```

## Completion Criteria

- [ ] Scenario is bounded and architecture-relevant.
- [ ] Participants come from accepted architecture/contracts.
- [ ] Participant abstraction is consistent.
- [ ] Initiating event is explicit.
- [ ] Happy path is modeled.
- [ ] Important alternatives are modeled.
- [ ] Relevant failure paths are modeled or gaps flagged.
- [ ] Retry appears only when accepted.
- [ ] Retry owner/condition/terminal outcome are explicit when known.
- [ ] Timeout appears only when accepted/material.
- [ ] Timeout observer/fallback are explicit when known.
- [ ] Authorization is modeled at the authoritative boundary.
- [ ] Frontend visibility is not treated as authorization.
- [ ] Tenant/resource scope is explicit where material.
- [ ] Concurrency is modeled only when material.
- [ ] Concurrency outcome is not invented.
- [ ] Idempotency/duplicate semantics are not invented.
- [ ] Event ordering semantics are not invented.
- [ ] Parallel/loop/optional/alternative fragments are semantically justified.
- [ ] Storage interactions are architecture-level, not SQL-level.
- [ ] Important persistence/provider ordering is explicit or flagged.
- [ ] Audit behavior is included only when relevant.
- [ ] Provider integration does not invent protocol details.
- [ ] Degraded mode reflects accepted requirements.
- [ ] User-visible/system-observable outcome is clear.
- [ ] Sequence is not a process flow/state machine/C4/DFD/deployment diagram.
- [ ] Participants align with C4/ADRs.
- [ ] Diagram syntax is version-control friendly.
- [ ] Message labels are semantic.
- [ ] Large sequences are split when necessary.
- [ ] Traceability exists.
- [ ] Only relevant scenarios are modeled.
- [ ] Participant/order/auth/failure/retry/timeout/idempotency audits pass.
- [ ] Architecture/state/process conflicts are surfaced.
- [ ] Downstream DFD/event/deployment/validation handoffs are explicit.
- [ ] Final readiness is explicit.
