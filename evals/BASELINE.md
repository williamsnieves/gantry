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

# What a review reads

Measured on 2026-11-24 with the trace added to `evals/review.py`, on the planted-leak case, one trial. The runtime's default model was `claude-opus-5-5` for this run; the earlier review runs used `claude-fable-5-2`, so its cost ($3.20) and time (508 s) are not comparable with theirs. The defect was found again: six of seven gates demanded changes, and Frontend Code Review passed with conditions.

| Agent | Requests | Largest prompt (tokens) | Prompt tokens, all requests | Files read |
|---|---|---|---|---|
| lead | 21 | 87,827 | 1,081,860 | 0 |
| qa | 8 | 29,513 | 183,668 | 13 |
| detail-analyst | 7 | 39,720 | 167,621 | 21 |
| validator | 7 | 19,436 | 103,704 | 0 (used the shell) |
| reviewer | 4 | 38,718 | 100,599 | 11 |
| security | 4 | 25,235 | 74,574 | 10 |
| frontend-code-review | 4 | 21,935 | 64,524 | 8 |
| backend-code-review | 3 | 16,563 | 37,035 | 6 |

Words read with the Read tool, by kind of file:

| Kind | Words |
|---|---|
| Agent contracts | 13,252 |
| Reports of other gates | 11,871 |
| Project code | 5,260 |
| Skills | 634 |

What this shows:

- The lead is where the tokens go: 60% of all prompt tokens. Every specialist returns its report to the lead, the lead writes it to disk word for word (seven writes of 650 to 1,400 words), and the report then stays in the lead's context, which grew from 24,500 to 87,800 tokens.
- Skills are almost never read. Six of seven specialists read none, although each contract names a skill as its authoritative procedure. The defect was found without them.
- Agent contracts are the largest thing read, two and a half times the project code under review.
- Detail Analyst and Reviewer reread every other gate's report in full.

One trial, one easy defect: this says where the weight is, not what can be removed safely.

# Specialists write their own report

Measured on 2026-11-24, both cases, one trial each, `claude-fable-5-2`. On Claude Code each specialist saves its report under `.harness/runtime/claude/artifacts/` and replies to the lead with the decision, the conditions and the path; the hook confines a specialist to its own report file. The specialist is also told to keep the report proportionate and to omit empty template sections.

| Case | Before | After |
|---|---|---|
| severity-filter-clean (control) | $5.56, 402 s, 6 of 6, `PRE_PR_PASS_WITH_CONDITIONS` | $4.37, 331 s, 6 of 6, `PRE_PR_PASS_WITH_CONDITIONS` |
| severity-filter-tenant-leak | $6.59, 485 s, 7 of 7, `PRE_PR_BLOCKED` | $5.31, 364 s, 7 of 7, `PRE_PR_BLOCKED` |

- Cost fell by about a fifth and wall time by about a fifth to a quarter, with the same verdicts. In the leak case the same six gates named the defect; Frontend Code Review passed with conditions, as before.
- Every report was written by its specialist; the lead wrote none. Reports were 270 to 927 words in the control (3,945 in total) and 633 to 1,263 in the leak case (6,286 in total).
- The lead is still the largest consumer: 18 and 19 requests, 780,691 and 848,608 prompt tokens, with a largest prompt of about 60,000 tokens (87,827 in the earlier instrumented run, which used a different model).
- Agent contracts remain the largest thing read (11,176 and 13,910 words). In the leak case six specialists read the Validator report.

An earlier attempt without the proportionate-report rule was worse than the baseline: $7.23 and $7.72, reports of about 2,400 words each because specialists filled the whole template, and the leak run reached its spending cap before the Reviewer ran. In that attempt the Validator also blocked the control because checks cannot be executed in the sandbox; the eval prompt now tells the lead to pass that limit on to every specialist.

One trial per case. The difference between before and after is within what a second trial could move; it shows the change is not worse, not how much better it is.

# Where the money goes

Read on 2026-11-24 from the traces and billing figures of the two runs above; no new review run.

Share of the bill by kind of token, derived from the usage the runtime reports (a cache read billed at a tenth of an input token, a cache write at 1.25 or 2 times, an output token at 5 times; both runs fit those ratios to within 1%):

| Kind | Control | Leak |
|---|---|---|
| Output tokens, all agents | 36% | 37% |
| Cache writes by specialists (what they read for the first time) | 32% | 33% |
| Cache writes by the lead | 14% | 12% |
| Cache reads, all agents | 18% | 18% |

- The lead is not the main cost. It makes 18 to 19 requests and holds most of the prompt tokens, but nearly all of them are cache reads. Its reads and writes together are about a quarter of the bill. The table of prompt tokens per agent overstates it, because it counts a cached token the same as a new one.
- The lead's request count is structural: one request per specialist that returns (to record the gate), plus the plan and the final gate. Two requests are wasted on reading the diff twice; that is under 1% of the bill.
- The harness adds about 2,400 tokens to the lead's starting context (agent list, rules, `AGENTS.md`), measured by starting a session in the sandbox with and without them. The other 21,700 tokens are the runtime's own. The 110 skills cost nothing at the start: only two are registered with Claude Code.
- Each specialist starts at 6,500 to 8,000 tokens and writes 20,000 to 35,000 tokens to the cache over its run. Agent contracts are about a tenth of that, around 3% of the bill.
- What is left is the number of specialists. A specialist costs roughly $0.50 to $0.75, and in the leak case six of seven reported the same defect.

Output tokens per agent are not available: the stream reports them only partially.

# Stopping at the first stage that does not pass

Measured on 2026-11-24, `claude-fable-5-2`, one trial each. `route.py` now ends `plan` and every `gate` with a `next:` line. Gates run in stages (Validator, the specialists, Detail Analyst, Reviewer), and a finished stage with a gate that did not pass stops the review.

| Case | Before | After |
|---|---|---|
| severity-filter-tenant-leak | $5.31, 364 s, 7 of 7 gates, `PRE_PR_BLOCKED` | $1.17, 104 s, 1 of 7 gates, `PRE_PR_BLOCKED` |
| severity-filter-clean (control) | $4.37, 331 s, 6 of 6, `PRE_PR_PASS_WITH_CONDITIONS` | $4.91, 388 s, 6 of 6, `PRE_PR_PASS_WITH_CONDITIONS` |

- In the leak case the Validator named the defect and demanded changes, the router printed `next: stop`, and the lead went straight to the Final Pre-PR Gate, which listed the six gates not run and why.
- The control is unaffected by design: nothing rejects, so every gate runs. Its cost moved from $4.37 to $4.91 with no change that explains it; that is the spread between two trials of the same case.
- The saving depends on which stage rejects. Here it was the first. A defect that only a specialist sees would still run the Validator and every specialist, and save only Detail Analyst and Reviewer.
- What is given up: the leak case used to return six independent reports of the defect and whatever else those gates noticed. Now those gates run after the fix.

A first run of this change did not stop: the eval prompt still told the lead to run the remaining gates after a rejection, and the lead followed the prompt over the router ($5.90, 7 of 7 gates). The prompt was corrected and the leak case rerun. It shows that the `next:` line is advice the lead can be talked out of, not an enforced limit.
