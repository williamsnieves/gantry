# Domain Data Model

## Document Control

- Product/system:
- Initiative:
- Model version:
- Status:
- Source requirements/use cases:
- Source state/process models:
- Source C4/ADR:
- Source DFD:
- Owner:
- Date:
- Applicable `AGENTS.md`:

## Modeling Scope

- Domain/system scope:
- Purpose:
- Current / target / transition:
- Conceptual model: yes/no
- Logical model: yes/no
- Physical schema: yes/no
- ERD useful: yes/no
- Explicit exclusions:

# Conceptual Data Model

## Concept Catalog

| ID | Concept | Kind | Meaning | Business owner | Authoritative data owner | Tenant scoped? | Source |
|---|---|---|---|---|---|---|---|
| CON-001 | | entity/value/concept/external-reference/derived/ephemeral | | | | yes/no/TBD | |

## Relationship Catalog

| ID | Source concept | Relationship | Target concept | Source cardinality | Target cardinality | Ownership semantics | Source |
|---|---|---|---|---|---|---|---|
| REL-001 | | | | | | | |

## Conceptual Invariants

| ID | Invariant | Concepts | Rule/source |
|---|---|---|---|
| INV-001 | | | |

## Tenant Boundaries

| Concept | Tenant owner/scope | Cross-tenant relationship allowed? | Rule/source | Gap |
|---|---|---|---|---|
| | | | | |

## Lifecycle Linkage

| Concept | State machine | Accepted states | Data implications |
|---|---|---|---|
| | | | |

# Logical Data Model

## Logical Entity / Value Catalog

| Concept | Identity semantics | Required logical attributes | Optional logical attributes | Derived? | Persisted? | Notes |
|---|---|---|---|---|---|---|
| | | | | yes/no/TBD | yes/no/TBD | |

## Identifier Catalog

| Concept | Identifier meaning | Internal/external | Stability/scope | Format decided? | Source |
|---|---|---|---|---|---|
| | | | | yes/no | |

## Ownership / Authority Matrix

| Data concept | Authoritative owner | Readers/consumers | Mutation authority | C4 mapping | Notes |
|---|---|---|---|---|---|
| | | | | | |

## Relationship / Optionality Matrix

| Relationship | Required? | Cardinality | Lifecycle condition | Invariant |
|---|---|---|---|---|
| | | | | |

## Derived / Ephemeral / External Data

| Concept | Classification | Source | Persistence expectation | Notes |
|---|---|---|---|---|
| | AUTHORITATIVE / DERIVED / EPHEMERAL / EXTERNAL_REFERENCE | | | |

# ERD Decision

- ERD generated: yes/no
- Level: CONCEPTUAL / LOGICAL / PHYSICAL
- Why it adds value:
- Why deeper level is not needed:

## ERD Source

```mermaid
erDiagram
    %% Add only evidence-backed conceptual/logical relationships.
```

# Physical Schema Gate

- Physical schema needed now: yes/no
- Reason:
- Persistence technology decided:
- Physical details explicitly in scope:
- Handoff required:

## Alignment Audits

### DFD
- Missing stored concepts:
- Data-classification mismatch:
- Ownership contradiction:

### C4 / ADR
- Unowned authoritative concepts:
- Responsibility conflict:
- Invented service/store ownership:

### State Machines
- Unknown/missing lifecycle state:
- Illegal lifecycle attribute:
- History semantics conflict:

### Use Cases / Business Rules
- Relationship missing for accepted behavior:
- Cardinality contradicts behavior:
- Invariant missing/conflicting:

## Model Integrity Audits

### Duplicate / Overloaded Concepts
- Potential synonyms:
- Overloaded terms:
- Clarifications required:

### Cardinality
- Unsupported cardinalities:
- Inverse inconsistencies:
- Optionality gaps:

### Ownership
- Ambiguous ownership:
- Circular ownership:
- Shared-authority gaps:

### Tenant Boundaries
- Missing tenant scope:
- Cross-tenant leakage:
- Global-vs-tenant ambiguity:

### Physical Leakage
- Table/column/type/index assumptions:
- ORM/API DTO leakage:
- Event-schema leakage:

## Current / Target / Migration Notes

- Current model:
- Target model:
- Identity changes:
- Ownership changes:
- Cardinality changes:
- Lifecycle normalization:
- Migration mapping required:

## Downstream Handoffs

### Event Flow
- Concepts/lifecycle changes likely to produce/consume events:

### Deployment
- Data-location/residency/storage topology questions:

### Physical Schema / Persistence
- Concepts requiring physical design:

### Architecture Validation
- Invariants/cardinalities/ownership rules to validate:

## Gap Ledger

| ID | Area | Gap | Type | Owner |
|---|---|---|---|---|
| | | | RELATIONSHIP_SEMANTICS_REQUIRED / CARDINALITY_REQUIRED / IDENTIFIER_SEMANTICS_REQUIRED / DATA_OWNERSHIP_REQUIRED / INVARIANT_REQUIRED / TENANT_SCOPE_REQUIRED / LIFECYCLE_ALIGNMENT_REQUIRED / AGGREGATE_BOUNDARY_REQUIRED | |

## Final Decision

- Decision: DOMAIN_DATA_MODEL_READY / DOMAIN_DATA_MODEL_READY_WITH_OPEN_QUESTIONS / DOMAIN_DATA_MODEL_REQUIRES_RELATIONSHIP_SEMANTICS / DOMAIN_DATA_MODEL_REQUIRES_CARDINALITY / DOMAIN_DATA_MODEL_REQUIRES_IDENTIFIER_SEMANTICS / DOMAIN_DATA_MODEL_REQUIRES_DATA_OWNERSHIP / DOMAIN_DATA_MODEL_REQUIRES_TENANT_SCOPE / DOMAIN_DATA_MODEL_REQUIRES_LIFECYCLE_ALIGNMENT / DOMAIN_DATA_MODEL_CONFLICTED / BLOCKED
- Blocking relationship/cardinality gaps:
- Ownership/tenant gaps:
- Lifecycle conflicts:
- Physical schema required now:
- Ready for `modeling-event-flows`:
