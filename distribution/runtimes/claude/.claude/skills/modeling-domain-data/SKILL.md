---
name: modeling-domain-data
description: Models conceptual and logical domain data, including concepts/entities, relationships, cardinality, ownership, identifiers, invariants, tenant boundaries, and lifecycle, without prematurely equating domain entities with database tables. Use after requirements, use cases, state/process models, accepted architecture, and DFDs provide enough semantic evidence to define the information model. Produce a conceptual model first, a logical model when useful, and a physical schema only when explicitly required. Generate an ERD only when persistence relationships benefit from visualization. Do not invent fields, table names, SQL types, indexes, foreign keys, partitions, persistence technology, retention policy, or aggregate boundaries that are not supported by evidence.
---

# Modeling Domain Data

## Purpose

Model the system's data concepts and their relationships without prematurely turning the domain model into a database schema.

Canonical progression:

```text
Conceptual Data Model
→ Logical Data Model
→ Physical Schema (only when needed)
```

Output:

```text
domain-data-model.md
```

## Core Principle

A domain/data model should first answer:

```text
what concepts exist?
what do they mean?
how are they related?
what owns them?
how are they identified?
what invariants constrain them?
how do tenant and lifecycle boundaries affect them?
```

It should not begin with:

```text
tables
columns
SQL types
indexes
foreign keys
```

unless physical persistence design is explicitly required.

# Use When

- Domain concepts must be clarified across requirements and architecture.
- Use cases refer to related business objects whose relationships are not explicit.
- Persistence ownership needs clarification.
- Cardinalities matter.
- Tenant-scoped ownership matters.
- Lifecycle/state models imply data invariants.
- DFDs reveal important stored/derived data concepts.
- Architecture boundaries need logical data ownership.
- An ERD would materially clarify persistence relationships.

# Do Not Use When

- The task is only data movement/trust boundaries; use `modeling-data-flows`.
- The task is physical SQL schema design.
- The task is repository/ORM implementation.
- The task is event contract modeling; use `modeling-event-flows`.
- The task is lifecycle transition modeling; use `modeling-state-machines`.
- The task is architecture decomposition.
- The task is to force one table per Domain Entity.

# Inputs

Preferred:

- functional requirements;
- use-case catalog;
- process-flow model;
- state-machine model;
- accepted ADRs/C4 architecture;
- data-flow model;
- business rules;
- accepted tenant boundaries;
- accepted identifiers;
- accepted persistence/ownership constraints;
- applicable `AGENTS.md`.

Optional:

- existing domain model;
- existing ERD/schema;
- API/event contracts;
- data dictionary;
- legacy persistence model;
- migration requirements.

# Outputs

- Conceptual data model.
- Logical data model when useful.
- Optional physical-schema handoff.
- Concept/entity catalog.
- Relationship/cardinality catalog.
- Identifier catalog.
- Ownership/authority model.
- Invariant catalog.
- Tenant-boundary model.
- Lifecycle linkage.
- Optional ERD.
- Traceability and modeling-gap ledger.

# Modeling Layers

## Conceptual

Focus:

```text
business concepts
meaning
relationships
ownership
high-level cardinality
```

No implementation fields/types required.

## Logical

Focus:

```text
logical entities/value concepts
identifiers
relationship mechanics
required/optional associations
logical ownership
invariants
lifecycle-relevant attributes
```

Still technology-neutral.

## Physical

Focus only when explicitly needed:

```text
tables/collections
columns
types
keys
indexes
partitions
constraints
migration
```

Physical schema is downstream by default.

# Step 1 — Establish Modeling Scope

Record:

```text
domain/bounded system scope
model purpose
source requirements/models
conceptual/logical/physical levels requested
current vs target model
```

Do not model the whole enterprise by default.

# Step 2 — Extract Domain Concepts

Candidate concepts come from:

```text
FRs
use cases
business rules
state machines
process flows
DFD stores/data categories
ADRs/C4 responsibilities
```

Examples:

```text
Organization
User
Support Agent
Conversation
Message
Internal Note
Channel Connection
Assignment
Audit Entry
AI Suggestion
```

Do not automatically promote every noun.

# Step 3 — Concept Test

A useful concept should have meaningful domain semantics.

Avoid accidental concepts such as:

```text
Request DTO
Response DTO
Controller
Database Row
JSON Payload
```

unless the task is explicitly technical data modeling.

# Step 4 — Entity vs Value Concept

Where useful distinguish:

```text
entity
→ has identity over time

value concept
→ defined primarily by its value
```

Do not force DDD terminology if evidence does not support it.

# Step 5 — Concept Definition

For each concept record:

```text
name
meaning
scope
identity significance
owner/authority
source
```

Avoid vague definitions.

# Step 6 — Relationships

Model semantic relationships.

Examples:

```text
Organization owns Conversations
Conversation contains Messages
Conversation may be assigned to Support Agent
Organization has Channel Connections
Manager performs privileged Reassignment
```

Do not model implementation joins.

# Step 7 — Relationship Direction

Name relationships semantically in both directions when useful.

Example:

```text
Organization owns Conversation
Conversation belongs to Organization
```

# Step 8 — Cardinality

Roadmap-required.

Use:

```text
1
0..1
0..*
1..*
```

only when evidence supports it.

If unknown:

```text
CARDINALITY_REQUIRED
```

Do not infer from database habits.

# Step 9 — Optionality

Cardinality and optionality should reflect business semantics.

Example:

```text
Conversation → assigned agent: 0..1
```

only if unassigned conversations are accepted.

# Step 10 — Ownership

Roadmap-required.

Distinguish:

```text
business ownership
authoritative data ownership
lifecycle ownership
persistence ownership
```

where relevant.

Do not treat "can read" as "owns".

# Step 11 — Architecture Ownership

Map authoritative logical data to the accepted architecture boundary.

Example:

```text
Conversation data
→ Conversation capability/module
```

Do not invent a separate service.

# Step 12 — Shared Data

If multiple capabilities read a concept:

```text
one may still be authoritative owner
others may consume/reference it
```

Avoid ambiguous shared ownership.

Use:

```text
DATA_OWNERSHIP_REQUIRED
```

when unresolved.

# Step 13 — Identifiers

Roadmap-required.

Record semantic identifiers only when known.

Examples:

```text
organization identifier
conversation identifier
message identifier
external provider message identifier
```

Do not invent UUID/ULID/integer/string formats.

# Step 14 — Natural vs Surrogate Identity

Only decide when required.

Do not assume surrogate keys.

# Step 15 — External Identifiers

Keep external provider identifiers distinct from internal identity when useful.

Do not assume they are globally unique beyond provider guarantees.

# Step 16 — Identity Stability

Ask:

```text
does identity persist across lifecycle changes?
can external mapping change?
```

Record only known semantics.

# Step 17 — Invariants

Roadmap-required.

Invariants describe business/data truths that must hold.

Examples:

```text
Conversation belongs to exactly one Organization.
Reassignment target must belong to same Organization.
Internal Note is not customer-visible.
Cross-tenant conversation ownership is forbidden.
```

Link to business rules.

# Step 18 — Invariant vs Validation

Invariant:

```text
must always hold in valid domain state
```

Input validation:

```text
checks one incoming request
```

Do not conflate.

# Step 19 — Tenant Boundaries

Roadmap-required.

For each tenant-scoped concept record:

```text
tenant owner
tenant-scoped identifier assumptions
cross-tenant relationship rules
shared/global concepts
```

Do not invent tenant-per-schema/database design.

# Step 20 — Cross-Tenant Relationships

Explicitly flag any accepted cross-tenant relation.

If none:

```text
cross-tenant ownership forbidden
```

where supported.

# Step 21 — Lifecycle

Roadmap-required.

Link concepts to state machines.

Example:

```text
Conversation
states:
OPEN
RESOLVED
```

Do not duplicate transition logic in the data model.

# Step 22 — Lifecycle Attributes

Logical data model may include lifecycle-relevant attributes such as:

```text
status
resolved timestamp
```

only if source evidence supports them.

Do not invent timestamps.

# Step 23 — Historical Data

If audit/history is required, model the concept:

```text
Audit Entry
Assignment History
Status History
```

only when requirements support persistence/history.

Do not assume event sourcing.

# Step 24 — Event vs Historical Record

An event in `modeling-event-flows` is not automatically a stored history entity.

# Step 25 — Derived Data

Mark concepts as:

```text
AUTHORITATIVE
DERIVED
EPHEMERAL
EXTERNAL_REFERENCE
```

when useful and supported.

Example:

```text
AI Suggestion
→ DERIVED / optional
```

Do not assume it is persisted.

# Step 26 — Ephemeral Data

Do not model transient AI suggestions/messages as persistent logical entities unless persistence is required.

# Step 27 — External Data

Provider-owned concepts may be represented as external references/mappings.

Avoid copying external schemas into the domain model unless needed.

# Step 28 — Conceptual Model

Produce a concise conceptual model first.

Example:

```text
Organization
  1 ── owns ── 0..* Conversation

Conversation
  1 ── contains ── 1..* Message
```

Only use supported cardinalities.

# Step 29 — Logical Model

Add detail only when it improves architecture/implementation reasoning:

```text
identity
ownership
required/optional relation
invariant
lifecycle linkage
external reference
```

# Step 30 — Physical Schema Gate

Before physical modeling ask:

```text
Is a physical persistence decision explicitly required now?
```

If no:

```text
PHYSICAL_SCHEMA_NOT_NEEDED
```

# Step 31 — Physical Schema Handoff

When needed later, physical design may include:

```text
table/collection design
keys
indexes
constraints
partitioning
types
migration
```

This skill should hand off rather than invent.

# Step 32 — Domain Entity != Table

Roadmap-critical.

Do not assume:

```text
Domain Entity
→ one table
```

Possible persistence mappings can be:

```text
multiple concepts → one table
one concept → multiple tables
embedded/document
external reference
derived view
not persisted
```

No choice without evidence.

# Step 33 — Value Object != Table

Value concepts often do not need independent persistence identity.

Do not create tables automatically.

# Step 34 — Aggregate Boundary

Only model aggregate/transaction boundaries when domain evidence supports them.

Do not infer from relationships alone.

Use:

```text
AGGREGATE_BOUNDARY_REQUIRED
```

if explicitly needed but unresolved.

# Step 35 — Transaction Boundary

Logical ownership/invariants may suggest transaction concerns, but do not select DB transaction strategy.

# Step 36 — ERD Decision

Roadmap-required.

Generate an ERD when:

```text
persistence relationships
cardinality
ownership
or logical structure
benefit materially from a visual model
```

Skip if the conceptual relationship catalog is clearer.

# Step 37 — ERD Scope

ERD should represent the chosen modeling level.

Label:

```text
CONCEPTUAL ERD
LOGICAL ERD
PHYSICAL ERD
```

Do not mix levels.

# Step 38 — Conceptual ERD

Shows:

```text
concepts
relationships
high-level cardinality
```

Avoid fields.

# Step 39 — Logical ERD

May show:

```text
logical identifiers
selected logical attributes
relationship optionality
```

without SQL technology.

# Step 40 — Physical ERD

Only when physical schema is explicitly in scope.

# Step 41 — ERD Syntax

Prefer version-control-friendly formats:

```text
Mermaid erDiagram
PlantUML
repository standard
```

# Step 42 — ERD Overload

Do not put every attribute into the diagram.

Keep detailed data dictionary outside visual if needed.

# Step 43 — Relationship Ambiguity

Use:

```text
RELATIONSHIP_SEMANTICS_REQUIRED
```

when relationship meaning is unclear.

# Step 44 — Cardinality Gap

Use:

```text
CARDINALITY_REQUIRED
```

# Step 45 — Identifier Gap

Use:

```text
IDENTIFIER_SEMANTICS_REQUIRED
```

# Step 46 — Ownership Gap

Use:

```text
DATA_OWNERSHIP_REQUIRED
```

# Step 47 — Invariant Gap

Use:

```text
INVARIANT_REQUIRED
```

when the model depends on an unresolved business rule.

# Step 48 — Tenant Scope Gap

Use:

```text
TENANT_SCOPE_REQUIRED
```

# Step 49 — Lifecycle Gap

Use:

```text
LIFECYCLE_ALIGNMENT_REQUIRED
```

if data model and state machine disagree.

# Step 50 — DFD Alignment

Stored/logical concepts should align with DFD stores/data categories.

Use:

```text
DOMAIN_DATA_DFD_CONFLICT
```

when contradictory.

# Step 51 — C4 Alignment

Authoritative ownership should align with accepted architecture responsibilities.

Use:

```text
DOMAIN_DATA_C4_CONFLICT
```

# Step 52 — State Machine Alignment

Lifecycle values/states must align with state machine.

Do not add states from legacy DB enum unless accepted domain behavior supports them.

# Step 53 — Use Case Alignment

Concept relationships should support accepted use cases.

Example:

```text
Reassign Conversation
```

needs enough relationship semantics to represent current/target assignment.

# Step 54 — Duplicated Concept Audit

Detect synonyms:

```text
Customer Organization
Tenant
Account
```

Ask whether they are one concept or distinct.

Do not merge silently.

# Step 55 — Overloaded Concept Audit

A concept with multiple unrelated meanings may need clarification.

# Step 56 — Orphan Concept Audit

Every concept should have:

```text
meaning
source
relationship or reason
```

# Step 57 — Circular Ownership Audit

Avoid:

```text
A owns B
B owns A
```

unless ownership semantics are intentionally different and explained.

# Step 58 — Cardinality Consistency Audit

Check inverse relationships.

# Step 59 — Tenant Leakage Audit

Check:

```text
concept lacks tenant ownership?
cross-tenant relationship implied?
global concept accidentally tenant-scoped?
```

# Step 60 — Lifecycle Consistency Audit

Check:

```text
data model state/status
↔ state machine
```

# Step 61 — Physical Leakage Audit

Remove:

```text
VARCHAR
BIGINT
UUID
INDEX
FK
PK
partition key
table name
ORM annotation
```

unless physical level explicitly requested.

# Step 62 — API DTO Leakage Audit

Do not model API request/response DTOs as canonical domain data.

# Step 63 — Event Schema Leakage Audit

Do not model event payload schemas here unless they are canonical domain concepts.

Detailed events belong to `modeling-event-flows`.

# Step 64 — Privacy Data Classification Link

Reference data classifications from DFD/privacy work.

Do not duplicate or override them.

# Step 65 — Sensitive Data Notes

Logical model can note:

```text
contains personal data
contains secret/auth data
```

based on DFD evidence.

Do not add legal conclusions.

# Step 66 — Retention

Retention is not a cardinality/lifecycle fact unless accepted.

Reference privacy policy gaps rather than inventing deletion states.

# Step 67 — Current vs Target

For brownfield:

```text
CURRENT conceptual/logical model
TARGET conceptual/logical model
TRANSITION mappings
```

Do not mix them silently.

# Step 68 — Legacy Schema

Legacy tables may provide evidence but are not automatically the canonical domain model.

# Step 69 — Migration Handoff

Flag:

```text
concept renames
ownership changes
cardinality changes
identity changes
state normalization
```

for later migration planning.

# Step 70 — Event Flow Handoff

Flag concepts/lifecycle changes that produce or consume architectural events.

# Step 71 — Deployment Handoff

Only data-location/residency/storage-topology questions move to deployment architecture.

# Step 72 — Validation Handoff

Accepted invariants/ownership/cardinalities become validation criteria for `validating-architecture-design`.

# Model Quality Status

Use:

```text
READY
READY_WITH_OPEN_QUESTIONS
REQUIRES_RELATIONSHIP_SEMANTICS
REQUIRES_CARDINALITY
REQUIRES_IDENTIFIER_SEMANTICS
REQUIRES_DATA_OWNERSHIP
REQUIRES_TENANT_SCOPE
REQUIRES_LIFECYCLE_ALIGNMENT
CONFLICTED
```

# Final Decision

Use:

```text
DOMAIN_DATA_MODEL_READY
DOMAIN_DATA_MODEL_READY_WITH_OPEN_QUESTIONS
DOMAIN_DATA_MODEL_REQUIRES_RELATIONSHIP_SEMANTICS
DOMAIN_DATA_MODEL_REQUIRES_CARDINALITY
DOMAIN_DATA_MODEL_REQUIRES_IDENTIFIER_SEMANTICS
DOMAIN_DATA_MODEL_REQUIRES_DATA_OWNERSHIP
DOMAIN_DATA_MODEL_REQUIRES_TENANT_SCOPE
DOMAIN_DATA_MODEL_REQUIRES_LIFECYCLE_ALIGNMENT
DOMAIN_DATA_MODEL_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/domain-data-model.md
```

## Completion Criteria

- [ ] Modeling scope and requested levels are explicit.
- [ ] Conceptual model is created before logical/physical detail.
- [ ] Concepts have clear domain meaning.
- [ ] Every noun is not automatically promoted to entity.
- [ ] Entity/value distinction is used only when useful.
- [ ] Relationships are semantic, not implementation joins.
- [ ] Cardinalities are evidence-backed or explicitly unknown.
- [ ] Optionality reflects domain semantics.
- [ ] Business/data/lifecycle/persistence ownership are distinguished when needed.
- [ ] Authoritative ownership aligns with architecture or conflicts are surfaced.
- [ ] Identifiers are semantic and format-neutral unless decided.
- [ ] External IDs remain distinct where useful.
- [ ] Invariants are explicit and rule-backed.
- [ ] Invariants are not confused with request validation.
- [ ] Tenant boundaries are explicit without tenant-storage invention.
- [ ] Cross-tenant relationships are explicit or prohibited.
- [ ] Lifecycle links to state machines rather than duplicating transition rules.
- [ ] History/audit concepts are not invented.
- [ ] Derived/ephemeral/external data is distinguished when useful.
- [ ] Conceptual and logical layers remain technology-neutral.
- [ ] Physical schema is omitted unless explicitly required.
- [ ] Domain entity is not automatically mapped 1:1 to a table.
- [ ] Aggregate/transaction boundaries are not inferred without evidence.
- [ ] ERD is generated only when it materially helps.
- [ ] ERD level is labeled and not mixed.
- [ ] DFD/C4/state/use-case alignment is audited.
- [ ] Duplicate/overloaded/orphan concepts are audited.
- [ ] Ownership/cardinality/tenant/lifecycle consistency is audited.
- [ ] SQL/ORM/API DTO/event-schema leakage is removed.
- [ ] Privacy classifications are referenced, not overridden.
- [ ] Brownfield current/target models are distinguished.
- [ ] Migration/event/deployment/validation handoffs are explicit.
- [ ] Final readiness is explicit.

## References

- Read `references/conceptual-logical-physical-layering.md` first.
- Read `references/concepts-entities-values-and-identifiers.md`.
- Read `references/relationships-cardinality-optionality-and-ownership.md`.
- Read `references/invariants-tenancy-lifecycle-and-history.md`.
- Read `references/erd-selection-levels-and-visual-discipline.md`.
- Read `references/domain-data-vs-schema-dfd-event-and-api-models.md`.
- Read `references/brownfield-current-target-migration-and-alignment.md`.
- Read `references/domain-data-model-audit.md` before completion.
