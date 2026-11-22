---
description: Run the portable software-engineering harness for the current change. Use for meaningful implementation, remediation, migration, review, release, or pre-PR work. Classify the change, route only the required specialist gates, preserve dynamic triggers and typed handoffs, use safe parallel review when possible, run targeted remediation/re-review, then integrate through Detail Analyst, Reviewer, and the Final Pre-PR Gate.
---

# Harness Run — Claude Code Adapter

Use the portable contracts in:

```text
.harness/core/routing/
.harness/core/pre-pr/
```

## Execution

1. Establish the current change identity and accepted behavior.
2. Apply the portable change classification and risk-trigger model.
3. Produce/update `.harness/runtime/claude/routing-plan.yaml`.
4. Run Validator first when required.
5. For every routed specialist whose prerequisites are ready:
   - use the matching project subagent in `.claude/agents/`;
   - keep each specialist read-only;
   - give it the same stable change identity/snapshot;
   - pass only bounded authoritative context/evidence.
6. Fan out independent reviews.
7. Record each gate result using the portable gate-result envelope.
8. If a specialist emits a new trigger, update routing and launch the newly required agent.
9. If blockers exist, create a root-cause-aware remediation plan. Do not let review agents implement.
10. After remediation, rerun only invalidated gates plus Validator as required.
11. Run `detail-analyst` after specialist convergence.
12. Run `reviewer` only after all REQUIRED gates are terminal.
13. Apply the portable Final Pre-PR Gate.
14. Never allow PR creation unless terminal state is:
    - `PRE_PR_PASS`, or
    - `PRE_PR_PASS_WITH_CONDITIONS`.

## Claude execution mode

Default:
```text
named subagents through Agent tool
```

If Agent Teams is explicitly enabled and the routed review set benefits from peer communication/coordination, the lead may reuse the same `.claude/agents/*` definitions as teammate types.

Agent Teams is an execution optimization, not the source of routing truth.
