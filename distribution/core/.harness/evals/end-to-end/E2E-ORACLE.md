# End-to-End Semantic Oracle

## Purpose

Define what must remain semantically stable across implementations and runtimes.

The oracle does not require identical wording.

## Classification Oracle

Must preserve:

```text
work mode
material scopes
material risk triggers
```

## Routing Oracle

For each agent:

```text
REQUIRED
CONDITIONAL
NOT_TRIGGERED
NOT_APPLICABLE
ALREADY_SATISFIED
BLOCKED
```

with a reason.

## Handoff Oracle

A receiver must know:

```text
why it was activated
what scope is relevant
what facts/evidence already exist
what remains unknown
what action/output is expected
what allows re-entry
```

## Execution Oracle

Independent read-only specialist gates may run concurrently.

A runtime may serialize them.

It may not:

```text
skip
merge away
or weaken
```

their semantic responsibilities.

## Blocking Oracle

Strict precedence:

```text
proven changes-required blocker
> unresolved authoritative decision
> missing required evidence
> valid non-blocking condition
> pass/not-required
```

## Re-Review Oracle

After remediation:

```text
rerun every invalidated gate
do not mechanically rerun unrelated gates
```

## Reviewer Oracle

Reviewer must:

```text
preserve original specialist decisions
normalize without weakening
detect stale/missing/contradictory gates
preserve conditions
```

## Final Gate Oracle

Only:

```text
PRE_PR_PASS
PRE_PR_PASS_WITH_CONDITIONS
```

may allow PR creation.

## Runtime Oracle

Claude/Codex/Cursor/OpenCode/OMP may differ in:

```text
model
process model
parallelism implementation
tool syntax
directory layout
message transport
```

They must match in:

```text
semantic routing
gate ownership
blocking
handoffs
re-review
final decision
```
