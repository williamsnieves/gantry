# Model and Platform Portability

## Portable Core

Keep stable:

- infrastructure mission;
- architecture-vs-implementation distinction;
- CI/IaC/runtime/rollout review method;
- evidence requirements;
- decision vocabulary;
- finding schema;
- handoff contract;
- completion criteria;
- evaluation fixtures.

## Platform Adapter

May vary:

- GitHub/GitLab/CircleCI/etc.;
- Terraform/Pulumi/CloudFormation;
- Kubernetes/Helm/Kustomize;
- AWS/GCP/Azure;
- Vercel/Railway/other PaaS;
- Docker/build tools;
- cloud CLI;
- observability tooling.

## Qualification Metrics

Evaluate:

- invented-infrastructure rate;
- dangerous IaC change detection;
- CI secret/permission detection;
- GitHub Actions trust-boundary reasoning;
- migration/rollback reasoning;
- environment mismatch detection;
- Kubernetes cargo-cult rate;
- provider-neutrality;
- security/performance boundary discipline;
- plan-vs-safety reasoning;
- handoff quality;
- no-write compliance.

## Stronger Reasoning Trigger

Escalate for:

- production IAM;
- multi-environment pipelines;
- destructive IaC;
- database migrations;
- Kubernetes rollouts;
- multi-service compatibility;
- canary/blue-green;
- DR/failover;
- cloud-network boundaries;
- CI supply-chain/untrusted fork risk.
