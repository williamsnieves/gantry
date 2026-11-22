---
name: modeling-state-machines
description: Models lifecycle behavior for entities, workflows, and long-running processes using explicit states, events, guards, transitions, actions/effects, terminal states, and illegal-transition rules. Use after functional requirements/use cases/process flows exist when correctness depends on which transitions are valid from which states. Produce a state-machine catalog and diagram with traceability to requirements/business rules, including cancellation, rollback/reopen, concurrency, and failure transitions when supported. Do not use a state machine as a generic process flow, sequence diagram, architecture diagram, or implementation enum dump; do not invent states, transitions, retry policies, or concurrency semantics.
---

# Modeling State Machines

## Purpose

Model valid lifecycle behavior and state transitions.

Core workflow:

```text
requirements / use cases / process flows
→ identify lifecycle subject
→ identify stable states
→ identify events
→ identify guards
→ define legal transitions
→ define actions/effects
→ define terminal states
→ define illegal transitions
→ analyze cancellation/rollback/concurrency
→ produce state-machine model
→ validate completeness and reachability
```

Output:

```text
state-machine-model.md
```

## Core Principle

A state machine answers:

```text
what state is the subject in?
what event may occur?
under what guard?
what transition is legal?
what state/effect follows?
```

It does not primarily answer:

```text
what happens next in a workflow?        → process flow
who can do what?                        → use case
who sends what message to whom?         → sequence diagram
what architecture components exist?     → C4
```

## Use When

- An entity has a meaningful lifecycle.
- Legal/illegal transitions matter.
- Business behavior depends on current state.
- Cancellation/reopen/rollback semantics matter.
- Concurrency may cause conflicting transitions.
- Payment/order/subscription/workflow states must be explicit.
- A process flow reveals stable states.
- Implementation correctness depends on state transition rules.

## Do Not Use When

- The problem is only a simple linear workflow.
- There are no meaningful stable states.
- The question is business decision branching rather than lifecycle.
- The question is message ordering among components.
- The task is to enumerate implementation enum values without business semantics.
- The task is architecture design.

## Inputs

Preferred:

- functional requirements;
- use-case catalog;
- process-flow model;
- business rules;
- current lifecycle documentation;
- relevant NFR/QA scenarios;
- concurrency/idempotency/cancellation requirements;
- applicable `AGENTS.md`.

Optional:

- existing enum/state definitions;
- database status fields;
- domain model;
- provider state model;
- legacy lifecycle behavior.

## Outputs

- State Machine Model.
- State catalog.
- Event catalog.
- Guard catalog.
- Transition table.
- Illegal transition table.
- Terminal-state definition.
- Concurrency/conflict notes.
- Cancellation/rollback/reopen analysis.
- Traceability matrix.
- Optional Mermaid/PlantUML state diagram.
- Handoff to sequence/data/architecture work.

# State Machine Identity

Use stable IDs:

```text
SM-001
SM-002
```

# State IDs

Use:

```text
S-001
S-002
```

or meaningful canonical names when already accepted:

```text
OPEN
RESOLVED
CANCELLED
```

# Event IDs

Use:

```text
EV-001
EV-002
```

# Transition IDs

Use:

```text
TR-001
TR-002
```

# Step 1 — Define Lifecycle Subject

State exactly what owns the state.

Good:

```text
Conversation lifecycle
Payment attempt lifecycle
Subscription lifecycle
Deployment lifecycle
```

Bad:

```text
Support Platform State
```

unless system-wide state is genuinely the subject.

# Step 2 — Stable State Test

A state should represent a meaningful condition that can persist between events.

Good:

```text
OPEN
RESOLVED
CANCELLED
PENDING_APPROVAL
```

Bad:

```text
CLICKING_BUTTON
CALLING_API
VALIDATING_FORM
```

Those are activities, not stable lifecycle states.

# Step 3 — State vs Attribute

Not every attribute value is a state-machine state.

Example:

```text
priority = HIGH
```

does not necessarily define lifecycle.

Use state only when transitions/allowed behavior depend on it.

# Step 4 — Initial State

Identify:

```text
initial state
creation event/condition
```

If unknown:

```text
INITIAL_STATE_REQUIRED
```

Do not invent.

# Step 5 — Terminal States

Identify terminal states explicitly.

Examples:

```text
CANCELLED
COMPLETED
EXPIRED
FAILED_PERMANENTLY
```

Do not mark a state terminal if requirements allow future transitions.

# Step 6 — Events

Events trigger transition consideration.

Examples:

```text
resolve requested
payment confirmed
approval rejected
timeout reached
provider callback received
user cancels
```

Events should be business/domain meaningful.

Avoid implementation events:

```text
HTTP 200 received
function returned
component mounted
```

unless externally defined contract semantics require them.

# Step 7 — Guards

A guard determines whether a transition is permitted.

Example:

```text
OPEN --resolveRequested [actor may resolve]--> RESOLVED
```

Guards should link to business rules/permissions.

Do not hide conditions in transition names.

# Step 8 — Actions / Effects

Transitions may cause effects.

Examples:

```text
record resolution
emit business event
capture audit record
preserve entitlement
```

Keep effects semantic.

Do not prescribe infrastructure.

# Step 9 — Transition Table

Use:

```text
current state
event
guard
next state
effect
source
```

Every accepted transition should be explicit.

# Step 10 — Illegal Transitions

Roadmap evaluation:

Explicitly identify important invalid transitions.

Example:

```text
RESOLVED + resolveRequested
→ INVALID / NO_OP / IDEMPOTENT
```

Only choose the semantics if requirements support them.

Otherwise:

```text
ILLEGAL_TRANSITION_BEHAVIOR_REQUIRED
```

# Step 11 — No-Op vs Error vs Idempotent

Do not assume.

Possible semantics:

```text
reject
ignore/no-op
return current state
idempotently succeed
```

Must come from requirements/contracts.

# Step 12 — Reopen

Roadmap evaluation:

If lifecycle supports:

```text
RESOLVED → OPEN
```

define event, permission/guard, and effects.

If “reopen” is only discussed but unaccepted:

```text
TRANSITION_NOT_ACCEPTED
```

Do not include it as legal.

# Step 13 — Cancel

Cancellation should define:

```text
from which states?
by whom?
what guard?
what final/next state?
what side effects remain/rollback?
```

Do not model a global cancel from every state unless supported.

# Step 14 — Rollback / Compensation

Rollback may mean:

```text
state restoration
compensating business action
```

Do not assume technical database rollback.

If external side effects already occurred, model compensation semantics only if accepted.

# Step 15 — Failure States

Use failure states only if failures persist as meaningful lifecycle conditions.

Examples:

```text
PAYMENT_FAILED
DELIVERY_FAILED
```

A transient technical error does not automatically deserve a state.

# Step 16 — Pending / In-Progress States

Long-running workflows may need:

```text
PENDING
PROCESSING
AWAITING_PROVIDER
AWAITING_APPROVAL
```

only when other behavior depends on them.

Avoid state explosion.

# Step 17 — State Explosion Audit

Do not create a state for every combination of attributes.

Example:

```text
OPEN_HIGH_PRIORITY_ASSIGNED_AI_ENABLED
```

is usually wrong.

Prefer orthogonal attributes/sub-state machines only when necessary.

# Step 18 — Composite States

Use hierarchical/composite states when:

```text
several states share behavior/transitions
```

and the notation improves clarity.

Do not introduce UML hierarchy without need.

# Step 19 — Parallel Regions

Use orthogonal/parallel states only if the subject genuinely has independent concurrent lifecycle dimensions.

Avoid complexity unless requirements demand it.

# Step 20 — Concurrency

Roadmap evaluation:

Analyze conflicting concurrent events.

Example:

```text
Agent A resolves conversation
while
Manager reassigns conversation
```

Questions:

```text
which transition wins?
is one rejected?
are both valid?
what observable state results?
```

If unspecified:

```text
CONCURRENCY_POLICY_REQUIRED
```

Do not invent locking/versioning strategy.

# Step 21 — Race Conditions

Identify state-transition races at semantic level.

Do not prescribe optimistic locking, mutexes, transactions, etc.

Those are architecture/implementation tactics.

# Step 22 — Idempotency

If repeated event semantics matter:

```text
same payment callback received twice
```

record desired transition behavior if accepted.

Do not infer idempotency from implementation convention.

# Step 23 — External Event Ordering

Provider/events may arrive:

```text
late
duplicate
out of order
```

Model valid semantic handling only when requirements support it.

Flag missing policy otherwise.

# Step 24 — Time-Based Transitions

Examples:

```text
pending expires
trial ends
retention period reached
```

Use only accepted time values/policies.

Do not invent timers.

# Step 25 — Automatic Transitions

An automatic transition can occur without external actor action after a condition/event.

Keep event explicit:

```text
timeoutElapsed
providerConfirmed
```

Avoid magical unlabeled arrows.

# Step 26 — Entry / Exit Actions

Use only when they add meaningful lifecycle semantics.

Example:

```text
enter RESOLVED → record resolved timestamp
```

Do not encode implementation hooks.

# Step 27 — Invariants by State

States may imply invariants.

Example:

```text
RESOLVED
→ no new standard reply allowed
```

only if requirements support it.

Link business rule.

# Step 28 — Allowed Capabilities by State

A useful matrix:

| State | Capability | Allowed |
|---|---|---|

Example:

```text
OPEN → reply = yes
RESOLVED → reply = no/TBD
```

This exposes missing product decisions.

# Step 29 — Process Flow Relationship

Process flow may contain:

```text
request
→ decision
→ resolve
```

State machine extracts:

```text
OPEN --resolveRequested--> RESOLVED
```

Do not duplicate entire process logic in state machine.

# Step 30 — Use Case Relationship

Use cases provide events/goals.

Example:

```text
UC Resolve Conversation
→ event resolveRequested
```

# Step 31 — Sequence Relationship

Later sequence diagrams can show:

```text
how resolveRequested is processed across participants
```

State machine only defines valid semantic transition.

# Step 32 — Data Model Relationship

State machine may reveal:

```text
status
timestamps
history
transition ownership
```

but does not design schema.

Flag for:

```text
modeling-domain-data
```

# Step 33 — External Provider State

Do not merge provider lifecycle into internal lifecycle unless they are intentionally one conceptual state machine.

Example:

```text
internal payment session state
vs
provider payment state
```

may need mapping rather than one enum.

# Step 34 — State Mapping

If external/provider states exist, record mapping separately.

Do not assume 1:1 equivalence.

# Step 35 — Reachability

Audit:

```text
every state reachable from initial?
```

If not, state may be orphaned or missing transition.

# Step 36 — Terminal Reachability

Can expected terminal outcomes actually be reached?

# Step 37 — Dead States

A nonterminal state with no valid outgoing transition may be a dead state.

Flag:

```text
DEAD_STATE
```

unless intentionally terminal.

# Step 38 — Missing Transition Audit

For each event/state combination that matters, determine:

```text
legal
illegal
not applicable
unspecified
```

Do not require exhaustive Cartesian matrix for irrelevant combinations.

# Step 39 — Transition Conflict Audit

No two accepted transitions should have same:

```text
state + event + overlapping guard
```

and incompatible next states unless nondeterminism is intentional.

Flag:

```text
NONDETERMINISTIC_TRANSITION
```

# Step 40 — Guard Completeness

If two branches cover:

```text
amount > 0
amount < 0
```

what about zero?

Use domain-appropriate completeness audit.

# Step 41 — Invariant Audit

Check that transitions preserve accepted invariants.

# Step 42 — History / Audit

If transition history is a requirement, note:

```text
transition history/audit required
```

Do not design event sourcing automatically.

# Step 43 — Diagram Syntax

Prefer version-control-friendly formats.

Preferred:

```text
Mermaid stateDiagram-v2
PlantUML state diagram
```

# Step 44 — Mermaid Example

```text
stateDiagram-v2
    [*] --> OPEN
    OPEN --> RESOLVED: resolveRequested
    RESOLVED --> [*]
```

Only include accepted transitions.

# Step 45 — Diagram Labels

Prefer:

```text
event [guard] / effect
```

where useful.

Keep labels readable.

# Step 46 — Split Large State Machines

If lifecycle becomes unreadable:

```text
split by bounded lifecycle
use composite states
or separate related machines
```

Do not create mega-diagrams.

# Step 47 — Brownfield State Models

Compare:

```text
current states/transitions
accepted target states/transitions
migration/coexistence
```

Do not delete legacy states without evidence.

# Step 48 — Migration State

Temporary migration states are valid only if operational/product behavior requires them.

# Step 49 — State Naming

Use business language.

Good:

```text
PENDING_APPROVAL
ACTIVE
SUSPENDED
```

Bad:

```text
STATUS_2
STEP_7
```

unless legacy mapping must be documented.

# Step 50 — Ambiguous State

Flag:

```text
STATE_DEFINITION_REQUIRED
```

if the same label has multiple meanings.

# Step 51 — Missing Event

Flag:

```text
TRANSITION_EVENT_REQUIRED
```

when transition exists conceptually but trigger is undefined.

# Step 52 — Missing Guard

Flag:

```text
TRANSITION_GUARD_REQUIRED
```

when permission/business condition is unclear.

# Step 53 — Missing Outcome

Flag:

```text
TRANSITION_OUTCOME_REQUIRED
```

when post-transition state/effect is ambiguous.

# Step 54 — Concurrency Gap

Use:

```text
CONCURRENCY_POLICY_REQUIRED
```

# Step 55 — Ordering Gap

Use:

```text
EVENT_ORDERING_POLICY_REQUIRED
```

# Step 56 — Illegal Transition Gap

Use:

```text
ILLEGAL_TRANSITION_BEHAVIOR_REQUIRED
```

# Step 57 — State Machine Quality Status

Use:

```text
READY
READY_WITH_OPEN_QUESTIONS
REQUIRES_STATE_DEFINITION
REQUIRES_TRANSITION_RULE
REQUIRES_CONCURRENCY_POLICY
REQUIRES_EVENT_ORDERING_POLICY
CONFLICTED
```

# Final Decision

Use:

```text
STATE_MACHINE_MODEL_READY
STATE_MACHINE_MODEL_READY_WITH_OPEN_QUESTIONS
STATE_MACHINE_MODEL_REQUIRES_STATE_DEFINITION
STATE_MACHINE_MODEL_REQUIRES_TRANSITION_RULE
STATE_MACHINE_MODEL_REQUIRES_CONCURRENCY_POLICY
STATE_MACHINE_MODEL_REQUIRES_EVENT_ORDERING_POLICY
STATE_MACHINE_MODEL_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/state-machine-model.md
```

## Completion Criteria

- [ ] Lifecycle subject is explicit.
- [ ] States represent stable meaningful conditions.
- [ ] Attributes/activities are not inflated into states.
- [ ] Initial state is explicit or gap flagged.
- [ ] Terminal states are explicit and truly terminal.
- [ ] Events are business/domain meaningful.
- [ ] Guards are explicit and rule-backed.
- [ ] Transition effects remain semantic.
- [ ] Legal transitions are tabulated.
- [ ] Important illegal transitions are explicit.
- [ ] Reject/no-op/idempotent semantics are not invented.
- [ ] Reopen/cancel/rollback/compensation are modeled only when supported.
- [ ] Failure/pending states exist only when lifecycle-significant.
- [ ] State explosion is avoided.
- [ ] Composite/parallel states are used only when justified.
- [ ] Concurrent transition conflicts are analyzed.
- [ ] Race policy/locking implementation is not invented.
- [ ] Duplicate/out-of-order external event semantics are captured only when supported.
- [ ] Time-based transitions use accepted policy values.
- [ ] State invariants and allowed capabilities are captured when relevant.
- [ ] Process/use-case/sequence responsibilities remain separate.
- [ ] Provider state is not blindly merged with internal state.
- [ ] Reachability and terminal reachability are audited.
- [ ] Dead/orphan states are detected.
- [ ] Missing/overlapping transitions and guards are audited.
- [ ] Accepted invariants are preserved.
- [ ] History/audit requirement does not imply event sourcing.
- [ ] Diagram is version-control friendly and readable.
- [ ] Brownfield current/target lifecycles are distinguished.
- [ ] Business language is used for states.
- [ ] Missing state/event/guard/outcome/concurrency/ordering policies are explicit.
- [ ] Data/sequence handoffs are identified.
- [ ] Final readiness is explicit.

## References

- Read `references/state-machine-purpose-subject-states-events-and-transitions.md` first.
- Read `references/guards-effects-illegal-transitions-and-invariants.md`.
- Read `references/cancellation-rollback-reopen-failure-and-terminal-states.md`.
- Read `references/concurrency-idempotency-ordering-and-race-semantics.md`.
- Read `references/state-explosion-composite-parallel-and-provider-state.md`.
- Read `references/reachability-determinism-completeness-and-diagram-discipline.md`.
- Read `references/state-machine-vs-process-sequence-usecase-and-data-model.md`.
- Read `references/state-machine-model-audit.md` before completion.
