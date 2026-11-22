---
name: designing-system-architecture
description: Generates multiple candidate system architectures from accepted architecture drivers, quality-attribute scenarios, constraints, assumptions, use cases, process flows, state machines, risks, and dependencies. Use after architecture drivers are identified and before trade-off analysis or ADR creation. Define system boundaries, major responsibilities, decomposition options, data ownership, communication styles, failure boundaries, integration patterns, deployment shapes, consistency expectations, operational implications, and unresolved risks for each candidate. Do not select a winner by preference, trend, or technology familiarity; do not fabricate requirements, collapse alternatives too early, or perform detailed C4/sequence/ERD/deployment modeling yet.
---

# Designing System Architecture

## Purpose

Generate viable candidate architectures from evidence.

Core workflow:

```text
architecture drivers
+ constraints
+ quality scenarios
+ behavioral models
+ dependencies
+ risks
        ↓
clarify system boundary
        ↓
derive architectural forces
        ↓
generate multiple viable candidates
        ↓
describe structure/data/communication/deployment/failure/operations
        ↓
identify assumptions + risks
        ↓
define evaluation hooks
        ↓
handoff to trade-off analysis
```

Output:

```text
candidate-system-architectures.md
```

## Core Principle

Architecture must be derived from:

```text
drivers
constraints
trade-offs
```

not:

```text
technology preference
trend
familiarity
resume-driven design
```

This skill generates candidates.

It does NOT choose the winner.

# Use When

- `identifying-architecture-drivers` has produced a usable driver set.
- A greenfield system needs architecture candidates.
- A major architectural change needs alternatives.
- System boundaries, decomposition, data ownership, communication, failure isolation, deployment, or operational model need to be considered.
- Architecture review needs explicit alternatives before trade-off analysis.

# Do Not Use When

- Requirements are still vague.
- Architecture drivers have not been identified.
- The task is to compare/select between already-defined candidates; use `analyzing-architecture-tradeoffs`.
- The task is to record a decision; use `recording-architecture-decisions`.
- The task is to create detailed C4/sequence/data/deployment diagrams.
- The task is to choose technologies without driver evidence.

# Inputs

Preferred:

- architecture drivers record;
- constraints;
- assumptions;
- quality-attribute scenarios;
- functional requirements;
- use-case catalog;
- process-flow model;
- state-machine model;
- risks;
- external dependencies;
- current architecture for brownfield;
- applicable `AGENTS.md`.

Optional:

- organizational/team topology;
- provider limitations;
- cost envelope;
- current production baseline;
- migration constraints;
- compliance/security boundaries.

# Outputs

- Candidate architecture set.
- Candidate architecture summaries.
- System boundary and context assumptions.
- Responsibility/decomposition models.
- Data ownership models.
- Communication style options.
- Failure-boundary analysis.
- Deployment-shape options.
- Operational implications.
- Candidate-specific risks.
- Candidate-specific assumptions.
- Open decisions.
- Evaluation criteria mapping.
- Handoff to `analyzing-architecture-tradeoffs`.

# Candidate Count

Prefer:

```text
2–4 meaningfully different candidates
```

when the design space allows it.

Do not manufacture fake alternatives.

If only one candidate is realistically viable because hard constraints eliminate others, state:

```text
SINGLE_VIABLE_CANDIDATE_DUE_TO_CONSTRAINTS
```

and explain why.

# Step 1 — Establish Architecture Scope

Record:

```text
system boundary
decision horizon
greenfield/brownfield
what is inside scope
what is explicitly outside scope
```

Do not design the entire enterprise if the decision is for one bounded system.

# Step 2 — Load Architecture Drivers

Summarize:

```text
PRIMARY drivers
SECONDARY drivers
CONDITIONAL drivers
CONSTRAINTS
ASSUMPTIONS
TENSIONS
MISSING EVIDENCE
```

Do not reclassify them silently.

# Step 3 — Derive Architectural Forces

Translate each driver into mechanism-neutral architectural pressure.

Example:

```text
Driver:
tenant isolation

Force:
architecture needs authoritative tenant boundaries
across data access, authorization, and integrations
```

Do not jump directly to schema-per-tenant or microservices.

# Step 4 — Identify Major Responsibilities

Derive major responsibilities from:

```text
use cases
functional capabilities
process flows
state machines
external interactions
```

Examples:

```text
conversation management
channel ingestion
identity/access
AI assistance
auditability
operator diagnostics
```

These are responsibilities, not automatically services.

# Step 5 — Identify Candidate Boundaries

Potential boundary criteria:

```text
business capability
data ownership
security boundary
failure boundary
team ownership
change rate
external integration
consistency boundary
```

Do not split solely because “microservices scale.”

# Step 6 — Candidate Architecture Families

Possible families include:

```text
modular monolith
service-oriented architecture
microservices
event-driven architecture
serverless
hybrid
```

Use only plausible families.

Do not include a family just to fill the list.

# Step 7 — Candidate A: Simplicity-Oriented

Often appropriate to consider:

```text
modular monolith
```

when:

```text
one/small team
moderate scale
strong consistency
low operational overhead
rapid delivery
```

But do not make it default.

Describe why it is viable relative to drivers.

# Step 8 — Candidate B: Boundary/Isolation-Oriented

Potentially:

```text
service-oriented / selectively separated services
```

when some capabilities need independent failure, scaling, data, or security boundaries.

Do not call everything a microservice.

# Step 9 — Candidate C: Distribution/Event-Oriented

Potentially:

```text
event-driven or more distributed architecture
```

when strong drivers justify:

```text
asynchronous decoupling
high throughput
independent scaling
event integration
failure isolation
```

Do not add event-driven architecture for ordinary CRUD.

# Step 10 — Brownfield Candidate

For existing systems include candidate paths such as:

```text
evolve current architecture
modularize in place
extract bounded capability
strangler migration
platform replacement
```

Only when supported.

# Step 11 — Candidate Structure

For each candidate record:

```text
architecture style/family
major runtime/deployable units
major responsibilities
dependency direction
boundary rationale
```

Avoid class/module-level design.

# Step 12 — Data Ownership

For each candidate describe:

```text
who owns which data concept?
what is shared?
what is authoritative?
what consistency boundary exists?
```

Do not design tables/ERD yet.

# Step 13 — Shared Database Warning

If multiple deployable units share one DB, record:

```text
coupling implications
ownership ambiguity
migration coordination
```

Do not declare it universally wrong.

# Step 14 — Data Distribution Warning

If data is split across services, record:

```text
cross-boundary consistency
query composition
transaction implications
migration complexity
```

Do not imply distributed data is free.

# Step 15 — Communication Style

Possible:

```text
in-process calls
synchronous request/response
asynchronous messaging
event publication
batch/file exchange
```

Select only at architectural level.

Do not define endpoints/topics yet.

# Step 16 — Synchronous Communication

Record implications:

```text
latency coupling
availability coupling
failure propagation
simpler immediate consistency
```

# Step 17 — Asynchronous Communication

Record implications:

```text
temporal decoupling
eventual consistency
retries
duplication
ordering
observability complexity
```

Do not prescribe broker technology.

# Step 18 — Consistency Model

Identify needed model at candidate level:

```text
strong/local transactional consistency
eventual consistency across boundaries
compensating workflow
```

Only where requirements support it.

# Step 19 — Long-Running Workflows

Use process/state evidence to identify:

```text
orchestration
choreography
manual handoff
provider callback
pending state
```

Do not choose saga/event sourcing unless justified.

# Step 20 — Failure Boundaries

For each candidate ask:

```text
what can fail independently?
what failure propagates?
what capability can degrade?
what external dependency is isolated?
```

# Step 21 — Provider Failure

For provider-dependent systems, evaluate candidate ability to:

```text
isolate provider failure
preserve core capability
surface degraded mode
maintain diagnosis
```

without yet designing circuit breakers/queues.

# Step 22 — Security / Trust Boundaries

Describe:

```text
where trust changes
where tenant boundary must be enforced
where sensitive data crosses external boundary
where privilege domains differ
```

Do not perform STRIDE yet.

# Step 23 — Deployment Shape

At candidate level describe:

```text
single deployable
few independently deployable units
many independent services
regional topology
serverless functions
```

Do not create detailed deployment diagrams yet.

# Step 24 — Scaling Shape

Describe:

```text
what scales together
what can scale independently
what data bottlenecks remain
```

Only use actual scale drivers.

# Step 25 — Operational Model

For each candidate include:

```text
deployment complexity
monitoring/diagnosis burden
incident surface
on-call complexity
release coordination
environment count
```

This is especially important for small teams.

# Step 26 — Team / Ownership

Architecture can consider:

```text
single-team ownership
multiple autonomous teams
platform team boundaries
```

Do not force Conway's Law mechanically.

# Step 27 — Change / Modifiability

For each candidate describe:

```text
which changes are localized
which require coordinated change
how external providers are added
```

Use quality scenarios.

# Step 28 — Cost Shape

Without inventing numbers, describe likely cost characteristics:

```text
baseline infra overhead
operational tooling burden
data-transfer costs
idle capacity
managed-service dependency
```

Only where relevant.

# Step 29 — Vendor Lock-In

Identify candidate-specific lock-in:

```text
cloud primitives
provider SDKs
proprietary messaging
managed databases
```

Do not assume lock-in is always bad.

# Step 30 — Complexity Budget

Every candidate consumes complexity.

Classify qualitatively:

```text
LOW
MEDIUM
HIGH
VERY_HIGH
```

and explain the dominant sources.

Do not pretend distributed systems have zero cost.

# Step 31 — Architecture Assumptions

Record candidate-specific assumptions.

Examples:

```text
single-team ownership remains
provider throughput is sufficient
cross-capability transactions are rare
```

Do not treat assumptions as facts.

# Step 32 — Candidate Risks

Examples:

```text
operational overload
coupling
consistency complexity
deployment coordination
provider lock-in
migration risk
observability gaps
```

# Step 33 — Candidate Unknowns

Record evidence needed before evaluation:

```text
scale target
provider limit
RTO/RPO
data residency
budget
team growth
```

# Step 34 — Constraints Check

For each candidate:

```text
SATISFIES
PARTIALLY_SATISFIES
VIOLATES
UNKNOWN
```

for each hard constraint.

A candidate violating a hard constraint is not viable unless the constraint itself is challengeable and explicitly being reconsidered.

# Step 35 — Driver Coverage

Map each candidate to each driver:

```text
supports strongly
supports
neutral
weak
unknown
```

Do NOT score/select yet.

That is trade-off analysis.

# Step 36 — Candidate Differentiation

Each candidate must be meaningfully distinct in:

```text
boundary/decomposition
data ownership
communication
deployment
failure isolation
operational model
```

Do not create:

```text
Candidate A: microservices on Kubernetes
Candidate B: microservices on ECS
```

if the architectural structure is effectively identical.

# Step 37 — Avoid Technology-Only Alternatives

Architecture alternatives should differ architecturally, not just vendor/tool.

# Step 38 — Avoid Premature Product Selection

Do not say:

```text
Candidate A is best.
```

Use:

```text
Candidate A favors simplicity and strong local consistency.
Candidate B favors selective failure/scaling isolation.
```

# Step 39 — Candidate Evaluation Hooks

For each candidate define questions later trade-off analysis must answer.

Example:

```text
Can this candidate satisfy tenant isolation
without excessive operational complexity for one five-person team?
```

# Step 40 — Architecture Decision Gaps

Use:

```text
ARCHITECTURE_INPUT_REQUIRED
```

for missing evidence that prevents meaningful candidate design.

# Step 41 — Candidate Viability Status

Use:

```text
VIABLE
VIABLE_WITH_CONDITIONS
AT_RISK
NOT_VIABLE
INSUFFICIENT_EVIDENCE
```

This is not final selection.

# Step 42 — Architecture Design Decision

Final skill status:

```text
CANDIDATE_ARCHITECTURES_READY
CANDIDATE_ARCHITECTURES_READY_WITH_CONDITIONS
CANDIDATE_ARCHITECTURES_REQUIRE_DRIVER_MEASURE
CANDIDATE_ARCHITECTURES_REQUIRE_CONSTRAINT_DECISION
CANDIDATE_ARCHITECTURES_REQUIRE_DEPENDENCY_EVIDENCE
CANDIDATE_ARCHITECTURES_SINGLE_VIABLE_CANDIDATE
BLOCKED
```

# Output

Use:

```text
assets/candidate-system-architectures.md
```

# Handoff to Trade-Off Analysis

Provide:

```text
candidate set
drivers
constraints
assumptions
risk profile
operational complexity
data/consistency model
failure model
evaluation questions
unknowns
```

Then:

```text
analyzing-architecture-tradeoffs
```

can compare candidates systematically.

## Completion Criteria

- [ ] Architecture scope and decision horizon are explicit.
- [ ] Driver/constraint/assumption inputs are preserved.
- [ ] Architectural forces are mechanism-neutral.
- [ ] Major responsibilities are derived from product behavior.
- [ ] Candidate boundaries use business/data/security/failure/team/change evidence.
- [ ] Multiple candidates are generated when the design space supports it.
- [ ] Fake alternatives are not manufactured.
- [ ] Candidate architectures are meaningfully different architecturally.
- [ ] Candidate structure/deployable units are described at high level.
- [ ] Data ownership/authority is explicit.
- [ ] Shared-data/distributed-data coupling is acknowledged.
- [ ] Communication style and consistency implications are explicit.
- [ ] Long-running workflows/provider callbacks are represented at architecture level.
- [ ] Failure boundaries and degraded-mode implications are explicit.
- [ ] Trust/security boundaries are explicit without threat modeling.
- [ ] Deployment/scaling shape is described without detailed deployment modeling.
- [ ] Operational complexity is explicit.
- [ ] Team/ownership implications are explicit.
- [ ] Modifiability and change-locality implications are explicit.
- [ ] Cost/vendor lock-in/complexity characteristics are visible when relevant.
- [ ] Candidate-specific assumptions/risks/unknowns are explicit.
- [ ] Hard constraint compliance is checked.
- [ ] Driver coverage is mapped without selecting a winner.
- [ ] Architecture alternatives are not merely technology/vendor substitutions.
- [ ] No architecture candidate is declared best.
- [ ] Evaluation hooks are produced.
- [ ] Missing evidence blocking architecture is explicit.
- [ ] Handoff to trade-off analysis is complete.
- [ ] Final readiness is explicit.

## References

- Read `references/architecture-scope-drivers-forces-and-candidate-generation.md` first.
- Read `references/responsibility-boundaries-decomposition-and-ownership.md`.
- Read `references/data-ownership-consistency-and-communication-styles.md`.
- Read `references/failure-security-deployment-scaling-and-operational-model.md`.
- Read `references/team-modifiability-cost-complexity-and-lockin.md`.
- Read `references/brownfield-migration-and-evolution-candidates.md`.
- Read `references/constraint-compliance-driver-coverage-and-candidate-differentiation.md`.
- Read `references/candidate-system-architecture-audit.md` before completion.
