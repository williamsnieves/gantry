# CI/CD and GitHub Actions Review

## Pipeline Questions

```text
what triggers it?
what code is trusted?
what permissions exist?
what secrets are available?
what artifact is produced?
what environment is targeted?
what approvals exist?
what happens on concurrency/retry?
how is deployment verified?
```

## GitHub Actions Risk Areas

Review when applicable:

```text
pull_request
pull_request_target
workflow_dispatch inputs
workflow_run
forks
repository/environment secrets
GITHUB_TOKEN permissions
OIDC
third-party actions
shell interpolation
artifact upload/download
caches
environment protection
```

## Least Privilege

Set permissions according to actual steps.

Avoid write/admin scopes merely because they are convenient.

## Build Once

Where supported:

```text
source commit
→ immutable artifact
→ promote artifact
```

This improves traceability/rollback.

Do not force this model if platform architecture intentionally rebuilds per environment.

## Post-Deploy Verification

High-risk deploys should prove more than job exit success.

Possible:

```text
version
health/readiness
critical smoke
error rate
migration status
```

Use only relevant signals.
