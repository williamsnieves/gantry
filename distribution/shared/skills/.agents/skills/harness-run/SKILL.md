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

1. Inspect the current change and establish the accepted behavior. `.harness/project.yaml`, when present, describes the project's stack and the commands that check it; pass its path to the specialists instead of rediscovering them. Do the same with `docs/conventions.md` when it exists: it is what the project's own code is judged against. Then run `python3 .harness/bin/mutate.py`; it does nothing unless the project turned mutation testing on. For each `survived:` line, add the test that fails on that change and run it again; a survivor you leave becomes a condition at the final gate.
2. Run `python3 .harness/bin/route.py vocabulary` and classify the change: one work mode, every scope that applies, and every risk trigger the change causes, each with evidence from the change.
3. Run `python3 .harness/bin/route.py plan --runtime <runtime> --work-mode <MODE> --scope <SCOPE> --trigger "<DIMENSION>=<evidence>"`, repeating `--scope` and `--trigger` as needed. It writes `routing-plan.yaml` in the state directory and prints the gates. Never write or edit the plan by hand: rerun the command when the classification or the change itself changes. If it adds a trigger from the changed files, keep it; use `--dismiss "<DIMENSION>=<reason>"` only when it clearly does not apply.
4. Gates run in stages: Validator, then the specialists, then Detail Analyst, then Reviewer. `route.py plan` and every `route.py gate` end with a `next:` line that names the gates to run now; `python3 .harness/bin/route.py next --runtime <runtime>` prints it again. Follow it. When it says `next: stop`, a stage did not pass: do not launch the later gates, go to step 12 and report the blockers, because those gates would judge a change that has to be edited anyway.
5. Launch the matching specialist agent for every routed gate whose prerequisites are ready. When a `models:` line follows `next:`, launch each gate it names on that model. Keep each specialist read-only, give all agents in a wave the same change, and pass only bounded authoritative context and evidence.
6. Run independent read-heavy reviews in parallel where the runtime supports it.
7. Each specialist's report belongs at `artifacts/<agent>-report.md` in the state directory. On Claude Code the specialist saves it itself and replies with its decision, conditions and the path: do not ask it for the report text and do not rewrite the file. On other runtimes, save the report it returns, unchanged. Then record its result: `python3 .harness/bin/route.py gate --runtime <runtime> --agent <agent> --decision <DECISION> --report <report file>`. Map the specialist's own decision to `PASS`, `PASS_WITH_CONDITIONS` (add one `--condition "<text>"` per condition), `CHANGES_REQUIRED` or `BLOCKED` without weakening it.
8. When a specialist reports a risk outside its own scope (a new routing trigger or a handoff to another gate), record it with that gate's result by adding `--trigger "<DIMENSION>=<what it saw>"` to `route.py gate`, even when its decision is `PASS`. If the plan does not cover that risk, the `next:` line says so: rerun `route.py plan` with the trigger added, pass the finding on as a typed handoff, and launch any newly required gate.
9. If remediation is required, return implementation to the parent/authorized worker; specialists remain reviewers.
10. After any edit to the change, rerun `route.py plan`: every recorded result is now stale. Rerun the gates the edit materially invalidates, plus Validator. For a gate the edit cannot have affected, keep its result with `route.py gate --runtime <runtime> --agent <agent> --carry-forward "<why the edit does not affect it>"`.
11. Run `detail-analyst` and then `reviewer` once every other REQUIRED gate has a passing recorded result, and record theirs the same way.
12. Run `python3 .harness/bin/route.py ready --runtime <runtime>`. This is the Final Pre-PR Gate. Create a pull request only when it prints `PRE_PR_PASS` or `PRE_PR_PASS_WITH_CONDITIONS`, and put the conditions and the `pillar:` lines it prints in the pull request description, unchanged. When it prints `PRE_PR_BLOCKED`, resolve each blocker it lists; do not edit the plan or the gate records by hand.

If concurrency is unavailable, run the same gates sequentially. Never reduce the gate set: a review that stopped early stays blocked until every required gate has passed.
