---
name: harness-run
description: Run the portable software-engineering harness for the current change. Use for meaningful implementation, remediation, migration, review, release, or pre-PR work. Classify the change, route only the required specialist gates, preserve dynamic triggers and typed handoffs, use safe parallel review when possible, run targeted remediation/re-review, then integrate through Detail Analyst, Reviewer, and the Final Pre-PR Gate.
---

# Harness Run

Routing is computed by `.harness/bin/route.py`; you classify the change, it decides the gates. The contracts for what happens after routing are in `.harness/core/pre-pr/` and `.harness/agents/`.

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

1. Inspect the current change and establish the accepted behavior.
2. Run `python3 .harness/bin/route.py vocabulary` and classify the change: one work mode, every scope that applies, and every risk trigger the change causes, each with evidence from the change.
3. Run `python3 .harness/bin/route.py plan --runtime <runtime> --work-mode <MODE> --scope <SCOPE> --trigger "<DIMENSION>=<evidence>"`, repeating `--scope` and `--trigger` as needed. It writes `routing-plan.yaml` in the state directory and prints the gates. Never write or edit the plan by hand: rerun the command when the classification or the change itself changes. If it adds a trigger from the changed files, keep it; use `--dismiss "<DIMENSION>=<reason>"` only when it clearly does not apply.
4. Run Validator first when required.
5. Launch the matching specialist agent for every routed gate whose prerequisites are ready. Keep each specialist read-only, give all agents in a wave the same stable change identity, and pass only bounded authoritative context and evidence.
6. Run independent read-heavy reviews in parallel where the runtime supports it.
7. Preserve every specialist's original decision and gate-result envelope.
8. When a specialist reports a new material trigger, rerun `route.py plan` with that trigger added, pass the finding on as a typed handoff, and launch any newly required gate.
9. Do not run Reviewer until every REQUIRED routed gate is terminal.
10. If remediation is required, return implementation to the parent/authorized worker; specialists remain reviewers.
11. After remediation, rerun only materially invalidated gates plus required Validator checks.
12. Run `detail-analyst`, then `reviewer`.
13. Apply `.harness/core/pre-pr/FINAL-PRE-PR-GATE.md`.
14. PR creation is allowed only for `PRE_PR_PASS` or `PRE_PR_PASS_WITH_CONDITIONS`.

If concurrency is unavailable, execute the same semantic DAG sequentially. Never reduce the gate set.
