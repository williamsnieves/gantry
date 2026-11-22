---
name: modeling-process-flows
description: Models business workflows, decision trees, validation chains, approvals, retries, fallbacks, manual/automated handoffs, and operational procedures as clear process flows or flowcharts. Use after functional requirements/use cases exist when the key question is how process logic branches and proceeds, not how system participants interact over time or how an entity transitions between lifecycle states. Produce process-flow models with explicit start/end, actors/swimlanes when useful, activities, decisions, conditions, loops, failure/fallback paths, and traceability. Do not turn flowcharts into sequence diagrams, state machines, architecture diagrams, UI click scripts, or implementation internals; do not invent branch rules or retry policies.
---

# Modeling Process Flows

## Purpose

Model process and decision logic clearly.

Core workflow:

```text
requirements / use cases
→ choose process scope
→ identify start/end
→ identify activities
→ identify decisions and conditions
→ identify loops/retries
→ identify manual/automated handoffs
→ identify fallback/failure paths
→ assign ownership/swimlanes when useful
→ produce flowchart
→ validate reachability/completeness
```

Output:

```text
process-flow-model.md
```

## Core Principle

A process flow answers:

```text
what happens next?
under what condition?
who/what performs the step?
where can the process branch, loop, fail, or terminate?
```

It does not primarily answer:

```text
who can do what?           → use cases
how participants interact? → sequence diagrams
what states are valid?     → state machines
what components exist?     → C4
```

## Use When

- A use case has important conditional branching.
- Business approval or validation logic needs visualization.
- Retry/fallback behavior matters.
- A manual and automated workflow interact.
- An onboarding/business process has several decisions.
- An operational runbook/procedure needs logic flow.
- A product workflow has loops, rejection paths, escalation, or cancellation.
- A complex use case is easier to reason about visually as a decision process.

## Do Not Use When

- The main question is actors/capabilities; use `modeling-use-cases`.
- The main question is entity lifecycle/valid transitions; use `modeling-state-machines`.
- The main question is ordered interaction between frontend/API/services/providers; use `modeling-system-sequences`.
- The main question is architecture structure; use `modeling-c4-architecture`.
- The task is implementation control flow inside code.
- The task is BPMN-specific compliance unless explicitly requested.

## Inputs

Preferred:

- functional requirements catalog;
- use-case catalog;
- business rules;
- product decisions;
- failure/alternative flows;
- permission rules;
- external-system behavior;
- operational procedures;
- relevant NFR/QA references;
- applicable `AGENTS.md`.

Optional:

- existing flowcharts;
- legacy process docs;
- policy/approval rules;
- support/runbook procedures;
- SLA/escalation rules.

## Outputs

- Process Flow Model.
- Flow boundary/scope.
- Activity/decision catalog.
- Swimlane/ownership mapping when useful.
- Branch-condition ledger.
- Loop/retry/fallback ledger.
- Dead-end/unreachable-path audit.
- Traceability to FRs/use cases/business rules.
- Handoff to state-machine and sequence modeling.

# Process Flow Identity

Use stable IDs:

```text
PF-001
PF-002
PF-003
```

# Flow Status

Use:

```text
PROPOSED
REVIEW_REQUIRED
ACCEPTED
DEFERRED
REJECTED
SUPERSEDED
```

# Flow Anatomy

Each flow should include:

```text
ID
title
scope
trigger/start
end conditions
participants/owners
activities
decisions
branch conditions
loops/retries
failure/fallback paths
manual/automated handoffs
business rules
linked use cases/FRs
open questions
```

# Step 1 — Define the Process Question

State exactly what the flow is trying to explain.

Good:

```text
How does a manager reassign a conversation,
including scope validation and invalid-target handling?
```

Bad:

```text
How does the whole support platform work?
```

Keep flows bounded.

# Step 2 — Define Start and End

Every process flow needs:

```text
START
one or more valid END outcomes
```

Possible end types:

```text
SUCCESS
REJECTED
CANCELLED
FAILED
ESCALATED
DEFERRED
```

Do not leave dangling branches.

# Step 3 — Identify Activities

An activity is meaningful process work.

Examples:

```text
manager selects target agent
system validates same-organization rule
agent provides manual reply
operator reviews failed ingestion
```

Avoid internal implementation steps like:

```text
call function
serialize JSON
write DB row
```

unless the process itself is technical/operational and that detail is the subject.

# Step 4 — Identify Decisions

Decisions should be explicit questions with mutually understandable branches.

Example:

```text
Target agent belongs to same organization?
├── yes
└── no
```

Do not label a diamond:

```text
Validate
```

without expressing the condition.

# Step 5 — Decision Branch Labels

Prefer:

```text
Yes / No
Valid / Invalid
Approved / Rejected
Available / Unavailable
```

or domain-specific labels.

Every outgoing branch should be understandable.

# Step 6 — Conditions

Trace branch conditions to:

```text
business rules
functional requirements
product decisions
policy
```

Do not invent conditions.

# Step 7 — Conditional Branching

Roadmap evaluation:

Model explicit branching where outcomes differ materially.

Example:

```text
AI available?
├── yes → offer AI suggestion
└── no  → continue manual reply
```

Do not branch on implementation conditions that users/business do not care about.

# Step 8 — Validation Flows

Useful pattern:

```text
input/request
→ validate preconditions
→ validate scope/permission
→ validate business rules
→ proceed or reject
```

But do not imply a mandatory validation order unless requirements/policy require it.

# Step 9 — Retry Loops

Roadmap evaluation:

Represent retries only when retry behavior is accepted.

Record:

```text
retry trigger
max attempts / deadline if known
backoff if product/operationally relevant
terminal outcome
```

If policy is unknown:

```text
RETRY_POLICY_REQUIRED
```

Do not invent “3 retries”.

# Step 10 — Loop Safety

Every loop should have:

```text
entry condition
continuation condition
exit condition
```

Avoid infinite/undefined loops.

# Step 11 — Manual Approval

Roadmap evaluation:

Represent:

```text
request
→ waiting/pending
→ human reviewer decision
→ approved/rejected/needs changes
```

If timing/escalation is unspecified, mark it.

Do not invent approval SLA.

# Step 12 — Manual/Automated Handoffs

Use swimlanes or owner labels when the process crosses:

```text
user
manager
system
operator
external provider
```

This clarifies responsibility.

# Step 13 — Swimlanes

Use swimlanes when ownership transitions are important.

Example:

```text
Manager | Support Platform | Target Agent
```

Do not add swimlanes if all steps belong to one actor/system and they add clutter.

# Step 14 — Failure Fallback

Roadmap evaluation:

Example:

```text
AI provider unavailable
→ manual reply fallback
```

or:

```text
payment provider unavailable
→ preserve current subscription
→ show retry-later outcome
```

Fallback must come from requirements.

# Step 15 — Degraded Mode

Represent a degraded path when a capability remains partially available.

Example:

```text
external provider down
→ read-only existing data remains available
```

Do not design how degradation is implemented.

# Step 16 — Cancellation

If process can be cancelled, identify:

```text
who can cancel
when
what outcome/state remains
```

Do not invent cancel behavior.

# Step 17 — Escalation

Operational/business flows may have:

```text
retry exhausted
→ escalate to operator
```

Only when supported.

# Step 18 — Time-Based Decisions

Possible:

```text
deadline reached?
approval timeout?
retention period expired?
```

Only use accepted time/policy values.

# Step 19 — Parallel Activities

Use parallel branches only when activities may/should proceed independently.

Do not imply concurrency unless supported.

If ordering matters, keep sequential.

# Step 20 — Merge / Join

Make it clear where branches rejoin.

Avoid ambiguous converging arrows.

# Step 21 — Error vs Rejection

Distinguish:

```text
business rejection
validation rejection
system failure
dependency failure
cancel
```

when outcomes differ.

# Step 22 — Process State vs Entity State

A flow can mention process states like:

```text
pending approval
waiting for input
```

but if the core question becomes valid lifecycle transitions:

```text
OPEN → RESOLVED → REOPENED
```

handoff to:

```text
modeling-state-machines
```

# Step 23 — Process Flow vs Sequence Diagram

If the model starts focusing on:

```text
Frontend → API → Service → DB → Provider
```

it has become a sequence diagram.

A process flow focuses on:

```text
activities
decisions
conditions
outcomes
```

Participants may be shown, but timing/messages are secondary.

# Step 24 — Process Flow vs Use Case

Use case:

```text
actor goal and structured behavior
```

Process flow:

```text
decision/process logic inside/across one or more use cases
```

Do not replace all written use cases with flowcharts.

# Step 25 — Process Flow vs State Machine

Flowchart:

```text
workflow logic
```

State machine:

```text
entity/system lifecycle and legal transitions
```

# Step 26 — Flowchart Syntax

Prefer version-control-friendly formats.

Preferred:

```text
Mermaid flowchart
PlantUML activity diagram
```

Use the format best suited to repository/tooling.

# Step 27 — Mermaid Discipline

Use meaningful node IDs and labels.

Example:

```text
flowchart TD
    A[Manager requests reassignment]
    B{Target agent in same organization?}
    C[Reassign conversation]
    D[Reject reassignment]

    A --> B
    B -->|Yes| C
    B -->|No| D
```

Avoid excessively long labels.

# Step 28 — PlantUML Activity Diagrams

Use when:

```text
swimlanes
fork/join
more formal activity semantics
```

are useful.

# Step 29 — Diagram Split

If a flow has too many nodes/branches:

```text
split by sub-process or capability
```

Do not produce unreadable mega-flowcharts.

# Step 30 — Subflows

A subflow is appropriate when:

```text
it is meaningful on its own
reused by several process flows
or hides detail while preserving clarity
```

Do not create subflows for trivial steps.

# Step 31 — Business Rule Linking

Decision nodes should reference rules.

Example:

```text
D2: Same organization?
Rule: BR-003
```

# Step 32 — Traceability

Each flow/activity/decision should trace where useful to:

```text
UC
FR
business rule
PRD decision
NFR/QA
```

# Step 33 — Coverage

For each selected use case/FR:

```text
FLOW_COVERED
PARTIALLY_COVERED
NO_PROCESS_FLOW_NEEDED
MISSING_FLOW
BLOCKED_BY_DECISION
```

Not every use case needs a flowchart.

# Step 34 — Decision Completeness Audit

For every decision:

```text
are all meaningful outcomes represented?
```

Example:

```text
payment result
```

may require:

```text
success
failure
cancelled
pending
```

if requirements support them.

Do not force binary yes/no when domain has more outcomes.

# Step 35 — Reachability Audit

Verify:

```text
every node reachable?
every branch terminates/rejoins?
any orphan nodes?
any impossible path?
```

# Step 36 — Dead-End Audit

A dead end is acceptable only if it is an explicit terminal outcome.

Otherwise flag:

```text
FLOW_DEAD_END
```

# Step 37 — Loop Audit

Check:

```text
retry has exit?
manual rework has termination?
approval loop can finish?
```

# Step 38 — Contradiction Audit

Check flow against requirements.

Example:

```text
flow allows agent reassignment
but BR says manager only
```

Flag:

```text
FLOW_REQUIREMENT_CONFLICT
```

# Step 39 — Unspecified Branch Behavior

Use:

```text
BRANCH_BEHAVIOR_REQUIRED
```

when requirements do not define what happens.

Do not guess.

# Step 40 — Retry Policy Gap

Use:

```text
RETRY_POLICY_REQUIRED
```

when a retry is implied but attempts/timing/terminal behavior matter and are unspecified.

# Step 41 — Approval Policy Gap

Use:

```text
APPROVAL_POLICY_REQUIRED
```

when reviewer/criteria/timeout/escalation are unclear.

# Step 42 — UI Leakage Audit

Remove unnecessary:

```text
click button
modal opens
dropdown
toast
```

unless UX behavior itself is the process being modeled.

# Step 43 — Architecture Leakage Audit

Remove:

```text
queue
cache
microservice
database
controller
worker
Kafka
```

unless modeling an operational/technical process where those are intentionally in scope and already accepted architecture.

# Step 44 — Implementation Control Flow Audit

Do not model:

```text
if variable == null
for each item
try/catch
```

unless the user explicitly asks for algorithm/code flow.

# Step 45 — State-Machine Handoff

Flag when flow reveals:

```text
stable states
allowed transitions
forbidden transitions
events/guards
```

for:

```text
modeling-state-machines
```

# Step 46 — Sequence Handoff

Flag when flow involves several participants/external systems and timing/order matters.

Later:

```text
modeling-system-sequences
```

# Step 47 — Architecture Input

Process flows can reveal:

```text
long-running workflows
manual handoffs
external dependency pressure
retry/failure requirements
approval boundaries
```

but do not design architecture.

# Flow Quality Status

Use:

```text
READY
READY_WITH_OPEN_QUESTIONS
REQUIRES_BRANCH_RULE
REQUIRES_RETRY_POLICY
REQUIRES_APPROVAL_POLICY
REQUIRES_REQUIREMENT_CLARIFICATION
CONFLICTED
```

# Final Decision

Use:

```text
PROCESS_FLOW_MODEL_READY
PROCESS_FLOW_MODEL_READY_WITH_OPEN_QUESTIONS
PROCESS_FLOW_MODEL_REQUIRES_BRANCH_RULE
PROCESS_FLOW_MODEL_REQUIRES_RETRY_POLICY
PROCESS_FLOW_MODEL_REQUIRES_APPROVAL_POLICY
PROCESS_FLOW_MODEL_REQUIRES_REQUIREMENT_CLARIFICATION
PROCESS_FLOW_MODEL_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/process-flow-model.md
```

## Completion Criteria

- [ ] Flow scope/question is explicit.
- [ ] Start and terminal outcomes are explicit.
- [ ] Activities are meaningful process steps.
- [ ] Decisions are expressed as understandable conditions.
- [ ] Outgoing decision branches are labeled.
- [ ] Conditions trace to requirements/rules.
- [ ] Conditional branching models product/business logic, not implementation trivia.
- [ ] Retry loops are modeled only when supported.
- [ ] Retry loops have explicit exit/terminal behavior or a gap is flagged.
- [ ] Manual approvals identify reviewer/decision flow when known.
- [ ] Manual/automated handoffs are clear.
- [ ] Swimlanes are used only when ownership clarity benefits.
- [ ] Failure/fallback/degraded paths are represented where supported.
- [ ] Cancellation/escalation/time-based paths are not invented.
- [ ] Parallelism is shown only when supported.
- [ ] Branch merges/joins are readable.
- [ ] Business rejection vs system/dependency failure is distinguished when needed.
- [ ] Process flow is not a disguised sequence diagram.
- [ ] Process flow is not a substitute for use-case modeling.
- [ ] Lifecycle-heavy logic is handed to state-machine modeling.
- [ ] Diagram syntax is version-control friendly.
- [ ] Mega-flows are split when necessary.
- [ ] Business rules are referenced.
- [ ] Traceability exists.
- [ ] Only relevant use cases/FRs are flow-modeled.
- [ ] Decisions are complete for supported domain outcomes.
- [ ] Reachability/dead-end/loop audits pass.
- [ ] Requirement contradictions are surfaced.
- [ ] Unspecified branch/retry/approval behavior remains explicit.
- [ ] UI/architecture/implementation control-flow leakage is removed.
- [ ] State-machine and sequence candidates are identified.
- [ ] Final readiness is explicit.

## References

- Read `references/process-flow-purpose-scope-and-diagram-selection.md` first.
- Read `references/activities-decisions-conditions-and-branch-completeness.md`.
- Read `references/loops-retries-approvals-fallbacks-and-handoffs.md`.
- Read `references/swimlanes-parallelism-subflows-and-diagram-discipline.md`.
- Read `references/traceability-reachability-deadends-and-conflicts.md`.
- Read `references/process-vs-usecase-state-sequence-and-architecture.md`.
- Read `references/process-flow-model-audit.md` before completion.
