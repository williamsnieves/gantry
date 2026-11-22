# Architecture Trade-off Analysis

## Document Control

- Product/system:
- Initiative:
- Analysis version:
- Status:
- Source candidate architectures:
- Source architecture drivers:
- Source quality scenarios:
- Decision owner:
- Date:
- Applicable `AGENTS.md`:

## Decision Scope

- Decision:
- Time horizon:
- Candidates:
- Primary drivers:
- Secondary/conditional drivers:
- Hard constraints:
- Critical unknowns:

## Candidate Normalization

| Candidate | Comparable abstraction? | Normalization issue |
|---|---|---|
| | yes/no | |

## Evaluation Criteria

| Criterion | Type | Source | Importance/authority | Measure known? |
|---|---|---|---|---|
| | DRIVER / HARD_CONSTRAINT / QUALITY_ATTRIBUTE / RISK / OPERABILITY / TEAM_FIT / MIGRATION / COST / REVERSIBILITY / DEPENDENCY | | | |

## Hard Constraint Gate

| Candidate | Constraint | Result | Evidence | Eliminated? |
|---|---|---|---|---|
| | | PASS / FAIL / UNKNOWN | | yes/no |

## Driver-by-Candidate Matrix

| Driver | Candidate A | Candidate B | Candidate C |
|---|---|---|---|
| | STRONG / GOOD / ADEQUATE / WEAK / POOR / UNKNOWN | | |

## Detailed Candidate Evaluation

### Candidate A — [Name]

#### Primary Driver Response

| Driver | Rating | Benefit | Liability | Risk | Evidence strength |
|---|---|---|---|---|---|
| | | | | | HIGH / MEDIUM / LOW / UNKNOWN |

#### Quality Attribute Effects

- Availability/resilience:
- Consistency:
- Performance:
- Scalability:
- Security/isolation:
- Modifiability:
- Observability:
- Recoverability:

#### Team / Operational Effects

- Cognitive load:
- Deployment count/complexity:
- On-call/incident burden:
- Release coordination:
- Specialized expertise:

#### Migration / Brownfield

- 

#### Cost / Lock-In

- Cost drivers:
- Lock-in:
- Evidence:

#### Reversibility / Optionality

- Reversibility:
- Future options preserved:
- Hard-to-reverse commitments:

#### Risks Introduced

- 

#### Assumptions Required

- 

#### Unknowns

- 

#### Viability

- Status:
- Reason:

> Repeat for Candidate B/C.

## Trade-Off Tension Matrix

| Tension | Candidate A position | Candidate B position | Candidate C position |
|---|---|---|---|
| availability ↔ cost | | | |
| consistency ↔ latency | | | |
| isolation ↔ complexity | | | |
| modifiability ↔ simplicity | | | |
| independent deployability ↔ coordination | | | |
| observability ↔ privacy | | | |

## Sensitivity Analysis

| Unknown / assumption | Candidate(s) affected | If resolved low/weak | If resolved high/strict | Could flip recommendation? |
|---|---|---|---|---|
| | | | | yes/no |

## Sensitivity Points

| Architecture property/decision | Quality attribute(s) affected | Why sensitive |
|---|---|---|
| | | |

## Trade-Off Points

| Architecture property/decision | Improves | Worsens | Notes |
|---|---|---|---|
| | | | |

## Candidate Risks / Non-Risks

| Candidate | Concern | Classification | Evidence |
|---|---|---|---|
| | | RISK / NON_RISK / UNCERTAIN | |

## Dominance / Pareto Analysis

- Dominated candidates:
- Evidence:
- Pareto-optimal candidates:
- Areas with unknown evidence preventing dominance claims:

## Weighted Scoring Decision

- Numeric scoring appropriate: yes/no
- Accepted weighting model:
- If no, reason:
- If yes, source/owner:

## Architecture Spikes / Evidence Work

| Evidence gap | Proposed spike/measurement | Why it could change decision |
|---|---|---|
| | | |

## Recommendation

- Outcome: RECOMMEND_CANDIDATE / RECOMMEND_CONDITIONAL_CANDIDATE / DEFER_PENDING_EVIDENCE / NO_CLEAR_WINNER / SINGLE_VIABLE_CANDIDATE / REJECT_ALL_CANDIDATES
- Recommended candidate:
- Why:
- Drivers best satisfied:
- Trade-offs accepted:
- Risks accepted:
- Assumptions:
- Conditions:
- Missing evidence:
- Decision owner:

## Decision Reversal Triggers

| Trigger | Why it changes the decision | Candidate likely favored |
|---|---|---|
| | | |

## ADR Handoff

- Decision to record:
- Context:
- Options considered:
- Recommended/selected option:
- Consequences:
- Accepted trade-offs:
- Risks:
- Conditions:
- Reversal triggers:
- Open evidence:
- Ready for `recording-architecture-decisions`:

## Final Status

- Status: ARCHITECTURE_TRADEOFF_ANALYSIS_READY / ARCHITECTURE_TRADEOFF_ANALYSIS_READY_WITH_CONDITIONS / ARCHITECTURE_TRADEOFF_REQUIRES_EVIDENCE / ARCHITECTURE_TRADEOFF_REQUIRES_CONSTRAINT_DECISION / ARCHITECTURE_TRADEOFF_NO_CLEAR_WINNER / ARCHITECTURE_TRADEOFF_SINGLE_VIABLE_CANDIDATE / ARCHITECTURE_TRADEOFF_REJECTS_ALL_CANDIDATES / BLOCKED
- Blocking evidence:
- Constraint decisions:
- No-clear-winner reason:
- Ready for ADR:
