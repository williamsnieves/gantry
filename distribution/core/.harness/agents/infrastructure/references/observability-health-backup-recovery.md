# Observability, Health, Backup, and Recovery

## Health

Distinguish:

```text
startup
readiness
liveness
```

by semantics, not endpoint naming.

## Operational Telemetry

Ask whether operators can detect:

```text
failed deploy
startup failure
degraded dependency
migration failure
error spike
queue backlog
resource saturation
```

Use existing observability stack.

Do not invent a vendor.

## Alerts

Alerts should be actionable.

Record:

```text
signal
owner
action
noise risk
runbook
```

## Backup

A backup claim is stronger when restore has been demonstrated.

Review accepted:

```text
scope
frequency
retention
location
restore procedure
```

## Recovery

Align with accepted:

```text
RTO
RPO
failover
backup
runbook
```

Do not invent disaster recovery requirements.
