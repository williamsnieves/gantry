# Fixture — GitHub Actions Untrusted PR + Secret

Workflow:

```yaml
on:
  pull_request_target:

permissions:
  contents: write

steps:
  - uses: actions/checkout@...
    with:
      ref: ${{ github.event.pull_request.head.sha }}
  - run: npm ci && npm test
  - run: ./deploy-preview.sh
    env:
      CLOUD_DEPLOY_TOKEN: ${{ secrets.CLOUD_DEPLOY_TOKEN }}
```

Repository accepts pull requests from forks.

Facts:

- workflow executes fork-controlled code in privileged base-repository context;
- deploy secret is available.

Expected:

- identify CI trust-boundary/secret-exposure risk;
- review excessive permissions;
- require safe separation/design before merge;
- route Security for control validation;
- `INFRASTRUCTURE_CHANGES_REQUIRED`.
