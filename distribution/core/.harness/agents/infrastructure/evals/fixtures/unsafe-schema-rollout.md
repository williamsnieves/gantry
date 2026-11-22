# Fixture — Unsafe Schema Rollout

Current production:

- application v1 reads column `legacy_status`.

Change:

- migration immediately drops `legacy_status`;
- application v2 reads `status`;
- rolling deployment means v1 and v2 coexist for several minutes;
- deployment pipeline runs migration before replacing all v1 replicas;
- rollback would restore v1 binary after column has been dropped.

Expected:

- identify mixed-version incompatibility;
- rollback is unsafe;
- require staged compatible migration/order;
- `INFRASTRUCTURE_CHANGES_REQUIRED`.
