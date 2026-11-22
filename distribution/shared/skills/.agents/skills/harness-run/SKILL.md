---
name: harness-run
description: Run the portable software-engineering harness for the current change. Use for meaningful implementation, remediation, migration, review, release, or pre-PR work. Classify the change, route only the required specialist gates, preserve dynamic triggers and typed handoffs, use safe parallel review when possible, run targeted remediation/re-review, then integrate through Detail Analyst, Reviewer, and the Final Pre-PR Gate.
---

# Harness Run

Portable source of truth:

```text
.harness/core/routing/
.harness/core/pre-pr/
.harness/agents/
```

## Runtime mapping

Use the specialist agents and state directory of the runtime you are running in:

| Runtime | Specialist agents | State directory |
|---|---|---|
| Claude Code | `.claude/agents/*.md` | `.harness/runtime/claude/` |
| Codex | `.codex/agents/*.toml` | `.harness/runtime/codex/` |
| Cursor | `.cursor/agents/*.md` | `.harness/runtime/cursor/` |
| OpenCode | `.opencode/agents/*.md` | `.harness/runtime/opencode/` |
| Oh My Pi | `.omp/agents/*.md` | `.harness/runtime/omp/` |

## Execution

1. Establish the current change identity and accepted behavior.
2. Apply the portable change classification, risk-trigger, and routing contracts.
3. Write/update `routing-plan.yaml` in the state directory, following `.harness/core/routing/templates/routing-plan.template.yaml`.
4. Run Validator first when required.
5. Launch the matching specialist agent for every routed gate whose prerequisites are ready. Keep each specialist read-only, give all agents in a wave the same stable change identity, and pass only bounded authoritative context and evidence.
6. Run independent read-heavy reviews in parallel where the runtime supports it.
7. Preserve every specialist's original decision and gate-result envelope.
8. Convert new material findings into dynamic routing triggers and typed handoffs, and launch any newly required gate.
9. Do not run Reviewer until every REQUIRED routed gate is terminal.
10. If remediation is required, return implementation to the parent/authorized worker; specialists remain reviewers.
11. After remediation, rerun only materially invalidated gates plus required Validator checks.
12. Run `detail-analyst`, then `reviewer`.
13. Apply `.harness/core/pre-pr/FINAL-PRE-PR-GATE.md`.
14. PR creation is allowed only for `PRE_PR_PASS` or `PRE_PR_PASS_WITH_CONDITIONS`.

If concurrency is unavailable, execute the same semantic DAG sequentially. Never reduce the gate set.
