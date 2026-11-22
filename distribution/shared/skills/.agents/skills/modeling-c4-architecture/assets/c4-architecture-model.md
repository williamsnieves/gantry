# C4 Architecture Model

## Document Control

- Product/system:
- Initiative:
- Model version:
- Status:
- Architecture / ADR basis:
- Owner:
- Date:
- Applicable `AGENTS.md`:

## Model Scope

- System of interest:
- Purpose:
- Audience:
- Decision horizon:
- Included:
- Excluded:

## Level Selection

| Level | Decision | Rationale |
|---|---|---|
| L1 System Context | REQUIRED / USEFUL / NOT_NEEDED / DEFERRED / INSUFFICIENT_EVIDENCE | |
| L2 Containers | REQUIRED / USEFUL / NOT_NEEDED / DEFERRED / INSUFFICIENT_EVIDENCE | |
| L3 Components | REQUIRED / USEFUL / NOT_NEEDED / DEFERRED / INSUFFICIENT_EVIDENCE | |
| L4 Code | REQUIRED / USEFUL / NOT_NEEDED / DEFERRED / INSUFFICIENT_EVIDENCE | |

## Element Catalog

| ID | Level | Type | Name | Status | Responsibility | Technology | Owner | Source |
|---|---|---|---|---|---|---|---|---|
| | L1/L2/L3/L4 | Person/System/External System/Container/Component/Code | | CURRENT/TARGET/TRANSITION/PROPOSED/DEPRECATED/EXTERNAL | | | | |

## Relationship Catalog

| ID | Source | Destination | Description | Technology/protocol | Source evidence |
|---|---|---|---|---|---|
| REL-001 | | | | | |

# L1 — System Context

## Context Narrative

- People:
- System of interest:
- External software systems:
- Critical relationships:
- System boundary:

## Diagram Source

```text
[Use repository-preferred Structurizr DSL / C4-PlantUML / supported Mermaid C4 syntax]
```

## L1 Audit

- Missing people:
- Missing external systems:
- Internal containers leaked into L1:
- Unlabeled/weak relationships:
- Density/readability concerns:

# L2 — Container Model

## Container Catalog

| Container ID | Name | Type | Responsibility | Technology | Data ownership | Status |
|---|---|---|---|---|---|---|
| | | application/data store/etc. | | | | |

## Container Relationships

| Source | Destination | Relationship | Architectural implication |
|---|---|---|---|
| | | | |

## Diagram Source

```text
[Use repository-preferred C4 syntax]
```

## L2 Audit

- Missing accepted containers:
- Shared-data ownership ambiguity:
- Technology assumptions not decided:
- Missing external relationships:
- Abstraction mixing:
- Deployment-instance leakage:

# L3 — Component Model (Optional)

## L3 Decision

- Container modeled:
- Why L3 is useful/required:
- Why other containers do not need L3:

## Component Catalog

| Component ID | Container | Name | Responsibility | Interface/relationship | Source |
|---|---|---|---|---|---|
| | | | | | |

## Diagram Source

```text
[Optional C4 component diagram source]
```

## L3 Audit

- Folder/class leakage:
- Over-modeling:
- Missing architectural component:
- Responsibility overlap:

# L4 — Code (Exceptional)

- Included: yes/no
- Strong maintenance reason:
- Stable code boundary:
- Why other documentation is insufficient:
- Source/model:

## Current / Target / Transition Notes

- Current architecture:
- Target architecture:
- Transitional elements:
- Deprecated elements:
- Migration ambiguity:

## ADR / Driver Traceability

| C4 element/relationship | ADR | Architecture driver | Rationale |
|---|---|---|---|
| | | | |

## Downstream Modeling Handoffs

### Sequence Candidates

| Relationship/use case | Why runtime sequence matters |
|---|---|
| | |

### Data-Flow / STRIDE Candidates

| Relationship/boundary | Sensitive/trust consideration |
|---|---|
| | |

### Deployment Candidates

| Logical container | Deployment questions deferred |
|---|---|
| | |

## Gap Ledger

| ID | Level | Gap | Type | Owner |
|---|---|---|---|---|
| | | | STRUCTURE_DECISION_REQUIRED / C4_RELATIONSHIP_GAP / C4_ADR_CONFLICT / RELATIONSHIP_CLARIFICATION_REQUIRED | |

## Final Decision

- Decision: C4_MODEL_READY / C4_MODEL_READY_WITH_OPEN_QUESTIONS / C4_MODEL_REQUIRES_STRUCTURE_DECISION / C4_MODEL_REQUIRES_RELATIONSHIP_CLARIFICATION / C4_MODEL_REQUIRES_ADR_ALIGNMENT / C4_MODEL_CONFLICTED / BLOCKED
- Blocking structure gaps:
- ADR conflicts:
- Relationship gaps:
- L3 status:
- L4 status:
- Ready for downstream models:
