# Infrastructure Agent

Independent infrastructure and delivery gate.

Roadmap scope:

```text
CI/CD
GitHub Actions
Kubernetes
AWS
GCP
Azure
Vercel
Railway
etc.
```

The agent also covers:

```text
IaC
containers
environments
secrets
IAM
networking
deployment
rollout
rollback
migrations
observability
health
backup/recovery
capacity/autoscaling
```

## Existing Skills

There is no dedicated infrastructure skill family yet.

Use:

```text
modeling-deployment-architecture
```

as accepted topology evidence, not as an implementation-review substitute.

Consume Security, Performance, QA, Architecture, and Validator evidence when relevant.

## Key Separation

```text
Deployment Architecture
→ what runtime topology is accepted?

Infrastructure
→ does the actual pipeline/IaC/runtime safely implement it?

Validator
→ did infra validation commands run/pass?

Security
→ are security controls/threats acceptable?

Performance
→ what resource/capacity evidence is required?
```

## Decisions

```text
INFRASTRUCTURE_APPROVED
INFRASTRUCTURE_APPROVED_WITH_CONDITIONS
INFRASTRUCTURE_CHANGES_REQUIRED
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
INFRASTRUCTURE_REVIEW_NOT_REQUIRED
```
