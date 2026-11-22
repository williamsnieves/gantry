---
name: analyzing-architecture-tradeoffs
description: Compares candidate system architectures against accepted architecture drivers, quality-attribute scenarios, constraints, risks, assumptions, team/operational context, and migration realities. Use after `designing-system-architecture` has produced meaningful candidates and before recording ADRs. Evaluate each candidate qualitatively and quantitatively only where evidence supports it; expose benefits, liabilities, sensitivity to unknowns, irreversible commitments, operational complexity, failure behavior, and hard-constraint violations. Eliminate non-viable candidates, identify dominated options, and recommend a candidate only when evidence is strong enough. Do not invent scores, weights, SLOs, costs, or provider capabilities, and do not turn the comparison into popularity voting or technology preference.
---

# Analyzing Architecture Trade-offs

## Purpose

Compare candidate architectures rigorously against what the system actually needs.

Core workflow:

```text
candidate architectures
+ architecture drivers
+ quality scenarios
+ constraints
+ assumptions
+ risks
        ↓
normalize evaluation criteria
        ↓
eliminate hard-constraint violations
        ↓
evaluate each candidate
        ↓
surface strengths / liabilities
        ↓
analyze trade-off tensions
        ↓
analyze sensitivity to unknowns
        ↓
identify dominated / conditional options
        ↓
recommend or defer
```

Output:

```text
architecture-tradeoff-analysis.md
```

## Core Principle

Architecture trade-off analysis is not:

```text
Candidate A = 8.7
Candidate B = 8.3
therefore A wins
```

unless the scoring model, weights, measurements, and decision utility are actually authoritative.

Prefer evidence-based comparative reasoning:

```text
driver
→ candidate response
→ benefit
→ cost/liability
→ risk
→ uncertainty
```

## Use When

- Candidate architectures already exist.
- Architecture drivers are explicit.
- A decision must be made between meaningful alternatives.
- Quality attributes conflict.
- Hard constraints may eliminate options.
- Team/operational complexity matters.
- Migration/brownfield trade-offs matter.
- Unknown scale/provider/recovery evidence may change the decision.

## Do Not Use When

- Only one vague architecture idea exists.
- Architecture drivers are not defined.
- The task is to generate candidate architectures; use `designing-system-architecture`.
- The decision is already accepted and only needs documentation; use `recording-architecture-decisions`.
- The task is detailed benchmarking/testing rather than architecture evaluation.

## Inputs

Preferred:

- candidate architecture record;
- architecture drivers record;
- quality-attribute scenarios;
- constraints;
- assumptions;
- candidate risks;
- operational/team context;
- provider/dependency evidence;
- migration constraints;
- relevant cost evidence;
- applicable `AGENTS.md`.

Optional:

- benchmark results;
- incident evidence;
- proof-of-concept results;
- provider SLAs/quotas;
- current production metrics;
- architecture spikes.

## Outputs

- Trade-off analysis.
- Candidate viability/elimination record.
- Driver-by-candidate matrix.
- Quality-attribute comparison.
- Trade-off tension analysis.
- Assumption/sensitivity analysis.
- Reversibility/optionality analysis.
- Risk exposure comparison.
- Recommendation or explicit defer decision.
- ADR handoff.

# Evaluation Principle

For each driver:

```text
What does the driver require?
How does each candidate respond?
What does that response improve?
What does it make worse?
What uncertainty remains?
```

# Step 1 — Establish Decision Scope

Record:

```text
decision to make
time horizon
candidate set
driver set
hard constraints
decision owner
known missing evidence
```

Do not widen the decision silently.

# Step 2 — Normalize Candidates

Before comparison, ensure candidates are comparable at the same architectural abstraction level.

Bad:

```text
Candidate A: modular monolith
Candidate B: Kafka
```

One is architecture, one is a technology/tactic.

If candidates are not comparable:

```text
CANDIDATE_NORMALIZATION_REQUIRED
```

# Step 3 — Normalize Evaluation Criteria

Build criteria only from:

```text
architecture drivers
hard constraints
quality scenarios
explicit risks
migration constraints
team/operational context
authoritative cost criteria
```

Do not add fashionable criteria.

# Criterion Types

Use:

```text
DRIVER
HARD_CONSTRAINT
QUALITY_ATTRIBUTE
RISK
OPERABILITY
TEAM_FIT
MIGRATION
COST
REVERSIBILITY
DEPENDENCY
```

# Step 4 — Hard Constraint Gate

Before scoring/comparing preferences:

```text
Does candidate violate a hard constraint?
```

Use:

```text
PASS
FAIL
UNKNOWN
```

A hard-constraint `FAIL` normally eliminates the candidate.

If the constraint is explicitly challengeable:

```text
CONSTRAINT_EXCEPTION_REQUIRES_DECISION
```

# Step 5 — Evidence Strength

For every evaluation record evidence:

```text
HIGH
MEDIUM
LOW
UNKNOWN
```

Evidence may come from:

```text
requirement
quality scenario
benchmark
existing-system measurement
provider documentation
prototype
incident data
architectural reasoning
```

Distinguish observed evidence from inference.

# Step 6 — Candidate Rating Vocabulary

Prefer qualitative ratings:

```text
STRONG
GOOD
ADEQUATE
WEAK
POOR
UNKNOWN
```

Do not convert them to numbers unless an accepted scoring model exists.

# Step 7 — Primary Driver Evaluation

Primary architecture drivers deserve explicit analysis.

For each candidate:

```text
support
mechanism
benefit
liability
risk
evidence
```

Mechanism should be architectural, not low-level implementation.

# Step 8 — Conditional Driver Evaluation

For drivers pending measures:

```text
evaluate sensitivity
```

Example:

```text
If scale remains modest:
Candidate A is adequate.

If scale reaches X:
Candidate B may gain advantage.

X is currently unknown.
```

Do not invent threshold X.

Use:

```text
THRESHOLD_REQUIRED
```

# Step 9 — Quality Attribute Trade-offs

Common tensions:

```text
availability ↔ cost
consistency ↔ latency
security isolation ↔ operational complexity
modifiability ↔ simplicity
independent deployment ↔ distributed coordination
observability ↔ privacy
performance ↔ resource cost
```

For each tension explain how candidates position differently.

# Step 10 — Availability / Resilience

Evaluate:

```text
failure isolation
degraded mode
dependency coupling
recovery blast radius
single points of failure
```

Do not assume distributed = more available.

Distributed systems can add:

```text
network failures
coordination failures
partial failures
```

# Step 11 — Consistency

Evaluate:

```text
local transaction simplicity
cross-boundary coordination
eventual consistency exposure
compensation burden
user-visible stale state
```

Do not label eventual consistency as bad by default.

# Step 12 — Performance

Use actual performance evidence only.

If targets are TBD:

```text
PERFORMANCE_DECISION_SENSITIVE_TO_MEASURE
```

Do not claim microservices are faster or monoliths slower in general.

# Step 13 — Scalability

Evaluate:

```text
what scales together
what scales independently
bottlenecks
state/data constraints
operational implications
```

Unknown scale:

```text
SCALE_EVIDENCE_REQUIRED
```

# Step 14 — Security / Tenant Isolation

Evaluate:

```text
trust boundary clarity
data-boundary clarity
policy enforcement locations
cross-boundary attack surface
operational complexity
```

Do not equate “separate service” with guaranteed isolation.

# Step 15 — Modifiability

Evaluate real change scenarios.

Example:

```text
Add a new messaging provider.
```

Ask:

```text
how many boundaries change?
what coordination is required?
what regression surface expands?
```

# Step 16 — Observability / Diagnosability

Distributed architectures may improve boundary attribution but add correlation complexity.

Simple architectures may be easier to inspect but provide coarser failure boundaries.

Evaluate against actual operational scenarios.

# Step 17 — Recoverability

If RTO/RPO are unknown:

```text
do not claim one candidate wins
```

Identify which architectural differences become relevant once targets exist.

# Step 18 — Team Fit

Evaluate:

```text
cognitive load
operational ownership
deployment count
on-call burden
specialized expertise
coordination
```

A five-person team is material evidence.

Do not directly infer monolith = winner.

# Step 19 — Operational Complexity

Explicitly compare:

```text
deployments
runtime units
network boundaries
observability
incident response
release coordination
data migrations
failure modes
```

# Step 20 — Migration / Brownfield

Evaluate:

```text
migration steps
coexistence
rollback
data migration
client compatibility
operational transition
```

Do not prefer rewrite by default.

# Step 21 — Cost

Only use authoritative cost data where available.

Without numbers, describe:

```text
cost drivers
baseline overhead
operational burden
managed-service exposure
data-transfer exposure
```

Do not invent monthly estimates.

# Step 22 — Vendor Lock-In

Evaluate:

```text
switching cost
proprietary dependency
operational benefit
delivery acceleration
```

Lock-in can be an acceptable trade-off.

# Step 23 — Reversibility

Classify decisions/traits:

```text
EASY_TO_REVERSE
MODERATE
HARD_TO_REVERSE
VERY_HARD_TO_REVERSE
```

Examples:

```text
service boundary
public contract
data partitioning
event schema
regional topology
```

Do not use reversibility as sole decision criterion.

# Step 24 — Optionality

A candidate may preserve future options.

Examples:

```text
modular monolith with explicit internal boundaries
→ may preserve later extraction options

early microservices
→ may preserve independent scaling but commit earlier to distributed operations
```

Evaluate evidence, not slogans.

# Step 25 — Complexity Cost

Use qualitative classification:

```text
LOW
MEDIUM
HIGH
VERY_HIGH
```

Then explain what consumes complexity.

# Step 26 — Risk Comparison

For each candidate identify:

```text
delivery risk
operational risk
data/consistency risk
security risk
dependency risk
migration risk
organizational risk
```

# Step 27 — Failure Mode Expansion

A candidate that solves one problem may introduce new failures.

Example:

```text
separate ingestion service
→ isolates provider ingestion
but introduces network/deployment/data coordination failure modes
```

Make this explicit.

# Step 28 — Assumption Dependency

For each candidate:

```text
what assumptions must be true for it to remain a good choice?
```

# Step 29 — Sensitivity Analysis

Roadmap-worthy rule:

Ask:

```text
Which unknown, if resolved differently, could flip the recommendation?
```

Examples:

```text
future scale
RTO/RPO
provider SLA
team growth
cost ceiling
data residency
```

Use:

```text
DECISION_SENSITIVE
DECISION_ROBUST
```

# Step 30 — Threshold Analysis

When a decision depends on a threshold but value is unknown:

```text
record threshold question
```

Do not invent it.

# Step 31 — Dominated Candidate

A candidate is dominated when another candidate is:

```text
equal or better on all material criteria
and strictly better on at least one
```

given current evidence.

Use cautiously.

Do not claim domination across `UNKNOWN` evidence.

# Step 32 — Candidate Elimination

Reasons:

```text
hard constraint violation
unacceptable risk
missing required capability
dominated under current evidence
operational infeasibility
```

Record explicit reason.

# Step 33 — Pareto Frontier

When no candidate dominates:

```text
several candidates may be Pareto-optimal
```

Then decision depends on stakeholder trade-off preference.

Do not force a winner.

# Step 34 — Weighted Scoring

Use numeric weights ONLY if:

```text
decision makers explicitly accepted weights
criteria are comparable enough
scoring scale is defined
evidence supports scores
```

Otherwise:

```text
DO_NOT_SCORE
```

# Step 35 — Fake Precision

Prohibited:

```text
Candidate A = 87/100
Candidate B = 84/100
```

based on qualitative intuition.

# Step 36 — Decision Rules

Possible decision outcomes:

```text
RECOMMEND_CANDIDATE
RECOMMEND_CONDITIONAL_CANDIDATE
DEFER_PENDING_EVIDENCE
NO_CLEAR_WINNER
SINGLE_VIABLE_CANDIDATE
REJECT_ALL_CANDIDATES
```

# Step 37 — Recommendation Standard

A recommendation must include:

```text
recommended candidate
why
drivers it best satisfies
trade-offs explicitly accepted
risks
assumptions
conditions
evidence gaps
what would reverse the decision
```

# Step 38 — Conditional Recommendation

Example:

```text
Recommend Candidate A for v1
provided scale remains within the as-yet-unmeasured range
and no strict independent-deployment requirement emerges.
```

But do not use vague conditions if they are actually blocking.

# Step 39 — Defer Decision

Use:

```text
DEFER_PENDING_EVIDENCE
```

when missing evidence could materially flip choice.

Architecture discipline includes knowing when NOT to decide.

# Step 40 — Decision Reversal Triggers

Record:

```text
if scale exceeds accepted threshold
if team splits into independent ownership
if RTO/RPO becomes strict
if residency policy changes
if provider SLA is insufficient
```

Only use actual plausible unknowns.

# Step 41 — Proof / Spike Need

If evidence gap can be reduced cheaply:

```text
ARCHITECTURE_SPIKE_RECOMMENDED
```

Examples:

```text
load benchmark
provider failure simulation
migration rehearsal
prototype
```

Do not request spikes reflexively.

# Step 42 — ATAM-Inspired Thinking

Use architecture trade-off thinking inspired by:

```text
quality scenarios
sensitivity points
trade-off points
risks
non-risks
```

Do not claim formal ATAM completion unless the full method was actually performed.

# Step 43 — Sensitivity Point

A sensitivity point is an architecture decision/property where small changes significantly affect a quality attribute.

Example:

```text
number of independently deployed units
```

may strongly affect:

```text
operational complexity
failure isolation
```

# Step 44 — Trade-Off Point

A trade-off point affects multiple qualities in opposing directions.

Example:

```text
synchronous boundary
```

may improve:

```text
immediate consistency
```

while worsening:

```text
availability coupling
```

# Step 45 — Risk / Non-Risk

Use:

```text
RISK
NON_RISK
UNCERTAIN
```

for architecture concerns where evidence supports it.

Do not pretend absence of evidence = non-risk.

# Step 46 — Constraint Challenge

If the best candidate violates a challengeable constraint:

```text
do not silently waive it
```

Use:

```text
CONSTRAINT_EXCEPTION_REQUIRES_DECISION
```

# Step 47 — Stakeholder Preference

If candidates remain Pareto-optimal, the decision may require product/engineering/security/operations preference.

Record the decision owner.

# Step 48 — Traceability

Every major conclusion should trace to:

```text
driver
quality scenario
constraint
risk
candidate evidence
```

# Step 49 — Recommendation Is Not ADR

This skill can recommend.

It does not create the formal decision record.

Next:

```text
recording-architecture-decisions
```

# Final Status

Use:

```text
ARCHITECTURE_TRADEOFF_ANALYSIS_READY
ARCHITECTURE_TRADEOFF_ANALYSIS_READY_WITH_CONDITIONS
ARCHITECTURE_TRADEOFF_REQUIRES_EVIDENCE
ARCHITECTURE_TRADEOFF_REQUIRES_CONSTRAINT_DECISION
ARCHITECTURE_TRADEOFF_NO_CLEAR_WINNER
ARCHITECTURE_TRADEOFF_SINGLE_VIABLE_CANDIDATE
ARCHITECTURE_TRADEOFF_REJECTS_ALL_CANDIDATES
BLOCKED
```

# Output

Use:

```text
assets/architecture-tradeoff-analysis.md
```

## Completion Criteria

- [ ] Decision scope and candidate set are explicit.
- [ ] Candidates are normalized to comparable abstraction.
- [ ] Criteria derive only from drivers/constraints/quality/risk/context.
- [ ] Hard constraints are checked before preference comparison.
- [ ] Evidence strength is visible.
- [ ] Primary drivers are analyzed explicitly.
- [ ] Conditional drivers are treated with sensitivity rather than invented measures.
- [ ] Availability/resilience trade-offs are explicit.
- [ ] Consistency trade-offs are explicit.
- [ ] Performance/scale claims use real evidence only.
- [ ] Security/tenant-isolation implications are explicit.
- [ ] Modifiability is evaluated against actual change scenarios.
- [ ] Observability/diagnosability implications are explicit.
- [ ] Recoverability remains conditional if RTO/RPO are unknown.
- [ ] Team and operational complexity are explicit.
- [ ] Brownfield/migration trade-offs are explicit when relevant.
- [ ] Cost is not numerically fabricated.
- [ ] Vendor lock-in is evaluated proportionately.
- [ ] Reversibility and optionality are explicit.
- [ ] Candidate complexity is explicit.
- [ ] Risks introduced by each candidate are explicit.
- [ ] Assumption dependence is explicit.
- [ ] Sensitivity analysis identifies decision-flipping unknowns.
- [ ] Thresholds are not invented.
- [ ] Dominated candidates are only labeled with sufficient evidence.
- [ ] Pareto-optimal candidates are allowed.
- [ ] Weighted numeric scoring is not used without an accepted model.
- [ ] Fake precision is absent.
- [ ] Recommendation can be conditional or deferred.
- [ ] Decision reversal triggers are explicit.
- [ ] Architecture spikes are recommended only when they resolve material uncertainty.
- [ ] Sensitivity/trade-off points are identified where useful.
- [ ] Constraint exceptions are never silently waived.
- [ ] Major conclusions are traceable.
- [ ] ADR handoff is explicit.
- [ ] Final status is explicit.

## References

- Read `references/tradeoff-analysis-scope-criteria-and-evidence.md` first.
- Read `references/quality-attribute-tensions-and-candidate-comparison.md`.
- Read `references/team-operations-migration-cost-and-lockin.md`.
- Read `references/risk-assumptions-sensitivity-thresholds-and-reversibility.md`.
- Read `references/dominance-pareto-weighting-and-fake-precision.md`.
- Read `references/atam-inspired-sensitivity-tradeoff-risk-thinking.md`.
- Read `references/recommendation-defer-reversal-triggers-and-adr-handoff.md`.
- Read `references/architecture-tradeoff-analysis-audit.md` before completion.
