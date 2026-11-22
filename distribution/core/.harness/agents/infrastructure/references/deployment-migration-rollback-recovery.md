# Deployment, Migration, Rollback, and Recovery

## Deployment Strategy

Choose only from accepted/platform-supported strategies.

Review:

```text
risk
compatibility
state
traffic control
rollback
cost
platform capability
```

## Migration Ordering

For full-stack/schema changes, explicitly define ordering.

Typical questions:

```text
can old code run with new schema?
can new code run before migration?
can frontend deploy before backend?
can consumer deploy before producer?
```

## Rollback

Rollback needs:

```text
artifact
config
schema/data
traffic
secret state
external effects
```

`git revert` alone is insufficient.

## Irreversible Change

If rollback becomes impossible:

```text
make it explicit
→ define forward-fix/recovery
→ increase rollout verification
```

## Feature Flags

Flags require:

```text
owner
default
scope
security boundary
cleanup/removal trigger
```

Do not let temporary flags become permanent architecture silently.
