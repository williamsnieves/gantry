# Baseline

First live measurement of the harness, taken before any slimming or enforcement work. Later runs are compared against this.

- Harness: commit `bee4128` (v1 content with the integrity fixes and the Gantry rename).
- Runtime: Claude Code 2.1.330, model `claude-fable-5-2`, no user settings, memory or MCP servers.
- Date: 2026-11-22. One trial per scenario, so nothing here says how repeatable each result is.

| Scenario | Result | Plan follows template | Turns | Cost | Seconds |
|---|---|---|---|---|---|
| small-frontend | pass | yes | 10 | $0.79 | 51 |
| tiny-multitenant-auth | pass | yes | 13 | $0.92 | 66 |
| fullstack-medium | fail: Security made required | yes | 17 | $0.92 | 64 |
| schema-migration | fail: plan is not valid YAML | no | 13 | $1.03 | 83 |
| architecture-only | pass | yes | 14 | $0.98 | 82 |
| test-only-remediation | pass | yes | 9 | $0.77 | 53 |

Totals: 4 of 6 passed, no required gate was missed in any scored plan, $5.40, 398 seconds. Across the six trials the agent read about 1.8 million cached input tokens and wrote about 37,000 output tokens, only to decide which gates apply.

## What the failures show

**schema-migration.** The agent wrote ``evidence: Incident gains required `priority: number`.`` as an unquoted YAML value, which does not parse. The routing decision could not be read at all. A plan that is hand-written YAML can break on any colon in free text.

**fullstack-medium.** The agent required Security because the change adds a query parameter to an endpoint and rewrites the `where` clause of a tenant-scoped query. `RISK-TRIGGER-MODEL.md` lists "multi-tenancy" and "public entry point" as Security triggers, so the agent followed the contract. The scenario oracle says Security is not triggered for a medium full-stack feature with an API change. The contract and its own oracle disagree; this is not clearly an agent error.

## Other observations

- **Trigger entries have no defined shape.** The template shows `risk_triggers: []`. Every plan wrote mappings instead of names, with keys that vary between runs (`trigger`, `triggers`, `evidence`, `source`). The scorer reads the `dimension` key.
- **Scopes drift from the oracle vocabulary.** Two plans listed `SECURITY` as a scope, and one omitted `API_CONTRACT`.
- **No side effects.** No trial changed a file other than the routing plan, and every plan was written to the expected path.

# After the deterministic router

Same six cases, same runtime and model, one trial each, on 2026-11-22. The only change is that the agent classifies the change and `.harness/bin/route.py` computes and writes the plan.

| Measure | Baseline | With router |
|---|---|---|
| Scenarios passed | 4 of 6 | 5 of 6 |
| Plans that follow the template | 5 of 6 | 6 of 6 |
| Required gate missed | 0 | 0 |
| Cost | $5.40 | $3.11 |
| Wall time | 398 s | 167 s |
| Agent turns | 76 | 42 |
| Cached input tokens read | 1.81 million | 0.88 million |
| Output tokens | 37,259 | 12,097 |

All six plans pass `route.py check`. No trial changed a file other than the plan.

**fullstack-medium still fails**, for the same reason: the agent declares a SECURITY trigger for a new query parameter merged into a tenant-scoped `where` clause, and the rules then require Security. The disagreement between the trigger vocabulary and the scenario oracle is now isolated to one classification choice, but it is not resolved.

**Classification still varies.** Scopes were under- or over-declared in four of the six plans (for example `TEST_ONLY` without `FRONTEND`, or `SECURITY` listed as a scope). None of these changed a gate decision in this run.

One trial per scenario is still too few to say how repeatable either column is.

# After moving context to on-demand

Same six cases, runtime and model, one trial each, on 2026-11-22. Changes: Claude agents no longer preload skills, Claude receives only the two entry-point skills, and the always-loaded rules files are a short map.

| Measure | With router | Context on demand |
|---|---|---|
| Scenarios passed | 5 of 6 | 5 of 6 |
| Plans that follow the template | 6 of 6 | 6 of 6 |
| Required gate missed | 0 | 0 |
| Cost | $3.11 | $2.38 |
| Wall time | 167 s | 204 s |
| Cached input tokens read | 0.88 million | 0.75 million |

Wall time went up while turns and tokens went down, so it is most likely variation between runs; one trial each cannot settle that.

Always-on cost, measured with `evals/context_cost.py` (same trivial prompt in a bare and an installed copy of the fixture):

| | Input tokens |
|---|---|
| Bare project | 20,076 |
| Harness installed, before | 30,045 (9,969 added) |
| Harness installed, after | 22,819 (2,743 added) |

Skills preloaded into a Claude specialist before it reads any code, in words: qa 38,262 to 0, frontend-code-review 34,487 to 0, security 22,428 to 0, infrastructure 20,797 to 0. Each agent now lists the same skills by path and reads the ones a change needs. Whether specialists review as well with on-demand skills is not measured: these scenarios stop at routing.

# After narrowing the Security trigger

The trigger vocabulary and the `fullstack-medium` oracle disagreed (see above). The vocabulary was changed: Security is triggered by a change to how access is decided, by something newly exposed, or by newly handled sensitive data, and not merely by code that runs behind authentication or reads tenant-scoped data.

Two trials each of the two cases this affects, on 2026-11-22:

| Scenario | Expected | Trial 1 | Trial 2 |
|---|---|---|---|
| fullstack-medium (new filter on a tenant-scoped list) | Security not required | pass | pass |
| tiny-multitenant-auth (one line relaxing tenant isolation) | Security required | pass | pass |

Both scenarios reached the same routing decision in both trials. The other four cases were not rerun; their last result is 4 of 4 passing, so the expected total is 6 of 6, not yet measured in a single run.

# Review quality, first run

Measured with `evals/review.py` on 2026-11-23, Claude Code, `claude-fable-5-2`, one trial per case. This is the first measurement of what happens after routing: the specialists run, their results are recorded with `route.py gate`, and `route.py ready` computes the final gate.

| Case | Gates run | Final gate | Outcome | Cost | Wall time |
|---|---|---|---|---|---|
| severity-filter-tenant-leak (planted cross-tenant leak) | 7 of 7 | `PRE_PR_BLOCKED` | Defect named by 6 of 7 gates, including Security and QA | $6.59 | 485 s |
| severity-filter-clean (control) | 6 of 6 | `PRE_PR_BLOCKED` | Rejected by QA, Detail Analyst and Reviewer | $6.17 | 537 s |

What this shows:

- The flow works end to end. Every routed gate ran and was recorded, the final gate was computed from the ledger, and no project file was edited in either run.
- The planted defect was found. In the leak case Security was routed and required, because the classifier saw the tenant predicate change; in the control it was not.
- The control was not clean, so its result is not a false-alarm rate. The request said users could filter the list, but the change shipped a control wired to no screen and had no controller or client tests. QA rejected it for exactly that, with the code reviewers passing the same facts as conditions. The control and the request were corrected after this run (scope stated, controller and client tests added) and have not been rerun.
- A full review is expensive: about $6 and 8 to 9 minutes for a six-file change, and about 14,600 words of reports across both runs. In the leak case six gates reported the same defect independently.
- QA noted that its contract cites `references/qa-decision-policy.md`, which is not installed. Seven agent contracts cite `references/` files that do not exist (nine files in total).

Not measured: repeatability, and a subtler defect that only one specialist is placed to see.

## Corrected control

Rerun on 2026-11-24 with the corrected control (scope stated in the request, controller and client tests added), after the dead citations in the agent contracts were removed. One trial.

| Case | Gates run | Final gate | Outcome | Cost | Wall time |
|---|---|---|---|---|---|
| severity-filter-clean (control) | 6 of 6 | `PRE_PR_PASS_WITH_CONDITIONS` | No gate demanded changes | $5.56 | 402 s |

Detail Analyst passed outright. The other five gates passed with conditions, and every condition is the same one: run tests, typecheck and lint where dependencies are installed, because the sandbox cannot. No project file was edited.

With the first run, that is one defect found out of one and one control passed out of one. Two trials show the flow discriminates between these two changes; they are not a detection rate or a false-alarm rate.
