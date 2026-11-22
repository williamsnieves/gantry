# Legacy Domain Model Extraction Record

## Context

- Change/capability:
- Selected behavior:
- Repository/service:
- Brownfield adaptation record:
- Governing standard:
- Repository-local rules:
- Discovery owner/date:

## Readiness

- Behavior scope clear:
- Current runtime evidence:
- Product terminology:
- Data evidence:
- Test/contract evidence:
- Known contradictions:
- Initial decision:
- Conditions/blockers:

## Evidence Sources

| Source | Scope | Reliability for this question | Findings |
|---|---|---|---|
| Product docs | | | |
| Tests | | | |
| Public API/events | | | |
| Database constraints/data | | | |
| Incidents/logs/metrics | | | |
| Code paths | | | |
| Provider docs | | | |

## Ubiquitous Language

| Preferred term | Meaning | Synonyms/overloads | Technical terms to avoid | Confidence |
|---|---|---|---|---|
| | | | | |

## Current Behavior Map

```text
trigger
→ actor/context
→ preconditions
→ decision
→ state transition
→ durable effect
→ external effect
→ semantic result
```

- Entry points:
- Writers:
- Readers:
- Jobs/webhooks/reconciliation:
- Public outcomes:

## Decision Inventory

| Decision | Current location | Classification | Inputs | Outcome | Evidence |
|---|---|---|---|---|---|
| | | DOMAIN_RULE/APPLICATION_ORCHESTRATION/PERSISTENCE_MECHANIC/PROVIDER_PROTOCOL/DELIVERY_CONCERN/COMPATIBILITY_RULE/SECURITY_POLICY/UNKNOWN | | | |

## State Transitions

| Current state | Trigger | Preconditions | Next state | Rejection | Evidence/confidence |
|---|---|---|---|---|---|
| | | | | | |

## Invariant Candidates

| ID | Candidate invariant | Type | Proposed owner | Evidence | Counterexamples | Confidence | Status |
|---|---|---|---|---|---|---|---|
| | | CREATION/STATE_TRANSITION/CROSS_ENTITY/TEMPORAL/UNIQUENESS/AUTHORIZATION/APPLICATION/TECHNICAL | | | | HIGH/MEDIUM/LOW | PROPOSED/SUPPORTED/TENTATIVE/REJECTED/DECISION_REQUIRED |

## Candidate Entities

### <Entity>

- Status:
- Identity:
- Lifecycle:
- Creation:
- Public behaviors:
- Invariants:
- Mutable state:
- Related Value Objects:
- Consistency boundary:
- Evidence:
- Uncertainty:

## Candidate Value Objects

| Candidate | Primitive shape | Semantics/validation | Equality/normalization | Evidence | Status |
|---|---|---|---|---|---|
| | | | | | |

## Candidate Domain Services

| Candidate | Business operation | Inputs/output | Why no Entity owns it | Purity evidence | Status |
|---|---|---|---|---|---|
| | | | | | |

## Candidate Domain Errors and Outcomes

| Meaning | Classification | Evidence | Technical/public mappings excluded |
|---|---|---|---|
| | DOMAIN_ERROR/APPLICATION_ERROR/TECHNICAL_FAILURE/PUBLIC_COMPATIBILITY_ERROR | | |

## Candidate Repository Concepts

| Semantic operation | Domain/Application need | Evidence | Technical details excluded |
|---|---|---|---|
| | | | |

## Technical Concepts Excluded From Domain

| Concept | Actual owner | Reason |
|---|---|---|
| HTTP status | Delivery | |
| ORM record | Infrastructure | |
| Provider SDK type | Infrastructure | |
| Retry header | Infrastructure | |
| Legacy compatibility status | Compatibility boundary | |

## Legacy and Unknown Data

| State/data | Classification | Proposed handling | Decision/evidence |
|---|---|---|---|
| | BUSINESS_STATE/TECHNICAL_PROCESS_STATE/COMPATIBILITY_STATE/CORRUPT_OR_UNKNOWN_STATE | REPAIR/QUARANTINE/REJECT/COMPATIBILITY_MAP/MIGRATE/DECISION_REQUIRED | |

## Contradictions

| Rule/term | Path/source A | Path/source B | Impact | Decision owner/status |
|---|---|---|---|---|
| | | | | |

## Known Bugs and Compatibility Quirks

| Behavior | Classification | Proposed treatment | Decision |
|---|---|---|---|
| | ACCEPTED_BEHAVIOR/KNOWN_BUG_TO_CORRECT/UNKNOWN_INTENT/COMPATIBILITY_QUIRK | | |

## Domain Test Proposal

| Candidate behavior/invariant | Given | When | Then | Status |
|---|---|---|---|---|
| | | | | |

## Proposal Challenge

- Concepts based only on tables:
- Provider terminology leaking inward:
- Value Objects without semantics:
- Services that are orchestration:
- Speculative future concepts:
- Anemic areas:
- Cross-entity consistency risk:
- Scope too broad:

## Decisions Required

| Question | Evidence/options | Why it matters | Owner | Blocking |
|---|---|---|---|---|
| | | | | |

## Modeling Proposal Summary

- Capability boundary:
- Supported Entities:
- Tentative Entities:
- Supported Value Objects:
- Tentative Value Objects:
- Supported Domain Services:
- Semantic errors:
- Repository concepts:
- Explicit exclusions:
- Conditions:

## Handoff

| Concept/work | Status | Next skill |
|---|---|---|
| | APPROVED/TENTATIVE/BLOCKED | |

## Final Decision

- Decision:
- Conditions:
- Missing evidence:
- Blocking decisions:
- Recommended next step:
