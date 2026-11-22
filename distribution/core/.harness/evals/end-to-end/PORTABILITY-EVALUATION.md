# Runtime Portability Evaluation

## Goal

Verify that runtime adapters are implementations of the harness, not alternate harnesses.

## Adapter Under Test

For every runtime:

```text
Claude Code
Codex
Cursor
OpenCode
Oh My Pi
```

run the same canonical scenarios.

## Must Match

Compare against oracle:

```text
work mode
scopes
risk triggers
required gate set
conditional gates activated
dynamic escalations
specialist ownership
blocker class
re-review set
Reviewer decision
Final Pre-PR decision
```

## May Differ

Allowed runtime differences:

```text
parallel vs sequential execution
model provider
agent process/session model
skill discovery path
hook mechanism
MCP usage
transport format
cost
latency
```

## Portability Failure

Examples:

```text
OMP adapter skips Security because swarm node unavailable
Claude adapter treats QA as Validator
Codex adapter changes blocker precedence
Cursor adapter omits Detail Analyst
OpenCode adapter cannot carry re-entry context and silently drops it
```

These are semantic failures.

## Runtime Efficiency Metrics

Later collect:

```text
total wall-clock time
agent invocations
token use
model cost
context duplication
failed tool calls
handoff retry count
```

These optimize the adapter.

They must not alter semantic correctness.

## Oh My Pi Evaluation

OMP is a natural candidate for DAG execution.

Evaluate:

```text
fan-out correctness
fan-in correctness
typed handoff preservation
dynamic node activation
remediation wave creation
model routing independence
failure propagation
```

The OMP workflow definition should be generated/projected from portable policy.

It must not become the source of truth.

## Sequential Runtime Evaluation

If a runtime does not support parallel subagents:

```text
execute DAG topologically
```

Semantic score should remain equal.

Only latency differs.
