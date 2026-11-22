---
name: designing-software-system
description: Orchestrates the complete requirements-engineering and software-architecture workflow by selecting the smallest complete graph of specialized skills needed for the system's risk, complexity, lifecycle, data, eventing, deployment, and security profile. Use when taking a product/system idea from requirements through an accepted Architecture Package and handoff to OpenSpec or implementation planning. Route to requirements, behavioral modeling, architecture design/trade-off/ADR, structural/runtime/data/event/deployment modeling, STRIDE, and architecture validation only when applicable. Do not execute every skill mechanically, skip required gates, invent missing evidence, silently choose architecture, or replace specialized skills with a shallow all-in-one analysis.
---

# Designing Software System

## Purpose

Orchestrate the complete requirements-engineering and system-architecture process.

Canonical roadmap workflow:

```text
elicit requirements
→ create PRD
→ define FR
→ define NFR
→ define quality attributes
→ identify constraints/assumptions
→ identify architecture drivers
→ model use cases/process flows where useful
→ design candidate architectures
→ analyze trade-offs
→ record ADRs
→ select architecture diagrams/models
→ model C4
→ model sequences
→ model states/data/event/deployment where applicable
→ threat-model with STRIDE
→ validate architecture
→ produce accepted Architecture Package
→ hand off to OpenSpec / implementation planning
```

Primary responsibility:

```text
select the smallest complete architecture-skill graph
```

Do not run every modeling skill mechanically.

Output:

```text
software-system-orchestration-plan.md
```

plus the resulting Architecture Package produced by delegated skills.

# Core Principle

The orchestrator should optimize for:

```text
minimum sufficient artifacts
+
complete risk coverage
+
traceable decisions
```

not:

```text
maximum number of documents
```

A small CRUD system and a payment platform should not execute the same graph.

# Use When

- A product/system idea needs requirements and architecture from end to end.
- A major feature/system needs structured architecture before OpenSpec/implementation.
- The user wants a complete architecture workflow rather than one isolated artifact.
- A brownfield system needs requirements clarification, target architecture, and validation.
- The correct modeling subset is not yet known.
- Architecture risk/complexity must determine which specialized skills activate.

# Do Not Use When

- The user asks for one specific bounded skill artifact.
- Requirements and architecture are already complete and only implementation is needed.
- The task is a local code change with no architecture significance.
- The task is only code review/security review/testing.
- The task is to mechanically generate every architecture diagram.

# Inputs

## Preferred

- system/product idea or change request;
- existing requirements/PRD if any;
- existing architecture/current-state docs if brownfield;
- business goals/non-goals;
- known actors/users;
- known quality/security/compliance constraints;
- external dependencies/providers;
- existing ADRs;
- applicable `AGENTS.md`.

## Optional

- existing OpenSpec;
- current C4/DFD/ERD/sequence/deployment models;
- production metrics;
- provider documentation;
- RTO/RPO/SLOs;
- regulatory/privacy policies;
- team/ownership topology.

Do not invent missing architecture-significant inputs.

# Outputs

The orchestrator itself produces:

```text
software-system-orchestration-plan.md
```

The delegated graph may produce:

```text
requirements elicitation record
PRD
functional requirements catalog
NFR catalog
quality attribute scenarios
architecture drivers record
use-case catalog
process-flow model
state-machine model
candidate system architectures
architecture trade-off analysis
ADRs
C4 architecture model
sequence model
data-flow model
domain-data model
event-flow model
deployment architecture model
STRIDE threat model
architecture validation report
accepted Architecture Package
```

Only include artifacts justified by the selected graph.

# Orchestration State

Use:

```text
DISCOVERY
REQUIREMENTS_FOUNDATION
BEHAVIORAL_MODELING
ARCHITECTURE_DECISIONS
ARCHITECTURE_MODELING
SECURITY_VALIDATION
ARCHITECTURE_ACCEPTANCE
HANDOFF
BLOCKED
```

# Step 1 — Establish System Scope

Record:

```text
system/change
greenfield/brownfield
decision horizon
business goal
actors
external systems
known risks
team/ownership context
```

Avoid enterprise-wide scope unless requested.

# Step 2 — Discover Existing Evidence

Before creating anything, inspect whether the repository/package already has:

```text
PRD
FR/NFR
quality scenarios
drivers
ADRs
C4
sequence/state/data/event/deployment models
threat model
validation report
```

Reuse valid/current artifacts.

Do not duplicate them.

# Step 3 — Determine Artifact Freshness

Classify existing artifacts:

```text
CURRENT
STALE
CONFLICTED
INCOMPLETE
MISSING
NOT_APPLICABLE
```

A stale artifact is not equivalent to missing; it may require update rather than recreation.

# Step 4 — Requirements Foundation Gate

Always ask whether the system has enough authoritative requirements to make architecture decisions.

Minimum expected:

```text
goals/non-goals
actors/capabilities
FRs
NFRs / quality expectations
constraints
assumptions
risks
```

If not:

```text
run requirements foundation
```

# Step 5 — Requirements Skill Graph

Default sequence when requirements are insufficient:

```text
eliciting-software-requirements
→ creating-product-requirement-documents
→ defining-functional-requirements
→ defining-non-functional-requirements
→ defining-quality-attributes
→ identifying-architecture-drivers
```

Do not skip architecture drivers.

# Step 6 — Existing PRD Path

If a trustworthy PRD already exists:

```text
do not recreate it automatically
```

Validate whether FR/NFR/quality/driver evidence is sufficient.

Run only missing/invalid downstream skills.

# Step 7 — Requirements Decision Gaps

If an architecture-significant requirement lacks authority or measure:

```text
route back to relevant requirements skill
```

Examples:

```text
unknown scale → defining-non-functional-requirements
vague availability → defining-quality-attributes / NFR
unclear actor behavior → defining-functional-requirements
```

# Step 8 — Behavioral Modeling Gate

Behavioral models are conditional.

Ask:

```text
Are actor-goal interactions complex enough for use cases?
Are process decisions/approvals/retries important?
Does a meaningful lifecycle exist?
```

# Step 9 — Use-Case Activation

Run:

```text
modeling-use-cases
```

when:

```text
multiple actors
privilege boundaries
external actors
complex alternative behaviors
capability coverage needs
```

Skip for trivial behavior when FRs are enough.

# Step 10 — Process-Flow Activation

Run:

```text
modeling-process-flows
```

when behavior has:

```text
conditional branching
manual approval
validation chains
retry loops
fallback
operational procedures
multi-party handoffs
```

# Step 11 — State-Machine Activation

Run:

```text
modeling-state-machines
```

when correctness depends on:

```text
stable lifecycle states
legal/illegal transitions
cancellation
reopen/rollback
concurrent transitions
terminal states
```

Typical activation:

```text
payment
order
subscription
workflow
ticket lifecycle
deployment lifecycle
```

# Step 12 — Behavioral Model Skip Discipline

Do not activate a model only because it exists in the roadmap.

Use:

```text
NOT_APPLICABLE
```

with rationale.

# Step 13 — Architecture-Driver Readiness Gate

Do not generate architecture candidates until:

```text
primary drivers
constraints
assumptions
critical risks
```

are sufficiently clear.

If not:

```text
route backward
```

# Step 14 — Candidate Architecture Design

Run:

```text
designing-system-architecture
```

to generate viable alternatives.

Do not select winner here.

# Step 15 — Trade-Off Gate

Run:

```text
analyzing-architecture-tradeoffs
```

when more than one viable candidate exists or when a single candidate still needs explicit driver/trade-off justification.

# Step 16 — Decision Authority Gate

If recommendation exists but authority has not accepted it:

```text
ADR status = PROPOSED
```

Do not pretend architecture is accepted.

# Step 17 — ADR Activation

Run:

```text
recording-architecture-decisions
```

for architecture-significant choices.

Do not ADR every implementation detail.

# Step 18 — Architecture Modeling Selection

After architecture direction is stable, select only diagrams/models that answer material questions.

Use the question-driven rule:

```text
Use Case
→ actors/capabilities

Process Flow
→ process/decision logic

State Machine
→ lifecycle/transitions

C4
→ static architecture structure

Sequence
→ interactions over time

DFD
→ data movement/trust boundaries

Domain Data
→ concepts/relationships/ownership

Event Flow
→ async event semantics

Deployment
→ runtime topology
```

# Step 19 — C4 Activation

Normally run:

```text
modeling-c4-architecture
```

for system architecture work.

Default:

```text
L1 + L2
```

L3 only when justified.

L4 exceptional.

# Step 20 — Sequence Activation

Run:

```text
modeling-system-sequences
```

for critical runtime paths involving:

```text
multiple participants
external providers
authorization
failure propagation
timeouts/retries
concurrency/idempotency
```

Not every use case needs a sequence.

# Step 21 — DFD Activation

Run:

```text
modeling-data-flows
```

when any of these apply:

```text
personal/sensitive data
multi-tenancy
third-party data transfer
secrets
public trust boundary
data residency
privacy/security review
STRIDE required
```

# Step 22 — Domain-Data Activation

Run:

```text
modeling-domain-data
```

when:

```text
data concepts/ownership/cardinality/invariants matter
multiple capabilities share domain concepts
persistence ownership is unclear
tenant/lifecycle data semantics matter
```

Simple stateless integrations may not need a detailed domain data model.

# Step 23 — Event-Flow Activation

Run:

```text
modeling-event-flows
```

only when asynchronous/event-driven behavior is accepted or materially required.

Do not activate because “events are scalable.”

# Step 24 — Deployment Activation

Run:

```text
modeling-deployment-architecture
```

when:

```text
availability/recovery
scaling
regions/zones
network/trust placement
data residency
external connectivity
secrets
observability
runtime placement
```

are architecture-significant.

For small internal CRUD with conventional hosting and no special infrastructure constraints:

```text
deployment detail may be deferred/minimal
```

# Step 25 — Small Internal CRUD Profile

Roadmap example.

Likely graph:

```text
requirements foundation
→ architecture drivers
→ candidate architecture / trade-off if needed
→ ADR
→ C4 L1/L2
→ domain data if relationships matter
→ key sequence only if needed
→ validation
```

Likely skip:

```text
event flow
complex state machine
detailed DFD
complex deployment modeling
```

unless actual risk triggers them.

# Step 26 — Payment Platform Profile

Roadmap example.

Likely require:

```text
state machines
sequence diagrams
DFD
deployment model
event flows
STRIDE
explicit reliability/security quality scenarios
```

because payment correctness/security/recovery are architecture-significant.

# Step 27 — Multi-Tenant SaaS Profile

Likely activate:

```text
use cases
quality attributes
architecture drivers
C4
tenant-aware domain data
DFD
critical auth sequences
STRIDE
deployment if isolation/residency/recovery require it
```

# Step 28 — External-Provider-Heavy Profile

Likely activate:

```text
sequences
DFD
provider failure quality scenarios
trade-off analysis
deployment connectivity
event flow only if async contract exists
STRIDE
```

# Step 29 — Event-Driven Platform Profile

Likely activate:

```text
state model where lifecycle matters
sequence for critical flows
DFD
domain data
event flows
deployment
STRIDE
```

# Step 30 — Brownfield Modernization Profile

Likely activate:

```text
requirements/driver refresh
current/target C4
trade-off analysis
ADRs
brownfield state/data model as needed
migration-sensitive sequences
deployment transition view
validation
```

Do not assume rewrite.

# Step 31 — Critical/Regulated Profile

Likely activate broader evidence:

```text
measurable NFRs/quality scenarios
state/process models
C4
failure sequences
DFD
domain data
event flows if used
detailed deployment/recovery
STRIDE
security control requirements
architecture validation
```

# Step 32 — Skill Activation Classification

For every skill use:

```text
REQUIRED
CONDITIONAL
OPTIONAL
SKIP
BLOCKED
ALREADY_SATISFIED
```

# Step 33 — Activation Rationale

Each selected/skipped skill must include:

```text
why
source trigger
expected artifact/question
dependency
```

No unexplained graph nodes.

# Step 34 — Dependency Graph

Represent orchestration as a DAG, not a flat checklist.

Example:

```text
FR/NFR/QA
   ↓
drivers
   ↓
candidate architecture
   ↓
trade-offs
   ↓
ADRs
   ↓
C4
 ┌─┼───────────────┐
 ↓ ↓               ↓
seq data           deployment
    ↓
   DFD
    ↓
 STRIDE
    ↓
validation
```

Actual graph varies.

# Step 35 — Parallelism

Independent modeling tasks may run in parallel only after shared architecture decisions stabilize.

Possible parallel branches:

```text
C4
├── sequence modeling
├── domain data
├── DFD
└── deployment
```

when dependencies permit.

Do not parallelize tasks that depend on unresolved upstream decisions.

# Step 36 — Join Gates

Before STRIDE/validation, join relevant model branches.

Validate they refer to the same architecture version.

# Step 37 — Backtracking

The orchestrator must route backward when downstream work exposes missing evidence.

Examples:

```text
sequence reveals undefined retry semantics
→ requirements/NFR decision gap

deployment reveals impossible RTO
→ trade-off/architecture decision

DFD reveals unresolved third-party data policy
→ privacy/security/product decision

state model reveals missing lifecycle behavior
→ FR/business decision
```

# Step 38 — No Silent Repair

The orchestrator must not silently modify upstream decisions.

Route to the owning skill/decision authority.

# Step 39 — STRIDE Activation

Reuse:

```text
threat-modeling-with-stride
```

when meaningful trust/security risk exists.

Strong triggers:

```text
multi-tenancy
public entry points
authentication/authorization
privileged operations
sensitive/personal data
third-party integrations
secrets
payments
uploads
deployment trust boundaries
```

# Step 40 — STRIDE Input Gate

Prefer:

```text
C4
+ DFD
+ critical sequences
+ deployment/trust topology
```

as available.

Do not wait for every model if threat modeling can validly start earlier, but revisit after topology changes.

# Step 41 — Security Control Handoff

STRIDE can produce:

```text
required control intent
```

Implementation verification remains downstream:

```text
reviewing-application-security
verifying-security-controls
```

# Step 42 — Architecture Validation Activation

Run:

```text
validating-architecture-design
```

before Architecture Package acceptance.

This gate is not optional for meaningful architecture work.

# Step 43 — Validation Feedback Loop

If validation returns:

```text
ARCHITECTURE_REQUIRES_REWORK
ARCHITECTURE_REQUIRES_DECISIONS
ARCHITECTURE_REQUIRES_EVIDENCE
ARCHITECTURE_SECURITY_BLOCKED
ARCHITECTURE_CONFLICTED
```

route findings to owning skills.

Then revalidate.

# Step 44 — Architecture Acceptance Gate

Architecture Package is accepted only when validation returns:

```text
ARCHITECTURE_VALIDATED
```

or:

```text
ARCHITECTURE_VALIDATED_WITH_CONDITIONS
```

and conditions are compatible with the next phase.

# Step 45 — Conditional Acceptance

Conditions must be explicit.

Examples:

```text
cloud runtime TBD
database technology TBD
provider SLA evidence required before production
security control implementation required downstream
```

Do not hide architecture-significant blockers as conditions.

# Step 46 — Architecture Package Assembly

Package can include only applicable artifacts.

Potential contents:

```text
PRD
Requirements Catalog
Quality Attribute Scenarios
Constraints & Assumptions
Architecture Drivers
Candidate Architectures
Trade-off Analysis
ADRs
Use Cases
Flowcharts
C4
Sequence Diagrams
State Machines
DFDs
Domain Data Model / ERD
Event Flows
Deployment Diagram
Threat Model
Architecture Validation Report
```

# Step 47 — Package Manifest

Record for each artifact:

```text
path/name
status
version
source authority
required/conditional
dependencies
```

# Step 48 — Accepted Architecture Summary

Produce concise:

```text
system purpose
primary drivers
accepted architecture decisions
key boundaries
critical quality/security constraints
known deferred decisions
```

# Step 49 — Open Decision Ledger

Separate:

```text
non-blocking deferred decisions
blocking decisions
implementation-level TBDs
evidence/measurement gaps
```

# Step 50 — Handoff to OpenSpec / Implementation Planning

Roadmap-required final handoff.

Provide:

```text
accepted behavior
architecture constraints
ADRs
critical flows
domain/tenant invariants
required security controls
quality scenarios
deployment assumptions
deferred decisions
validation conditions
```

# Step 51 — Do Not Convert Architecture Package into OpenSpec Automatically

Architecture defines system-level constraints.

OpenSpec defines accepted implementation change behavior.

Hand off; do not collapse the two.

# Step 52 — OpenSpec Readiness

Use:

```text
READY
READY_WITH_CONDITIONS
NOT_READY
```

# Step 53 — Smallest Complete Graph Rule

A graph is complete when:

```text
every primary driver has sufficient decision/model/evidence coverage
every hard constraint is respected
critical behavior is unambiguous enough
security/trust risk is modeled
architecture is validated
```

Adding more diagrams after that is optional unless they reduce material risk.

# Step 54 — Over-Modeling Detection

Flag:

```text
OVER_MODELING
```

when a selected skill does not answer a material architecture question.

# Step 55 — Under-Modeling Detection

Flag:

```text
UNDER_MODELING
```

when a material risk has no appropriate model/evidence.

Examples:

```text
payment lifecycle without state machine
sensitive third-party transfer without DFD
distributed async system without event semantics
strict RTO/RPO without deployment/recovery model
```

# Step 56 — Ritual Architecture Detection

Flag workflows that require:

```text
every diagram
every ADR type
every model
```

regardless of system risk.

Use:

```text
RITUAL_ARCHITECTURE
```

# Step 57 — Premature Technology Decision Detection

Flag:

```text
technology selected before drivers/trade-offs
```

unless it is a hard constraint.

# Step 58 — Authority Boundary

The orchestrator may:

```text
identify decision needed
route decision
prepare alternatives
record accepted authority
```

It may not:

```text
invent product/security/legal authority
```

# Step 59 — Scope Change

If architecture discovery changes scope materially:

```text
return to PRD/requirements
```

Do not continue on stale scope.

# Step 60 — Risk Escalation

If new evidence raises risk profile:

```text
upgrade architecture profile
activate additional skills
```

Example:

```text
small CRUD
→ later includes personal data + external AI
→ activate DFD + STRIDE + provider/security sequences
```

# Step 61 — Risk Reduction

If evidence removes complexity:

```text
skip/deactivate unnecessary models
```

Do not preserve artifacts merely because they were originally planned.

# Step 62 — Existing Artifact Reuse

If artifact already satisfies the current gate:

```text
ALREADY_SATISFIED
```

Do not recreate.

# Step 63 — Conflicting Existing Artifacts

If conflicts exist:

```text
BLOCKED
```

or route to validation/ADR reconciliation.

Do not pick latest file timestamp as truth automatically.

# Step 64 — Orchestration Plan Structure

The plan should contain:

```text
scope
risk/profile classification
existing artifact inventory
selected skill DAG
activation rationale
parallelizable branches
join gates
backtracking rules
expected artifacts
acceptance gate
handoff
```

# Step 65 — Progress Tracking

Each node state:

```text
NOT_STARTED
READY
RUNNING
BLOCKED
COMPLETE
SKIPPED
SUPERSEDED
```

# Step 66 — Node Completion Evidence

A skill node is complete only when its own completion criteria pass.

Do not mark complete because a file exists.

# Step 67 — Orchestration Finding Types

Use:

```text
MISSING_INPUT
MISSING_DECISION
STALE_ARTIFACT
CONFLICTED_ARTIFACT
UNDER_MODELING
OVER_MODELING
RITUAL_ARCHITECTURE
PREMATURE_TECHNOLOGY_DECISION
SECURITY_MODEL_REQUIRED
VALIDATION_BLOCKER
```

# Step 68 — Orchestration Readiness

Use:

```text
ORCHESTRATION_PLAN_READY
ORCHESTRATION_PLAN_READY_WITH_CONDITIONS
ORCHESTRATION_REQUIRES_REQUIREMENTS
ORCHESTRATION_REQUIRES_DECISIONS
ORCHESTRATION_REQUIRES_SECURITY_MODEL
ORCHESTRATION_REQUIRES_ARTIFACT_RECONCILIATION
BLOCKED
```

# Step 69 — Final System Status

Use:

```text
ARCHITECTURE_PACKAGE_ACCEPTED
ARCHITECTURE_PACKAGE_ACCEPTED_WITH_CONDITIONS
ARCHITECTURE_PACKAGE_REQUIRES_REWORK
ARCHITECTURE_PACKAGE_REQUIRES_DECISIONS
ARCHITECTURE_PACKAGE_SECURITY_BLOCKED
ARCHITECTURE_PACKAGE_CONFLICTED
BLOCKED
```

# Step 70 — Completion Criteria

- [ ] System/change scope and decision horizon are explicit.
- [ ] Existing artifacts are inspected before creating new ones.
- [ ] Artifact freshness/conflicts are classified.
- [ ] Requirements foundation is sufficient before architecture.
- [ ] Requirements skills are skipped/reused only with evidence.
- [ ] Architecture drivers exist before candidate design.
- [ ] Behavioral models activate only when they answer material questions.
- [ ] Use-case/process/state models are not run mechanically.
- [ ] Candidate architectures precede trade-off selection.
- [ ] Trade-off analysis precedes accepted architecture decision.
- [ ] ADR authority/status is respected.
- [ ] C4 is used for meaningful system architecture structure.
- [ ] Sequence/DFD/domain/event/deployment models are selected by risk/question.
- [ ] Small CRUD does not receive complex modeling without triggers.
- [ ] High-risk payment/regulated systems receive the necessary deeper models.
- [ ] Skill activation has explicit rationale.
- [ ] Selected skills form a dependency DAG.
- [ ] Parallelism occurs only after shared decisions stabilize.
- [ ] Join gates verify architecture-version consistency.
- [ ] Downstream gaps route backward to the owning skill/decision.
- [ ] No upstream decision is silently repaired.
- [ ] STRIDE activates when trust/security risk warrants it.
- [ ] Architecture validation runs before package acceptance.
- [ ] Validation failures route to rework and revalidation.
- [ ] Architecture Package includes only applicable artifacts.
- [ ] Package manifest/status/version/authority are explicit.
- [ ] Blocking vs deferred decisions are separated.
- [ ] Smallest-complete-graph condition is demonstrated.
- [ ] Over-modeling/under-modeling/ritual architecture are audited.
- [ ] Premature technology decisions are detected.
- [ ] Authority boundaries are respected.
- [ ] Risk profile can expand or shrink dynamically.
- [ ] Existing valid artifacts are reused.
- [ ] Node completion is evidence-based.
- [ ] OpenSpec/implementation handoff preserves architecture intent.
- [ ] Final system/package status is explicit.

## References

- Read `references/orchestration-scope-profiles-and-smallest-complete-graph.md` first.
- Read `references/requirements-foundation-and-backtracking-gates.md`.
- Read `references/behavioral-model-selection-usecase-process-state.md`.
- Read `references/architecture-decision-model-selection-and-dependency-dag.md`.
- Read `references/security-stride-validation-and-feedback-loop.md`.
- Read `references/system-profiles-small-crud-payment-saas-event-brownfield-critical.md`.
- Read `references/package-assembly-openspec-handoff-and-acceptance-gates.md`.
- Read `references/software-system-orchestration-audit.md` before completion.
