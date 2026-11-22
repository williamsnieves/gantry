# Infrastructure Review Report

## Gate Decision

- Decision: INFRASTRUCTURE_APPROVED / INFRASTRUCTURE_APPROVED_WITH_CONDITIONS / INFRASTRUCTURE_CHANGES_REQUIRED / BLOCKED_PENDING_DECISION / BLOCKED_PENDING_EVIDENCE / INFRASTRUCTURE_REVIEW_NOT_REQUIRED
- Review version:
- Reviewer:
- Date:
- Target change / PR:
- Scope:
- Re-review required: yes/no

## Authoritative Basis

- Applicable `AGENTS.md`:
- OpenSpec / requirement:
- Deployment architecture:
- ADRs:
- Architecture validation:
- Security report:
- Performance report:
- QA report:
- Validator report:
- Accepted infrastructure/project policy:

## Environment Matrix

| Environment | Exists? | Deployment mechanism | Config source | Secret source | Exposure | Validation gate |
|---|---|---|---|---|---|---|
| CI | | | | | | |
| Preview | | | | | | |
| Staging | | | | | | |
| Production | | | | | | |
| DR | | | | | | |

## Deployment Architecture Alignment

- Accepted runtime nodes:
- Actual runtime resources:
- Accepted region/zone:
- Actual placement:
- Accepted ingress/network:
- Actual exposure:
- Accepted stateful dependencies:
- Actual services:
- Accepted observability/secrets:
- Actual implementation:
- Phantom/unapproved infrastructure:
- Missing accepted infrastructure:

## CI/CD

### Trigger / Scope
-

### Permissions
-

### Untrusted Input
-

### Secrets
-

### Build / Tests
-

### Artifact / Provenance
-

### Environment / Approval
-

### Concurrency / Retry
-

### Deployment / Post-Deploy
-

## IaC

- Tool:
- State/backend:
- Plan evidence:
- Creates:
- Updates:
- Replaces:
- Destroys:
- Sensitive changes:
- Unexpected cascades:
- Manual resources/drift:
- Import/adoption:
- Result:

## Container / Runtime

- Artifact/image:
- Base/runtime:
- Runtime user:
- Secret baking:
- Build context:
- Startup/shutdown:
- Health:
- Resource config:
- Result:

## Kubernetes / Platform Runtime

- Applicable: yes/no
- Workload:
- Service/Ingress:
- ServiceAccount/RBAC:
- Network policy:
- Config/Secrets:
- Resource requests/limits:
- Startup/liveness/readiness:
- Rollout:
- PDB/topology:
- Autoscaling:
- Result:

## IAM / Secrets / Network

### IAM
- Workload identity:
- Human/deploy identity:
- Privilege scope:
- Wildcards:
- Environment constraints:

### Secrets
- Source:
- CI access:
- Runtime delivery:
- Rotation:
- Logs/artifacts exposure:

### Network
- Public exposure:
- Private resources:
- Ingress:
- Egress:
- Provider callbacks:
- TLS/domain:
- DFD/Security alignment:

## Deployment / Rollout

- Strategy:
- Why appropriate:
- Artifact promotion:
- Order:
- Feature flags:
- Traffic switch:
- Post-deploy verification:
- Abort condition:

## Migration / Compatibility

- Schema/data migration:
- Execution owner:
- Idempotency:
- Mixed-version compatibility:
- Backfill:
- Rollback after migration:
- Forward-fix:
- Observability:
- Cleanup/contract step:

## Rollback / Recovery

- Previous artifact available:
- Config rollback:
- Schema compatibility:
- Data irreversibility:
- Secret state:
- Traffic rollback:
- External side effects:
- Recovery/runbook:
- Result:

## Observability / Health

- Logs:
- Metrics:
- Traces:
- Deployment markers:
- Startup:
- Readiness:
- Liveness:
- Alerts:
- Runbooks:
- Sensitive telemetry constraints:
- Result:

## Backup / DR

- Applicable:
- Backup:
- Restore evidence:
- RTO/RPO:
- Failure-domain strategy:
- DR runbook:
- Result:

## Capacity / Autoscaling

- Performance evidence:
- CPU/memory:
- Replicas:
- Autoscaling:
- Connection limits:
- Worker concurrency:
- Bottleneck:
- Headroom:
- Result:

## Drift / Manual Steps

| ID | Step/drift | Environment | Why exists | Owner | Verification | Exit path |
|---|---|---|---|---|---|---|
| | | | | | | |

## Findings

### INFRA-001 — [Title]

- Severity: CRITICAL / HIGH / MEDIUM / LOW
- Confidence: HIGH / MEDIUM / LOW
- Category: CI_CD / GITHUB_ACTIONS / SUPPLY_CHAIN / ARTIFACT / CONTAINER / IAC / KUBERNETES / CLOUD_RUNTIME / NETWORK / IAM / SECRETS / CONFIGURATION / ENVIRONMENT / DEPLOYMENT / ROLLOUT / ROLLBACK / MIGRATION / DATABASE_INFRA / OBSERVABILITY / HEALTH_PROBES / BACKUP_RECOVERY / CAPACITY / AUTOSCALING / DRIFT / MANUAL_STEP / COMPATIBILITY
- Environment:
- Architecture/policy basis:
- Resource/file/workflow:
- Failure scenario:
- Evidence:
- Impact:
- Smallest remediation:
- Verification:
- Rollback/recovery implication:
- Blocking: yes/no
- Handoff / owner:

## Decision / Evidence Questions

| ID | Decision/evidence | Why needed | Blocking? | Route |
|---|---|---|---|---|
| | | | | Architecture / Security / Performance / Validator / Product |

## Handoffs

| Finding / need | Recipient | Expected output | Blocking | Re-entry condition |
|---|---|---|---|---|
| | | | | |

## Residual Operational Risk

- Manual steps:
- Drift:
- Rollback limitations:
- Capacity uncertainty:
- Provider/platform dependency:
- Observability gaps:
- Deferred cleanup:

## Summary

- Critical findings:
- High findings:
- Medium findings:
- Low findings:
- Blocking decisions:
- Blocking evidence:
- Rollback readiness:
- Deployment readiness:
- Why final decision is justified:

## Exact Next Action

-
