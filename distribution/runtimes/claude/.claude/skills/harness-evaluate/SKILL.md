---
description: Evaluate the Claude Code harness adapter against the canonical portable end-to-end scenarios. Use when testing or qualifying the adapter, checking semantic drift, or comparing Claude Code execution with another runtime.
---

# Evaluate Claude Code Harness Adapter

Use:

```text
.harness/evals/
```

as the semantic oracle.

For each canonical scenario compare:

```text
classification
risk triggers
semantic gate set
dynamic escalations
handoff ownership/completeness
blocking class
re-review set
Reviewer decision
Final Pre-PR decision
```

Do not score wording similarity.

Record runtime-specific metrics separately:

```text
wall-clock time
agent invocations
tokens
tool failures
permission prompts
handoff retries
```

A runtime optimization must never weaken the semantic oracle.
