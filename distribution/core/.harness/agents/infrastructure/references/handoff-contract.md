# Infrastructure Handoff Contract

Every handoff must include:

- recipient;
- INFRA finding/question ID;
- affected environment/resource/workflow;
- accepted architecture/security/performance expectation;
- evidence;
- operational failure scenario;
- required next action;
- expected output/evidence;
- blocking status;
- re-entry condition.

## Validator

Route exact execution of:

```text
CI checks
terraform validate/plan
helm lint/template
manifest validation
container build
deployment dry-run
smoke check
migration check
```

Validator reports execution truth.

Infrastructure interprets operational meaning.

## Security

Route:

```text
IAM/control requirement
CI secret/security issue
network exposure
secret delivery
artifact provenance
runtime hardening
```

Security determines control adequacy/residual risk.

## Performance

Route resource/capacity evidence:

```text
CPU/memory sizing
replica count
autoscaling metric
connection pool
worker concurrency
```

Infrastructure must not invent performance requirements.

## Architecture Review

Route any required topology decision/change:

```text
new service
new queue/cache/store
region/failure-domain change
deployment strategy architecture
data-store ownership
public/private boundary
```

## Code Review

Route application/runtime defects such as:

```text
bad shutdown handling
invalid config parsing
migration implementation bug
health endpoint logic bug
```

when the defect is code-owned.

## QA

Route deployment smoke/acceptance scenario quality when broader behavioral proof is needed.

## Detail Analyst

Route missing propagation across:

```text
spec
IaC
CI
config
runbook
monitoring
feature flags
cleanup
```

## Product / Architecture Owner

Route unresolved downtime/release/region/provider/environment decisions.

## Reviewer

Handoff final infrastructure decision, blockers, conditions, rollback status, drift and residual operational risk.

## Rule

Never hand off vague requests such as:

```text
"fix CI"
"review Kubernetes"
"add monitoring"
```

Name the exact resource, scenario, evidence and re-entry condition.
