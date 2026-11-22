---
name: modeling-data-flows
description: Models how data moves across external entities, processes, data stores, systems, and trust boundaries, with explicit data classes, ownership, direction, third-party transfers, secrets, privacy/security relevance, residency constraints, and traceability. Use after accepted architecture/C4 and important runtime sequences exist, especially before STRIDE threat modeling, privacy review, or security validation. Produce a data-flow model and DFD views without inventing fields, schemas, protocols, encryption, retention, regions, controls, or provider behavior. Do not use DFDs as sequence diagrams, ERDs, process flows, state machines, or deployment diagrams.
---

# Modeling Data Flows

## Purpose

Model how data moves through the system.

Canonical focus:

```text
external entities
+ processes
+ data stores
+ data flows
+ trust boundaries
```

Primary security handoff:

```text
DFD
+ trust boundaries
→ threat-modeling-with-stride
```

Output:

```text
data-flow-model.md
```

# Core Principle

A DFD answers:

```text
what data moves?
from where?
to where?
through which process?
into which store?
across which trust boundary?
for what purpose?
```

It does not primarily answer:

```text
in what runtime order?              → sequence diagram
what entities/cardinality exist?    → domain data model / ERD
what business branch happens next?  → process flow
what lifecycle transition occurs?   → state machine
what static components exist?       → C4
where runtime nodes are hosted?      → deployment architecture
```

# Use When

- Sensitive or regulated data moves across the architecture.
- External providers receive/send data.
- Tenant boundaries matter.
- Trust boundaries need explicit modeling.
- Privacy review needs data-transfer visibility.
- Secrets/credentials cross boundaries.
- Data residency constraints may affect flows/stores.
- STRIDE threat modeling needs a DFD.
- Third-party transfer or logging/analytics behavior matters.
- Sequence models exist but do not expose enough data/security semantics.

# Do Not Use When

- Only static structure is needed.
- The task is exact message timing/order.
- The task is conceptual entity/relationship modeling.
- The task is database schema design.
- The task is deployment topology.
- Data classifications/purposes are not known enough to model without invention.
- The task is to choose encryption/control mechanisms.

# Inputs

Preferred:

- C4 architecture model;
- system sequence models;
- functional requirements;
- NFRs / privacy/security requirements;
- quality scenarios;
- ADRs;
- external integration contracts;
- known data classifications;
- accepted tenant boundaries;
- accepted data residency policy;
- accepted retention/privacy policy;
- secret/credential handling requirements;
- applicable `AGENTS.md`.

Optional:

- existing DFDs;
- privacy inventory;
- data catalog;
- threat model;
- provider agreements;
- logging/analytics requirements;
- deployment model.

# Outputs

- Data Flow Model.
- DFD context/level views when useful.
- External entity catalog.
- Process catalog.
- Data store catalog.
- Data-flow catalog.
- Trust-boundary catalog.
- Data classification and purpose matrix.
- Third-party transfer inventory.
- Secret/credential flow inventory.
- Residency/privacy gap ledger.
- STRIDE handoff.
- Traceability.

# DFD Vocabulary

Use:

```text
External Entity
Process
Data Store
Data Flow
Trust Boundary
```

Avoid mixing C4 semantics into DFD notation without a clear mapping.

# Element Identity

Prefer stable IDs:

```text
EE-001   external entity
PROC-001 process
DS-001   data store
DF-001   data flow
TB-001   trust boundary
```

Follow repository convention if one exists.

# Step 1 — Define DFD Scope

Record:

```text
system/scenario being modeled
architecture version / ADR basis
security/privacy question
included flows
excluded flows
```

Keep each DFD bounded enough to review.

# Step 2 — Select DFD Level

Useful levels:

```text
Context DFD
→ system as one process + external entities + major flows

Level 1 DFD
→ major internal processes/stores + trust boundaries

Focused DFD
→ one sensitive scenario/integration
```

Do not create deeper decomposition without a security/privacy question.

# Step 3 — External Entities

External entities may include:

```text
end user
administrator
operator
identity provider
payment provider
email provider
analytics provider
partner system
```

Do not model internal modules as external entities.

# Step 4 — Processes

Processes transform, validate, route, authorize, or otherwise act on data.

Examples:

```text
Conversation Processing
Tenant Authorization
Channel Integration
AI Assistance
Audit/Operations
```

A process is not automatically a deployable service.

Use architecture-aligned responsibilities.

# Step 5 — Data Stores

Stores may include:

```text
primary persistent store
audit store
object storage
cache
secret store
```

only when accepted architecture says they exist.

Do not invent stores.

# Step 6 — Data Flows

Every flow should identify:

```text
source
destination
data category/content
purpose
direction
trust boundary crossed
source evidence
```

# Step 7 — Semantic Data Labels

Good:

```text
customer conversation content
tenant-scoped conversation request
AI prompt/context
audit event metadata
authentication assertion
provider credentials
```

Bad:

```text
payload
data
JSON
object
```

unless no more precise semantics are known.

# Step 8 — Field Discipline

Do not invent exact fields.

If exact content is unknown:

```text
FIELDS_TBD
```

Keep category-level semantics.

# Step 9 — Data Classification

Use accepted classification scheme if one exists.

Otherwise use neutral descriptive categories such as:

```text
PUBLIC
INTERNAL
CONFIDENTIAL
PERSONAL_DATA
AUTHENTICATION_DATA
SECRET
FINANCIAL
HEALTH
UNKNOWN
```

Do not infer sensitive classes without evidence.

# Step 10 — Purpose

Each material flow should state why the data moves.

Examples:

```text
display conversation
authorize tenant access
deliver outbound email
generate optional AI suggestion
record privileged action
diagnose ingestion failure
```

Purpose is important for privacy review.

# Step 11 — Data Owner / Controller Semantics

Record accepted ownership/accountability where known.

Examples:

```text
tenant organization
support platform
external provider
TBD
```

Do not invent legal-controller/processor roles.

# Step 12 — Trust Boundaries

Roadmap-critical.

A trust boundary is where trust assumptions/security authority changes.

Examples:

```text
user device ↔ platform
platform ↔ external provider
tenant A ↔ tenant B isolation boundary
public internet ↔ private application environment
privileged operator boundary
```

Only model boundaries supported by architecture/context.

# Step 13 — Tenant Boundary

For multi-tenant systems, explicitly represent:

```text
tenant context
tenant-scoped data
cross-tenant prohibition
```

Do not invent tenant-per-database/schema architecture.

# Step 14 — External Provider Boundary

Third-party provider interaction generally crosses a trust/organizational boundary.

Record:

```text
data sent
data received
purpose
provider
classification
unknown policy/contract details
```

# Step 15 — Third-Party Transfer

Roadmap-critical.

For every third-party transfer capture:

```text
recipient/provider
data category
purpose
direction
legal/policy basis if explicitly known
residency if known
retention if known
```

If unknown:

```text
THIRD_PARTY_POLICY_REQUIRED
```

Do not invent GDPR roles, DPA terms, or jurisdiction.

# Step 16 — Privacy

Roadmap-critical.

Privacy review questions:

```text
is personal data transferred?
is purpose known?
is data minimized?
is retention known?
is deletion/export behavior known?
is third-party transfer known?
is logging duplicating sensitive content?
```

Do not solve privacy policy inside DFD.

# Step 17 — Data Minimization

If only a subset is required for an external provider and policy requires minimization, record that requirement.

Do not invent which fields can be removed.

Use:

```text
MINIMIZATION_DECISION_REQUIRED
```

when detail is unresolved.

# Step 18 — Residency

Roadmap-critical.

Record accepted:

```text
data class
store/process/provider
required geography/jurisdiction
```

If no residency requirement exists:

```text
RESIDENCY_NOT_SPECIFIED
```

Do not invent EU-only/US-only.

# Step 19 — Retention

Capture retention only when accepted.

If unresolved:

```text
RETENTION_POLICY_REQUIRED
```

Do not invent 30/90/365 days.

# Step 20 — Secrets

Roadmap-critical.

Model secret/credential flows where relevant:

```text
provider API credential
service credential
authentication token
signing secret
```

Do not expose actual secret values.

# Step 21 — Secret Flow Questions

Record:

```text
where secret originates
which process consumes it
whether it crosses trust boundary
whether it is stored
```

Do not invent vault/key-management mechanism.

# Step 22 — Authentication Data

Possible:

```text
identity assertion
session credential
access token
```

Only if accepted flow requires it.

Do not copy full token contents into diagrams.

# Step 23 — Authorization Context

For protected data flows, show authorization context where material.

Example:

```text
Support Agent
→ Tenant Authorization Process:
tenant-scoped conversation request/context
```

Do not model UI visibility as authorization.

# Step 24 — Logging / Audit

Logging can create additional data flows/stores.

If accepted:

```text
privileged action
→ audit/operations process
→ audit store
```

Classify logged data.

Do not assume full payload logging.

# Step 25 — Observability

Operational telemetry may contain:

```text
tenant identifier
provider identifier
error metadata
request metadata
```

Do not assume conversation content is logged.

If unclear:

```text
LOGGING_DATA_SCOPE_REQUIRED
```

# Step 26 — AI Provider Transfers

For AI interactions, explicitly record:

```text
what customer/tenant context is sent
what response returns
purpose
third-party boundary
classification
retention/training policy if known
```

If provider policy unknown:

```text
AI_DATA_POLICY_REQUIRED
```

Do not invent provider guarantees.

# Step 27 — Email / Messaging Providers

Record:

```text
message content
recipient/sender metadata
tenant/channel context
provider response/message
```

only at known semantic level.

# Step 28 — Data Store Read/Write Direction

Distinguish:

```text
read
write
read/write
```

when important.

# Step 29 — Derived Data

If a process creates derived data:

```text
AI suggestion
audit metadata
aggregated metric
```

classify it separately if risk/privacy differs.

# Step 30 — Data Duplication

Identify when the same data may exist in:

```text
primary store
logs
audit
provider
analytics
cache
backup
```

only where accepted/evidenced.

Do not invent copies.

# Step 31 — Temporary Data

If transient processing is known:

```text
memory/temp file/staging
```

can be represented when material.

Do not invent temporary storage mechanisms.

# Step 32 — Encryption Boundary

Do not assume encryption state.

If requirement says:

```text
data encrypted in transit/at rest
```

record requirement reference.

Do not choose TLS/KMS/cipher.

# Step 33 — Integrity Requirements

Record accepted integrity/authenticity requirements for flows.

Do not choose signing/hashing technique.

# Step 34 — Flow Direction

Avoid ambiguous bidirectional arrows.

Prefer separate flows if:

```text
request data
response data
```

have different classifications/purposes.

# Step 35 — Flow Granularity

Do not create one flow per field.

Prefer meaningful categories.

Split when:

```text
classification differs
purpose differs
trust boundary differs
retention differs
recipient differs
```

# Step 36 — DFD Context View

Context view should show:

```text
system as one process
external entities
major incoming/outgoing data
major trust boundaries
```

Useful for overall threat-model scope.

# Step 37 — DFD Level 1

Level 1 can show:

```text
major internal processes
stores
external entities
trust boundaries
```

aligned with accepted architecture.

# Step 38 — Focused DFD

Create focused DFDs for:

```text
authentication
AI transfer
payment
email ingestion
privileged audit
file upload
```

when security/privacy review benefits.

Do not create all possible focused DFDs automatically.

# Step 39 — Diagram Syntax

Prefer version-control-friendly representations.

Options:

```text
Mermaid flowchart
PlantUML
Graphviz
repository DFD convention
```

The semantic catalog is primary.

# Step 40 — Diagram Shape Discipline

Represent different DFD element types consistently.

Do not rely solely on color.

# Step 41 — DFD vs Sequence

Sequence:

```text
temporal order
```

DFD:

```text
data movement and boundaries
```

Do not number DFD arrows.

# Step 42 — DFD vs C4

C4:

```text
architecture structure
```

DFD:

```text
security/privacy-relevant data movement
```

DFD processes may map to C4 containers/components, but semantics are different.

# Step 43 — DFD vs ERD

ERD/domain data:

```text
entities + relationships + cardinality
```

DFD:

```text
data moving among processes/stores/entities
```

Do not put foreign keys/cardinality into DFD.

# Step 44 — DFD vs Event Flow

Event flow will later define:

```text
producer
event
consumer
schema/contract
delivery semantics
ordering/replay
```

DFD can classify the event data and trust crossing without owning those delivery semantics.

# Step 45 — DFD vs Deployment

Residency/trust boundaries may reference deployment constraints, but nodes/regions/topology belong to deployment architecture.

# Step 46 — C4 Alignment

Every internal DFD process/store should map to:

```text
accepted C4 element
or
explicit logical responsibility inside an accepted container
```

If not:

```text
DFD_C4_ALIGNMENT_REQUIRED
```

# Step 47 — Sequence Alignment

Data flows should not contradict accepted sequence participants/direction.

Use:

```text
DFD_SEQUENCE_CONFLICT
```

# Step 48 — Privacy Requirement Alignment

If privacy requirements say data must not leave a boundary but DFD shows transfer:

```text
DFD_PRIVACY_CONFLICT
```

# Step 49 — Residency Alignment

If accepted residency constraint conflicts with provider/store location:

```text
DFD_RESIDENCY_CONFLICT
```

Do not resolve silently.

# Step 50 — Tenant Isolation Audit

Check:

```text
any cross-tenant flow?
any shared process/store without tenant-scoped context?
any external transfer lacking tenant purpose?
```

Flag questions, not invented controls.

# Step 51 — Secret Exposure Audit

Check:

```text
secret flows to unnecessary participant?
secret stored where not evidenced?
secret crosses third party?
```

# Step 52 — Third-Party Audit

Check every external transfer for:

```text
data class
purpose
policy/residency/retention known?
```

# Step 53 — Logging Audit

Check whether logs/audit/telemetry receive sensitive content.

If unknown:

```text
LOGGING_DATA_SCOPE_REQUIRED
```

# Step 54 — Store Audit

Every store should state:

```text
data classes
purpose
authority/owner if known
retention/residency if known
```

# Step 55 — Orphan Flow Audit

Every flow must connect valid source/destination.

# Step 56 — Orphan Store/Process Audit

Every process/store should have at least one meaningful flow unless intentionally isolated.

# Step 57 — Data Classification Gap

Use:

```text
DATA_CLASSIFICATION_REQUIRED
```

# Step 58 — Purpose Gap

Use:

```text
DATA_PURPOSE_REQUIRED
```

# Step 59 — Third-Party Policy Gap

Use:

```text
THIRD_PARTY_POLICY_REQUIRED
```

# Step 60 — Residency Gap

Use:

```text
RESIDENCY_POLICY_REQUIRED
```

only when residency must be decided; otherwise use `RESIDENCY_NOT_SPECIFIED`.

# Step 61 — Retention Gap

Use:

```text
RETENTION_POLICY_REQUIRED
```

# Step 62 — Secret Handling Gap

Use:

```text
SECRET_HANDLING_DECISION_REQUIRED
```

# Step 63 — Logging Scope Gap

Use:

```text
LOGGING_DATA_SCOPE_REQUIRED
```

# Step 64 — Threat Modeling Handoff

For each trust boundary, process, store, and external flow provide STRIDE input.

Canonical:

```text
DFD
+ trust boundaries
→ threat-modeling-with-stride
```

# Step 65 — STRIDE Element Mapping

Typical threat review anchors:

```text
External Entity
Process
Data Store
Data Flow
Trust Boundary
```

Do not perform the full threat analysis here.

# Step 66 — STRIDE Preparation

Provide:

```text
assets
entry points
trust boundaries
sensitive flows
external dependencies
privileged flows
secrets
```

# Step 67 — Privacy Review Handoff

Provide:

```text
personal data flows
third-party transfers
unknown retention
unknown residency
unknown minimization
logging duplication
```

# Step 68 — Domain Data Handoff

Flag data concepts/stores needing:

```text
modeling-domain-data
```

Do not create conceptual/logical ERD inside DFD.

# Step 69 — Event Flow Handoff

Flag data flows that are architecturally asynchronous/events.

# Step 70 — Deployment Handoff

Flag residency/network/trust questions requiring deployment topology.

# Model Quality Status

Use:

```text
READY
READY_WITH_OPEN_QUESTIONS
REQUIRES_DATA_CLASSIFICATION
REQUIRES_DATA_PURPOSE
REQUIRES_THIRD_PARTY_POLICY
REQUIRES_RESIDENCY_POLICY
REQUIRES_RETENTION_POLICY
REQUIRES_SECRET_HANDLING_DECISION
REQUIRES_C4_ALIGNMENT
CONFLICTED
```

# Final Decision

Use:

```text
DATA_FLOW_MODEL_READY
DATA_FLOW_MODEL_READY_WITH_OPEN_QUESTIONS
DATA_FLOW_MODEL_REQUIRES_DATA_CLASSIFICATION
DATA_FLOW_MODEL_REQUIRES_DATA_PURPOSE
DATA_FLOW_MODEL_REQUIRES_THIRD_PARTY_POLICY
DATA_FLOW_MODEL_REQUIRES_RESIDENCY_POLICY
DATA_FLOW_MODEL_REQUIRES_RETENTION_POLICY
DATA_FLOW_MODEL_REQUIRES_SECRET_HANDLING_DECISION
DATA_FLOW_MODEL_REQUIRES_C4_ALIGNMENT
DATA_FLOW_MODEL_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/data-flow-model.md
```

## Completion Criteria

- [ ] DFD scope/security/privacy question is explicit.
- [ ] DFD level/view choice is justified.
- [ ] External entities are truly external.
- [ ] Internal processes align with accepted architecture responsibilities.
- [ ] Data stores are not invented.
- [ ] Every material data flow has source/destination/direction.
- [ ] Data labels are semantic, not generic payload labels.
- [ ] Exact fields are not invented.
- [ ] Classification uses accepted evidence or remains unknown.
- [ ] Purpose is explicit.
- [ ] Ownership/accountability is not invented.
- [ ] Trust boundaries are explicit.
- [ ] Tenant boundary is represented without inventing tenancy storage.
- [ ] Third-party transfers are explicit.
- [ ] Privacy/residency/retention gaps remain visible.
- [ ] Secret flows are modeled without exposing values or inventing vault mechanisms.
- [ ] Authentication/authorization data is modeled only where relevant.
- [ ] Logging/audit/telemetry data flows are not assumed.
- [ ] AI/provider transfers do not inherit invented policy guarantees.
- [ ] Data-store read/write direction is clear where material.
- [ ] Derived/duplicated/temp data is represented only with evidence.
- [ ] Encryption/integrity requirements do not imply chosen controls.
- [ ] Flow granularity is useful and not field-level noise.
- [ ] Context/Level 1/focused DFDs are created only when useful.
- [ ] Diagram syntax is version-control friendly.
- [ ] DFD is not a sequence/C4/ERD/event/deployment diagram.
- [ ] C4/sequence/privacy/residency conflicts are surfaced.
- [ ] Tenant/secret/third-party/logging/store audits are performed.
- [ ] Orphan elements/flows are checked.
- [ ] Classification/purpose/policy/residency/retention/secret gaps are explicit.
- [ ] STRIDE handoff is explicit.
- [ ] Privacy/domain/event/deployment handoffs are explicit.
- [ ] Final readiness is explicit.

## References

- Read `references/dfd-purpose-scope-levels-and-elements.md` first.
- Read `references/data-classification-purpose-ownership-and-granularity.md`.
- Read `references/trust-boundaries-tenancy-third-party-and-residency.md`.
- Read `references/privacy-retention-minimization-logging-and-ai-transfers.md`.
- Read `references/secrets-authentication-authorization-and-integrity-flows.md`.
- Read `references/dfd-vs-c4-sequence-erd-event-and-deployment.md`.
- Read `references/stride-preparation-traceability-and-model-alignment.md`.
- Read `references/data-flow-model-audit.md` before completion.
