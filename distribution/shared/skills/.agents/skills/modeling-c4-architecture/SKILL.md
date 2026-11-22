---
name: modeling-c4-architecture
description: Portable engineering capability `modeling-c4-architecture`. Use when
  the harness or a specialist agent explicitly requires this named capability.
---
# Modeling C4 Architecture

## Purpose

Model static architecture structure using C4 abstraction levels.

Canonical levels:

```text
L1 System Context
L2 Containers
L3 Components
L4 Code
```

Default expectation:

```text
L1 + L2
```

Use L3 only where complexity justifies it.

Avoid L4 unless there is a strong maintenance reason.

Output:

```text
c4-architecture-model.md
```

# Core Principle

C4 answers:

```text
what is the system?
who uses it?
what external systems does it depend on?
what major runtime/data containers exist?
what responsibilities do they own?
how are they structurally related?
```

It does not primarily answer:

```text
what happens over time?           → sequence diagram
what decisions/branches occur?     → process flow
what states/transitions exist?     → state machine
how data crosses trust boundaries? → DFD
what entities/relationships exist? → domain data model / ERD
where runtime instances are hosted?→ deployment diagram
```

# Use When

- Architecture decisions are accepted/proposed enough to model structure.
- System boundaries must be communicated.
- External people/systems and dependencies need a context view.
- Major deployable/runtime/data containers need a container view.
- One complex container needs internal component structure for maintenance/review.
- Architecture documentation needs a version-controlled structural model.
- ADRs need a visual/structural consequence model.

# Do Not Use When

- Candidate architectures are still being compared.
- The task is to choose architecture.
- The task is time-ordered interaction modeling.
- The task is a business workflow.
- The task is lifecycle/state modeling.
- The task is data lineage/trust-flow analysis.
- The task is detailed deployment topology.
- The task is class/package browsing without architecture purpose.

# Inputs

Preferred:

- accepted/proposed ADRs;
- selected architecture summary;
- architecture drivers;
- candidate/trade-off analysis as context;
- use cases/capabilities;
- known runtime/deployable units;
- known external systems;
- known technology choices only when decided;
- ownership/responsibility information;
- applicable `AGENTS.md`.

Optional:

- existing C4 model;
- codebase/module structure;
- deployment model;
- system inventory;
- provider contracts;
- security boundaries.

# Outputs

- C4 model document.
- L1 System Context diagram/source.
- L2 Container diagram/source.
- Optional L3 Component diagrams/source.
- Exceptional L4 model only with explicit justification.
- Element catalog.
- Relationship catalog.
- Level-selection rationale.
- Traceability to ADRs/drivers.
- Modeling-gap ledger.
- Downstream sequence/DFD/deployment handoffs.

# C4 Vocabulary

Use:

```text
Person
Software System
Container
Component
Code element (rare)
Relationship
Boundary
```

# Step 1 — Establish Model Scope

Record:

```text
system being modeled
architecture version / ADR basis
modeling purpose
audience
decision horizon
```

Do not model the entire enterprise unless needed.

# Step 2 — Level Selection

Start with:

```text
L1 + L2
```

Then ask:

```text
Does L3 materially improve understanding,
maintenance, ownership, security review,
or change reasoning for a specific container?
```

If no:

```text
skip L3
```

Ask for L4:

```text
Is code-level structure sufficiently stable,
architecturally important,
and costly to rediscover?
```

If no:

```text
skip L4
```

# Level Selection Status

Use:

```text
REQUIRED
USEFUL
NOT_NEEDED
DEFERRED
INSUFFICIENT_EVIDENCE
```

# Step 3 — System Context (L1)

L1 should contain:

```text
people / external actors
system of interest
external software systems
high-level relationships
```

It should answer:

```text
Who uses the system?
What does it do at a high level?
What other systems does it depend on?
```

# L1 Boundary Rule

The system of interest is one box.

Do not expose its internal containers at L1.

# L1 Person Rule

Use meaningful roles:

```text
Support Agent
Organization Manager
Operator
```

not individual names unless the system truly integrates with a named organizational role/entity.

# L1 External System Rule

Examples:

```text
Email Provider
AI Provider
Identity Provider
Website Chat Provider
```

Do not model internal modules as external systems.

# L1 Relationship Rule

Label relationships with intent.

Good:

```text
Support Agent → Support Platform
"Manages customer conversations"
```

Bad:

```text
Uses
Calls
Connects
```

when a more meaningful label is known.

# Step 4 — Container Model (L2)

C4 Container means a separately runnable/deployable application or data store/runtime boundary in the C4 sense.

Examples:

```text
Web Application
Backend Application
Worker
Database
Message Broker
Mobile App
Serverless Function
```

Only include containers that exist in the accepted architecture.

# Container != Docker Container

Do not assume C4 `Container` means Docker/Kubernetes container.

# L2 Responsibilities

Each container should have:

```text
name
type
responsibility
technology if decided
owner if useful
```

# L2 Technology Labels

Include technology only when actually decided.

Good:

```text
Technology: TBD
```

when architecture selected the boundary but not implementation technology.

Do not fill:

```text
React
Node.js
PostgreSQL
Kafka
Kubernetes
```

from familiarity or preference.

# Step 5 — Data Stores

A database/data store may be a C4 container.

State:

```text
what it stores / owns
which container has authoritative write ownership
who reads it
```

Do not design ERD.

# Shared Data Store

If multiple containers access one data store:

```text
show the structural relationship
```

and flag ownership ambiguity if relevant.

Do not hide coupling.

# Step 6 — External Relationships at L2

Show relevant external systems where needed to understand container responsibilities.

Example:

```text
Channel Integration
→ Email Provider
```

Avoid duplicating every L1 relation if it adds no value.

# Step 7 — Component Model (L3)

L3 models meaningful components inside ONE container.

A component is a cohesive group of functionality behind a meaningful interface.

Use L3 for questions like:

```text
How is this complex container internally decomposed?
Where is tenant authorization enforced conceptually?
How are provider adapters separated from core business rules?
Which internal components own conversation behavior vs integration?
```

# L3 Justification

Possible justifications:

```text
complexity
security boundary
change hotspot
maintenance
ownership
architectural rule enforcement
critical integration boundary
```

Record justification per L3 diagram.

# L3 Anti-Pattern

Do not turn every folder/class into a C4 component.

Bad:

```text
UserController
UserService
UserRepository
UserMapper
```

unless these are genuine long-lived architecture components, which is uncommon.

# Step 8 — L4 Code

L4 is exceptional.

Possible justification:

```text
stable framework/plugin architecture
safety-critical code structure
generated-code boundary
long-lived public extension API
complex code architecture costly to rediscover
```

Do not create L4 for ordinary packages/classes.

Use:

```text
L4_JUSTIFICATION_REQUIRED
```

if requested without reason.

# Step 9 — Relationship Direction

Every relationship should have:

```text
source
destination
description
technology/protocol only if relevant and decided
```

Do not leave unlabeled arrows when semantics are known.

# Step 10 — Relationship Scope

Show architectural dependencies, not every possible call.

Prefer:

```text
Web App → Backend Application
"Uses support capabilities"
```

not dozens of endpoint-specific edges.

# Step 11 — Bidirectional Relationships

Avoid one bidirectional arrow if the meanings differ.

Prefer two labeled relationships where direction matters.

# Step 12 — Structural Dependency vs Runtime Interaction

C4 may show structural communication/dependency.

Detailed runtime order belongs to sequences.

Example:

```text
Core Application → Email Provider
"Sends outbound customer messages"
```

C4 does not show:

```text
1. request
2. callback
3. retry
4. timeout
```

# Step 13 — Boundaries

Possible boundaries:

```text
system boundary
enterprise/organization boundary
trust/tenant boundary (when structurally relevant)
container/component boundary
```

Use boundaries to clarify ownership/scope, not decorative grouping.

# Step 14 — Tenant Boundaries

For multi-tenant systems, show tenant/user access relationships and structurally relevant authorization/data boundaries when useful.

Do not imply a tenancy storage implementation not decided.

# Step 15 — Trust Boundary Handoff

C4 may expose structural trust boundaries.

Detailed data-flow/threat analysis belongs to:

```text
modeling-data-flows
threat-modeling-with-stride
```

# Step 16 — Architecture Decisions Traceability

For each major element/boundary, link to relevant ADR.

Example:

```text
Single deployable application
→ ADR-0001
```

# Step 17 — Driver Traceability

Link structural choices to drivers when useful.

Example:

```text
Provider integration boundary
→ AD-002 provider-outage resilience
→ AD-004 provider modifiability
```

Do not restate trade-off analysis.

# Step 18 — Accepted vs Proposed Structure

If ADR is PROPOSED, model status must show:

```text
PROPOSED_STRUCTURE
```

Do not present as final architecture.

# Step 19 — Existing vs Target Architecture

For brownfield systems distinguish:

```text
CURRENT
TARGET
TRANSITION
```

Do not mix current and future elements without labels.

# Step 20 — Model Element Status

Use:

```text
CURRENT
TARGET
TRANSITION
PROPOSED
DEPRECATED
EXTERNAL
```

when helpful.

# Step 21 — Naming

Use domain/architecture language.

Good:

```text
Support Platform
Channel Integration Module
Conversation Module
Audit Module
```

Bad:

```text
Service1
Backend2
Misc Utils
```

# Step 22 — Responsibility Descriptions

Each element gets one concise responsibility statement.

Avoid technology-only descriptions.

Bad:

```text
Node.js service
```

Good:

```text
Owns support conversation behavior and coordinates authorized agent actions.
```

# Step 23 — Technology Description Discipline

Technology answers:

```text
How is the element implemented?
```

Responsibility answers:

```text
Why does the element exist?
```

Never substitute one for the other.

# Step 24 — Diagram Syntax

Prefer version-controlled text.

Recommended options:

```text
Structurizr DSL
PlantUML with C4-PlantUML
Mermaid C4 where repository/tooling supports it reliably
```

Follow repository convention if one exists.

Do not force a syntax unsupported by the target renderer.

# Step 25 — Syntax Neutrality

The skill's semantic model is primary.

If no rendering convention exists:

```text
provide an element/relationship catalog
plus a portable text diagram source
```

# Step 26 — Context Diagram Density

L1 should normally be simple enough to understand quickly.

If dozens of external systems appear:

```text
group/split by relevant ecosystem
or show only architecturally relevant relationships
```

# Step 27 — Container Diagram Density

If L2 becomes unreadable:

```text
split by system/zone
or create supplementary focused views
```

without changing element identity.

# Step 28 — Stable Element Identity

Assign stable model IDs:

```text
PERSON-001
SYS-001
EXTSYS-001
CONT-001
COMP-001
REL-001
```

or repository convention.

# Step 29 — Relationship Consistency

Same relationship must not have contradictory labels across diagrams.

# Step 30 — Level Consistency

Do not place:

```text
Component
```

directly inside System Context without its container hierarchy.

Maintain:

```text
System
→ Container
→ Component
→ Code
```

# Step 31 — Abstraction Mixing Audit

Bad diagram:

```text
Support Agent
Backend
ConversationController
PostgreSQL table
AWS Region
```

all at one level.

Flag:

```text
C4_ABSTRACTION_MIXING
```

# Step 32 — Runtime Instance Leakage

Do not show:

```text
pod-1
pod-2
node-a
availability-zone-b
```

in logical C4 container/component views.

Those belong to deployment modeling.

# Step 33 — Data Model Leakage

Do not show:

```text
Conversation table
Agent row
Tenant foreign key
```

as C4 elements.

Use domain data model/ERD later.

# Step 34 — Process/State Leakage

Do not embed:

```text
Approved?
Resolved?
Retry 3 times
```

into C4.

# Step 35 — Sequence Leakage

Do not number C4 arrows to imply runtime order.

# Step 36 — Event Flow Leakage

C4 may show event relationship structurally if decided.

Detailed:

```text
producer
event
consumer
delivery semantics
ordering/retry
```

belongs to `modeling-event-flows`.

# Step 37 — Deployment Handoff

C4 L2 identifies logical/runtime containers.

`modeling-deployment-architecture` later maps them to:

```text
nodes
regions
clusters
platforms
replicas
network zones
```

# Step 38 — Sequence Handoff

Identify critical relationships requiring runtime sequence models.

Examples:

```text
inbound email ingestion
AI-assisted reply
authentication flow
```

# Step 39 — DFD Handoff

Identify relationships carrying sensitive/trust-boundary data.

# Step 40 — Component Model Handoff Discipline

If L3 is justified, choose only the container needing deeper modeling.

Do not generate L3 for all containers automatically.

# Step 41 — Model Completeness

L1 audit:

```text
people?
system of interest?
relevant external systems?
meaningful relations?
```

L2 audit:

```text
accepted containers?
responsibilities?
data stores?
external dependencies?
relationships?
```

# Step 42 — Orphan Element Audit

Every non-root element should have a reason/relationship.

Flag unconnected diagram boxes unless intentionally isolated.

# Step 43 — Missing Relationship Audit

If source docs say two elements interact and C4 omits the architecturally important relation:

```text
C4_RELATIONSHIP_GAP
```

# Step 44 — Architecture Conflict Audit

If C4 structure contradicts accepted ADR:

```text
C4_ADR_CONFLICT
```

Do not silently “fix” the ADR or diagram.

# Step 45 — Unresolved Structure

Use:

```text
STRUCTURE_DECISION_REQUIRED
```

if architecture hasn't decided an element/boundary.

Do not invent containers.

# Step 46 — L3 Need Decision

Use:

```text
L3_NOT_NEEDED
L3_USEFUL
L3_REQUIRED
L3_DEFERRED
```

# Step 47 — L4 Need Decision

Default:

```text
L4_NOT_NEEDED
```

unless strong evidence exists.

# Step 48 — Model Quality Status

Use:

```text
READY
READY_WITH_OPEN_QUESTIONS
REQUIRES_STRUCTURE_DECISION
REQUIRES_RELATIONSHIP_CLARIFICATION
REQUIRES_ADR_ALIGNMENT
CONFLICTED
```

# Final Decision

Use:

```text
C4_MODEL_READY
C4_MODEL_READY_WITH_OPEN_QUESTIONS
C4_MODEL_REQUIRES_STRUCTURE_DECISION
C4_MODEL_REQUIRES_RELATIONSHIP_CLARIFICATION
C4_MODEL_REQUIRES_ADR_ALIGNMENT
C4_MODEL_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/c4-architecture-model.md
```

## Completion Criteria

- [ ] System/model scope is explicit.
- [ ] Architecture/ADR basis is recorded.
- [ ] L1 + L2 are the default selected levels.
- [ ] L3 has explicit justification when included.
- [ ] L4 has a strong maintenance justification or is omitted.
- [ ] L1 contains people, system of interest, external systems, and meaningful relations.
- [ ] Internal containers are not leaked into L1.
- [ ] L2 containers correspond to accepted logical/runtime boundaries.
- [ ] C4 Container is not confused with Docker container.
- [ ] Responsibilities are domain/architecture oriented.
- [ ] Technology labels are included only when decided.
- [ ] Data stores show structural ownership without ERD detail.
- [ ] External dependencies are modeled at relevant levels.
- [ ] L3 components are cohesive architectural components, not folders/classes.
- [ ] Relationships are directed/labeled meaningfully.
- [ ] Structural relationships are not expanded into runtime sequences.
- [ ] Boundaries clarify scope/ownership/trust without inventing implementation.
- [ ] Tenant/security boundaries do not invent storage topology.
- [ ] ADR/driver traceability exists.
- [ ] Proposed/current/target structure is not mixed ambiguously.
- [ ] Naming is meaningful.
- [ ] Version-control-friendly source is preferred.
- [ ] Stable element IDs exist.
- [ ] Element/relationship definitions remain consistent across views.
- [ ] Abstraction levels are not mixed.
- [ ] Runtime instances/deployment nodes are excluded.
- [ ] ERD/process/state/sequence/event-flow details are excluded.
- [ ] Sequence/DFD/deployment handoffs are identified.
- [ ] L3 is not generated for every container.
- [ ] L1/L2 completeness is audited.
- [ ] Orphan elements/missing relations are audited.
- [ ] ADR conflicts are surfaced.
- [ ] Undecided structure remains explicit.
- [ ] Final readiness is explicit.

## References

- Read `references/c4-purpose-levels-and-level-selection.md` first.
- Read `references/system-context-people-external-systems-and-boundaries.md`.
- Read `references/container-model-responsibilities-data-stores-and-technologies.md`.
- Read `references/component-model-l3-and-code-level-l4-discipline.md`.
- Read `references/relationships-identities-naming-and-consistency.md`.
- Read `references/c4-vs-sequence-dfd-domain-event-and-deployment-models.md`.
- Read `references/brownfield-current-target-and-adr-traceability.md`.
- Read `references/c4-architecture-model-audit.md` before completion.
