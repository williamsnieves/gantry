# Portable Software Engineering Harness

Use the portable harness for meaningful software engineering work.

## Source of truth

```text
.harness/core/
.harness/agents/
.claude/skills/
```

Claude-specific files are execution adapters. They MUST NOT redefine portable engineering semantics.

## Before work

Classify the task as one of:

```text
DISCOVERY
ARCHITECTURE_ONLY
IMPLEMENTATION
REVIEW_ONLY
REMEDIATION
MIGRATION
RELEASE_ONLY
```

For implementation/review/release work, use `/harness-run` or follow the same routing contract.

## Routing

Run the smallest complete gate set.

```text
change size ≠ risk
```

Never skip a required gate because the diff is small.

Never run expensive unrelated specialists mechanically.

## Specialists

Available project agent types:

```text
validator
detail-analyst
backend-code-review
backend-architecture-review
frontend-code-review
frontend-architecture-review
qa
performance
security
infrastructure
reviewer
```

Use exact specialist ownership.

## Stable review snapshot

Do not let implementation mutate the same working state while read-only specialist review is in flight.

All agents in one review wave must inspect the same change identity.

## Parallelism

Independent read-only specialist reviews may run concurrently.

If concurrency is unavailable, execute the same semantic DAG sequentially.

## Dynamic routing

A specialist may discover a new material trigger.

Record the trigger, update routing, and launch the required gate before Reviewer fan-in.

## Blocking

Never average approvals.

A valid specialist blocker remains a blocker until its owner re-verifies remediation.

Missing required evidence is not PASS.

## Re-review

After remediation, rerun only materially invalidated gates.

Reviewer always re-integrates before final pre-PR.

## Final gate

Only:

```text
PRE_PR_PASS
PRE_PR_PASS_WITH_CONDITIONS
```

allow transition to PR creation.

Any post-gate edit makes final readiness stale.
