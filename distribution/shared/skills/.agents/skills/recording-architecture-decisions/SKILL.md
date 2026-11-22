---
name: recording-architecture-decisions
description: Records accepted or proposed architecture decisions as durable Architecture Decision Records (ADRs) with stable identity, status, context, drivers, decision, alternatives considered, accepted trade-offs, consequences, risks, revisit triggers, and references. Use after architecture trade-off analysis has produced a recommendation or after an authoritative architecture decision has been made. Preserve uncertainty and decision authority, link each ADR to the evidence that justified it, and maintain supersession/deprecation history. Do not invent acceptance, rewrite history, collapse several unrelated decisions into one ADR, or use ADRs as substitutes for architecture design documents, C4 diagrams, implementation specs, or project logs.
...
---

# Recording Architecture Decisions

## Purpose

Turn architecture decisions into durable, reviewable, traceable ADRs.

Canonical ADR shape:

```text
ID
title
status
context
drivers
decision
alternatives considered
trade-offs
consequences
risks
revisit triggers
references
```

Output:

```text
ADR-*.md
```

## Core Principle

An ADR records:

```text
what was decided
why it was decided
what alternatives were considered
what trade-offs were accepted
what consequences follow
what evidence could trigger reconsideration
```

It is not a full architecture design document.

# Use When

- `analyzing-architecture-tradeoffs` has produced a recommendation and an authoritative owner accepts/proposes a decision.
- A significant architecture choice needs durable history.
- A constraint-driven choice must be documented.
- A prior ADR is superseded or deprecated.
- A brownfield architecture decision needs explicit evolution history.
- Future engineers need to know why the architecture is the way it is.

# Do Not Use When

- Candidate architectures have not yet been designed.
- Trade-offs have not been analyzed and no authoritative decision exists.
- The task is to generate architecture options.
- The task is to create C4/sequence/data/deployment diagrams.
- The task is to write implementation details or user stories.
- The task is to summarize every small coding convention as an ADR.

# Inputs

Preferred:

- architecture trade-off analysis;
- accepted architecture decision / decision-owner statement;
- architecture drivers;
- quality-attribute scenarios;
- candidate architecture record;
- constraints;
- risks;
- assumptions;
- decision reversal triggers;
- applicable `AGENTS.md`.

Optional:

- existing ADR index;
- superseded ADRs;
- architecture repository conventions;
- proof-of-concept/benchmark evidence;
- migration plans;
- policy documents.

# Outputs

- One or more ADR files.
- ADR index/update notes when repository convention requires it.
- Supersession/deprecation links.
- Traceability to drivers/trade-off analysis.
- Open implementation/modeling handoffs.

# ADR Identity

Prefer stable sequential IDs:

```text
ADR-0001
ADR-0002
ADR-0003
```

Use repository convention if one exists.

Do not reuse a retired ADR ID.

# ADR Filename

Preferred:

```text
ADR-0001-use-modular-monolith-for-v1.md
```

or repository convention.

Keep title concise and decision-oriented.

# ADR States

Use exactly:

```text
PROPOSED
ACCEPTED
SUPERSEDED
DEPRECATED
REJECTED
```

## PROPOSED

Decision is documented for review but not yet authoritative.

## ACCEPTED

Decision has authoritative acceptance.

## SUPERSEDED

A newer ADR replaces this decision.

Must reference:

```text
superseded by ADR-XXXX
```

## DEPRECATED

Decision is no longer recommended/current but may still exist in the system.

## REJECTED

Proposal was considered and explicitly rejected.

# Step 1 — Establish Decision Authority

Before setting status, identify:

```text
decision owner
approval evidence
decision date
decision scope
```

If no authoritative acceptance exists:

```text
status = PROPOSED
```

Never infer `ACCEPTED`.

# Step 2 — One Decision per ADR

An ADR should capture one coherent architectural decision.

Bad:

```text
Use modular monolith,
PostgreSQL,
Kafka,
Kubernetes,
and Datadog.
```

unless they are inseparable parts of one decision, which is uncommon.

Prefer separate ADRs when choices can change independently.

# Step 3 — Decision Significance

Use ADRs for decisions that are:

```text
architecturally significant
hard to reverse
cross-cutting
constraint-defining
risk-sensitive
long-lived
```

Do not create ADRs for routine local implementation details.

# Step 4 — Title

Use an action/decision title.

Good:

```text
Use a Modular Monolith for the Initial Support Platform
Separate Channel Ingestion from Core Conversation Processing
Keep Provider Integrations Behind Stable Internal Boundaries
```

Avoid:

```text
Architecture Decision
System Design
ADR about Microservices
```

# Step 5 — Context

Context should explain:

```text
problem/decision being faced
system scope
relevant existing conditions
why a decision is needed now
```

Do not restate the whole PRD.

# Step 6 — Drivers

List only drivers materially relevant to this decision.

Examples:

```text
tenant isolation
provider-outage resilience
small operations team
future provider modifiability
unknown scale
```

Trace to driver IDs when available.

# Step 7 — Constraints

Include hard constraints that shaped the choice.

Do not mislabel preferences as constraints.

# Step 8 — Assumptions

Material assumptions should be visible.

Example:

```text
The five-engineer team will remain the sole owner for v1.
```

If assumption changes, it may become a revisit trigger.

# Step 9 — Decision Statement

The decision must be concrete enough to understand.

Good:

```text
For v1, implement the product as a single deployable application
with explicit internal business-capability modules and stable integration boundaries.
```

Bad:

```text
Use a scalable architecture.
```

# Step 10 — Architecture Boundary

Record what the decision does and does not decide.

Example:

```text
This ADR decides deployable-unit granularity.
It does not select database technology, cloud runtime, or messaging broker.
```

This prevents accidental scope creep.

# Step 11 — Alternatives Considered

List meaningful alternatives actually evaluated.

For each:

```text
alternative
why viable
why not selected
conditions under which it might become preferable
```

Do not invent fake alternatives.

# Step 12 — Rejected vs Not Selected

Distinguish:

```text
not selected for this decision
```

from:

```text
REJECTED ADR status
```

An alternative in one ADR does not need its own rejected ADR unless repository practice requires it.

# Step 13 — Trade-Offs Accepted

State explicit trade-offs.

Example:

```text
Accept weaker independent runtime isolation
in exchange for lower operational complexity.
```

This is one of the most important ADR sections.

Do not write only benefits.

# Step 14 — Positive Consequences

Examples:

```text
lower deployment count
simpler local transactions
lower operational burden
faster initial delivery
```

Use evidence from analysis.

# Step 15 — Negative Consequences

Examples:

```text
capabilities cannot scale independently at first
runtime failure isolation is coarser
future extraction may require migration work
```

Negative consequences are mandatory for meaningful ADRs.

# Step 16 — Neutral Consequences

Some consequences are neither good nor bad.

Example:

```text
module boundaries become an important internal governance concern
```

Include when useful.

# Step 17 — Risks

Record remaining decision-specific risks.

Examples:

```text
internal module boundaries may erode
provider ingestion growth may later require extraction
unknown scale may invalidate current deployment granularity
```

# Step 18 — Risk Mitigation

ADR may record high-level mitigation/monitoring:

```text
enforce module boundaries
measure ingestion load
revisit after scale evidence
```

Do not turn ADR into implementation plan.

# Step 19 — Revisit Triggers

Roadmap-required and mandatory for significant decisions.

Examples:

```text
accepted scale target exceeds current candidate assumptions
team splits into autonomous ownership units
strict independent scaling becomes necessary
RTO/RPO become incompatible with current topology
provider ingestion becomes dominant failure/scale source
```

Do not use vague:

```text
revisit if needed
```

# Step 20 — Reversal Conditions

Where useful, state:

```text
what evidence would make another alternative preferable?
```

This preserves decision adaptability.

# Step 21 — References

Link to:

```text
architecture trade-off analysis
architecture drivers
quality scenarios
candidate architecture record
benchmarks/spikes
policy/constraint docs
related ADRs
```

Use repository-relative paths/IDs where possible.

# Step 22 — Traceability

Recommended chain:

```text
requirement / QA scenario
→ architecture driver
→ candidate architecture
→ trade-off analysis
→ ADR
```

# Step 23 — Status Transitions

Valid lifecycle examples:

```text
PROPOSED → ACCEPTED
PROPOSED → REJECTED
ACCEPTED → SUPERSEDED
ACCEPTED → DEPRECATED
```

Do not erase prior states.

# Step 24 — Supersession

When a decision changes:

```text
old ADR:
status = SUPERSEDED
superseded by = ADR-XXXX

new ADR:
supersedes = ADR-YYYY
```

Preserve history.

# Step 25 — Deprecation

Use `DEPRECATED` when:

```text
decision remains present/recognized
but should no longer guide new design
```

Do not use it as synonym for superseded.

# Step 26 — Rejection

A `REJECTED` ADR is useful when:

```text
the proposal itself was formally documented
and future recurrence would benefit from the history
```

Otherwise an alternative can remain inside an accepted ADR.

# Step 27 — Contradiction Audit

Check new ADR against existing accepted ADRs.

If conflict exists:

```text
ADR_CONFLICT_REQUIRES_RESOLUTION
```

Do not silently override.

# Step 28 — Supersession Audit

If the new decision replaces an old one:

```text
update both links/statuses
```

if repository write scope permits.

# Step 29 — Scope Overlap Audit

Two accepted ADRs should not accidentally own the same decision with incompatible outcomes.

# Step 30 — Decision vs Implementation Detail

ADR can decide:

```text
modular monolith
selective service boundary
event-driven integration
strong consistency boundary
single-region deployment
```

when architecturally significant.

Avoid low-level implementation details unless they themselves are architecture-significant.

# Step 31 — Technology ADRs

Technology choice can justify an ADR when it materially affects:

```text
architecture
operability
data
lock-in
security
cost
interoperability
```

Do not ADR every dependency/package.

# Step 32 — Temporary Decisions

A temporary decision can still be an ADR.

State:

```text
time horizon
revisit trigger
expiration/review date if authoritative
```

Do not invent dates.

# Step 33 — Unknowns

Preserve unresolved evidence.

Example:

```text
Scale threshold remains unknown.
This decision is accepted for v1 with a scale-measurement revisit trigger.
```

Do not rewrite unknowns as certainty.

# Step 34 — Accepted With Conditions

ADR state remains:

```text
ACCEPTED
```

only if authority accepted it.

Conditions belong in:

```text
decision
assumptions
revisit triggers
```

Do not invent a new roadmap status like `CONDITIONALLY_ACCEPTED`.

# Step 35 — Consequence Ownership

When meaningful, record who must handle a consequence.

Example:

```text
Engineering owns internal boundary governance.
Operations owns deployment/runbook impact.
```

Do not invent owners.

# Step 36 — ADR Index

If repository convention uses an ADR index, update:

```text
ID
title
status
date
supersession
```

Do not create an index if the repository does not use one unless user asks.

# Step 37 — Date Discipline

Use actual decision date if known.

If unknown:

```text
TBD
```

Do not use file creation date as decision date unless that is accepted convention.

# Step 38 — Decision Owner Discipline

If owner unknown:

```text
TBD
```

Do not invent architect/CTO approval.

# Step 39 — ADR Template Discipline

Keep ADR concise enough to read.

Move detailed evidence to references instead of duplicating whole analysis.

# Step 40 — Architecture Model Handoff

An accepted ADR may trigger:

```text
modeling-c4-architecture
modeling-system-sequences
modeling-data-flows
modeling-domain-data
modeling-event-flows
modeling-deployment-architecture
```

Do not create those artifacts inside the ADR skill.

# Step 41 — Threat Modeling Handoff

If ADR introduces:

```text
new trust boundary
new external integration
new data flow
new privilege domain
```

flag downstream:

```text
threat-modeling-with-stride
```

# Step 42 — Validation Handoff

Accepted ADRs become validation targets for:

```text
validating-architecture-design
```

# ADR Quality Status

Use:

```text
READY
READY_WITH_OPEN_REFERENCES
REQUIRES_DECISION_AUTHORITY
REQUIRES_TRADEOFF_ANALYSIS
REQUIRES_SUPERSESSION_RESOLUTION
CONFLICTED
```

# Final Skill Decision

Use:

```text
ADR_READY
ADR_READY_WITH_OPEN_REFERENCES
ADR_REQUIRES_DECISION_AUTHORITY
ADR_REQUIRES_TRADEOFF_ANALYSIS
ADR_REQUIRES_SUPERSESSION_RESOLUTION
ADR_CONFLICTED
BLOCKED
```

# Output

Create one or more:

```text
ADR-*.md
```

using:

```text
assets/ADR-template.md
```

## Completion Criteria

- [ ] ADR ID follows repository convention.
- [ ] Title is concise and decision-oriented.
- [ ] Status is exactly one of PROPOSED/ACCEPTED/SUPERSEDED/DEPRECATED/REJECTED.
- [ ] ACCEPTED is never inferred without authority.
- [ ] Decision owner/evidence is recorded or TBD.
- [ ] One coherent architecture decision per ADR.
- [ ] Decision is architecturally significant enough to warrant ADR.
- [ ] Context explains why the decision is needed.
- [ ] Relevant architecture drivers are linked.
- [ ] Constraints and assumptions remain distinct.
- [ ] Decision statement is concrete.
- [ ] Decision scope/non-decisions are explicit where useful.
- [ ] Alternatives considered are meaningful and real.
- [ ] Reasons alternatives were not selected are evidence-backed.
- [ ] Accepted trade-offs are explicit.
- [ ] Positive consequences are explicit.
- [ ] Negative consequences are explicit.
- [ ] Remaining risks are explicit.
- [ ] Revisit triggers are explicit and non-vague.
- [ ] Reversal conditions are included when useful.
- [ ] References link to evidence.
- [ ] Traceability to trade-off analysis/drivers exists.
- [ ] Superseded ADRs preserve history.
- [ ] Deprecation is not confused with supersession.
- [ ] Existing accepted ADR conflicts are checked.
- [ ] Implementation detail does not overwhelm architecture decision.
- [ ] Unknown evidence remains visible.
- [ ] No unapproved status vocabulary is introduced.
- [ ] ADR index is updated only when repository convention requires it.
- [ ] Dates/owners are not invented.
- [ ] Detailed architecture models remain downstream.
- [ ] Security/validation handoffs are flagged where relevant.
- [ ] Final ADR readiness is explicit.
