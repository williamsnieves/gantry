---
name: identifying-architecture-drivers
description: Identifies the small set of architecture-significant requirements, quality scenarios, constraints, assumptions, risks, and dependencies that should materially shape system architecture. Use after functional requirements, non-functional requirements, and quality-attribute scenarios exist, and before candidate architecture design or trade-off analysis. Classify each input as ARCHITECTURE_DRIVER, IMPORTANT_REQUIREMENT, LOCAL_DESIGN_CONCERN, CONSTRAINT, ASSUMPTION, or NOT_ARCHITECTURE_SIGNIFICANT; preserve uncertainty and distinguish significance from business priority. Do not promote vague aspirations into drivers, choose architecture, prescribe tactics, or treat every requirement as architecture-significant.
---

# Identifying Architecture Drivers

## Purpose

Reduce the requirements space to the small set of concerns that should materially influence architecture.

Core workflow:

```text
FRs
+ NFRs
+ Quality Attribute Scenarios
+ Constraints
+ Assumptions
+ Risks
+ Dependencies
        ↓
evaluate architectural significance
        ↓
classify
        ↓
prioritize / rank significance
        ↓
identify conflicts and unresolved evidence
        ↓
produce architecture-driver set
```

Output:

```text
architecture-drivers-record.md
```

## Core Principle

Important does not mean architecture-significant.

```text
business priority
≠
architecture significance
```

A requirement is an architecture driver when satisfying it materially affects one or more of:

```text
system structure
major boundaries
deployment topology
data ownership/consistency
communication style
failure isolation
scaling strategy
security/trust boundaries
technology/platform constraints
operational model
cost envelope
team/organizational structure
```

## Classification

Use exactly:

```text
ARCHITECTURE_DRIVER
IMPORTANT_REQUIREMENT
LOCAL_DESIGN_CONCERN
CONSTRAINT
ASSUMPTION
NOT_ARCHITECTURE_SIGNIFICANT
```

### ARCHITECTURE_DRIVER

A requirement/scenario/constraint that materially shapes architecture.

### IMPORTANT_REQUIREMENT

Important product/system behavior that architecture must support but which does not materially determine high-level structure.

### LOCAL_DESIGN_CONCERN

Affects localized implementation or component design rather than whole-system architecture.

### CONSTRAINT

Restricts solution space regardless of quality significance.

### ASSUMPTION

Unverified premise that may influence architecture and requires validation or explicit acceptance.

### NOT_ARCHITECTURE_SIGNIFICANT

Does not materially affect architecture for the current scope.

# Use When

- Requirements foundation is complete enough.
- Candidate architecture design is about to begin.
- The architecture team needs a bounded set of drivers.
- Quality scenarios need architectural-significance classification.
- Product requirements include strong scale, availability, security, compliance, or topology implications.
- Constraints such as cloud/on-premise/vendor/team/budget need to be distinguished from drivers.
- Architecture risks are emerging from dependencies/assumptions.

# Do Not Use When

- Requirements are still vague.
- NFRs and quality scenarios have not been defined enough to assess significance.
- The task is to choose architecture.
- The task is to compare candidate architectures.
- The task is to write ADRs.
- The task is to perform threat modeling.
- The task is to decide detailed component design.

# Inputs

Preferred:

- PRD;
- functional requirements catalog;
- non-functional requirements catalog;
- quality-attribute scenarios;
- constraints;
- assumptions;
- risks;
- external dependencies;
- team/organizational constraints;
- provider/platform policies;
- cost/budget constraints;
- applicable `AGENTS.md`.

Optional:

- brownfield architecture;
- production scale/baseline evidence;
- incident history;
- regulatory/policy evidence;
- existing deployment restrictions.

## Outputs

- Architecture Drivers Record.
- Classification matrix.
- Driver evidence and rationale.
- Constraint register.
- Assumption register.
- Conflict/tension register.
- Missing-evidence ledger.
- Candidate architecture evaluation criteria.
- Handoff to `designing-system-architecture`.

# Architectural Significance Test

For each candidate ask:

```text
Would materially different architectures be selected
or evaluated differently because of this requirement?
```

If no, it is probably not an architecture driver.

Also ask:

```text
Does it affect:
- decomposition?
- deployment?
- data ownership/consistency?
- communication style?
- trust/security boundary?
- failure boundary?
- scale model?
- geographic topology?
- operational model?
- cost structure?
- organizational ownership?
```

# Significance Dimensions

Evaluate:

```text
SCOPE
STRICTNESS
CRITICALITY
CROSS_CUTTING_IMPACT
FAILURE_IMPACT
SCALE
SECURITY_PRIVACY_IMPACT
EXTERNAL_DEPENDENCY
CONSTRAINT_STRENGTH
CHANGE_PRESSURE
REVERSIBILITY
```

Do not mechanically score every item unless scoring helps comparison.

# Step 1 — Establish Scope

Record:

```text
system/product scope
architecture decision horizon
greenfield/brownfield
PRD version
FR/NFR/QA versions
known constraints
```

Architecture significance is always relative to scope.

# Step 2 — Collect Candidate Inputs

Candidates can come from:

```text
FRs
NFRs
quality scenarios
constraints
assumptions
risks
dependencies
product decisions
brownfield compatibility
```

Do not include every requirement automatically in the final driver set.

# Step 3 — Separate Requirements from Constraints

A constraint says:

```text
solution space is restricted
```

Examples:

```text
must deploy on-premise
must use approved cloud
must preserve legacy protocol
fixed regional residency
team must use organization platform
```

A driver says:

```text
architecture must achieve a meaningful property/outcome
```

Constraints may themselves be architecture-significant, but classify them as `CONSTRAINT` and record their impact.

# Step 4 — Separate Assumptions

Examples:

```text
future scale remains below 10k tenants
provider outage is rare
single region is acceptable
team remains five engineers
```

If unverified:

```text
ASSUMPTION
```

Do not promote to driver/fact.

# Step 5 — Evaluate Functional Requirements

Most FRs are not architecture drivers individually.

Example:

```text
agent can add an internal note
```

Likely:

```text
IMPORTANT_REQUIREMENT
```

or:

```text
LOCAL_DESIGN_CONCERN
```

But a functional requirement may become architecture-significant if it implies:

```text
real-time collaboration
offline-first behavior
global synchronization
multi-party workflow
external protocol contract
high-volume streaming
```

# Step 6 — Evaluate NFRs / Quality Scenarios

Quality scenarios are frequent driver sources.

Candidate driver examples:

```text
strict p99 latency at high load
99.99% critical availability
RTO/RPO requirements
tenant isolation
real-time message delivery
global distribution
strong consistency
high-volume event throughput
provider-outage resilience
```

Do not treat vague NFRs with TBD measures as automatically strong drivers.

# Step 7 — Strictness

A quality requirement becomes more architecture-significant when the target is difficult relative to context.

Example:

```text
p95 < 2 seconds at low traffic
```

may not be a driver.

```text
p99 < 50 ms at 100k req/s globally
```

likely is.

Use actual evidence only.

# Step 8 — Scale

Roadmap evaluation:

```text
"must scale"
```

with no dimensions/measures is NOT enough to classify as a strong architecture driver.

Use:

```text
MEASURE_REQUIRED
```

or classify as an unresolved architecture-driver candidate.

But:

```text
100k concurrent connections
```

with authoritative source and product need likely is:

```text
ARCHITECTURE_DRIVER
```

because it can shape concurrency, infrastructure, communication, and resource models.

# Step 9 — Availability / Recovery

Strict availability and recovery requirements often drive:

```text
redundancy
failure boundaries
deployment topology
data replication strategy
provider isolation
```

But do not prescribe those tactics here.

Example:

```text
RTO ≤ 5 min
RPO ≤ 1 min
```

may be strong drivers if authoritative.

# Step 10 — Consistency / Data Integrity

Requirements such as:

```text
strong consistency across distributed actions
no double payment
strict ordering
tenant-level isolation
```

can materially shape architecture.

Classify based on accepted semantics.

# Step 11 — Security / Privacy Boundaries

Security/privacy can drive architecture when they affect:

```text
trust boundaries
tenant isolation
data residency
key/secrets separation
privilege domains
third-party data flow
regulatory boundaries
```

Do not perform STRIDE here.

# Step 12 — Geographic Distribution

Requirements around:

```text
multiple regions
data residency
global latency
disconnected/offline locations
```

may be drivers.

Do not invent multi-region architecture.

# Step 13 — Real-Time Behavior

Real-time or near-real-time requirements can be drivers if timing is strict and broad.

Do not classify “real-time” as driver when it is vague.

Require definition/measure.

# Step 14 — External Providers

External-provider dependency can be a driver when:

```text
provider outage must not break core capability
provider imposes strict quotas
provider is mandatory
provider callbacks are eventual
provider data residency changes boundaries
```

If provider not selected, record:

```text
DEPENDENCY_DECISION_REQUIRED
```

when selection affects architecture.

# Step 15 — Cost Envelope

A strict cost ceiling can drive architecture.

Example:

```text
monthly infra cost ≤ €12k
```

with scale/quality targets may be a driver/constraint pair.

No approved budget:

```text
NOT_ENOUGH_EVIDENCE
```

Do not invent cost targets.

# Step 16 — Team / Organization

Roadmap evaluation:

A five-person team may materially constrain operational complexity.

Classify based on actual architecture implications.

Examples:

```text
small single team
→ possibly CONSTRAINT / architecture-significant organizational context

independent teams requiring autonomous deployability
→ potentially ARCHITECTURE_DRIVER
```

Do not automatically choose monolith or microservices.

# Step 17 — Mandatory Platform

Roadmap evaluation:

If policy says:

```text
must run on GCP
```

classify:

```text
CONSTRAINT
```

with high architecture impact.

Do not classify as a quality driver just because it changes solution space.

# Step 18 — Small CRUD Feature

Roadmap evaluation:

Typical CRUD behavior with modest scale/quality constraints is usually:

```text
IMPORTANT_REQUIREMENT
```

or:

```text
LOCAL_DESIGN_CONCERN
```

not an architecture driver.

Avoid architecture inflation.

# Step 19 — Architecture Significance of Risk

A risk can become a driver input if mitigating it materially affects architecture.

Example:

```text
external provider outage threatens core support workflow
```

may support a resilience driver.

A low-impact UI copy risk does not.

# Step 20 — Reversibility

Hard-to-reverse decisions deserve more architectural attention.

Examples:

```text
data partitioning
public API contract
multi-region topology
event model
tenant isolation strategy
```

Use reversibility as significance evidence, not as a driver by itself.

# Step 21 — Cross-Cutting Impact

Requirements that affect many capabilities/layers are more likely drivers.

Example:

```text
tenant isolation across all data access
```

is more architecture-significant than one screen-level permission rule.

# Step 22 — Local Design Concern

Examples:

```text
specific sorting behavior
one local validation
one form interaction
one narrow adapter rule
```

may be important but local.

Do not elevate them.

# Step 23 — Important Requirement

Use this category for product-critical behavior architecture must support but that does not materially differentiate high-level architectures.

Examples:

```text
agents can resolve conversations
manager can reassign conversation
```

# Step 24 — Not Architecture Significant

Use when:

- requirement has no meaningful impact on architecture;
- concern is purely content/copy/presentation;
- local behavior is already handled inside accepted structure;
- impact is trivial relative to system scope.

Do not interpret this as “not important.”

# Step 25 — Driver Rationale

Every `ARCHITECTURE_DRIVER` must state:

```text
why it affects architecture
which architecture dimensions it affects
which evidence supports it
what would be different if it did not exist
```

# Step 26 — Driver Strength

Optionally classify:

```text
PRIMARY
SECONDARY
CONDITIONAL
```

### PRIMARY

Strongly differentiates architecture choices.

### SECONDARY

Meaningfully influences design but is not dominant.

### CONDITIONAL

Becomes a driver if unresolved measure/decision crosses a threshold.

Use only when useful.

# Step 27 — Architecture Driver Categories

Potential:

```text
FUNCTIONAL
QUALITY
SECURITY_PRIVACY
DATA
SCALE
AVAILABILITY_RECOVERY
INTEGRATION
DEPLOYMENT
ORGANIZATIONAL
COST
COMPLIANCE
BROWNFIELD
```

# Step 28 — Unknown Measures

If a candidate quality scenario lacks critical measure:

```text
ARCHITECTURE_DRIVER_CANDIDATE_REQUIRES_MEASURE
```

Do not pretend precision.

Example:

```text
dashboard must be fast
```

cannot meaningfully drive topology until target/load are understood.

# Step 29 — Threshold Thinking

Some requirements become drivers only beyond a threshold.

Example:

```text
10 concurrent users
vs
100k concurrent users
```

Record:

```text
conditional driver pending scale target
```

when appropriate.

# Step 30 — Driver Interactions

Drivers may reinforce or compete.

Examples:

```text
strict availability + low RTO
→ reinforce resilience pressure

privacy minimization + rich observability
→ tension

global latency + data residency
→ tension

strong consistency + low latency across regions
→ tension
```

Do not resolve here.

# Step 31 — Driver Conflicts

Use:

```text
DRIVER_CONFLICT_REQUIRES_DECISION
```

when accepted constraints/scenarios are not jointly satisfiable or evidence suggests serious incompatibility.

# Step 32 — Missing Evidence Ledger

For each unresolved candidate record:

```text
missing measure
missing authority
missing scale
missing provider capability
missing policy
missing cost
missing geography
```

# Step 33 — Assumption Risk

If architecture would depend strongly on an assumption:

```text
ARCHITECTURE_ASSUMPTION_HIGH_RISK
```

Examples:

```text
single region will always suffice
provider never unavailable
scale stays small
```

Do not bury these.

# Step 34 — Brownfield Drivers

Brownfield constraints can include:

```text
legacy protocol compatibility
database migration window
zero-downtime migration
old client coexistence
existing organizational/platform ownership
```

Some are constraints, some quality drivers, some important requirements.

Classify individually.

# Step 35 — Candidate Architecture Evaluation Criteria

Convert accepted drivers into criteria that future architecture options must be evaluated against.

Example:

```text
Driver:
tenant isolation

Evaluation criterion:
candidate architecture must provide clear authoritative tenant boundaries across data access and external integration paths
```

Do not specify the mechanism.

# Step 36 — Priority vs Significance Matrix

Where useful:

| Business Priority | Architecture Significance | Meaning |
|---|---|---|
| High | High | likely driver |
| High | Low | important requirement |
| Low | High | architecture driver despite lower product priority |
| Low | Low | local / not significant |

This prevents product priority from being the sole signal.

# Step 37 — Driver Set Size

Aim for the smallest useful set.

No fixed numeric limit, but if dozens of items are marked as drivers:

```text
reassess classification
```

Drivers should discriminate architecture choices.

# Step 38 — Architecture Inflation Audit

Flag patterns:

```text
every NFR → driver
every security requirement → driver
every integration → driver
every feature → driver
every constraint → driver
```

Architecture significance requires rationale.

# Step 39 — Technology Leakage

Do not transform drivers directly into tactics.

Example:

```text
Driver:
100k concurrent realtime connections

NOT:
use WebSockets + Kafka + Kubernetes
```

Those come in architecture design/trade-off analysis.

# Step 40 — Driver Readiness

Per item:

```text
READY
READY_WITH_CONDITIONS
REQUIRES_MEASURE
REQUIRES_AUTHORITY
REQUIRES_POLICY
REQUIRES_DEPENDENCY_EVIDENCE
CONFLICTED
```

# Final Decision

Use:

```text
ARCHITECTURE_DRIVERS_READY
ARCHITECTURE_DRIVERS_READY_WITH_CONDITIONS
ARCHITECTURE_DRIVERS_REQUIRE_MEASURES
ARCHITECTURE_DRIVERS_REQUIRE_PRODUCT_DECISION
ARCHITECTURE_DRIVERS_REQUIRE_POLICY_DECISION
ARCHITECTURE_DRIVERS_REQUIRE_DEPENDENCY_EVIDENCE
ARCHITECTURE_DRIVERS_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/architecture-drivers-record.md
```

# Handoff to Architecture Design

Provide:

```text
primary drivers
secondary drivers
constraints
assumptions
driver conflicts/tensions
missing evidence
candidate architecture evaluation criteria
non-driver important requirements
local concerns
```

Then:

```text
designing-system-architecture
```

can produce architecture candidates from actual evidence rather than technology preference.

## Completion Criteria

- [ ] System/decision scope is explicit.
- [ ] Inputs include FR/NFR/quality scenarios/constraints/assumptions/risks as available.
- [ ] Every candidate receives exactly one primary classification.
- [ ] Business priority is separated from architecture significance.
- [ ] Architecture drivers have explicit rationale.
- [ ] Driver rationale identifies affected architecture dimensions.
- [ ] Vague “must scale” is not treated as a strong driver without measure.
- [ ] Authoritative extreme scale can become a driver.
- [ ] Small/local CRUD behavior is not inflated into a driver.
- [ ] Mandatory cloud/on-premise/platform requirements are classified as constraints.
- [ ] Strict availability/RTO/RPO are treated according to authoritative measures.
- [ ] Tenant isolation/security/privacy boundaries are assessed for cross-cutting significance.
- [ ] Real-time/geographic/consistency requirements are assessed with actual strictness.
- [ ] External-provider dependencies are assessed for architectural impact.
- [ ] Cost envelope is only used when authoritative.
- [ ] Team/organizational constraints are represented without prescribing architecture.
- [ ] Assumptions remain assumptions until validated.
- [ ] High-risk architecture assumptions are visible.
- [ ] Brownfield compatibility/migration concerns are classified.
- [ ] Important requirements remain distinct from drivers.
- [ ] Local design concerns are kept local.
- [ ] Not-architecture-significant does not imply low business importance.
- [ ] Unknown measures/authority/policy/provider evidence are recorded.
- [ ] Driver interactions/tensions are visible.
- [ ] Conflicts are not silently resolved.
- [ ] Driver set is deliberately small enough to discriminate architecture options.
- [ ] Architecture tactics/technology choices are not selected.
- [ ] Candidate architecture evaluation criteria are produced.
- [ ] Final driver readiness is explicit.

## References

- Read `references/architecture-significance-classification-and-scope.md` first.
- Read `references/quality-scale-availability-recovery-and-consistency-drivers.md`.
- Read `references/security-privacy-geography-realtime-and-data-boundaries.md`.
- Read `references/constraints-assumptions-dependencies-cost-and-organization.md`.
- Read `references/brownfield-reversibility-risk-and-cross-cutting-impact.md`.
- Read `references/driver-priority-tensions-conflicts-and-missing-evidence.md`.
- Read `references/architecture-evaluation-criteria-and-design-handoff.md`.
- Read `references/architecture-drivers-record-audit.md` before completion.
