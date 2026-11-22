---
name: modeling-deployment-architecture
description: Portable engineering capability `modeling-deployment-architecture`. Use
  when the harness or a specialist agent explicitly requires this named capability.
---
# Modeling Deployment Architecture

## Purpose

Model runtime topology and infrastructure placement.

Roadmap-required concerns:

```text
regions / zones
compute
load balancers / gateways
databases
queues
object stores
caches
external providers
network / trust boundaries
observability
secrets
failover
```

Output:

```text
deployment-architecture-model.md
```

## Core Principle

Deployment architecture answers:

```text
where do logical/runtime containers run?
what infrastructure/runtime nodes host them?
how are they exposed?
where is data placed?
what network/trust boundaries exist?
what scales or fails independently?
what observability/secrets/failover topology is required?
```

It does not primarily answer:

```text
what logical containers/components exist?  → C4
what messages happen in what order?        → sequence
what data concepts/cardinality exist?      → domain data
what data moves across trust boundaries?   → DFD
what event contract/delivery semantics?     → event flow
```

# Use When

- Accepted logical containers need runtime placement.
- Availability/recovery/scaling drivers require topology reasoning.
- Region/zone placement matters.
- Gateways/load balancers/network boundaries matter.
- Persistent stores/queues/caches/object stores must be placed.
- External provider connectivity affects runtime topology.
- Observability and secret distribution affect operations/security.
- Failover/recovery assumptions must be made explicit.
- Architecture validation needs deployment feasibility evidence.

# Do Not Use When

- Logical architecture is still undecided.
- The task is selecting among architecture candidates.
- The task is only C4 logical modeling.
- The task is provider/event delivery semantics.
- The task is detailed IaC implementation.
- The task is cloud cost optimization without accepted deployment scope.
- The task is choosing Kubernetes/cloud/database technology from preference.

# Inputs

Preferred:

- accepted ADRs;
- C4 architecture model;
- sequence models;
- DFD/trust-boundary model;
- domain-data model;
- event-flow model;
- architecture drivers;
- availability/recovery/scaling/security NFRs;
- accepted cloud/on-prem constraints;
- accepted data residency;
- accepted secret-handling decisions;
- provider/network requirements;
- applicable `AGENTS.md`.

Optional:

- current deployment;
- infrastructure inventory;
- cloud architecture diagrams;
- RTO/RPO;
- SLOs;
- provider regions;
- network policies;
- observability stack;
- disaster-recovery runbooks.

# Outputs

- Deployment Architecture Model.
- Logical-container → deployment-node mapping.
- Region/zone topology.
- Compute/runtime placement.
- Entry/gateway/load-balancing model.
- Data-store/queue/cache/object-store placement.
- External-provider connectivity.
- Network/trust-boundary model.
- Observability placement.
- Secret/credential distribution model.
- Failover/recovery topology.
- Scaling/blast-radius analysis.
- Unknowns/gaps.
- Architecture-validation handoff.

# Deployment Element Identity

Use stable IDs:

```text
REG-001
ZONE-001
NODE-001
GW-001
DB-001
QUEUE-001
CACHE-001
OBJ-001
OBS-001
SEC-001
EXT-001
REL-001
```

or repository convention.

# Step 1 — Establish Deployment Scope

Record:

```text
system/environment
architecture/ADR version
current / target / transition
environment(s) in scope
availability/recovery horizon
cloud/on-prem constraints
```

Do not model every environment unless useful.

# Step 2 — Map C4 Containers to Deployment Nodes

Start from accepted C4 logical/runtime containers.

For each:

```text
logical container
→ runtime/deployment node
→ instance/replica model if decided
→ network zone/boundary
```

If placement is undecided:

```text
PLACEMENT_DECISION_REQUIRED
```

Do not invent runtime units.

# Step 3 — Logical vs Physical Distinction

C4 Container:

```text
logical runtime/deployable unit
```

Deployment Node:

```text
environment/runtime/infrastructure location hosting instances
```

Do not conflate them.

# Step 4 — Environment Modeling

Possible:

```text
production
staging
disaster recovery
edge/on-prem site
```

Only include environments relevant to the architecture question.

# Step 5 — Regions

Roadmap-required.

Record accepted region requirements:

```text
single region
multi-region
region TBD
on-prem location
```

If no decision:

```text
REGION_DECISION_REQUIRED
```

Do not invent `eu-west-1`, `europe-west1`, etc.

# Step 6 — Zones / Failure Domains

Roadmap-required.

Record zones/failure domains only when accepted/relevant.

Possible:

```text
single failure domain
multi-zone
zone topology TBD
```

Do not claim multi-AZ automatically.

# Step 7 — Residency Alignment

If DFD/privacy says data must remain in a geography:

```text
deployment placement must satisfy it
```

If conflict:

```text
DEPLOYMENT_RESIDENCY_CONFLICT
```

Do not silently move data.

# Step 8 — Compute

Roadmap-required.

Compute may include:

```text
VMs
containers
serverless
PaaS application runtime
bare metal
edge runtime
```

Only name technology if accepted.

Otherwise:

```text
compute runtime: TBD
```

# Step 9 — Compute Unit Mapping

For every logical application/container record:

```text
runtime placement
replication/scaling model
resource isolation if known
```

Do not invent CPU/memory sizes.

# Step 10 — Replica Count

Only record explicit counts when authoritative.

Otherwise:

```text
REPLICA_COUNT_TBD
```

Do not invent 2/3 replicas.

# Step 11 — Autoscaling

Only model autoscaling if accepted.

Record:

```text
what scales
trigger/metric if known
min/max if known
```

Do not invent HPA/CPU thresholds.

# Step 12 — Load Balancers / Gateways

Roadmap-required.

Use when accepted architecture requires:

```text
public ingress
API gateway
reverse proxy
load balancer
edge gateway
```

Do not invent one because most systems have one.

# Step 13 — Ingress Responsibility

Record:

```text
what traffic enters
what trust boundary is crossed
what routing/security responsibility exists
```

Do not turn this into WAF/TLS implementation selection without decision.

# Step 14 — Public vs Private Exposure

Classify deployment nodes/interfaces as:

```text
PUBLIC
PRIVATE
RESTRICTED
EXTERNAL
UNKNOWN
```

when evidence supports it.

# Step 15 — Network Boundaries

Roadmap-required.

Represent:

```text
public internet boundary
private application network
data-store boundary
operator/admin boundary
provider boundary
tenant/user boundary
```

as deployment-relevant zones.

Do not invent VPC/subnet/CIDR design.

# Step 16 — Trust Boundaries

Align with DFD.

Deployment diagram should show where trust boundaries map physically/logically.

If deployment topology contradicts DFD trust model:

```text
DEPLOYMENT_DFD_CONFLICT
```

# Step 17 — Databases

Roadmap-required.

Map accepted persistent data stores to runtime placement.

Record:

```text
primary/replica role if decided
region/zone
writer/readers
backup/failover if decided
```

Do not invent DB technology.

# Step 18 — Database Authority

Deployment model should preserve logical data ownership.

Do not let infrastructure placement imply shared write ownership.

# Step 19 — Database Replication

Only show:

```text
replica
multi-zone
cross-region copy
```

when accepted.

Do not claim synchronous/asynchronous replication without evidence.

# Step 20 — Backup

Backup belongs in deployment/recovery when required.

Record only accepted:

```text
backup exists
frequency
retention
location
restore path
```

If required but unknown:

```text
BACKUP_POLICY_REQUIRED
```

# Step 21 — Queues

Roadmap-required, but only if accepted architecture includes one.

If event-flow says transport is TBD:

```text
do not invent queue/broker
```

Use:

```text
MESSAGING_INFRASTRUCTURE_DECISION_REQUIRED
```

# Step 22 — Queue Placement

When accepted, record:

```text
runtime/service
region/failure domain
producer connectivity
consumer connectivity
retention/dead-letter topology if decided
```

# Step 23 — Object Stores

Roadmap-required only when accepted.

Use for:

```text
uploads
documents
artifacts
backups
media
```

Do not invent object storage.

# Step 24 — Cache

Roadmap-required only when accepted.

A performance concern does NOT imply a cache.

If cache accepted, record:

```text
purpose
placement
scope
failure effect
authority relationship
```

Do not treat cache as source of truth unless decision says so.

# Step 25 — External Providers

Roadmap-required.

Show:

```text
identity provider
email provider
AI provider
payment provider
partner systems
```

and runtime connectivity/trust boundary.

Do not imply provider region/SLA if unknown.

# Step 26 — Provider Reachability

Record:

```text
public outbound connectivity
private link
provider callback ingress
provider polling
```

only when accepted.

If integration pattern unresolved:

```text
PROVIDER_CONNECTIVITY_DECISION_REQUIRED
```

# Step 27 — DNS / Service Discovery

Only model if architecture decision requires it.

Do not invent service mesh/discovery.

# Step 28 — Observability

Roadmap-required.

Model deployment-level telemetry path when accepted:

```text
application/runtime
→ logs/metrics/traces
→ observability sink/platform
```

Do not invent vendor.

# Step 29 — Observability Ownership

Record:

```text
what emits telemetry
where it is collected
who can access it
retention/data scope if known
```

Align sensitive logging with DFD.

# Step 30 — Logging Data Conflict

If deployment sends sensitive data to observability contrary to DFD/privacy:

```text
DEPLOYMENT_OBSERVABILITY_PRIVACY_CONFLICT
```

# Step 31 — Health Checks

Only model if accepted/required for failover/load balancing.

Do not invent endpoints/probes.

# Step 32 — Secrets

Roadmap-required.

Model:

```text
which runtime needs which secret category
where secret source/store exists if decided
how secret reaches consumer at architectural level
```

Never include secret values.

# Step 33 — Secret Store

Do not invent Vault/KMS/Secret Manager.

If mechanism undecided:

```text
SECRET_STORE_DECISION_REQUIRED
```

# Step 34 — Secret Scope

Avoid exposing one shared credential to unrelated runtime units.

Record least-distribution intent if accepted.

Do not invent exact IAM policy.

# Step 35 — Key / Certificate Placement

Only include when accepted security architecture requires it.

Do not invent certificate managers.

# Step 36 — Failover

Roadmap-required.

Model failover only if accepted availability/recovery requirements justify it.

Possible:

```text
instance replacement
zone failover
regional failover
provider failover
database failover
manual DR
```

Do not claim automatic failover without evidence.

# Step 37 — Failover Trigger

Record:

```text
what failure triggers failover
who/what detects it
automatic/manual
target
recovery consequence
```

if known.

# Step 38 — Failover Gap

Use:

```text
FAILOVER_STRATEGY_REQUIRED
```

when required but undecided.

# Step 39 — RTO / RPO

Align deployment strategy with accepted RTO/RPO.

If missing:

```text
RECOVERY_OBJECTIVES_REQUIRED
```

Do not invent.

# Step 40 — Recovery Path

For material failure modes ask:

```text
what remains available?
what is restored?
what data can be lost?
what operator action is needed?
```

Only answer from evidence.

# Step 41 — Single Point of Failure

Identify deployment SPOFs.

Examples may include:

```text
single runtime instance
single region
single writer
single gateway
single provider
```

Do not call something a SPOF if redundancy exists.

# Step 42 — Blast Radius

Record failure domains:

```text
instance
node
zone
region
database
provider
shared observability
shared secret system
```

when known.

# Step 43 — Availability Claim Standard

Never state:

```text
highly available
fault tolerant
resilient
```

without topology and requirement evidence.

Use:

```text
AVAILABILITY_CLAIM_UNSUPPORTED
```

# Step 44 — Scaling Shape

Record:

```text
what scales horizontally/vertically
what scales together
what remains bottleneck
```

only where accepted.

Do not invent autoscaling.

# Step 45 — Stateful vs Stateless Runtime

Only classify when architecture supports it.

Do not force statelessness.

# Step 46 — Session / Sticky Routing

Only include if accepted.

# Step 47 — Stateful Workload Placement

If persistent local state matters:

```text
placement/failover consequences
```

must be explicit.

# Step 48 — Network Dependency

Show runtime dependencies that materially affect availability/latency.

Do not draw every TCP link.

# Step 49 — Egress

External-provider flows may require outbound connectivity.

Show at architecture level when meaningful.

# Step 50 — Ingress

Provider callbacks/user traffic may require inbound connectivity.

Only if integration pattern accepted.

# Step 51 — Firewall / Security Group Boundary

Do not invent specific firewall rules.

You may record:

```text
only application runtime may access persistent store
```

if accepted as architectural access policy.

# Step 52 — Administrative Access

If operators/admins need production access, model boundary/path when material.

Do not invent bastion/VPN.

# Step 53 — Environment Isolation

If staging/prod isolation is an accepted constraint, represent it.

Do not assume shared/isolated accounts/projects.

# Step 54 — Multi-Tenant Deployment

Tenant isolation does not imply one deployment per tenant.

Do not invent dedicated tenant infrastructure.

# Step 55 — Tenant-Specific Deployment

Only model if explicitly required.

# Step 56 — Data Placement

Map domain/DFD data stores to deployment placement.

Do not introduce new persistence copies without evidence.

# Step 57 — Derived Stores / Caches

If deployment adds derived/read/cached stores, architecture/ADR evidence is required.

# Step 58 — Event Infrastructure Placement

Map event transport only after `modeling-event-flows`/ADR selects the infrastructure semantics.

Do not select a broker here.

# Step 59 — External Managed Service

If accepted:

```text
show external/managed trust boundary
responsibility split
region if known
failure dependency
```

# Step 60 — Shared Platform Services

Examples:

```text
observability
secrets
identity
gateway
messaging
```

May create shared blast radius.

Record explicitly.

# Step 61 — Control Plane vs Data Plane

Distinguish only where useful.

Do not introduce Kubernetes-style semantics automatically.

# Step 62 — Deployment Diagram Syntax

Prefer version-controlled source:

```text
PlantUML deployment diagram
Mermaid flowchart
Structurizr deployment view
repository convention
```

# Step 63 — C4 Deployment View

If repository uses Structurizr/C4 deployment views, preserve:

```text
Software System Instance
Container Instance
Deployment Node
Infrastructure Node
```

# Step 64 — Diagram Layering

A deployment diagram should show runtime topology, not class/module internals.

# Step 65 — Logical Container Mapping

Each deployed application/data runtime should map back to a C4 container/component responsibility.

# Step 66 — No Phantom Infrastructure

Every node/service/store must have source evidence.

Flag:

```text
UNSUPPORTED_DEPLOYMENT_ELEMENT
```

# Step 67 — Current / Target / DR Views

For brownfield/transition:

```text
CURRENT
TARGET
DISASTER_RECOVERY
TRANSITION
```

views may be separate.

Do not mix them ambiguously.

# Step 68 — Environment-Specific Differences

Only model differences that matter architecturally.

# Step 69 — C4 Alignment Audit

Check:

```text
all accepted C4 containers placed?
any deployment node hosting phantom logical service?
```

# Step 70 — Sequence Feasibility Audit

Check critical sequences against topology:

```text
can participants reach each other?
does private/public boundary permit flow?
is latency/failure dependency plausible?
```

Do not invent latency values.

# Step 71 — DFD Alignment Audit

Check:

```text
trust boundaries
third-party transfers
residency
secret flows
observability data
```

# Step 72 — Domain Data Alignment Audit

Check authoritative store placement and data ownership.

# Step 73 — Event Flow Alignment Audit

Check:

```text
selected messaging infrastructure exists?
producer/consumer connectivity feasible?
ordering/failover assumptions compatible?
```

# Step 74 — ADR Alignment Audit

If topology contradicts accepted ADR:

```text
DEPLOYMENT_ADR_CONFLICT
```

# Step 75 — Constraint Audit

Check:

```text
cloud/on-prem
residency
network
security
RTO/RPO
cost envelope
organization constraints
```

# Step 76 — Availability / Recovery Audit

For each availability/recovery claim:

```text
what topology supports it?
what failure domain?
what failover/recovery path?
what evidence?
```

# Step 77 — Security Boundary Audit

Check:

```text
public exposure
admin exposure
provider ingress/egress
database access
secret distribution
observability access
```

# Step 78 — Observability Audit

Check every critical runtime/failure domain has enough accepted telemetry path to diagnose architecture requirements.

Do not invent dashboards/alerts.

# Step 79 — Secret Distribution Audit

Check:

```text
which runtime receives each secret category?
is scope wider than required?
is source/store unknown?
```

# Step 80 — SPOF Audit

Identify single points and state whether:

```text
accepted
mitigated
unknown
```

# Step 81 — Failover Audit

Check:

```text
target exists?
trigger known?
state/data consistency compatible?
DNS/routing mechanism decided?
manual runbook required?
```

Do not invent mechanism.

# Step 82 — Capacity / Scale Gap

Use:

```text
CAPACITY_MODEL_REQUIRED
```

when scale driver requires sizing but measurements are missing.

# Step 83 — Region Gap

Use:

```text
REGION_DECISION_REQUIRED
```

# Step 84 — Zone Gap

Use:

```text
FAILURE_DOMAIN_DECISION_REQUIRED
```

# Step 85 — Compute Gap

Use:

```text
COMPUTE_RUNTIME_DECISION_REQUIRED
```

# Step 86 — Ingress Gap

Use:

```text
INGRESS_DECISION_REQUIRED
```

# Step 87 — Data Placement Gap

Use:

```text
DATA_PLACEMENT_DECISION_REQUIRED
```

# Step 88 — Messaging Gap

Use:

```text
MESSAGING_INFRASTRUCTURE_DECISION_REQUIRED
```

# Step 89 — Observability Gap

Use:

```text
OBSERVABILITY_PLACEMENT_REQUIRED
```

# Step 90 — Secret Gap

Use:

```text
SECRET_STORE_DECISION_REQUIRED
```

# Step 91 — Failover Gap

Use:

```text
FAILOVER_STRATEGY_REQUIRED
```

# Step 92 — Recovery Gap

Use:

```text
RECOVERY_OBJECTIVES_REQUIRED
```

# Model Quality Status

Use:

```text
READY
READY_WITH_OPEN_QUESTIONS
REQUIRES_REGION_DECISION
REQUIRES_FAILURE_DOMAIN_DECISION
REQUIRES_COMPUTE_RUNTIME_DECISION
REQUIRES_DATA_PLACEMENT
REQUIRES_MESSAGING_DECISION
REQUIRES_OBSERVABILITY_PLACEMENT
REQUIRES_SECRET_STORE_DECISION
REQUIRES_FAILOVER_STRATEGY
REQUIRES_RECOVERY_OBJECTIVES
REQUIRES_ARCHITECTURE_ALIGNMENT
CONFLICTED
```

# Final Decision

Use:

```text
DEPLOYMENT_MODEL_READY
DEPLOYMENT_MODEL_READY_WITH_OPEN_QUESTIONS
DEPLOYMENT_MODEL_REQUIRES_REGION_DECISION
DEPLOYMENT_MODEL_REQUIRES_FAILURE_DOMAIN_DECISION
DEPLOYMENT_MODEL_REQUIRES_COMPUTE_RUNTIME_DECISION
DEPLOYMENT_MODEL_REQUIRES_DATA_PLACEMENT
DEPLOYMENT_MODEL_REQUIRES_MESSAGING_DECISION
DEPLOYMENT_MODEL_REQUIRES_OBSERVABILITY_PLACEMENT
DEPLOYMENT_MODEL_REQUIRES_SECRET_STORE_DECISION
DEPLOYMENT_MODEL_REQUIRES_FAILOVER_STRATEGY
DEPLOYMENT_MODEL_REQUIRES_RECOVERY_OBJECTIVES
DEPLOYMENT_MODEL_REQUIRES_ARCHITECTURE_ALIGNMENT
DEPLOYMENT_MODEL_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/deployment-architecture-model.md
```

## Completion Criteria

- [ ] Deployment scope/environment/architecture basis are explicit.
- [ ] C4 logical containers map to runtime/deployment nodes.
- [ ] Logical vs physical deployment concepts are not conflated.
- [ ] Regions are explicit or undecided.
- [ ] Zones/failure domains are explicit or undecided.
- [ ] Residency constraints align with placement.
- [ ] Compute/runtime technology is not invented.
- [ ] Replica/autoscaling counts/thresholds are not invented.
- [ ] Gateways/load balancers appear only when accepted.
- [ ] Public/private/restricted exposure is explicit where known.
- [ ] Network/trust boundaries align with DFD.
- [ ] Database placement/replication/backup facts are evidence-backed.
- [ ] Queues/messaging infrastructure are not invented from event flows.
- [ ] Object stores/caches are not invented from generic need.
- [ ] External-provider connectivity does not invent callback/private-link patterns.
- [ ] Observability placement is explicit without vendor invention.
- [ ] Sensitive logging conflicts are surfaced.
- [ ] Secret distribution is modeled without values or invented secret-store technology.
- [ ] Failover is explicit only when supported.
- [ ] RTO/RPO alignment exists or recovery-objective gap is explicit.
- [ ] SPOFs/blast radius are explicit.
- [ ] HA/fault-tolerance claims are evidence-backed.
- [ ] Scaling shape is explicit without invented autoscaling.
- [ ] Administrative/environment/tenant deployment assumptions are not invented.
- [ ] Data/event placement aligns with domain/event models.
- [ ] Managed/shared platform services expose their blast radius.
- [ ] Deployment source is version-control friendly.
- [ ] Current/target/DR/transition views are separated where useful.
- [ ] C4/sequence/DFD/domain/event/ADR alignment audits pass or conflicts are surfaced.
- [ ] Security/observability/secret/SPOF/failover audits are performed.
- [ ] Region/zone/compute/ingress/data/messaging/observability/secret/failover/recovery gaps are explicit.
- [ ] Architecture-validation handoff is complete.
- [ ] Final readiness is explicit.

## References

- Read `references/deployment-scope-logical-mapping-regions-zones-and-compute.md` first.
- Read `references/ingress-network-trust-and-external-provider-connectivity.md`.
- Read `references/data-stores-queues-object-stores-caches-and-placement.md`.
- Read `references/observability-secrets-and-administrative-access.md`.
- Read `references/failover-recovery-spofs-blast-radius-and-scaling.md`.
- Read `references/deployment-vs-c4-sequence-dfd-event-and-domain-models.md`.
- Read `references/alignment-constraints-security-and-feasibility-audits.md`.
- Read `references/deployment-architecture-model-audit.md` before completion.
