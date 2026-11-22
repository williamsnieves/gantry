# Architecture Drivers Record

## Document Control

- Product/system:
- Initiative:
- Record version:
- Status:
- Source PRD:
- Source FR catalog:
- Source NFR catalog:
- Source QA scenarios:
- Owner:
- Date:
- Applicable `AGENTS.md`:

## Architecture Decision Scope

- System boundary:
- Decision horizon:
- Greenfield / brownfield:
- Areas explicitly out of scope:
- Known architecture constraints:

## Classification Matrix

| ID | Source item | Type | Business priority | Architecture significance | Classification | Readiness |
|---|---|---|---|---|---|---|
| | | FR / NFR / QA / CONSTRAINT / ASSUMPTION / RISK / DEPENDENCY | | HIGH / MEDIUM / LOW / TBD | ARCHITECTURE_DRIVER / IMPORTANT_REQUIREMENT / LOCAL_DESIGN_CONCERN / CONSTRAINT / ASSUMPTION / NOT_ARCHITECTURE_SIGNIFICANT | READY / READY_WITH_CONDITIONS / REQUIRES_MEASURE / REQUIRES_AUTHORITY / REQUIRES_POLICY / REQUIRES_DEPENDENCY_EVIDENCE / CONFLICTED |

## Architecture Drivers

### AD-001 — [Driver]

- Classification: ARCHITECTURE_DRIVER
- Strength: PRIMARY / SECONDARY / CONDITIONAL
- Category:
- Source item(s):
- Accepted requirement/scenario:
- Why architecture-significant:
- Architecture dimensions affected:
  - structure:
  - deployment:
  - data:
  - communication:
  - trust/security:
  - failure:
  - scale:
  - geography:
  - operations:
  - cost:
  - organization:
- Evidence:
- Strictness / measure:
- Business criticality:
- Reversibility impact:
- Cross-cutting scope:
- Linked risk:
- Linked constraints:
- Assumptions:
- Dependencies:
- Tensions:
- Missing evidence:
- Evaluation criterion:
- Readiness:

## Important Requirements

| Item | Why important | Why not architecture driver | Architecture support needed |
|---|---|---|---|
| | | | |

## Local Design Concerns

| Item | Local area | Reason local | Downstream owner |
|---|---|---|---|
| | | | |

## Constraints

### CON-001 — [Constraint]

- Constraint:
- Type:
- Source/authority:
- Strength:
- Architecture impact:
- Challengeable:
- Validation:
- Related driver(s):

## Assumptions

### ASM-001 — [Assumption]

- Assumption:
- Evidence:
- Confidence:
- Architecture impact if false:
- Validation action:
- Owner:
- Risk level:
- Related driver(s):

## High-Risk Architecture Assumptions

| Assumption | Why architecture depends on it | Failure impact | Action |
|---|---|---|---|
| | | | |

## Not Architecture Significant

| Item | Business relevance | Why not architecture-significant |
|---|---|---|
| | | |

## Missing Evidence Ledger

| Candidate | Missing evidence | Why it changes classification | Owner |
|---|---|---|---|
| | measure / authority / scale / provider / policy / cost / geography | | |

## Driver Interaction / Tension Matrix

| Driver A | Driver B / constraint | Relationship | Effect |
|---|---|---|---|
| | | reinforces / tensions / conflicts | |

## Driver Conflicts

| ID | Inputs | Conflict | Decision owner | Status |
|---|---|---|---|---|
| DC-001 | | | | DRIVER_CONFLICT_REQUIRES_DECISION / RESOLVED |

## Business Priority vs Architecture Significance

| Item | Business priority | Architecture significance | Interpretation |
|---|---|---|---|
| | | | |

## Candidate Architecture Evaluation Criteria

| Criterion ID | Driver/constraint | Candidate architecture must demonstrate |
|---|---|---|
| AC-EVAL-001 | | |

## Architecture Inflation Audit

- FRs incorrectly promoted:
- NFRs incorrectly promoted:
- Security concerns incorrectly promoted:
- Integrations incorrectly promoted:
- Constraints incorrectly treated as drivers:
- Driver set size:
- Reassessment required:

## Technology / Tactic Leakage Audit

- Technology choices removed:
- Architecture tactics removed:
- Accepted hard constraints retained:
- Remaining leakage:

## Architecture Design Handoff

### Primary Drivers

- 

### Secondary Drivers

- 

### Conditional Drivers

- 

### Constraints

- 

### Assumptions to Validate

- 

### Critical Tensions

- 

### Missing Evidence

- 

### Evaluation Criteria

- 

### Important Non-Driver Requirements

- 

## Final Decision

- Decision: ARCHITECTURE_DRIVERS_READY / ARCHITECTURE_DRIVERS_READY_WITH_CONDITIONS / ARCHITECTURE_DRIVERS_REQUIRE_MEASURES / ARCHITECTURE_DRIVERS_REQUIRE_PRODUCT_DECISION / ARCHITECTURE_DRIVERS_REQUIRE_POLICY_DECISION / ARCHITECTURE_DRIVERS_REQUIRE_DEPENDENCY_EVIDENCE / ARCHITECTURE_DRIVERS_CONFLICTED / BLOCKED
- Blocking measure gaps:
- Blocking product/policy decisions:
- Dependency evidence needed:
- Conflicts:
- Ready for `designing-system-architecture`:
