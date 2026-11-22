---
name: defining-functional-requirements
description: Converts accepted or review-ready PRD goals, journeys, product decisions, and functional candidates into a stable catalog of explicit, atomic, traceable, and testable functional requirements. Use after a PRD exists and before detailed use-case modeling, process-flow modeling, architecture design, user-story decomposition, or OpenSpec specification. For each requirement, identify actor, trigger, preconditions, required system behavior, observable outcome, postconditions, important alternatives/failures, source, status, and priority when authoritative. Split ambiguous compound behavior, preserve unresolved decisions, and avoid implementation or architecture detail. Do not invent behavior, silently resolve product questions, encode NFRs as functional requirements, or use mandatory language without accepted authority.
---

# Defining Functional Requirements

## Purpose

Turn PRD-level product intent into an explicit functional requirements catalog.

Core workflow:

```text
PRD
→ identify functional behavior
→ normalize actors + triggers
→ split compound behavior
→ define preconditions
→ define required behavior
→ define observable outcome
→ define postconditions
→ capture alternatives/failures
→ preserve decision/status/priority
→ trace to PRD goals + journeys
→ audit completeness/ambiguity
→ produce FR catalog
```

Output:

```text
functional-requirements-catalog.md
```

## Core Principle

A functional requirement describes:

```text
who/what initiates behavior
under what trigger/conditions
what the system must do
what observable result occurs
```

without prescribing implementation.

## Use When

- A PRD is ready enough for formal functional decomposition.
- Product goals and journeys need explicit system behaviors.
- A capability needs stable requirement IDs before modeling use cases.
- Functional scope must be traced into stories/OpenSpec/tests.
- Acceptance criteria need a requirements basis.
- Functional behavior spans humans and external systems.
- Permission and failure behavior must be formalized.

## Do Not Use When

- Product discovery is still vague.
- No PRD or equivalent accepted product context exists.
- The task is to define NFRs or quality attributes.
- The task is to model use cases/sequence diagrams.
- The task is to design APIs or architecture.
- The task is to write user stories directly from a vague request.
- The task is to choose technologies.

## Inputs

Preferred:

- PRD;
- goals;
- non-goals;
- actor map;
- user/system journeys;
- product decisions;
- PRD acceptance criteria;
- discovery traceability;
- unresolved questions/conflicts;
- applicable `AGENTS.md`.

Optional:

- existing functional requirements catalog;
- legacy-system behavior;
- policy/business-rule documents;
- external-provider behavior;
- accepted product prioritization.

## Outputs

- Functional requirements catalog.
- Requirement traceability matrix.
- Ambiguity/conflict ledger.
- Coverage matrix across PRD goals/journeys.
- Handoff notes for use cases, process flows, architecture, stories, OpenSpec, and testing.

# Requirement Identity

Use stable IDs:

```text
FR-001
FR-002
FR-003
```

Do not reuse an ID for a different semantic requirement.

If a requirement is retired:

```text
DEPRECATED
SUPERSEDED
REJECTED
```

Preserve its historical identity.

# Requirement Status

Use:

```text
PROPOSED
REVIEW_REQUIRED
ACCEPTED
DEFERRED
REJECTED
SUPERSEDED
```

Only mark `ACCEPTED` with authoritative evidence.

# Requirement Priority

Use the product's accepted prioritization scheme.

If unknown:

```text
TBD
```

Do not invent priority.

# Modal Language

Use mandatory language only when status/authority supports it.

Examples:

```text
ACCEPTED + mandatory
→ "The system must..."

PROPOSED
→ "The proposed behavior is..."
```

Do not use `MUST` to create false certainty.

# Requirement Anatomy

Each material FR should include:

```text
ID
title
status
priority
actor
trigger
preconditions
required behavior
observable outcome
postconditions
important alternatives
important failures
business rules / policy references
source / provenance
linked goals
linked journeys
linked PRD acceptance criteria
open questions
```

# Functional vs Non-Functional

Functional:

```text
what behavior occurs
```

Non-functional:

```text
how well / under what quality constraint
```

Example:

```text
FR:
The system returns the conversation list available to the agent.

NFR:
The conversation list meets the accepted latency target.
```

Do not merge them into one requirement unless the quality condition is itself inseparable product behavior.

# Step 1 — Establish Authoritative PRD Scope

Record:

```text
PRD version/status
goals
non-goals
accepted product decisions
actors
journeys
functional candidates
blocking questions
```

Do not formalize excluded scope.

# Step 2 — Extract Functional Behavior Candidates

Sources may include:

```text
PRD functional section
journeys
acceptance criteria
product decisions
business rules
brownfield preservation rules
external-system capabilities
```

Do not derive unrelated features from general domain knowledge.

# Step 3 — Normalize Actors

For each behavior identify the initiating actor or system actor.

Examples:

```text
support agent
tenant admin
end customer
identity provider
scheduled process
payment provider
```

If no actor/initiator can be determined:

```text
ACTOR_REQUIRED
```

Do not invent one.

# Actor vs Authority

The actor initiating a behavior is not necessarily the authority defining the rule.

Keep them distinct.

# Step 4 — Identify Trigger

A trigger answers:

```text
What event/request starts the behavior?
```

Examples:

```text
agent selects "Resolve"
provider sends callback
scheduled retention job runs
user submits upgrade confirmation
```

If behavior is continuous/passive, describe the condition rather than forcing an event.

# Step 5 — Split Compound Requirements

Bad:

```text
FR-001:
Agents can view, reply to, reassign, resolve, and export conversations.
```

Unless these are one indivisible transaction, split into atomic FRs.

Prefer:

```text
FR-001 view conversation
FR-002 reply
FR-003 add internal note
FR-004 resolve
FR-005 manager reassign
```

# Atomicity Rule

One FR should normally have one primary behavioral obligation.

Alternatives/failures may belong to the same FR when they are part of that behavior.

# Do Not Oversplit

Do not create separate FRs for trivial internal substeps.

Bad:

```text
FR-101 open modal
FR-102 render button
FR-103 call function
```

unless those are actual product requirements.

# Step 6 — Define Preconditions

Preconditions are facts that must already hold before the behavior applies.

Examples:

```text
conversation exists
subscription is active
actor is authenticated
payment session is pending
```

Do not encode implementation state like:

```text
React hook has loaded
```

# Authorization Preconditions

Be careful with permission language.

Possible:

```text
Precondition:
actor has the accepted product permission to perform reassignment
```

The later security/architecture specification decides enforcement details.

# Step 7 — Define Required Behavior

Behavior should be:

- observable;
- unambiguous enough to test;
- solution-neutral where practical;
- tied to actor/trigger/context.

Example:

```text
When a support agent submits a reply to an open conversation,
the system records the reply as part of that conversation
and makes it available to authorized participants.
```

Do not say:

```text
POST /api/messages
```

unless API shape itself is an accepted product/public requirement.

# Step 8 — Define Outcome

Outcome answers:

```text
What product/system state is observable after success?
```

Examples:

```text
conversation is marked resolved
assignment changes to selected agent
upgrade request is created
AI suggestion is displayed
```

# Step 9 — Define Postconditions

Postconditions are stable facts after completion.

Examples:

```text
resolved_at is conceptually set
new assignee owns the conversation
current entitlement remains unchanged after payment cancel
```

Avoid database-column language unless externally meaningful.

# Step 10 — Alternative Paths

Capture important valid alternatives.

Examples:

```text
AI unavailable
→ manual reply remains available

payment cancelled
→ subscription remains unchanged
```

Do not write every UI branch.

# Step 11 — Failure Paths

Capture failures that materially alter behavior.

Examples:

```text
permission denied
resource not found
conflicting state
provider unavailable
validation rejected
```

Do not invent technical status codes unless accepted elsewhere.

# Failure Requirement Rule

A failure path may be:

```text
inside the primary FR
```

when it is tightly tied to that action.

Use separate FR when failure behavior is independently significant/reusable.

# Step 12 — Conditional Behavior

Roadmap evaluation:

For conditional requirements explicitly identify:

```text
condition
branch A
branch B
observable outcomes
```

Example:

```text
If AI is available:
→ system may provide suggestion.

If AI is unavailable:
→ manual reply workflow remains available.
```

Avoid hidden conditions inside prose.

# Step 13 — External Integration Behavior

Roadmap evaluation:

Define product-level interaction, not protocol design.

Example:

```text
When the email provider delivers a new inbound customer message,
the system associates it with the appropriate organization/conversation
or records a processing failure according to accepted behavior.
```

Later architecture/API/event design decides mechanics.

# External Failure

Capture provider unavailable/invalid response behavior only if product requirements support it.

# Step 14 — Permissions

Roadmap evaluation:

Functional permission requirements should state:

```text
who may perform what behavior on what scope
```

Example:

```text
Only organization managers may reassign conversations within their organization.
```

Do not specify middleware/claims/token implementation.

# Authorization Ownership

Functional requirement:

```text
business capability rule
```

Security architecture later verifies authoritative enforcement.

# Step 15 — Failure Behavior

Roadmap evaluation:

A functional catalog must not contain only happy paths.

For critical mutations capture:

```text
validation failure
permission failure
conflict
provider failure
cancel/retry if product-visible
```

when supported by source.

# Step 16 — Ambiguous Requirement

Roadmap evaluation:

If PRD says:

```text
AI answers must always be correct
```

do not normalize it into a formal FR.

Use:

```text
AMBIGUOUS_OR_UNTESTABLE
```

with a clarification question.

# Ambiguity Classes

Use:

```text
ACTOR_AMBIGUOUS
TRIGGER_AMBIGUOUS
BEHAVIOR_AMBIGUOUS
OUTCOME_AMBIGUOUS
SCOPE_AMBIGUOUS
PRIORITY_AMBIGUOUS
CONDITION_AMBIGUOUS
UNTESTABLE_LANGUAGE
CONFLICTING_SOURCE
```

# Ambiguous Terms

Flag words like:

```text
easy
fast
intuitive
seamless
smart
always correct
support all
real-time
```

unless context makes them operationally clear.

Some belong to NFR/quality rather than FR.

# Step 17 — Business Rules

If a behavior relies on a product/business rule, link it.

Example:

```text
BR-001:
Only active subscriptions are eligible for upgrade.
```

Do not create a full Domain model yet.

Business rules may later feed:

```text
modeling-use-cases
designing-system-architecture
OpenSpec
```

# Business Rule vs FR

Business rule:

```text
constraint on valid behavior/state
```

FR:

```text
system behavior applying that rule
```

Do not conflate them.

# Step 18 — State Changes

When functional behavior changes lifecycle state, record semantic before/after.

Example:

```text
ACTIVE
→ RESOLVED
```

Do not create full state machine here.

Flag candidates for:

```text
modeling-state-machines
```

# Step 19 — Data Effects

Capture product-visible data effects:

```text
conversation retains internal note
assignment is updated
audit record is available
```

Do not create ERD/schema.

Flag data-model candidates for:

```text
modeling-domain-data
```

# Step 20 — Audit / Notification Behavior

If audit/notification is functionally required, make it explicit.

Example:

```text
When a manager reassigns a conversation,
the system records an auditable reassignment event.
```

Do not hide audit behavior only inside NFRs if it is an observable required capability.

# Step 21 — Batch / Scheduled / Automated Behavior

System actors can trigger FRs.

Example:

```text
When the approved retention period expires,
the retention process handles data according to accepted policy.
```

If policy is unresolved, do not create final behavior.

Use:

```text
PRODUCT_DECISION_REQUIRED
```

# Step 22 — Brownfield Preservation

For existing behavior classified:

```text
MUST_PRESERVE
```

create or retain requirements when that preservation matters.

Do not assume undocumented legacy quirks are requirements.

# Step 23 — Traceability

Each FR should trace to:

```text
PRD goal
journey
PRD requirement/candidate
PRD AC
source/discovery ID
```

This supports downstream:

```text
FR
→ use case
→ process/state/sequence model
→ OpenSpec
→ user story
→ tests
```

# Step 24 — Coverage Matrix

Audit every relevant PRD goal/journey.

Statuses:

```text
COVERED
PARTIALLY_COVERED
NO_FUNCTIONAL_REQUIREMENT_NEEDED
MISSING_FUNCTIONAL_REQUIREMENT
BLOCKED_BY_PRODUCT_DECISION
```

Do not create FRs just to force 100% numerical coverage.

# Step 25 — Acceptance Criteria Link

PRD ACs can map to one or more FRs.

Do not copy AC text as FR automatically.

Example:

```text
AC:
Manager can reassign conversation and change is visible.

May map to:
FR-010 permission to request reassignment
FR-011 system performs reassignment
FR-012 system exposes updated assignment
```

only when those are truly independent obligations.

# Step 26 — Requirement Dependencies

Record dependencies among FRs only when meaningful.

Example:

```text
FR-020 payment confirmation
depends on FR-018 payment initiation
```

Avoid implementation-order dependencies.

# Step 27 — Requirement Conflicts

If two FR candidates conflict, do not choose one.

Use:

```text
FUNCTIONAL_CONFLICT_REQUIRES_PRODUCT_DECISION
```

# Step 28 — Duplicate Detection

Merge semantically duplicate candidate requirements.

Preserve all source references.

Do not merge similar but distinct actor/scope behavior.

# Step 29 — Granularity Audit

Too broad:

```text
manage customers
```

Too narrow:

```text
click submit button
```

Better:

```text
create customer record
update customer contact details
archive customer record
```

at product/system behavior level.

# Step 30 — Testability Audit

Ask for each FR:

```text
Can an observer determine whether this behavior occurred correctly?
```

If not:

```text
REQUIRES_CLARIFICATION
```

Do not invent missing expected result.

# Step 31 — Architecture Leakage Audit

Remove/relocate details such as:

```text
microservice
Kafka topic
PostgreSQL table
React Query
REST controller
Redis cache
Kubernetes
```

unless explicitly part of accepted external/product contract or hard constraint.

# Step 32 — UI Leakage Audit

A product requirement may require:

```text
user can select a plan
```

but not necessarily:

```text
use a dropdown
```

unless the UI control itself is an accepted design/product requirement.

# Step 33 — API Leakage Audit

Avoid endpoint/method/status design unless already an accepted public contract.

Use:

```text
system rejects conflicting upgrade request
```

rather than:

```text
return 409
```

until specification/API design owns it.

# Step 34 — NFR Leakage Audit

Move quality statements such as:

```text
within 200ms
99.99% uptime
WCAG AA
```

to NFR catalog unless the functional behavior cannot be understood without them.

Cross-reference rather than duplicate.

# Functional Requirement Record

Use `assets/functional-requirements-catalog.md`.

# Requirement Quality Status

Per requirement:

```text
READY
READY_WITH_OPEN_QUESTION
REQUIRES_CLARIFICATION
REQUIRES_PRODUCT_DECISION
CONFLICTED
DEFERRED
```

# Catalog Final Decision

Use:

```text
FUNCTIONAL_REQUIREMENTS_READY
FUNCTIONAL_REQUIREMENTS_READY_WITH_OPEN_QUESTIONS
FUNCTIONAL_REQUIREMENTS_REQUIRE_PRD_DECISION
FUNCTIONAL_REQUIREMENTS_REQUIRE_CLARIFICATION
FUNCTIONAL_REQUIREMENTS_CONFLICTED
BLOCKED
```

# Handoff

Potential downstream consumers:

```text
modeling-use-cases
modeling-process-flows
modeling-state-machines
defining-non-functional-requirements
identifying-architecture-drivers
creating/editing OpenSpec changes
enriching-user-stories
planning stack vertical slices
test strategy
```

# Use Case Candidate Detection

Flag FR groups that share:

```text
actor
goal
trigger
business outcome
```

for:

```text
modeling-use-cases
```

# Process Flow Candidate Detection

Flag decision-heavy FR groups for:

```text
modeling-process-flows
```

# State Machine Candidate Detection

Flag lifecycle-heavy FR groups for:

```text
modeling-state-machines
```

# Architecture Input

The FR catalog is architecture input.

It is not architecture.

# Final Output Requirements

The catalog must include:

```text
document control
scope
actor glossary
functional requirements
business rules
ambiguities/conflicts
coverage matrix
traceability matrix
modeling handoff
final readiness
```

## Completion Criteria

- [ ] PRD version/status is recorded.
- [ ] Non-goals/excluded scope are respected.
- [ ] Stable FR IDs are assigned.
- [ ] Requirement status and priority preserve authority.
- [ ] Mandatory modality is not invented.
- [ ] Relevant actors are explicit.
- [ ] Missing actors are flagged rather than invented.
- [ ] Triggers are explicit when applicable.
- [ ] Compound behaviors are split when they represent independent obligations.
- [ ] Requirements are not oversplit into implementation steps.
- [ ] Preconditions are product/system conditions rather than implementation state.
- [ ] Required behavior is observable and solution-neutral where practical.
- [ ] Outcomes and postconditions are explicit when material.
- [ ] Important alternative paths are represented.
- [ ] Important failure behavior is represented.
- [ ] Conditional behavior exposes its conditions/branches.
- [ ] External integration requirements stay at product behavior level.
- [ ] Permission requirements identify actor, action, and scope.
- [ ] Ambiguous or untestable language is flagged.
- [ ] Business rules are linked but not confused with FRs.
- [ ] State/data effects are captured semantically without designing state machines/ERDs.
- [ ] Brownfield preservation is included only when supported.
- [ ] Requirements trace to PRD goals/journeys/ACs/sources.
- [ ] PRD coverage matrix exists.
- [ ] Duplicate requirements are consolidated.
- [ ] Conflicts remain unresolved until authoritative decision.
- [ ] Testability is audited.
- [ ] Architecture/API/UI implementation leakage is removed unless contractually required.
- [ ] NFR content is cross-referenced instead of duplicated.
- [ ] Use-case/process-flow/state-machine candidates are identified.
- [ ] Catalog readiness is explicit.

## References

- Read `references/functional-requirement-anatomy-atomicity-and-modality.md` first.
- Read `references/actors-triggers-preconditions-outcomes-and-postconditions.md`.
- Read `references/conditional-alternative-failure-and-permission-behavior.md`.
- Read `references/external-integrations-business-rules-state-and-data-effects.md`.
- Read `references/ambiguity-testability-and-implementation-leakage.md`.
- Read `references/traceability-coverage-duplicates-and-conflicts.md`.
- Read `references/brownfield-and-downstream-modeling-handoffs.md`.
- Read `references/functional-requirements-catalog-audit.md` before completion.
