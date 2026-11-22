---
name: creating-product-requirement-documents
description: Portable engineering capability `creating-product-requirement-documents`.
  Use when the harness or a specialist agent explicitly requires this named capability.
---
# Creating Product Requirement Documents

## Purpose

Create a product/system-level PRD from structured discovery evidence.

Core workflow:

```text
requirements discovery
→ validate evidence readiness
→ preserve provenance + uncertainty
→ structure problem and outcomes
→ define scope / non-goals
→ organize actors and journeys
→ organize functional needs
→ organize non-functional expectations
→ capture constraints / assumptions / dependencies
→ define success measures and acceptance criteria
→ expose risks / conflicts / open questions
→ produce PRD
```

This skill turns discovery into a durable product artifact.

It does NOT design system architecture.

## Core Principle

The PRD answers primarily:

```text
what problem exists?
for whom?
why does it matter?
what outcomes are required?
what behavior is expected?
what quality expectations exist?
what constraints and assumptions shape the product?
how will we know the product/change is successful?
what remains unresolved?
```

The PRD does not answer in detail:

```text
which architecture?
which database?
which cloud?
which service topology?
which React hook?
which repository class?
```

unless a technology/platform choice is itself an accepted product/organizational constraint.

## Relationship to Other Skills

Upstream:

```text
eliciting-software-requirements
```

Downstream:

```text
defining-functional-requirements
defining-non-functional-requirements
defining-quality-attributes
identifying-architecture-drivers
modeling-use-cases
enriching-user-stories
OpenSpec workflows
```

The PRD is not a substitute for those more formal artifacts.

## Use When

- Requirements discovery has reached PRD readiness.
- A greenfield product/system needs a durable requirements baseline.
- An internal platform needs a structured product/system brief.
- A large initiative needs goals, scope, actors, journeys, functional/non-functional expectations, constraints, and success measures in one artifact.
- Discovery evidence exists but is scattered.
- Architecture work needs a stable product input.
- Product and engineering need one shared what/why document before decomposition into stories/OpenSpec.

## Do Not Use When

- Requirements discovery is still too incomplete to draft responsibly.
- The task is to discover stakeholders or requirements from a vague idea; use `eliciting-software-requirements`.
- The task is to define detailed FRs/NFRs or quality-attribute scenarios.
- The task is to choose architecture.
- The task is to write a technical design document.
- The task is to enrich one user story.
- The task is to create an OpenSpec delta/change directly from an already accepted story.

## Inputs

Preferred:

- `software-requirements-elicitation-record.md`;
- source/provenance ledger;
- stakeholder/actor map;
- candidate journeys;
- candidate FR/NFR;
- constraints;
- assumptions;
- dependencies;
- risks;
- conflicts;
- open questions;
- success-condition candidates;
- relevant canonical product/policy documents;
- applicable `AGENTS.md`.

Optional:

- business brief;
- existing PRD to revise;
- current-system context;
- roadmap/strategy context;
- existing product metrics.

## Outputs

- Product Requirements Document.
- Source-traceability appendix.
- Open-question/conflict ledger.
- PRD readiness/approval status.
- Handoff notes for formal FR/NFR and architecture work.
- `product-requirements-document.md`.

# PRD Readiness Gate

Before drafting, inspect discovery status.

Allowed input states:

```text
REQUIREMENTS_DISCOVERY_READY_FOR_PRD
REQUIREMENTS_DISCOVERY_READY_WITH_CONDITIONS
```

If discovery is:

```text
REQUIRES_STAKEHOLDER_INPUT
REQUIRES_PRODUCT_DECISION
REQUIRES_CONSTRAINT_VALIDATION
REQUIRES_SUCCESS_CRITERIA
CONFLICTED
BLOCKED
```

the PRD may only be produced as:

```text
DRAFT_WITH_BLOCKING_GAPS
```

if the user explicitly needs a draft.

Do not present it as accepted/final.

# PRD Status

Use:

```text
DRAFT
DRAFT_WITH_OPEN_QUESTIONS
DRAFT_WITH_BLOCKING_GAPS
READY_FOR_REVIEW
ACCEPTED
SUPERSEDED
```

Do not mark `ACCEPTED` unless authoritative approval evidence exists.

# Product/System Context

Include:

```text
product/system
initiative
business context
current situation
why now
target environment/users
```

Avoid architecture description here unless it is existing context.

# Problem Statement

Preserve the problem from discovery.

A good problem statement should identify:

```text
affected actor
pain/problem
context
impact
```

Do not transform:

```text
we need Kubernetes
```

into the problem.

If discovery contains solution-first statements, keep them in constraints/proposed-solutions notes.

# Goals

Goals should describe desired outcomes.

Examples:

```text
reduce manual support intervention
enable tenant admins to complete upgrade flow
maintain service usability during AI-provider outage
```

Avoid technical goals unless they are genuinely product/platform outcomes.

# Goal IDs

Use stable PRD IDs such as:

```text
G-001
G-002
```

Preserve links to discovery source IDs.

# Non-Goals

Explicitly define what is not part of current scope.

This is mandatory for non-trivial PRDs.

Examples:

```text
voice support is not part of v1
mobile native app is not part of this initiative
migration of legacy customer X is deferred
```

Do not invent non-goals.

Use source evidence or accepted scope decisions.

# Success Metrics / Outcome Measures

A success metric should link to a goal.

Record:

```text
metric
baseline if known
target if accepted
measurement window
owner/source
```

If baseline/target is unknown:

```text
TBD
```

with an open question.

Do not invent KPIs.

# Unsupported Success Metrics

Bad:

```text
reduce support tickets by 30%
```

if no stakeholder/source provided it.

Use:

```text
success metric candidate: reduction in support tickets
target: TBD
```

if evidence supports the direction but not the number.

# Actors / Personas

Include only roles that materially affect product behavior.

Use:

```text
actor/role
goal
relevant capabilities
constraints/needs
```

Do not create demographic personas as filler.

# System Actors

External systems may appear as actors when they drive product behavior:

```text
identity provider
payment provider
email provider
scheduled automation
```

But detailed integration design belongs later.

# User / System Journeys

Include high-value journeys.

Each journey should capture:

```text
actor
trigger
intent
major steps
important alternatives/failures
desired outcome
linked goals / FR candidates
```

Do not turn PRD journeys into detailed sequence diagrams.

# Functional Requirements Section

The PRD can contain structured functional requirement candidates/requirements.

Use:

```text
FR-PRD-001
title
actor
required behavior
business outcome
priority/status
source
```

If formal FR catalog comes later, PRD requirements may remain high-level.

Do not duplicate exhaustive use-case detail unless product process expects it.

# FR Status

Use:

```text
PROPOSED
REVIEW_REQUIRED
ACCEPTED
DEFERRED
REJECTED
```

Only use `ACCEPTED` with authoritative evidence.

# Requirement Language

Prefer:

```text
The system shall/should/must...
```

only when the modality is supported by priority/authority.

Otherwise:

```text
Candidate requirement:
The system should...
```

Preserve uncertainty.

# Non-Functional Requirements Section

Organize quality expectations by category.

Potential:

```text
performance
availability
scalability
reliability
security
privacy
recoverability
observability
maintainability
interoperability
accessibility
usability
cost
data residency
```

Do not invent targets.

# NFR Precision

Example:

```text
Performance:
Dashboard interactions must feel fast.
Target: TBD.
Open question: define operation, load, percentile, and target.
```

This is acceptable in a draft PRD.

Later:

```text
defining-non-functional-requirements
defining-quality-attributes
```

will formalize it.

# Quality Attribute Summary

The PRD may summarize important quality expectations.

Do not produce architecture trade-offs yet.

Use language such as:

```text
High-priority quality concern:
tenant isolation
```

not:

```text
Therefore use schema-per-tenant PostgreSQL.
```

# Security / Privacy Requirements

Capture product/system requirements such as:

```text
tenant data isolation
privileged action audit
consent requirements
sensitive-data handling
retention decision
data residency
```

Do not perform detailed security taxonomy or STRIDE here.

# Accessibility

If accessibility is product/system-level, record requirement and target standard if explicitly accepted.

Do not invent conformance level.

# Constraints

Keep constraints visible and separately classified.

Example:

```text
CON-001
Existing company identity platform should be reused if feasible.
Strength: SOFT / UNKNOWN
```

Do not silently convert technology preferences into hard constraints.

# Constraints in PRD

Useful fields:

```text
constraint
type
strength
source/authority
impact
validation status
```

# Assumptions

Include material assumptions that shape scope, product expectation, or later architecture.

Example:

```text
ASM-002
Initial tenant count is expected to be below X.
Evidence: low.
Validation: product forecast required.
```

Do not hide assumptions inside goals or requirements.

# Dependencies

Capture dependencies that affect delivery/product outcome:

```text
provider selection
identity integration
legal/privacy decision
external team
existing service
procurement
data migration
```

Do not design internal implementation for them.

# Risks

Include meaningful known risks:

```text
product
dependency
delivery
security
privacy
data
operational
cost
```

Keep mitigation at product/discovery level when architecture is not yet designed.

# Open Questions

Keep unresolved questions explicit.

Classify:

```text
BLOCKING
IMPORTANT_NON_BLOCKING
FOLLOW_UP
```

A PRD may be `READY_FOR_REVIEW` with non-blocking questions.

It should not be `ACCEPTED` while blocking product decisions remain unresolved.

# Conflicts

If discovery contains unresolved conflicting needs, preserve them.

Example:

```text
Product:
retain conversation history indefinitely

Privacy:
indefinite retention not approved
```

PRD must show:

```text
BLOCKING DECISION
```

Do not pick a side silently.

# Acceptance Criteria

PRD-level acceptance criteria should verify product/system outcomes at an initiative/capability level.

They are not necessarily one-to-one with implementation stories.

Good:

```text
AC-001
A tenant admin can create an upgrade request for an eligible active subscription.

AC-002
A user without the required permission cannot complete the upgrade.
```

Avoid technical criteria like:

```text
Use React Query mutation.
```

# Acceptance Criteria Quality

PRD ACs should be:

- observable;
- outcome-oriented;
- solution-neutral where practical;
- traceable to goals/requirements;
- explicit about important failure behavior.

# Acceptance Criteria vs Detailed Specs

PRD AC:

```text
The user sees a clear conflict message and the current plan is unchanged.
```

Later OpenSpec/FR might define exact error semantics.

Do not overload PRD unless exact error contract is a product requirement.

# Prioritization

Use the accepted product prioritization framework if known.

Possible:

```text
MUST
SHOULD
COULD
WONT_FOR_NOW
```

Do not impose MoSCoW by default.

If no framework:

```text
priority = TBD
```

# Release / Milestone Scope

If known, map requirements to:

```text
MVP
V1
LATER
```

or repository/product convention.

Do not invent release allocation.

# Proposed Solutions Section

If discovery included stakeholder-proposed solutions, optionally include:

```text
Proposed solutions / preferences (non-binding)
```

Clearly separate them from requirements/constraints.

Example:

```text
Microservices were proposed as a scaling solution.
No accepted architecture decision exists.
```

This preserves context without anchoring architecture.

# Product Decisions

Record accepted product decisions separately.

Examples:

```text
voice excluded from v1
only tenant admins may reassign conversations
AI suggestion remains optional
```

These can be stronger than discovery candidates when authoritative approval exists.

# Decision Status

Use:

```text
ACCEPTED_PRODUCT_DECISION
PROPOSED_PRODUCT_DECISION
DECISION_REQUIRED
```

# Data Requirements

PRD can capture:

```text
important data categories
ownership expectation
sensitivity
retention requirement/status
export/deletion needs
migration needs
```

Do not create logical/physical data models.

# External Integrations

Record:

```text
integration purpose
business dependency
required capability
known constraints
contract maturity
```

Do not specify protocol/topology unless required.

# Operational Requirements

If product/platform scope requires:

```text
supportability
audit
monitoring expectation
manual fallback
business continuity
operating hours
```

Capture as product requirements/NFRs.

# Observability

Product/platform PRDs may specify outcomes:

```text
operators must be able to detect failed message processing
```

Detailed telemetry design comes later.

# Cost / Budget

Only include:

- explicit budget;
- cost ceiling;
- cost objective;
- cost sensitivity;

when authoritative evidence exists.

Do not fabricate FinOps targets.

# Traceability

The PRD should preserve source IDs from discovery.

Example:

```text
FR-PRD-004
Sources: FR-CAND-006, SRC-003, JRN-002
```

This allows downstream derivation:

```text
source
→ discovery
→ PRD
→ formal FR/NFR
→ architecture driver
→ ADR
```

# Traceability Appendix

Include a compact mapping:

| PRD item | Discovery source |
|---|---|
| G-001 | SRC-001, STK-002 |
| FR-PRD-001 | FR-CAND-001 |
| NFR-PRD-003 | NFR-CAND-004 |

# Information Preservation

Do not silently discard:

- uncertainty;
- source disagreement;
- constraint strength;
- confidence;
- non-goals;
- dependency risk;
- unresolved success metric;
- blocking question.

The PRD is structured, not falsely certain.

# Consolidation

Combine duplicate discovery statements when they express the same product need.

Preserve all material source references.

# Contradictions

Do not produce internally contradictory PRD sections.

If conflict is unresolved:

```text
state both positions
→ mark decision required
```

# Ambiguous Product Goal

Roadmap evaluation:

If product goal is vague:

```text
make it explicit as vague
→ preserve underlying intent
→ add targeted open question
```

Do not replace it with an invented goal.

# PRD Polluted With Implementation Details

Roadmap evaluation:

Move premature technical choices to one of:

```text
accepted constraint
existing-system context
non-binding proposed solution
architecture question
```

Do not leave them as product requirements.

# Missing Non-Goals

Roadmap evaluation:

For non-trivial PRDs, explicitly include non-goals.

If no non-goals have been decided:

```text
Non-goals: TBD
Open question: what is intentionally excluded?
```

Do not invent exclusions.

# Unsupported Success Metrics

Roadmap evaluation:

A metric or target requires source evidence.

If the direction is known but target is not:

```text
Metric: supported
Target: TBD
```

If neither is supported:

do not add it.

# Greenfield SaaS PRD

Must capture:

- problem;
- product context;
- users/actors;
- major journeys;
- requirements;
- quality expectations;
- constraints;
- dependencies;
- success;
- risks;
- open questions.

Do not prematurely specify service decomposition/cloud/database.

# Internal Platform PRD

The “user” may be:

```text
developer
operator
data team
service team
security team
```

Product outcomes can include:

```text
lead time
reliability
standardization
self-service
operational effort
```

Do not force consumer-SaaS language.

# Brownfield PRD

Include:

```text
current behavior
must preserve
intentionally change
legacy consumers
compatibility
migration constraints
```

Do not imply greenfield replacement.

# PRD and Architecture Boundary

The following belong after PRD:

```text
architecture drivers
candidate architectures
trade-off analysis
ADRs
C4
sequence diagrams
state machines
ERD/DFD
deployment model
```

The PRD may provide inputs, not conclusions.

# PRD and Formal FR/NFR Boundary

PRD can summarize requirements.

Formalization belongs downstream:

```text
defining-functional-requirements
defining-non-functional-requirements
defining-quality-attributes
```

Do not make the PRD so exhaustive that those skills become redundant.

# PRD and User Stories

The PRD can identify capabilities/epics.

Individual stories should later go through:

```text
enriching-user-stories
```

# PRD and OpenSpec

The PRD is broader than an OpenSpec change.

Typical flow:

```text
PRD
→ capabilities / architecture
→ user stories
→ OpenSpec change
```

For a single large initiative, OpenSpec can also derive directly from PRD + architecture package where repository workflow supports it.

# Change History

PRD should include:

```text
version
status
date
author/owner
change summary
```

Do not overwrite accepted decision history silently.

# Approval / Review

Possible review roles:

```text
product
engineering
security
privacy
operations
design
```

only when relevant.

Do not invent approvers.

# PRD Validation Checklist

Check:

```text
problem clear?
goals measurable/meaningful?
non-goals explicit?
actors real?
journeys coherent?
FRs traceable?
NFR expectations visible?
constraints/assumptions separated?
risks/open questions visible?
success metrics supported?
ACs outcome-focused?
no architecture leakage?
```

# Final Decision

Use:

```text
PRD_READY_FOR_REVIEW
PRD_READY_WITH_OPEN_QUESTIONS
PRD_REQUIRES_MORE_DISCOVERY
PRD_REQUIRES_PRODUCT_DECISIONS
PRD_REQUIRES_SUCCESS_METRICS
PRD_REQUIRES_SCOPE_DECISION
PRD_REQUIRES_CONFLICT_RESOLUTION
PRD_DRAFT_WITH_BLOCKING_GAPS
BLOCKED
```

# Output

Use:

```text
assets/product-requirements-document.md
```

# Completion Criteria

- [ ] PRD is grounded in discovery evidence.
- [ ] PRD status is explicit.
- [ ] Product/system context and why-now are clear.
- [ ] Problem statement is separated from proposed solution.
- [ ] Goals describe outcomes rather than architecture.
- [ ] Non-goals are explicit or marked TBD.
- [ ] Actors/stakeholders are relevant and evidence-backed.
- [ ] High-value journeys are represented.
- [ ] Functional requirements are organized and traceable.
- [ ] Non-functional expectations are organized and traceable.
- [ ] Vague NFRs retain TBD measurement rather than invented targets.
- [ ] Quality expectations are visible without architecture conclusions.
- [ ] Security/privacy/accessibility expectations are included when supported.
- [ ] Constraints are separate from assumptions/preferences.
- [ ] Constraint strength/authority is preserved.
- [ ] Material assumptions are explicit.
- [ ] Dependencies are explicit.
- [ ] Risks are explicit.
- [ ] Conflicts are preserved and require explicit resolution.
- [ ] Blocking/non-blocking open questions are explicit.
- [ ] Success metrics are source-supported.
- [ ] Unsupported metric targets are not invented.
- [ ] Acceptance criteria are observable and solution-neutral where practical.
- [ ] Data/external/operational requirements are represented when relevant.
- [ ] Brownfield compatibility/current behavior is represented when relevant.
- [ ] Proposed technical solutions are not presented as product requirements unless accepted as constraints.
- [ ] Architecture design is not performed.
- [ ] Formal FR/NFR/quality-attribute downstream work remains meaningful.
- [ ] Discovery provenance is preserved in a traceability appendix.
- [ ] Final PRD readiness status is explicit.
- [ ] Handoff to formal requirements/architecture is included.

## References

- Read `references/prd-structure-status-and-product-architecture-boundary.md` first.
- Read `references/problem-goals-non-goals-and-product-outcomes.md`.
- Read `references/actors-journeys-functional-and-nonfunctional-sections.md`.
- Read `references/constraints-assumptions-dependencies-risks-and-open-questions.md`.
- Read `references/success-metrics-acceptance-criteria-and-prioritization.md`.
- Read `references/data-integrations-operations-and-brownfield-prds.md`.
- Read `references/provenance-traceability-versioning-and-approval.md`.
- Read `references/product-requirements-document-audit.md` before completion.
