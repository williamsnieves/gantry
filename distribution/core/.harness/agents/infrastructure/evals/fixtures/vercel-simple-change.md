# Fixture — Vercel Application

Change:

- adds one production environment variable for a public API base URL;
- no secret;
- preview uses separate preview URL;
- build/runtime settings unchanged;
- accepted deployment architecture is Vercel-hosted frontend;
- rollback uses platform's previous deployment promotion;
- no database/migration/server state.

Expected:

- review PaaS environment/config/rollback;
- no Kubernetes/Terraform requirements;
- if configuration matches accepted topology and evidence is sufficient:
  `INFRASTRUCTURE_APPROVED`.
