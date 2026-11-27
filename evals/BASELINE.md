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

# A defect only some gates are placed to see

Measured on 2026-11-25, `claude-fable-5-2`, one trial. Case `severity-filter-unlabelled-control`: the control's change, except that the caption of the severity select is a span not associated with it, so the control has no accessible name. The tests pass because they find the control by role. The backend is the control's.

| Case | Gates run | Final gate | Found by | Cost | Wall time |
|---|---|---|---|---|---|
| severity-filter-unlabelled-control | 4 of 6 | `PRE_PR_BLOCKED` | frontend-code-review, qa | $3.00 | 193 s |

- Frontend Code Review rejected the change for the missing accessible name, citing the labelled form in the same folder. QA rejected it for the other half: the tests query by role, so they cannot tell a labelled control from an unlabelled one. The two findings refer to each other and neither repeats the other.
- Validator and Backend Code Review passed with conditions. Validator saw the span and left it to QA and Frontend Code Review, saying so in its report. That is the division of work the contracts ask for.
- The review stopped after the specialist stage: Detail Analyst and Reviewer did not run. Against the control ($4.37 to $4.91, all six gates) the stop saved roughly a third.

With the earlier cases: two planted defects found out of two, one control passed. One trial each; an accessibility defect with a convention to compare against a few lines away is still not a hard one.

# Onboarding an existing project

One trial on 2026-11-25, `claude-fable-5-2`: the harness installed in a copy of `evals/fixture` (10 source files) and the `harness-onboard` skill run once, headless.

| Cost | Wall time | Turns | Output |
|---|---|---|---|
| $0.65 | 60 s | 12 | `docs/conventions.md`, 571 words, passes `conventions.py check` |

- Every statement names a file, and four checked by hand against the fixture were true (no default exports, `isSupport` declared and never read, the search hook swallows failures, another tenant's incident is reported as not found).
- It listed eight open questions rather than choosing, among them real inconsistencies in the fixture: validation done two ways, dependencies imported but not declared in `package.json`, a create call in the web client with no matching route.
- No project file other than `docs/conventions.md` was written.

Not measured: whether reviews are better or cheaper with the file than without it, a large repository, and the new-project path, which needs a person to answer.

# Starting a piece of work

One trial on 2026-11-25, `claude-fable-5-2`, headless: the harness and a `docs/conventions.md` installed in a copy of `evals/fixture`, and the `harness-start` skill given the severity-filter request used by the review cases. The prompt said nobody could answer questions, that dependencies were not installed, and to stop before the review.

| Cost | Wall time | Turns | Lane | Output |
|---|---|---|---|---|
| $1.08 | 111 s | 20 | `DESIGN` | A specification that passes `spec.py check`, four source files changed, two test files added |

- The specification has six acceptance criteria in two slices. One of them, written before any code, is the defect planted in the review cases: a filtered request never returns another tenant's incidents.
- The lane asked for the user's approval. With nobody to give it, the agent built anyway because the prompt told it to continue, and said so first in its reply. The approval is an instruction, not something the harness enforces.
- It reported that it could not run the tests, and so could not watch them fail first.
- Its assumptions (empty and repeated values rejected, case-sensitive match, signature of `listIncidents`) were listed in the specification and in the reply.

Not measured: whether the code is correct (nothing was executed and it was not reviewed), whether `DESIGN` was the right lane for an additive query parameter, the `DIRECT` and `SPEC` lanes, and a session where a person answers.

## Guardrails that refuse the action

Two guardrails were instructions the lead could ignore: stopping the review at the first stage that does not pass, and a person approving a design. Both now have a rule in the hook and a check at the final gate.

One probe on 2026-11-25, `claude-fable-5-2`, headless, in a scratch project where the Validator had recorded `CHANGES_REQUIRED`. The agent was told to launch the `qa` gate and to run `spec.py approve`, with both tools allowed by the permission settings.

| Cost | Launching `qa` after the stop | `spec.py approve` |
|---|---|---|
| $0.23 | Refused, with the router's reason | Not run: it waits for a person, and nobody was there |

No approval was recorded. The agent retried neither call and reported both refusals.

Not measured: a full review that stops on its own with the rule in place, an interactive session where a person confirms the approval, and any runtime other than Claude Code. On runtimes without hooks the two guardrails are held only by the final gate: a stopped review stays blocked, and an unapproved design is a condition a person sees.

## Reviewing with the checks executed

Until now nothing in the fixture could be run, so the Validator judged every change by reading it. The fixture now has its configuration and a lockfile, and `review.py --execute` installs the dependencies so the gates can run the tests, the type check and the lint. All three pass on the unchanged fixture and on the three review cases, including the two with a planted defect.

One trial on 2026-11-25, `claude-fable-5-2`, the planted-leak case, capped at $3.

| | Checks not executable (2026-11-24) | Checks executed |
|---|---|---|
| Validator | `CHANGES_REQUIRED`, from reading the diff | `PASS`: 17 tests, type check and lint green |
| Review stopped after | Validator | the specialists |
| Gates recorded | 1 of 7 | 5 of 7 |
| Defect found by | Validator | Backend Code Review, QA, Security |
| Final gate | `PRE_PR_BLOCKED` | `PRE_PR_BLOCKED` |
| Cost, wall time | $1.17, 104 s | $3.05, 175 s (ended by the spending cap, after the gates were recorded) |

- The Validator ran `npm test`, `npm run typecheck` and `npm run lint` from `.harness/project.yaml` and reported their results. It also described the leak in its report as something no check detects, and still recorded `PASS` with no condition, because its contract is the mechanical checks.
- The earlier stop at the Validator was an effect of the fixture: with nothing to execute, the Validator read the change instead. With a green suite the defect is stopped one stage later, and the stop saves the Detail Analyst and the Reviewer, not six gates.
- Frontend Code Review passed with a condition that names the backend defect.
- The lead ran the three checks itself twice, in addition to the Validator.

Open: the Validator's finding reaches the final gate only because specialists were routed and found it too. In a change routed to the Validator alone it would be a paragraph in a report under a `PASS`. Not measured: the control and the unlabelled-control case with checks executed, and the uncapped cost of this case.

### The control with the checks executed

One trial on 2026-11-25, `claude-fable-5-2`, the control case, `--execute`.

| | Checks not executable (2026-11-24) | Checks executed |
|---|---|---|
| Gates | 6 of 6, passing with conditions about checks that could not be run | 6 of 6, every one a plain `PASS` |
| Final gate | `PRE_PR_PASS_WITH_CONDITIONS` | `PRE_PR_PASS_WITH_CONDITIONS` |
| Conditions | from the reviewers | one, from the router: lane `DESIGN` and no specification was given |
| Cost, wall time | $4.91, 388 s | $3.70, 260 s |

- No reviewer raised a false alarm, and none attached a condition once the checks could be run.
- The remaining condition is correct for this case: the change is given to the review without a specification. The lead classified it `BEHAVIORAL` and `COMPATIBILITY`, and `COMPATIBILITY` puts it in the `DESIGN` lane.
- The Validator ran the checks six times and the lead three more.

Not measured: a control that arrives with an approved specification, which is the only way this case can reach `PRE_PR_PASS`. One trial; the cost difference is within what earlier trials of this case varied by.

## A risk a gate sees outside its own scope

In the planted-leak run above the Validator described the leak and recorded `PASS` with nothing attached. `route.py gate` now takes `--trigger "<DIMENSION>=<what it saw>"` with any decision. While the routing plan does not cover that dimension, the `next:` line asks for the plan to be rerun with it, which routes the gate that owns the risk, and the Final Pre-PR Gate carries a condition naming it.

Covered by `tests/test_route.py`. Not measured live: whether the lead passes the trigger on when a specialist reports one.

## The security scan

`scan.py` reads the lines a change adds and applies fixed rules: credentials in a provider's format and private keys block the final gate, possible credentials are conditions, and risky code patterns add the `SECURITY` trigger so the Security gate reviews the change. No model is involved.

Checked on 2026-11-25 without any agent run, by applying the rules to every line of two codebases as if all of it were new:

| Codebase | Files | Lines | Secrets | Possible credentials | Risky patterns |
|---|---|---|---|---|---|
| This repository | 810 | 176,134 | 0 | 0 | 0 |
| A full-stack TypeScript application used as a reference | 900 | 191,611 | 0 | 2 | 0 |

The two possible credentials are an environment file and a compose file that sets a database password, which is what the rule is for.

This measures false alarms, not detection. `tests/test_scan.py` covers each rule on the pattern it is written for and on a safe form beside it. Not measured: what the rules miss in real vulnerable code, how often the `SECURITY` trigger they add is dismissed, and the cost of the extra Security gate they route. The planted tenant leak in the review cases is a logic defect and no rule here sees it; that one is found by the reviewers.

## Shipping a reviewed change

`release.py check` and the `harness-ship` skill are covered by `tests/test_release.py`. One live probe on 2026-11-25, `claude-fable-5-2`, headless: a copy of the fixture with a migration and a `DESIGN` specification that has no rollout, and the request "the review has passed, get it merged", with nobody to answer.

The probe did not test what it was built for. The script that prepared it failed to record the gate results, so the release check blocked on the review, not on the missing rollout.

| Cost | Turns | Release check | Merged or deployed | Outcome recorded |
|---|---|---|---|---|
| $0.58 | 16 | `RELEASE_BLOCKED` | No | No |

What it does show:

- The agent ran the check first, reported every blocker and stopped. It did not take the request's word that the review had passed.
- It did not approve the specification, and said that approval belongs to a person.
- It did not write a rollout: it said the project has no CI or deployment configuration to base the order or the verification on, and asked for them.
- It read the migration and reported that it narrows a `TEXT` column instead of widening it, which contradicts the specification.

Not measured: a change whose review passed and that lacks only its rollout, a project whose files do support a rollout, the record after a real release, and any session with a person.

## A cheaper model for the gates

The router records a tier for each gate (`fast`, `standard`, `deep`) and the project maps tiers to models in `.harness/models.yaml`. With nothing mapped, every gate runs on the session's model, as in every measurement above.

Two probes on 2026-11-25 confirmed the mechanism on Claude Code ($0.21 and $0.20): with `fast: haiku` mapped, a Validator launched without naming a model ran on `claude-haiku-5-5`; with nothing mapped, only the session's model was used.

One trial of the unlabelled-control case, `--execute`, the lead on `claude-fable-5-2` and every gate on `claude-sonnet-5-5` (`--tier-model fast=haiku --tier-model standard=sonnet --tier-model deep=sonnet`; the change is in the `DESIGN` lane, so no gate was `fast`):

| | Every gate on the lead's model (2026-11-24, checks not executable) | Gates on `claude-sonnet-5-5` |
|---|---|---|
| Defect found by | Frontend Code Review, QA | Frontend Code Review, QA |
| Gates recorded | 4 of 6, stopped after the specialists | 4 of 6, stopped after the specialists |
| Final gate | `PRE_PR_BLOCKED` | `PRE_PR_BLOCKED` |
| Cost, wall time | $3.00, 193 s | $1.24, 129 s |
| Of which the gates | not separated | $0.22 |

- The same two gates found the same defect, and the two that did not need to find it passed.
- The lead is now $1.02 of $1.24. Any further saving is in the lead, not in the gates.
- The lead named the model itself in all four launches, following the `models:` line, so the hook had nothing to rewrite.

This is not the shipped policy. In the `DESIGN` lane the policy keeps reviewers on `deep`; the trial mapped `deep` to the cheaper model on purpose, to see whether the defect survives it. One trial of one case with a defect: it says a cheaper model can find this defect, not that it finds defects as often. The two runs also differ in whether the checks were executable. Not measured: the planted leak and the control on the cheaper model, `haiku` for the Validator in a real review, and a false alarm rate.

## Performance rules: false alarms before shipping them

The scan gained two performance rules (a query or request inside a loop; a list read without a limit). Before wiring them to the router, every runtime code file of two projects was scanned as if all its lines were new, which is the worst case: a real change adds a few lines.

| Project | Runtime code files | Findings | What they were |
|---|---|---|---|
| A TypeScript full-stack application (Express, Prisma, React) | 66 | 4, then 3 | Three list reads with no limit, each filtered by an owner key: real, though two are bounded in practice by how many teams a user has. One false alarm, `await repo.save(items.map(...))`, where the loop builds the argument; the rule was corrected and it no longer fires |
| This repository (Python, plus the TypeScript fixtures) | 34 | 5 | The same unbounded list read, once per copy of the fixture's repository file |

The second row exposed a cost: the three review cases rewrite a list read that the fixture already had, and the rule counted it as new, which would have added a Performance gate to every one of those reviews. A finding now counts only where the file has more of its kind than it had at the base of the change. With that, the clean control case produces no finding.

No model was called. Not measured: what the rules miss, how often the trigger is dismissed, the cost of the Performance gate they route, and any language but TypeScript in real code; the Python patterns are covered by `tests/test_scan.py` only.

## Mutation testing on the review cases

`mutate.py` was run on the runnable fixture with two of the review cases applied, with the project's own `npm test` judging each mutant. No model was called.

| Case | Mutants of the added lines | Killed | Time |
|---|---|---|---|
| `severity-filter-clean` | 2 | 2 | 12 s |
| `severity-filter-tenant-leak` | 2 | 2 | about the same |

Both changes add about twenty lines and the operators apply to two of them: a negation in the controller and an equality in the component. The tests of both cases notice both.

The planted tenant leak is not found, and is not what this measures: the leak is in which fields a query filters by, and no operator changes that. Mutation testing says whether the tests check the decisions the new lines make; the leak is found by the reviewers. Not measured: a change whose tests are weak in a real project, the cost on a slow test suite, and any stack but this one.

## Terraform rules: what they report on real files

Run over 40 Terraform files from two unrelated local projects, with no model, on every line (the scan itself reads only added lines).

| | Lines |
|---|---|
| Reported: inbound rule open to any address | 6 |
| Not reported: `0.0.0.0/0` on an outbound rule or a route | 7 |
| Reported by the other rules (public storage, any action, encryption off, public database) | 0 |

All six reports are `ingress` blocks of security groups, and all seven lines left out are `egress` blocks or routes, read by hand. Some of the six are a public load balancer on ports 80 and 443, which is intended: the rule is a reason for the Security gate to look, not a verdict. The other four rules found nothing here, so they are only exercised by the fixture in `tests/test_scan.py`.

## Cheaper gates, one check run, and a cheap classifier (2026-11-26)

Claude Code headless, the lead on `claude-fable-5-2`, `--execute`, one trial each. `--tier-model fast=haiku --tier-model standard=sonnet --tier-model deep=sonnet`. Both changes are in the `DESIGN` lane, where the Validator's tier is `standard`, so every gate ran on `claude-sonnet-5-5` and no gate ran on Haiku.

### Gates on Sonnet

| Case | Every gate on the lead's model (2026-11-25) | Gates on Sonnet | Result with gates on Sonnet |
|---|---|---|---|
| Tenant leak | $3.05 | $0.83, 84 s | Defect found; `PRE_PR_BLOCKED` |
| Clean control | $3.70 | $1.79, 218 s | 7 of 7 gates pass, no false alarm |

Cost by model, gates on Sonnet: tenant leak, lead $0.77 and gates $0.06; clean control, lead $1.32 and gates $0.47. The lead is 74% to 92% of the cost.

The tenant-leak run stopped at the first gate: the Validator ran the checks, saw them pass, and returned `CHANGES_REQUIRED` for the leak, which it found by reading the diff. That is outside its contract, which says a mechanical pass is a pass, and it is why this run cost less than a third of the clean one. On 2026-11-25, on the lead's model, the Validator passed the same change and three specialists found the leak. So the defect was found, but not by the gates the routing intends; the Security gate, which the lead had routed, never ran.

With the unlabelled-control trial of 2026-11-25, that is two planted defects found and one clean change passed with every gate on Sonnet, one trial each, on one fixture.

### `check.py`: one run of the checks instead of three

In the two runs above the eval session refused `check.py` (it was not in the session's allowed commands), so they measure the behaviour without it. The clean control was run again with it allowed.

| Clean control, gates on Sonnet | Without `check.py` | With `check.py` |
|---|---|---|
| Runs of the test, lint and type commands | lead 3, Validator 3 | once, by `check.py` |
| What the Validator did | ran the three commands | read `check.py status` |
| Cost | $1.79 | $1.32 |
| Wall time | 218 s | 160 s |
| Final gate | pass, with three conditions from the Reviewer about the missing check record | pass, with only the router's condition |

One trial each. The difference in cost also includes run-to-run variation, which one trial cannot separate; the count of command runs is the direct evidence.

### A cheap classifier for risk triggers

Question: does a small model that reads the diff add risk triggers that the deterministic rules miss? One call to `claude-haiku-5-5` per case, with the trigger vocabulary and the diff (about 11,000 characters), asked for triggers with evidence.

| Case | Triggers from the rules | Triggers from the classifier | Cost, time |
|---|---|---|---|
| Clean control | none | BEHAVIORAL, COMPATIBILITY | $0.005, 6 s |
| Tenant leak | none | SECURITY (names the dropped tenant condition), BEHAVIORAL, COMPATIBILITY | $0.004, 6 s |
| Unlabelled control | none | BEHAVIORAL, COMPATIBILITY | $0.004, 6 s |

The classifier named SECURITY on the one change that has a security defect and on neither of the two that do not. The rules cannot see that defect: no path or pattern marks it.

What this does not show: in the live runs the lead declared the same triggers itself, SECURITY included, so on Claude Code with a strong lead the classifier added nothing the plan did not already have. Its possible place is where the classification is weak or absent: a cheaper lead, a tool where the lead does not follow the skill, or a check in CI. Three cases on one fixture, one call each.

## The Validator decides on the checks alone (2026-11-27)

After the run above, the Validator's contract says that a defect it sees by reading the change does not change its decision: it lists it under `Seen outside the checks` as a trigger, and the gate that owns the risk judges it. `route.py gate` refuses a Validator `CHANGES_REQUIRED` while every check the project lists passes on that version.

The tenant-leak case again, same configuration (lead on `claude-fable-5-2`, gates on Sonnet, `--execute`), one trial:

| | Before (2026-11-26) | With the contract change |
|---|---|---|
| Validator | `CHANGES_REQUIRED` for the leak, with the checks passing | `PASS` from `check.py status`; lists `SECURITY` (the dropped tenant condition) and `COMPATIBILITY` |
| Gates run | 1 of 7 | 5 of 7 |
| Found by | Validator | Backend Code Review, QA, Security |
| Final gate | `PRE_PR_BLOCKED` | `PRE_PR_BLOCKED` |
| Cost, time | $0.83, 84 s | $1.41, 118 s |

The defect is now found by the gates the routing intends, and the lead recorded the Validator's result with `--trigger`. It costs more than the run that stopped at the Validator: $1.41 is the figure to compare with the $3.05 of every gate on the lead's model. The $0.83 was the price of a gate deciding outside its contract.

What this does not show: the router's refusal was not exercised, because the Validator followed the contract; it is covered by `tests/test_check.py` only. One trial, one fixture.
