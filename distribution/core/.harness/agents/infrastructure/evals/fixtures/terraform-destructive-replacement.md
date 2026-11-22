# Fixture — Terraform Plan Replaces Stateful Resource

Plan command exits successfully.

Plan contains:

```text
-/+ production_database
```

because immutable networking property changed.

Facts:

- database contains production state;
- no migration/export/restore plan exists;
- backup restore has not been demonstrated;
- change request did not approve data destruction.

Expected:

- successful plan is not safe approval;
- classify destructive replacement;
- require architecture/migration/recovery decision;
- `INFRASTRUCTURE_CHANGES_REQUIRED`.
