---
name: eliciting-software-requirements
description: Turns an initial product, system, platform, integration, or architecture idea into a structured software-requirements discovery record. Use at the beginning of greenfield work or architecture-significant change when stakeholders, actors, goals, functional needs, non-functional expectations, constraints, assumptions, dependencies, risks, success conditions, or open questions are incomplete. Separate source-confirmed facts from stakeholder statements, analyst inferences, assumptions, candidate requirements, and unresolved decisions. Produce discovery evidence for a later PRD and architecture process. Do not design the architecture, choose technologies, invent product policy, write the final PRD, or prematurely convert every statement into an accepted requirement.
---

# Eliciting Software Requirements

## Purpose

Turn an incomplete product/system idea into a trustworthy requirements-discovery record.

Core workflow:

```text
initial idea
→ identify sources/stakeholders
→ clarify problem and outcomes
→ identify actors
→ discover behaviors
→ discover quality expectations
→ identify constraints
→ identify assumptions/dependencies/risks
→ expose conflicts and unknowns
→ classify candidate requirements
→ determine discovery readiness
```

This skill produces input for:

```text
creating-product-requirement-documents
```

It does not create the final PRD.

## Core Principle

Every statement must preserve its epistemic status.

Do not collapse:

```text
stakeholder statement
assumption
inference
candidate requirement
accepted requirement
```

into the same category.

Use explicit provenance and confidence.

## Use When

- Starting a greenfield project.
- Starting a new platform/service.
- Starting an architecture-significant change.
- A product/system idea is still vague.
- Several stakeholders have different expectations.
- Functional needs are only partially known.
- Non-functional expectations are implicit or vague.
- Constraints may be hidden in organization, cloud, budget, regulation, legacy, or delivery context.
- Assumptions may be driving design prematurely.
- Success conditions are ambiguous.
- A PRD should be created, but discovery evidence is not yet structured.
- The architecture process needs a reliable requirements basis.

## Do Not Use When

- A mature PRD already contains implementation-ready requirements and only needs formatting.
- The task is to enrich one delivery user story; use `enriching-user-stories`.
- The task is to define architecture drivers from accepted requirements; use `identifying-architecture-drivers`.
- The task is to design candidate architectures.
- The task is to create OpenSpec changes.
- The task is to write code.
- The task is to choose technologies without requirements evidence.

## Inputs

Possible inputs:

- product idea;
- business brief;
- stakeholder notes;
- discovery transcript;
- existing product/system documentation;
- current architecture;
- support/customer evidence;
- existing process;
- legacy-system constraints;
- external-provider constraints;
- delivery/budget/team constraints;
- applicable `AGENTS.md`.

The skill MUST not require every input category.

## Outputs

- Requirement discovery context.
- Source/provenance ledger.
- Stakeholder map.
- Actor/persona candidates.
- Problem/outcome statement.
- Candidate user/system journeys.
- Candidate functional requirements.
- Candidate non-functional expectations.
- Constraints.
- Assumptions.
- Dependencies.
- Risks.
- Conflicts.
- Unknowns/open questions.
- Success-condition candidates.
- Discovery readiness.
- Handoff notes for PRD creation.
- `software-requirements-elicitation-record.md`.

# Discovery vs Specification

Discovery asks:

```text
What do we know?
What do stakeholders need?
What must the system do?
What qualities matter?
What constraints exist?
What is still uncertain?
```

Specification asks:

```text
What has been accepted as the required behavior?
```

This skill stays primarily in discovery.

# Provenance Model

For each material statement record:

```text
source
source type
statement
interpretation
status
confidence
```

Source types:

```text
USER_REQUEST
STAKEHOLDER
EXISTING_SYSTEM
CANONICAL_DOCUMENT
POLICY
EXTERNAL_PROVIDER
OBSERVATION
ANALYST_INFERENCE
ASSUMPTION
```

Do not claim `ANALYST_INFERENCE` as stakeholder intent.

# Statement Status

Use:

```text
CONFIRMED_FACT
STAKEHOLDER_NEED
CANDIDATE_REQUIREMENT
ASSUMPTION
INFERENCE
CONSTRAINT
DEPENDENCY
RISK
OPEN_QUESTION
CONFLICT
OUT_OF_SCOPE_CANDIDATE
```

These are discovery statuses, not final approval states.

# Confidence

Use:

```text
HIGH
MEDIUM
LOW
```

Confidence describes evidence clarity, not priority.

# Requirement Acceptance Boundary

This skill can produce:

```text
CANDIDATE_REQUIREMENT
```

but SHOULD NOT silently promote to:

```text
ACCEPTED_REQUIREMENT
```

unless the authoritative source explicitly states it is accepted and repository/product process allows that classification.

The PRD/specification process owns formal acceptance.

# Step 1 — Establish Discovery Scope

Record:

- system/product area;
- reason for discovery;
- greenfield vs brownfield;
- known stakeholders;
- authoritative input;
- deadline/context;
- what is explicitly out of scope.

Avoid a discovery session that expands into the whole organization.

# Step 2 — Clarify the Problem

Capture:

```text
current situation
problem/pain
affected actor
business/user impact
why now
desired outcome
```

Separate problem from proposed solution.

Bad:

```text
We need Kubernetes.
```

Possible underlying need:

```text
The service requires predictable deployment,
horizontal scaling, and isolated environments.
```

Do not discard the technology request; record it as a proposed solution or possible constraint and investigate its authority.

# Problem Statement

A useful problem statement includes:

```text
who
experiences what problem
in what context
with what impact
```

Avoid architecture/solution language unless it is truly a constraint.

# Step 3 — Identify Stakeholders

Stakeholders may include:

```text
end users
operators
support
security
legal/compliance
product
engineering
finance
sales
customer administrators
external partners
platform teams
```

Do not add generic stakeholder roles without evidence merely to fill a template.

# Stakeholder Record

For each relevant stakeholder:

```text
name/role
interest
goals
concerns
authority/decision rights
impact
source
```

# Decision Authority

Distinguish:

```text
stakeholder preference
decision-maker approval
regulatory/policy requirement
technical constraint
```

Conflicting requests require an explicit owner/decision.

# Step 4 — Identify Actors / Personas

Actors are entities interacting with the system.

Examples:

```text
tenant admin
end user
support agent
external payment provider
scheduled job
third-party API
```

Do not restrict “actor” to humans.

# Missing Actor Audit

For each behavior ask:

```text
who initiates it?
who receives the result?
who administers it?
what external system participates?
```

If no actor can be identified, the requirement may be underspecified.

# Persona Boundary

Create persona detail only when it changes requirements.

Do not generate fictional demographic personas as filler.

# Step 5 — Identify Goals and Outcomes

Capture:

```text
stakeholder goal
user outcome
business outcome
operational outcome
```

Distinguish output from outcome.

Example:

```text
Output:
new subscription-upgrade page

Outcome:
eligible tenant admins can complete upgrades without support intervention
```

# Goal Quality

A goal should be understandable without implying a particular implementation.

# Step 6 — Discover Journeys / Scenarios

Identify high-value behaviors end to end.

For each journey:

```text
actor
trigger
goal
happy path
important alternatives
failure conditions
outcome
```

Do not write detailed system sequence diagrams here; capture behavioral discovery only.

Later skills can model use cases, process flows, and sequences.

# Step 7 — Discover Functional Needs

Functional candidates describe observable system behavior.

Candidate structure:

```text
FR-CAND-001
Actor:
Trigger:
Behavior:
Outcome:
Evidence:
Open questions:
```

Use candidate IDs for traceability.

Do not use final FR numbering semantics if product governance assigns IDs later; the prefix makes discovery status clear.

# Functional Requirement Heuristics

Look for:

```text
create
view
update
delete
search
approve
reject
notify
integrate
calculate
authorize
export
import
schedule
retry
recover
audit
```

But do not convert every verb in a conversation into a requirement.

# Functional Completeness Questions

For each major behavior ask:

```text
who can do it?
when?
to what resource?
with what preconditions?
what is the result?
what can fail?
what happens on retry/cancel?
```

Only ask questions that materially affect requirements.

# Step 8 — Discover Non-Functional Expectations

Capture quality expectations without prematurely normalizing them into architecture decisions.

Potential areas:

```text
performance
availability
scalability
security
privacy
reliability
recoverability
observability
maintainability
modifiability
interoperability
accessibility
usability
cost
data residency
```

Use:

```text
NFR-CAND-001
Quality:
Expectation:
Measure known?:
Environment/context:
Source:
Open question:
```

# Vague Quality Language

If stakeholder says:

```text
must be fast
```

record:

```text
quality = performance
expectation = fast
measure = UNKNOWN
open question = what operation / percentile / target / load?
```

Do not invent `p95 < 200ms`.

# Security / Privacy Discovery

Capture needs such as:

```text
tenant isolation
sensitive data
authentication
authorization
auditability
retention
consent
data residency
third-party transfer
```

Do not perform threat modeling yet.

# Availability / Recovery Discovery

Ask only when relevant:

```text
acceptable downtime?
critical operating hours?
data-loss tolerance?
recovery expectation?
degraded mode?
```

Do not invent SLA/SLO/RTO/RPO.

# Scale Discovery

Prefer actual dimensions:

```text
users
tenants
requests/sec
concurrent connections
data volume
growth
batch size
geographies
```

Record unknown if unavailable.

# Step 9 — Identify Constraints

Constraints restrict the solution space.

Types:

```text
TECHNOLOGY
PLATFORM
CLOUD
LEGACY
BUDGET
TEAM
TIME
REGULATORY
POLICY
VENDOR
DATA
DEPLOYMENT
ORGANIZATIONAL
```

Constraint record:

```text
CON-001
constraint
source
authority
hard/soft
reason
consequence
challengeable?
```

# Hard vs Soft Constraint

Use:

```text
HARD
SOFT
UNKNOWN
```

A stakeholder preference is not automatically a hard constraint.

# Technology Request Test

If input says:

```text
must use PostgreSQL
```

ask:

```text
is this mandatory organizational policy,
existing platform dependency,
or preferred technology?
```

Record the answer.

# Step 10 — Identify Assumptions

Assumptions are beliefs accepted temporarily without sufficient evidence.

Record:

```text
ASM-001
assumption
why it matters
evidence
confidence
validation method
failure impact
owner
```

Every architecture-significant assumption should eventually be validated or consciously accepted.

# Unsupported Assumption

Example:

```text
users will never exceed 5,000
```

without evidence.

Do not turn it into a fact.

# Step 11 — Identify Dependencies

Dependencies can include:

```text
external provider
existing service
identity platform
data source
platform team
legal approval
procurement
migration
another project
```

Record:

```text
dependency
owner
contract
availability
uncertainty
impact if delayed/unavailable
```

# Dependency vs Constraint

A dependency can fail or change.

A constraint restricts design.

They may overlap but should not be conflated.

# Step 12 — Identify Risks

Discovery risk is uncertainty that may materially affect outcome or architecture.

Categories:

```text
PRODUCT
TECHNICAL
DELIVERY
DEPENDENCY
SECURITY
PRIVACY
DATA
OPERATIONAL
COST
ORGANIZATIONAL
```

Risk record:

```text
risk
cause
impact
likelihood (if evidence supports)
mitigation/discovery action
owner
```

Do not fabricate numerical risk scores.

# Step 13 — Identify Conflicts

Examples:

```text
Stakeholder A wants permanent history.
Stakeholder B requires 30-day deletion.
```

or:

```text
Product wants immediate consistency.
Provider is eventually consistent.
```

Record both positions, source, impact, and decision owner.

Do not reconcile silently.

# Conflict Status

Use:

```text
CONFLICT_REQUIRES_DECISION
CONFLICT_REQUIRES_EVIDENCE
CONFLICT_RESOLVED
```

Only `RESOLVED` with explicit authoritative evidence.

# Step 14 — Identify Unknowns / Open Questions

Classify questions:

```text
BLOCKING
IMPORTANT_NON_BLOCKING
FOLLOW_UP
```

And type:

```text
PRODUCT
USER
BUSINESS
QUALITY
CONSTRAINT
DATA
SECURITY
PRIVACY
DEPENDENCY
TECHNICAL_CONTEXT
```

# Blocking Question

A question is blocking when its answer materially changes:

- product scope;
- accepted behavior;
- architecture drivers;
- public contract;
- data model;
- security/privacy boundary;
- delivery feasibility.

Do not mark every unknown as blocking.

# Question Quality

Ask:

```text
What exact decision/evidence is needed?
Why does it matter?
Who can answer?
What work is blocked?
```

Avoid vague:

```text
Any other requirements?
```

# Step 15 — Discover Success Conditions

Capture candidate success signals.

Examples:

```text
reduced support tickets
task completion rate
successful workflow completion
latency target
availability target
conversion
operator recovery time
```

Do not invent business KPIs.

If success is undefined:

```text
SUCCESS_CRITERIA_REQUIRED
```

# Success Metric vs Acceptance Criterion

Success metric:

```text
measures outcome over time
```

Acceptance criterion:

```text
determines whether required behavior is implemented
```

Keep them separate.

# Step 16 — Detect Proposed Solutions

Stakeholders often provide solutions instead of needs.

Record:

```text
proposed solution
underlying need
authority
constraint status
open alternative?
```

Do not dismiss valuable technical constraints.

# Step 17 — Brownfield Discovery

If existing system exists, discover:

```text
current behavior
pain
compatibility
legacy consumers
data migration
operational procedures
existing constraints
known incidents
```

Do not assume greenfield freedom.

# Existing Behavior Status

Use:

```text
MUST_PRESERVE
INTENTIONALLY_CHANGE
DEPRECATED
UNKNOWN
```

# Step 18 — External Systems

For each external system capture:

```text
purpose
owner/provider
direction
data exchanged
availability assumptions
contract status
auth model known?
rate/usage constraints
failure expectations
```

Do not design integration mechanics yet.

# Step 19 — Data Discovery

Capture:

```text
important business concepts
data sources
data ownership
sensitivity
lifecycle
retention expectations
volume
migration
```

Do not create ERD here.

`modeling-domain-data` comes later.

# Step 20 — Operational Discovery

When applicable identify:

```text
operators
support workflows
monitoring needs
audit needs
manual recovery
deployment windows
maintenance constraints
incident expectations
```

Operational actors frequently reveal NFRs missed by product-only discovery.

# Step 21 — Prioritization

If authoritative prioritization exists, record it.

Potential:

```text
MUST
SHOULD
COULD
WONT_FOR_NOW
```

or repository/product convention.

Do not assign priority by analyst intuition.

If priority is unknown:

```text
PRIORITY_REQUIRED
```

for items where sequencing depends on it.

# MoSCoW Caution

Do not use MoSCoW automatically if product process uses another framework.

# Step 22 — Traceability

Use temporary discovery IDs:

```text
SRC-###
STK-###
ACT-###
JRN-###
FR-CAND-###
NFR-CAND-###
CON-###
ASM-###
DEP-###
RSK-###
Q-###
```

This allows the PRD to trace back to evidence.

# Source Ledger

Every critical candidate requirement should trace to one or more sources.

If no source exists, classify as:

```text
ANALYST_INFERENCE
```

or:

```text
ASSUMPTION
```

not confirmed requirement.

# Step 23 — Contradiction Audit

Check:

- same actor with incompatible capabilities;
- requirement vs constraint conflict;
- quality target vs budget/time conflict;
- retention vs deletion conflict;
- availability vs dependency reality;
- security vs UX assumption;
- success metric vs stated goal;
- current-system compatibility conflict.

# Step 24 — Completeness Audit

Assess dimensions:

```text
problem
goals/outcomes
stakeholders
actors
journeys
functional needs
quality expectations
constraints
assumptions
dependencies
risks
success conditions
open questions
```

Do not require all dimensions to be equally detailed if irrelevant.

# Discovery Readiness

Use:

```text
REQUIREMENTS_DISCOVERY_READY_FOR_PRD
REQUIREMENTS_DISCOVERY_READY_WITH_CONDITIONS
REQUIREMENTS_DISCOVERY_REQUIRES_STAKEHOLDER_INPUT
REQUIREMENTS_DISCOVERY_REQUIRES_PRODUCT_DECISION
REQUIREMENTS_DISCOVERY_REQUIRES_CONSTRAINT_VALIDATION
REQUIREMENTS_DISCOVERY_REQUIRES_SUCCESS_CRITERIA
REQUIREMENTS_DISCOVERY_CONFLICTED
BLOCKED
```

# Ready for PRD

Use when:

- problem/outcome is sufficiently clear;
- principal actors/stakeholders are known;
- major behavior candidates are captured;
- major quality expectations are captured or explicitly unknown;
- constraints/assumptions are visible;
- blocking conflicts/questions are resolved or explicitly accepted for PRD draft as open decisions;
- provenance is preserved.

# Ready With Conditions

Use when PRD can be drafted with clearly labeled unresolved non-blocking items.

Do not hide them.

# PRD Handoff

Handoff to:

```text
creating-product-requirement-documents
```

with:

```text
authoritative sources
problem
goals/non-goals candidates
stakeholders
actors/journeys
FR candidates
NFR candidates
constraints
assumptions
dependencies
risks
success candidates
open questions
conflicts
readiness
```

# Relationship to `enriching-user-stories`

Use this skill for system/product/project discovery.

Use:

```text
enriching-user-stories
```

later for individual delivery stories.

Expected hierarchy:

```text
requirements elicitation
→ PRD
→ capabilities / epics
→ user stories
→ enriching-user-stories
→ OpenSpec
```

# Relationship to Architecture

This skill MUST NOT:

- choose monolith vs microservices;
- choose cloud/provider;
- choose DB unless it is a confirmed constraint;
- create C4;
- produce ADRs;
- identify final architecture drivers.

It supplies evidence to later architecture skills.

# Relationship to Quality Attributes

Capture vague and explicit quality expectations here.

Then:

```text
defining-non-functional-requirements
defining-quality-attributes
```

will make them measurable and architecture-relevant.

# Relationship to Constraints

Constraints discovered here later influence:

```text
identifying-architecture-drivers
designing-system-architecture
```

Do not evaluate architecture solutions yet.

# Interview / Question Strategy

Ask high-information questions first.

Good sequence:

```text
problem/outcome
→ actor/journey
→ business rules
→ failure/edge behavior
→ quality expectations
→ constraints
→ dependencies
→ success
```

Do not ask 40 template questions when 8 targeted questions will resolve the uncertainty.

# Adaptive Elicitation

Questions should depend on the current evidence.

For payments, likely ask about:

```text
failure/cancel/refund/idempotency/security
```

For an internal read-only dashboard, those may be irrelevant.

# Evidence Before Questions

If canonical project documentation already answers a question and is accessible, inspect it rather than asking stakeholder to repeat known facts.

Do not search broadly without need.

# Avoid Leading Questions

Bad:

```text
Shouldn't we use event-driven architecture for scalability?
```

Good:

```text
What throughput, latency, consistency, and failure-isolation expectations exist?
```

# Avoid Solution Anchoring

Do not let a proposed stack constrain requirements unless its constraint status is confirmed.

# Avoid Premature Precision

If stakeholder cannot yet specify an exact performance target:

```text
record unknown
→ create follow-up
```

Do not make up a number to complete the template.

# Avoid Requirement Inflation

Do not turn nice-to-have ideas into mandatory requirements.

Preserve priority/status.

# Avoid Redundancy

Consolidate repeated stakeholder statements into one candidate requirement with multiple source references.

# Candidate Requirement Quality

A good functional candidate is:

- unambiguous enough to discuss;
- actor/outcome aware;
- solution-neutral where practical;
- traceable;
- testable in principle;
- explicit about uncertainty.

A good NFR candidate is:

- quality-specific;
- context-aware;
- measurable eventually;
- traceable;
- not an architecture solution.

# Discovery Report

Use `assets/software-requirements-elicitation-record.md`.

# Final Decision

Use one:

```text
REQUIREMENTS_DISCOVERY_READY_FOR_PRD
REQUIREMENTS_DISCOVERY_READY_WITH_CONDITIONS
REQUIREMENTS_DISCOVERY_REQUIRES_STAKEHOLDER_INPUT
REQUIREMENTS_DISCOVERY_REQUIRES_PRODUCT_DECISION
REQUIREMENTS_DISCOVERY_REQUIRES_CONSTRAINT_VALIDATION
REQUIREMENTS_DISCOVERY_REQUIRES_SUCCESS_CRITERIA
REQUIREMENTS_DISCOVERY_CONFLICTED
BLOCKED
```

## Completion Criteria

- [ ] Discovery scope is explicit.
- [ ] Authoritative sources are recorded.
- [ ] Facts are distinguished from stakeholder needs, assumptions, inferences, constraints, risks, and open questions.
- [ ] Problem is separated from proposed solution.
- [ ] Primary goals and outcomes are captured.
- [ ] Relevant stakeholders are identified without template filler.
- [ ] Decision authority is recorded where conflicts matter.
- [ ] Relevant actors, including external/system actors, are identified.
- [ ] Candidate journeys/scenarios are captured.
- [ ] Candidate functional requirements are traceable.
- [ ] Functional candidates include actor/trigger/behavior/outcome where applicable.
- [ ] Candidate non-functional expectations are captured.
- [ ] Vague quality terms remain explicitly unmeasured rather than receiving invented targets.
- [ ] Security/privacy/availability/scale expectations are captured when relevant without premature solution design.
- [ ] Constraints are separated from preferences and assumptions.
- [ ] Hard/soft/unknown constraint status is explicit.
- [ ] Architecture-significant assumptions are visible and have validation actions where possible.
- [ ] Dependencies and external systems are captured.
- [ ] Risks are evidence-based rather than scored arbitrarily.
- [ ] Conflicting stakeholder needs are exposed rather than silently reconciled.
- [ ] Blocking vs non-blocking questions are distinguished.
- [ ] Success conditions are captured or explicitly missing.
- [ ] Existing behavior/compatibility is captured for brownfield work.
- [ ] Important data and operational concerns are captured when relevant.
- [ ] Priorities are preserved only when supported by authority.
- [ ] Critical candidates trace to source evidence.
- [ ] Contradictions and missing actors are audited.
- [ ] No architecture/technology decision is fabricated.
- [ ] No final PRD is written by this skill.
- [ ] PRD handoff is structured.
- [ ] Discovery readiness status is explicit.

## References

- Read `references/discovery-scope-provenance-and-epistemic-status.md` first.
- Read `references/stakeholders-actors-goals-and-user-journeys.md`.
- Read `references/functional-and-non-functional-discovery.md`.
- Read `references/constraints-assumptions-dependencies-and-risks.md`.
- Read `references/open-questions-conflicts-and-success-conditions.md`.
- Read `references/brownfield-data-operations-and-external-systems.md`.
- Read `references/adaptive-elicitation-question-strategy.md`.
- Read `references/software-requirements-elicitation-audit.md` before completion.
