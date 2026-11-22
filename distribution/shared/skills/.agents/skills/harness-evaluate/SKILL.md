---
name: harness-evaluate
description: Evaluate the current runtime's harness adapter against the canonical portable end-to-end scenarios. Use when testing or qualifying an adapter, checking semantic drift, or comparing one runtime's execution with another.
---

# Harness Evaluate

Use `.harness/evals/end-to-end/` as the semantic oracle.

For each canonical scenario compare semantic outcomes, not wording:

```text
work mode
scope
risk triggers
gate set
dynamic escalations
handoff ownership/completeness
blocking class
re-review set
Reviewer decision
Final Pre-PR decision
```

Record runtime-specific metrics separately:

```text
wall-clock time
agent invocations
tokens
tool failures
permission prompts
handoff retries
```

Never trade away Required Gate Recall, Blocker Preservation, Re-Review Recall, Stale Gate Detection, or Final Decision Accuracy for speed.
