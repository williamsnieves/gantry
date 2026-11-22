# Candidate System Architectures

## Document Control

- Product/system:
- Initiative:
- Record version:
- Status:
- Source architecture drivers:
- Source quality scenarios:
- Source behavioral models:
- Owner:
- Date:
- Applicable `AGENTS.md`:

## Architecture Scope

- System boundary:
- Decision horizon:
- Greenfield / brownfield:
- Included:
- Excluded:
- Existing architecture constraints:

## Driver / Constraint Summary

### Primary Drivers
-

### Secondary Drivers
-

### Conditional Drivers
-

### Hard Constraints
-

### Assumptions
-

### Critical Tensions
-

### Missing Evidence
-

## Architectural Forces

| Driver / constraint | Mechanism-neutral architectural force |
|---|---|
| | |

## Major Responsibilities

| Responsibility | Source capability/use case | Notes |
|---|---|---|
| | | |

## Candidate Architecture Overview

| Candidate | Family/style | Primary intent | Viability |
|---|---|---|---|
| A | | | VIABLE / VIABLE_WITH_CONDITIONS / AT_RISK / NOT_VIABLE / INSUFFICIENT_EVIDENCE |
| B | | | |
| C | | | |

# Candidate A — [Name]

## Summary

- Architecture family:
- Design intent:
- Why this candidate is plausible:

## Major Boundaries / Deployable Units

| Unit/boundary | Responsibilities | Ownership rationale |
|---|---|---|
| | | |

## Dependency Direction

- 

## Data Ownership

| Data/domain concept | Authoritative owner | Shared/read model | Consistency notes |
|---|---|---|---|
| | | | |

## Communication Style

| Interaction | Style | Rationale | Coupling/failure implication |
|---|---|---|---|
| | in-process / sync / async / event / batch | | |

## Consistency Model

- Local transactional boundaries:
- Cross-boundary consistency:
- Compensation/eventual consistency concerns:

## Long-Running Workflows

- 

## Failure Boundaries / Degraded Mode

- 

## Security / Trust Boundaries

- 

## Deployment Shape

- 

## Scaling Shape

- 

## Operational Model

- Deployment complexity:
- Release coordination:
- Observability burden:
- Incident/on-call complexity:

## Team / Ownership Fit

- 

## Modifiability

- Changes localized well:
- Changes requiring coordination:
- External-provider extension model:

## Cost / Lock-In / Complexity

- Cost shape:
- Vendor lock-in:
- Complexity budget: LOW / MEDIUM / HIGH / VERY_HIGH
- Main complexity sources:

## Candidate-Specific Assumptions

- 

## Candidate-Specific Risks

- 

## Candidate Unknowns

- 

## Constraint Compliance

| Constraint | Status | Notes |
|---|---|---|
| | SATISFIES / PARTIALLY_SATISFIES / VIOLATES / UNKNOWN | |

## Driver Coverage

| Driver | Support | Notes |
|---|---|---|
| | STRONG / SUPPORTS / NEUTRAL / WEAK / UNKNOWN | |

## Evaluation Questions

- 

## Viability

- Status:
- Conditions:
- Reasons at risk:

---

# Candidate B — [Name]

> Repeat the same structure.

# Candidate C — [Name]

> Repeat the same structure when useful.

## Candidate Differentiation Matrix

| Dimension | Candidate A | Candidate B | Candidate C |
|---|---|---|---|
| decomposition | | | |
| data ownership | | | |
| communication | | | |
| consistency | | | |
| failure isolation | | | |
| deployment | | | |
| independent scaling | | | |
| operational burden | | | |
| team fit | | | |
| modifiability | | | |
| lock-in | | | |

## Hard Constraint Elimination

| Candidate | Violated hard constraint | Eliminated? | Notes |
|---|---|---|---|
| | | yes/no | |

## Assumption / Evidence Gaps

| Candidate | Assumption / unknown | Why it matters | Evidence needed |
|---|---|---|---|
| | | | |

## Trade-Off Analysis Handoff

### Candidates to Compare
-

### Drivers to Evaluate
-

### Constraints
-

### Tensions
-

### Critical Unknowns
-

### Evaluation Questions
-

## Final Decision

- Decision: CANDIDATE_ARCHITECTURES_READY / CANDIDATE_ARCHITECTURES_READY_WITH_CONDITIONS / CANDIDATE_ARCHITECTURES_REQUIRE_DRIVER_MEASURE / CANDIDATE_ARCHITECTURES_REQUIRE_CONSTRAINT_DECISION / CANDIDATE_ARCHITECTURES_REQUIRE_DEPENDENCY_EVIDENCE / CANDIDATE_ARCHITECTURES_SINGLE_VIABLE_CANDIDATE / BLOCKED
- Blocking inputs:
- Eliminated candidates:
- Viable candidates:
- Ready for `analyzing-architecture-tradeoffs`:
