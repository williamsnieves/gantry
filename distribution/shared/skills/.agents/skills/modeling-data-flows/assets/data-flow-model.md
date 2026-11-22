# Data Flow Model

## Document Control

- Product/system:
- Initiative:
- Model version:
- Status:
- Source C4 model:
- Source sequence models:
- Source ADR(s):
- Privacy/security requirements:
- Owner:
- Date:
- Applicable `AGENTS.md`:

## DFD Scope

- System/scenario:
- Security/privacy question:
- Included:
- Excluded:
- DFD views selected: Context / Level 1 / Focused
- Rationale:

## External Entity Catalog

| ID | External Entity | Role | Organization/trust domain | Source |
|---|---|---|---|---|
| EE-001 | | | | |

## Process Catalog

| ID | Process | Responsibility | C4 mapping | Source |
|---|---|---|---|---|
| PROC-001 | | | | |

## Data Store Catalog

| ID | Store | Data classes | Purpose | Authoritative owner | Residency | Retention | C4 mapping |
|---|---|---|---|---|---|---|---|
| DS-001 | | | | | | | |

## Trust Boundary Catalog

| ID | Boundary | Separates | Why trust changes | Source |
|---|---|---|---|---|
| TB-001 | | | | |

## Data Flow Catalog

| ID | Source | Destination | Direction | Data category | Classification | Purpose | Trust boundary | Third party? | Source |
|---|---|---|---|---|---|---|---|---|---|
| DF-001 | | | | | | | | yes/no | |

## Third-Party Transfer Inventory

| Flow | Provider/entity | Data category | Purpose | Classification | Residency known? | Retention known? | Policy/source |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Secret / Credential Flow Inventory

| Flow | Secret/credential category | Origin | Consumer | Stored? | Boundary crossed | Source/gap |
|---|---|---|---|---|---|---|
| | | | | | | |

## Data Classification / Purpose Matrix

| Data category | Classification | Purpose(s) | Owner/authority | Unknowns |
|---|---|---|---|---|
| | | | | |

## Context DFD

```text
[Version-controlled DFD source]
```

## Level 1 DFD

```text
[Version-controlled DFD source]
```

## Focused DFDs

### [Sensitive Scenario]

```text
[Optional focused DFD]
```

## Privacy / Residency / Retention Review

### Personal Data
-

### Third-Party Transfers
-

### Residency
-

### Retention
-

### Minimization
-

### Logging / Telemetry Duplication
-

### AI Provider Data Policy
-

## Trust / Tenant Audit

- Cross-tenant flows:
- Missing tenant context:
- Shared processes/stores requiring tenant-scope clarification:
- Privileged/operator flows:
- External trust crossings:

## Secret Exposure Audit

- Unnecessary secret recipients:
- Secret storage assumptions:
- Third-party secret transfers:
- Secret-handling gaps:

## Third-Party Audit

| Provider | Transfer complete? | Classification known? | Purpose known? | Residency/retention/policy gaps |
|---|---|---|---|---|
| | | | | |

## Logging / Audit Data Audit

- Conversation content logged:
- Tenant identifiers logged:
- Provider identifiers logged:
- Privileged action content:
- Unknown logging scope:

## Alignment Audits

### C4 Alignment
- Unmapped processes:
- Unmapped stores:
- Architecture contradictions:

### Sequence Alignment
- Direction/order contradictions:
- Missing provider/system transfer:
- Unsupported flow:

### Privacy / Residency
- Privacy conflicts:
- Residency conflicts:
- Retention conflicts:

## STRIDE Handoff

### External Entities
-

### Processes
-

### Data Stores
-

### Data Flows
-

### Trust Boundaries
-

### High-Value / Sensitive Assets
-

### Entry Points
-

### Privileged Flows
-

### Secret Flows
-

## Other Modeling Handoffs

### Domain Data
- Concepts/stores needing conceptual/logical model:

### Event Flow
- Async/event flows needing detailed event semantics:

### Deployment
- Residency/network/trust questions needing topology:

## Gap Ledger

| ID | Area | Gap | Type | Owner |
|---|---|---|---|---|
| | | | DATA_CLASSIFICATION_REQUIRED / DATA_PURPOSE_REQUIRED / THIRD_PARTY_POLICY_REQUIRED / RESIDENCY_POLICY_REQUIRED / RETENTION_POLICY_REQUIRED / SECRET_HANDLING_DECISION_REQUIRED / LOGGING_DATA_SCOPE_REQUIRED / DFD_C4_ALIGNMENT_REQUIRED | |

## Final Decision

- Decision: DATA_FLOW_MODEL_READY / DATA_FLOW_MODEL_READY_WITH_OPEN_QUESTIONS / DATA_FLOW_MODEL_REQUIRES_DATA_CLASSIFICATION / DATA_FLOW_MODEL_REQUIRES_DATA_PURPOSE / DATA_FLOW_MODEL_REQUIRES_THIRD_PARTY_POLICY / DATA_FLOW_MODEL_REQUIRES_RESIDENCY_POLICY / DATA_FLOW_MODEL_REQUIRES_RETENTION_POLICY / DATA_FLOW_MODEL_REQUIRES_SECRET_HANDLING_DECISION / DATA_FLOW_MODEL_REQUIRES_C4_ALIGNMENT / DATA_FLOW_MODEL_CONFLICTED / BLOCKED
- Blocking classification gaps:
- Third-party/privacy gaps:
- Residency/retention gaps:
- Secret-handling gaps:
- C4/sequence conflicts:
- Ready for `threat-modeling-with-stride`:
