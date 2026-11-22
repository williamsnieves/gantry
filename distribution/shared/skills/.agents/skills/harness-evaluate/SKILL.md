---
name: harness-evaluate
description: Evaluate the Codex adapter against the portable end-to-end harness oracle, including routing, dynamic escalation, blockers, handoffs, re-review, Reviewer, final pre-PR semantics, and runtime efficiency.
---

# Evaluate Codex Harness Adapter

Use `.harness/evals/end-to-end/` as the oracle.

Compare semantic outcomes, not wording:

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

Record separately: wall-clock time, subagent invocations, tokens, approvals, tool failures, and handoff retries.

Never trade away Required Gate Recall, Blocker Preservation, Re-Review Recall, Stale Gate Detection, or Final Decision Accuracy for speed.
