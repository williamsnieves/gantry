# Execution State Model

## Run States

```text
ROUTING
WAITING_FOR_IMPLEMENTATION
VALIDATING
REVIEWING
WAITING_FOR_DECISION
WAITING_FOR_EVIDENCE
REMEDIATING
REVALIDATING
DETAIL_ANALYSIS
REVIEWER_INTEGRATION
FINAL_PRE_PR
COMPLETE
FAILED
BLOCKED
```

## Agent States

```text
NOT_APPLICABLE
NOT_TRIGGERED
QUEUED
WAITING_FOR_INPUT
RUNNING
PASS
PASS_WITH_CONDITIONS
CHANGES_REQUIRED
PENDING_DECISION
PENDING_EVIDENCE
NOT_REQUIRED
STALE
CANCELLED
```

## Transition Rule

Only orchestrator changes run state.

Agents change only their own result state and may emit:

```text
handoff
dynamic_trigger
reentry_requirement
```

## Stable Snapshot

Each review wave has:

```text
snapshot_id
change_identity
```

All concurrently running read-only agents in that wave should inspect the same snapshot.

## Wave

A `review_wave` is:

```text
one stable change identity
+
one routed agent set
+
all dynamic activations before next remediation
```

After remediation:

```text
wave_id increments
```

This makes OMP/swarm or sequential execution traceable.
