# Parallelism Policy

## Principle

Parallelize independent reasoning.

Serialize when one agent needs another agent's output or when concurrent mutation would invalidate evidence.

## Read-Only Review Fan-Out

These agents can often run in parallel after stable implementation and Validator preconditions:

```text
Backend Code Review
Backend Architecture Review
Frontend Code Review
Frontend Architecture Review
QA
Performance
Security
Infrastructure
```

Only routed/applicable agents participate.

## Preconditions for Parallel Review

Agents may run in parallel when they share:

```text
same change identity
stable repository state
sufficient accepted behavior
required domain inputs already available
read-only review authority
```

## Do Not Parallelize Mutations Against Review

Avoid:

```text
implementation agent editing files
while
specialist reviewers inspect same working tree
```

unless runtime provides isolated worktrees/snapshots and the harness explicitly tracks identities.

Preferred:

```text
freeze review snapshot
→ fan out read-only reviews
```

## Dependency-Constrained Reviews

Some specialist work may wait for prerequisites.

Examples:

```text
Security control verification
may require accepted control baseline

Performance
may require benchmark/load evidence

Infrastructure
may require accepted deployment target
```

Those gates may remain:

```text
WAITING_FOR_INPUT
```

while independent gates run.

## Architecture + Code Review

Code Review and Architecture Review may run in parallel if:

```text
architecture context is already stable
```

They need not serialize by default.

## QA + Code Review

QA may run in parallel with Code Review when:

```text
implementation/test state is stable
```

If Code Review later finds a production defect, QA evidence may become stale only for affected scenarios.

## Security Parallelism

Security may run concurrently with Code Review/QA when threat/control context is available.

Do not wait for Code Review just to discover security issues.

## Performance Parallelism

Performance may run concurrently if measurements are already available.

If measurements must first be generated:

```text
Validator / performance tooling execution
→ Performance interpretation
```

## Infrastructure Parallelism

Infrastructure can review IaC/pipeline/runtime in parallel with application reviews when rollout inputs are stable.

## Dynamic Fan-Out

A running gate may activate another gate.

Example:

```text
Backend Architecture Review
→ detects performance-sensitive per-item provider architecture
→ activate Performance
```

New gate joins the current fan-out as soon as prerequisites are satisfied.

## Fan-In Barrier

Reviewer must not run until:

```text
all REQUIRED routed specialist gates
are in a terminal state
```

Terminal:

```text
PASS-like
CHANGE_REQUIRED-like
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
NOT_REQUIRED
```

Not terminal:

```text
RUNNING
WAITING_FOR_INPUT
QUEUED
```

## Runtime Without Parallelism

If runtime cannot execute agents concurrently:

```text
execute same independent set sequentially
```

Do not remove gates.

## Oh My Pi / Swarm Adapters

OMP may map the fan-out into a DAG/swarm.

The OMP graph is an execution projection.

The source of truth remains:

```text
portable routing plan
+
parallelism policy
```

## Model Parallelism

Using different models for different agents is allowed.

Model assignment must not affect gate applicability.

## Maximum Concurrency

Portable core does not define a universal number.

Runtime adapter may limit concurrency based on:

```text
tool conflicts
rate limits
cost
context size
machine resources
```

but must preserve dependencies and gate completeness.
