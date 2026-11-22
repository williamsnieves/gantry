---
name: harness-run
description: Run the portable software-engineering harness for meaningful implementation, remediation, migration, review, release, or pre-PR work. Classify scope and risk, route only required specialist gates, delegate independent reviews to Codex subagents, preserve handoffs and dynamic triggers, perform targeted re-review, then integrate through Detail Analyst, Reviewer, and Final Pre-PR.
---

# Harness Run — Codex Adapter

Portable source of truth:

```text
.harness/core/routing/
.harness/core/pre-pr/
.harness/agents/
```

1. Establish change identity and accepted behavior.
2. Apply portable classification, risk, and routing contracts.
3. Write/update `.harness/runtime/codex/routing-plan.yaml`.
4. Run Validator first when required.
5. Spawn matching `.codex/agents/*.toml` specialists whose prerequisites are ready.
6. Delegate independent read-heavy reviews in parallel where useful; all agents in a wave inspect the same stable change identity.
7. Preserve every specialist's original decision and gate-result envelope.
8. Convert new material findings into dynamic routing triggers and typed handoffs.
9. Do not run Reviewer until every REQUIRED routed gate is terminal.
10. If remediation is required, return implementation to the parent/authorized worker; specialists remain reviewers.
11. After remediation, rerun only materially invalidated gates plus required Validator checks.
12. Run `detail-analyst`, then `reviewer`.
13. Apply `.harness/core/pre-pr/FINAL-PRE-PR-GATE.md`.
14. PR creation is allowed only for `PRE_PR_PASS` or `PRE_PR_PASS_WITH_CONDITIONS`.

If concurrency is unavailable, execute the same semantic DAG sequentially. Never reduce the gate set.
