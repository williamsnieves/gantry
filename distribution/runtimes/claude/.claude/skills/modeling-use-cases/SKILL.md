---
name: modeling-use-cases
description: Models actors, system capabilities, and structured use-case behavior from functional requirements, product goals, and journeys. Use after functional requirements exist and before detailed process-flow, sequence, state-machine, architecture, or implementation design. Produce a use-case catalog, written use-case records, actor/capability mappings, and use-case diagrams when they add clarity. Capture goal, preconditions, trigger, main flow, alternative flows, failure flows, postconditions, business rules, privilege boundaries, and external actors while preserving traceability to functional requirements. Do not turn use cases into UI click scripts, API sequences, architecture diagrams, or exhaustive UML ceremony; avoid abusing include/extend and do not invent actors or behavior.
---

# Modeling Use Cases

## Purpose

Model how actors achieve goals through the system.

Core workflow:

```text
functional requirements
→ identify actor goals
→ group related requirements by goal
→ define system boundary
→ define use cases
→ write structured flows
→ model alternatives/failures
→ map privileges/external actors
→ add use-case diagram when useful
→ audit traceability and granularity
```

Outputs:

```text
use-case-catalog.md
```

and optionally:

```text
use-case-diagram.md / Mermaid / PlantUML source
```

## Core Principle

A use case describes:

```text
actor
→ goal
→ interaction with system
→ observable outcome
```

It is not:

```text
UI click script
API call trace
sequence diagram
architecture component interaction
```

## Use When

- Functional requirements are ready enough to group into actor goals.
- Product/system behavior needs structured end-to-end use-case records.
- Several FRs together form a coherent user/system goal.
- Privilege boundaries matter.
- External systems participate as actors.
- Alternative and failure behavior needs to be organized.
- A use-case diagram would clarify actors and system capabilities.
- Process-flow or sequence modeling needs a behavior-level input.

## Do Not Use When

- Requirements are still vague.
- The task is to define functional requirements.
- The task is primarily a decision tree/workflow; use `modeling-process-flows`.
- The task is lifecycle/state transition modeling; use `modeling-state-machines`.
- The task is time-ordered component interaction; use `modeling-system-sequences`.
- The task is architecture structure; use `modeling-c4-architecture`.
- The task is implementation design.

## Inputs

Preferred:

- PRD;
- functional requirements catalog;
- actors;
- goals;
- journeys;
- business rules;
- permission/capability requirements;
- external-system requirements;
- relevant NFR references;
- applicable `AGENTS.md`.

Optional:

- existing use cases;
- brownfield behavior;
- product policy;
- legacy actor/capability model.

## Outputs

- Actor catalog.
- System boundary.
- Use-case catalog.
- Written use-case records.
- Actor → use-case capability matrix.
- Privilege-boundary map.
- External-actor participation map.
- Alternative/failure-flow coverage.
- Optional use-case diagram.
- Traceability matrix.
- Handoff to process-flow, state-machine, sequence, architecture, stories/OpenSpec.

# Use Case Identity

Use stable IDs:

```text
UC-001
UC-002
UC-003
```

Do not reuse IDs for different goals.

# Use Case Status

Use:

```text
PROPOSED
REVIEW_REQUIRED
ACCEPTED
DEFERRED
REJECTED
SUPERSEDED
```

Preserve source authority.

# Written Use Case Shape

Each use case should include:

```text
ID
title
status
primary actor
supporting actors
goal
scope/system boundary
stakeholders/interests
preconditions
trigger
main success flow
alternative flows
failure flows
postconditions
business rules
linked FRs
linked PRD goals/journeys
open questions
```

# Step 1 — Establish System Boundary

Before diagramming actors, define:

```text
what is inside the system being modeled?
what is external?
```

Example:

```text
Inside:
Support Platform

Outside:
Support Agent
Organization Manager
Email Provider
AI Provider
Identity Provider
```

Do not accidentally model internal services as external actors.

# Actor Definition

An actor is an external role/entity interacting with the system to achieve or support a goal.

Actors may be:

```text
human
external system
scheduled/external trigger
organization role
```

Actors are NOT:

```text
React component
controller
microservice
database
internal module
```

unless the modeling boundary explicitly makes them external.

# Step 2 — Build Actor Catalog

For each actor:

```text
ID
name
type
goal/interests
capabilities
scope
source
```

Do not invent fictional personas.

# Actor Generalization

Use actor generalization only when it clarifies true role inheritance.

Example:

```text
Support User
├── Agent
└── Manager
```

Only if shared capabilities and specialization are real.

Do not create abstract actors as diagram decoration.

# Step 3 — Group FRs by Goal

Use cases are goal-oriented.

Bad grouping:

```text
UC-001 Manage Conversations
```

if it hides many unrelated goals.

Better:

```text
UC-001 View Conversation
UC-002 Reply to Conversation
UC-003 Add Internal Note
UC-004 Resolve Conversation
UC-005 Reassign Conversation
```

But avoid creating one use case per trivial atomic FR if several are naturally one user goal.

# Use Case Granularity

A use case should represent a meaningful actor goal.

Too broad:

```text
Manage Support
```

Too narrow:

```text
Click Reply Button
```

Good:

```text
Reply to Customer Conversation
```

# Step 4 — Define Primary Actor

Primary actor:

```text
initiates the use case
and receives the main goal outcome
```

Supporting actors:

```text
participate but do not own the main goal
```

Examples:

```text
Primary: Support Agent
Supporting: AI Provider
```

for an AI-assisted reply case.

# Multiple Actors

Roadmap evaluation:

When multiple actors participate, distinguish:

```text
primary actor
supporting actor
secondary stakeholder
```

Do not list every stakeholder as an actor in the flow.

# Step 5 — Define Goal

Goal should be actor-oriented and outcome-oriented.

Example:

```text
Support agent sends a response to the customer conversation.
```

Avoid:

```text
Call message API.
```

# Step 6 — Preconditions

Preconditions describe facts that must already hold.

Examples:

```text
agent is authenticated
conversation exists
conversation belongs to actor's organization
conversation is open
```

Do not include implementation state.

# Step 7 — Trigger

Trigger is the event/intent that starts the use case.

Example:

```text
Agent decides to reply to an open conversation.
```

External actor example:

```text
Email provider delivers an inbound customer message.
```

# Step 8 — Main Success Flow

Write numbered steps at system-behavior level.

Example:

```text
1. Agent opens an eligible conversation.
2. System presents conversation context.
3. Agent provides reply content.
4. Agent submits the reply.
5. System validates that the actor may reply to the conversation.
6. System records the reply.
7. System makes the sent reply visible in the conversation.
8. Customer-facing delivery proceeds according to the accepted channel behavior.
```

Do not specify React components/controllers/queues.

# Flow Step Rule

Each step should describe:

```text
actor action
or
system response
```

not implementation mechanics.

# Step 9 — Alternative Flows

Alternative flows are valid alternate paths that still support the goal or a valid outcome.

Example:

```text
A1 — AI unavailable
1. Agent chooses manual reply.
2. System keeps manual reply available.
3. Continue at main flow step 3.
```

# Roadmap Evaluation: Alternative Flow

Alternative flows should be:

- meaningful;
- condition-triggered;
- traceable to requirements;
- not arbitrary edge-case enumeration.

# Step 10 — Failure Flows

Failure flows describe inability to complete the intended goal.

Examples:

```text
F1 — Actor lacks permission
F2 — Conversation is already resolved
F3 — Provider rejects delivery
```

State expected product/system outcome if requirements define it.

If unresolved:

```text
PRODUCT_DECISION_REQUIRED
```

Do not invent behavior.

# Failure vs Alternative

Alternative:

```text
goal continues via valid alternate path
```

Failure:

```text
goal cannot complete as intended
```

# Step 11 — Postconditions

Use:

```text
success postconditions
minimal guarantees
failure postconditions
```

Example:

```text
Success:
reply is part of the conversation history.

Failure:
no new reply is recorded if authorization is denied.
```

# Step 12 — Business Rules

Link relevant rules.

Example:

```text
BR-002:
Only organization managers may reassign conversations.
```

Do not recreate Domain modeling.

# Step 13 — Privilege Boundary

Roadmap evaluation:

Use cases should expose capability boundaries.

Example:

```text
Agent
→ Reply Conversation

Manager
→ Reply Conversation
→ Reassign Conversation
```

Do not confuse frontend visibility with authoritative permission.

Use-case model describes who is allowed to perform a capability at product level.

# Privilege Matrix

Produce:

| Actor | Use Case | Allowed | Scope/Rule |
|---|---|---|---|

when privilege differences matter.

# Step 14 — External Actors

Roadmap evaluation:

External systems may be actors.

Example:

```text
Email Provider
→ Deliver Inbound Message

AI Provider
→ Supply Reply Suggestion
```

Use case describes product-level interaction.

Do not specify webhook/API/event mechanics.

# Step 15 — System-Initiated Use Cases

Some use cases are triggered by external/time/policy events.

Examples:

```text
scheduled retention action
provider callback
billing cycle event
```

If no accepted actor/trigger exists, do not invent one.

# Step 16 — Include Relationship

Use `<<include>>` sparingly.

Appropriate when:

```text
a mandatory reusable sub-use-case
is always invoked by multiple base use cases
and has independent behavioral meaning
```

Example candidate:

```text
Authenticate User
```

only if authentication is intentionally modeled as a use case at this boundary.

Do not use `include` merely to avoid repeating 1–2 steps.

# Include Overuse

Roadmap evaluation:

Bad:

```text
Reply Conversation
<<include>> Validate Form
<<include>> Call API
<<include>> Save Message
```

These are internal steps, not reusable actor goals.

# Step 17 — Extend Relationship

Use `<<extend>>` only when:

```text
optional/conditional behavior
extends a complete base use case
at an explicit extension point
```

Example candidate:

```text
Generate AI Reply Suggestion
<<extend>>
Reply to Conversation
```

only if reply is complete without AI and AI is genuinely optional.

# Extend Overuse

Do not use `extend` for:

- normal error paths;
- every optional UI choice;
- alternative flows that are clearer inside the written use case;
- implementation plugins.

# Include vs Extend Rule

Prefer written alternative flows unless a separate use case has:

```text
independent actor goal
or
meaningful reusable product behavior
```

# Step 18 — Generalization

Use use-case generalization rarely.

Prefer explicit use cases unless specialization clearly shares semantics.

# Step 19 — Use Case Diagram Decision

Create a diagram when it clarifies:

```text
system boundary
actors
capabilities
privilege differences
external actors
major include/extend relationships
```

Skip it when the catalog already communicates the model and the diagram would add clutter.

# Diagram Purpose

Use-case diagram answers:

```text
who can do what with the system?
```

It does NOT answer:

```text
what happens step-by-step?
```

Written use cases answer the latter.

# Step 20 — Diagram Syntax

Prefer text-based diagrams suitable for version control.

Allowed:

```text
PlantUML
Mermaid if use-case notation is adequately represented
```

If Mermaid cannot express needed UML cleanly, prefer PlantUML or a simple relationship diagram.

Do not force a visual syntax that loses semantics.

# Step 21 — Diagram Layout

Keep:

```text
actors outside system boundary
use cases inside
relationships minimal
labels readable
```

Avoid spaghetti diagrams.

If many use cases exist, produce multiple bounded diagrams by capability/domain.

# Step 22 — Capability Matrix

Map actors to use cases.

This often gives more precise review evidence than a crowded diagram.

# Step 23 — Traceability

Each use case should trace to:

```text
FRs
PRD goal
journey
business rules
PRD AC
```

Every included FR should be either:

```text
covered by a use case
not use-case relevant
deferred
blocked
```

# Step 24 — Coverage Audit

Statuses:

```text
COVERED
PARTIALLY_COVERED
NO_USE_CASE_NEEDED
MISSING_USE_CASE
BLOCKED_BY_REQUIREMENT_DECISION
```

# Step 25 — Multiple FRs in One Use Case

Valid when the FRs collectively serve one actor goal.

Example:

```text
View conversation
Reply conversation
Record sent reply
```

may be one reply use case if the view step is only supporting context.

But independent goals should remain separate.

# Step 26 — One FR Across Multiple Use Cases

Also valid.

Example:

```text
tenant isolation
```

may constrain:

```text
view
reply
reassign
audit
```

Do not duplicate the rule inconsistently.

# Step 27 — Business Rule Centralization

Prefer one business-rule record referenced by multiple use cases.

# Step 28 — NFR References

Use cases may reference relevant NFRs:

```text
security
availability
accessibility
performance
```

Do not embed their detailed measures into flow steps unless behavior depends on them.

# Step 29 — Brownfield Use Cases

For existing systems, identify:

```text
current use case
changed behavior
preserved behavior
legacy actor
migration/coexistence
```

Do not assume undocumented existing behavior is required.

# Step 30 — Alternative/Failure Coverage Audit

For each critical use case ask:

```text
permission denied?
invalid state?
dependency unavailable?
cancel?
retry?
conflict?
```

only where requirements support relevance.

Do not invent edge behavior.

# Step 31 — Actor Scope Audit

Check that:

```text
manager action remains inside organization
tenant actor cannot cross tenant boundary
external actor scope is correct
```

# Step 32 — UI Leakage Audit

Remove:

```text
button
modal
dropdown
page route
component name
```

unless UI form itself is an accepted product requirement.

# Step 33 — API/Architecture Leakage Audit

Remove:

```text
HTTP POST
controller
service
Kafka
database
microservice
cache
```

unless externally required.

# Step 34 — Sequence Leakage Audit

If flow starts describing:

```text
Frontend → API → Service → DB
```

stop.

That belongs to:

```text
modeling-system-sequences
```

# Step 35 — Process-Flow Handoff

Flag use cases with:

```text
many business decisions
branching approvals
validation chains
loops/retries
manual/automated handoffs
```

for:

```text
modeling-process-flows
```

# Step 36 — State-Machine Handoff

Flag use cases that imply lifecycle transitions.

Example:

```text
Open → Resolved
Resolved → Reopened
```

for:

```text
modeling-state-machines
```

# Step 37 — Sequence Handoff

Flag integration-heavy use cases with several participants for later:

```text
modeling-system-sequences
```

# Step 38 — Architecture Input

Use cases can reveal:

```text
system boundaries
external actors
privilege boundaries
major capabilities
integration pressure
```

But do not derive architecture here.

# Step 39 — Open Questions

Use:

```text
PRODUCT_DECISION_REQUIRED
REQUIREMENT_CLARIFICATION_REQUIRED
ACTOR_SCOPE_REQUIRED
BUSINESS_RULE_REQUIRED
FAILURE_BEHAVIOR_REQUIRED
```

# Step 40 — Final Decision

Use:

```text
USE_CASE_MODEL_READY
USE_CASE_MODEL_READY_WITH_OPEN_QUESTIONS
USE_CASE_MODEL_REQUIRES_REQUIREMENT_CLARIFICATION
USE_CASE_MODEL_REQUIRES_PRODUCT_DECISION
USE_CASE_MODEL_REQUIRES_ACTOR_SCOPE
USE_CASE_MODEL_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/use-case-catalog.md
```

## Completion Criteria

- [ ] System boundary is explicit.
- [ ] Actors are external to the modeled system boundary.
- [ ] Relevant human and external-system actors are represented.
- [ ] Actors are not invented.
- [ ] Multiple-actor responsibilities are distinguished.
- [ ] Privilege boundaries are explicit where relevant.
- [ ] Use cases are actor-goal oriented.
- [ ] Granularity is neither “manage everything” nor UI-click-level.
- [ ] Stable use-case IDs/statuses exist.
- [ ] Each written use case has primary actor and goal.
- [ ] Preconditions are business/system facts.
- [ ] Trigger is explicit where relevant.
- [ ] Main success flow is system-behavior-level.
- [ ] Alternative flows are meaningful and requirement-backed.
- [ ] Failure flows are represented for critical cases when supported.
- [ ] Postconditions are explicit.
- [ ] Business rules are referenced rather than duplicated.
- [ ] External actors remain product-level, not protocol-level.
- [ ] Include is used only for meaningful mandatory reusable use cases.
- [ ] Extend is used only for meaningful optional/conditional extensions.
- [ ] Include/extend are not used as generic code reuse.
- [ ] Use-case generalization is used sparingly.
- [ ] Diagram is created only when it adds clarity.
- [ ] Diagram shows actors/capabilities/system boundary rather than sequence.
- [ ] Capability/privilege matrix exists when useful.
- [ ] FR/goal/journey/AC traceability exists.
- [ ] Coverage audit identifies missing/blocked use cases.
- [ ] NFR references do not leak detailed quality design into flows.
- [ ] Brownfield behavior is preserved only when authoritative.
- [ ] UI/API/architecture/sequence implementation leakage is removed.
- [ ] Process-flow candidates are identified.
- [ ] State-machine candidates are identified.
- [ ] Sequence candidates are identified.
- [ ] Final readiness is explicit.

## References

- Read `references/use-case-boundary-actors-goals-and-granularity.md` first.
- Read `references/preconditions-triggers-main-alternative-failure-and-postconditions.md`.
- Read `references/privilege-boundaries-multiple-actors-and-external-actors.md`.
- Read `references/include-extend-generalization-and-diagram-discipline.md`.
- Read `references/traceability-coverage-business-rules-and-nfr-links.md`.
- Read `references/brownfield-and-modeling-handoffs.md`.
- Read `references/use-case-model-audit.md` before completion.
