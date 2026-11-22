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
