# Deployment Architecture Model

## Document Control

- Product/system:
- Initiative:
- Model version:
- Status:
- Source ADR(s):
- Source C4:
- Source sequence/DFD/domain/event models:
- Environment(s):
- Owner:
- Date:
- Applicable `AGENTS.md`:

## Deployment Scope

- System/environment:
- Current / target / transition / DR:
- Availability horizon:
- Recovery horizon:
- Cloud/on-prem constraints:
- Residency constraints:
- Explicit exclusions:

## Logical Container → Deployment Mapping

| C4 element | Deployment node/runtime | Environment | Region | Zone/failure domain | Replication/scaling | Status | Source |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Region / Zone Topology

| ID | Region/location | Zone/failure domain | Purpose | Residency impact | Status/source |
|---|---|---|---|---|---|
| REG-001 | | | | | |

## Compute / Runtime Nodes

| ID | Runtime/node | Hosts | Runtime technology | Public/private | Scaling model | Failure domain | Source |
|---|---|---|---|---|---|---|---|
| NODE-001 | | | TBD | | | | |

## Ingress / Gateway / Load Balancing

| ID | Element | Traffic | Exposure | Routes to | Trust boundary | Technology | Source/gap |
|---|---|---|---|---|---|---|---|
| GW-001 | | | | | | TBD | |

## Data Store Placement

| ID | Logical store | Runtime/store | Region/zone | Authority | Replication | Backup | Failover | Source/gap |
|---|---|---|---|---|---|---|---|---|
| DB-001 | | | | | | | | |

## Messaging / Queue Placement

| ID | Logical event flow | Runtime transport | Region/zone | Producers | Consumers | Delivery/failover notes | Source/gap |
|---|---|---|---|---|---|---|---|
| QUEUE-001 | | TBD | | | | | MESSAGING_INFRASTRUCTURE_DECISION_REQUIRED |

## Object Stores

| ID | Purpose/data | Runtime/store | Region/zone | Authority | Replication/backup | Source |
|---|---|---|---|---|---|---|
| OBJ-001 | | | | | | |

## Caches

| ID | Purpose | Runtime/cache | Scope | Authority relationship | Failure effect | Source |
|---|---|---|---|---|---|---|
| CACHE-001 | | | | | | |

## External Provider Connectivity

| Provider | Direction | Connectivity pattern | Entry/egress boundary | Region/SLA known? | Failure dependency | Source/gap |
|---|---|---|---|---|---|---|
| | | TBD | | | | |

## Network / Trust Boundaries

| ID | Boundary/zone | Separates | Allowed architectural traffic | DFD mapping | Notes |
|---|---|---|---|---|---|
| TB-001 | | | | | |

## Observability Placement

| ID | Emitter/source | Telemetry type | Collector/sink | Trust/data sensitivity | Retention/access known? | Source/gap |
|---|---|---|---|---|---|---|
| OBS-001 | | logs/metrics/traces | TBD | | | |

## Secrets / Credentials

| ID | Secret category | Consumer runtime | Source/store | Distribution path | Trust boundary | Source/gap |
|---|---|---|---|---|---|---|
| SEC-001 | | | TBD | TBD | | SECRET_STORE_DECISION_REQUIRED |

## Failover / Recovery

| Failure | Detection | Failover/recovery target | Automatic/manual | Data consequence | RTO/RPO alignment | Source/gap |
|---|---|---|---|---|---|---|
| | | | | | | |

## Single Points of Failure / Blast Radius

| Element | Failure domain | Blast radius | Redundancy/failover | Status |
|---|---|---|---|---|
| | | | | ACCEPTED / MITIGATED / UNKNOWN |

## Scaling Shape

| Element | Scales independently? | Mechanism decided? | Bottleneck/coupling | Capacity evidence |
|---|---|---|---|---|
| | | | | |

## Deployment Diagram Source

```text
[Use repository-preferred PlantUML / Structurizr deployment view / Mermaid source]
```

## Current / Target / DR Views

### Current
-

### Target
-

### Disaster Recovery
-

### Transition
-

## Alignment Audits

### C4 / ADR
- Unplaced logical containers:
- Phantom deployment elements:
- Architecture contradictions:

### Sequence
- Unreachable participant pairs:
- Ingress/egress mismatch:
- Failure/latency feasibility concerns:

### DFD / Privacy
- Trust-boundary mismatch:
- Residency conflict:
- Third-party transfer mismatch:
- Observability privacy conflict:
- Secret-flow mismatch:

### Domain Data
- Authoritative store placement conflict:
- Replication/ownership ambiguity:

### Event Flow
- Missing messaging infrastructure:
- Producer/consumer connectivity mismatch:
- Delivery/failover incompatibility:

## Constraint / Feasibility Audits

### Availability / Recovery
- Unsupported HA claims:
- Missing failure domains:
- RTO/RPO mismatch:
- Failover target missing:

### Security
- Public exposure:
- Administrative exposure:
- Data-store access:
- Provider ingress/egress:
- Secret distribution:

### Observability
- Critical runtime without telemetry path:
- Failure domain without diagnosability:
- Sensitive data scope unknown:

### SPOF / Blast Radius
- Single region:
- Single runtime:
- Single writer/store:
- Single ingress:
- Single external provider:
- Shared platform dependency:

## Gap Ledger

| ID | Area | Gap | Type | Owner |
|---|---|---|---|---|
| | | | REGION_DECISION_REQUIRED / FAILURE_DOMAIN_DECISION_REQUIRED / COMPUTE_RUNTIME_DECISION_REQUIRED / INGRESS_DECISION_REQUIRED / DATA_PLACEMENT_DECISION_REQUIRED / MESSAGING_INFRASTRUCTURE_DECISION_REQUIRED / OBSERVABILITY_PLACEMENT_REQUIRED / SECRET_STORE_DECISION_REQUIRED / FAILOVER_STRATEGY_REQUIRED / RECOVERY_OBJECTIVES_REQUIRED / CAPACITY_MODEL_REQUIRED / DEPLOYMENT_C4_ALIGNMENT_REQUIRED | |

## Architecture Validation Handoff

- Deployment feasibility questions:
- Driver/quality scenarios to validate:
- Availability/recovery claims:
- Security/trust questions:
- Data placement/residency questions:
- Messaging/event questions:
- Operational/observability questions:
- Known blocking gaps:

## Final Decision

- Decision: DEPLOYMENT_MODEL_READY / DEPLOYMENT_MODEL_READY_WITH_OPEN_QUESTIONS / DEPLOYMENT_MODEL_REQUIRES_REGION_DECISION / DEPLOYMENT_MODEL_REQUIRES_FAILURE_DOMAIN_DECISION / DEPLOYMENT_MODEL_REQUIRES_COMPUTE_RUNTIME_DECISION / DEPLOYMENT_MODEL_REQUIRES_DATA_PLACEMENT / DEPLOYMENT_MODEL_REQUIRES_MESSAGING_DECISION / DEPLOYMENT_MODEL_REQUIRES_OBSERVABILITY_PLACEMENT / DEPLOYMENT_MODEL_REQUIRES_SECRET_STORE_DECISION / DEPLOYMENT_MODEL_REQUIRES_FAILOVER_STRATEGY / DEPLOYMENT_MODEL_REQUIRES_RECOVERY_OBJECTIVES / DEPLOYMENT_MODEL_REQUIRES_ARCHITECTURE_ALIGNMENT / DEPLOYMENT_MODEL_CONFLICTED / BLOCKED
- Blocking topology decisions:
- Recovery/failover gaps:
- Security/data-placement conflicts:
- Architecture alignment conflicts:
- Ready for `validating-architecture-design`:
