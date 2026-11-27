# Scenario runner

Runs the harness against a real agent runtime and scores what the agent decided. Use it to get a baseline before changing skills, contracts or routing, and to compare after.

```bash
python3 evals/run.py --runtime claude                              # all scenarios, one trial each
python3 evals/run.py --runtime claude --scenario small-frontend    # one scenario
python3 evals/run.py --runtime claude --trials 3                   # consistency across repeated runs
python3 evals/run.py --runtime claude --dry-run                    # build sandboxes, call nothing
python3 evals/run.py --rescore evals/results/<run>                 # re-score saved plans, call nothing
```

Measurements are recorded in [BASELINE.md](BASELINE.md).

[poc/](poc/README.md) is a protocol, not a script: three products on three stacks (Python, TypeScript, Go) for an agent to build with the harness, each with acceptance criteria the builder does not see.

`python3 evals/context_cost.py --runtime claude` measures what the harness adds to every session before any work starts.

Every live trial calls the agent runtime and costs tokens. `--max-budget-usd` caps each trial.

## What a trial does

1. Copies `evals/fixture/` (a small multi-tenant incident tracker) into a temporary directory.
2. Installs the harness into it with `gantry install` and commits that as the base.
3. Copies the case's `files/` over it, so the change shows up as uncommitted work in `git diff`.
4. Asks the runtime, headless, to use `harness-run` for that change and stop once the routing plan is written.
5. Reads `.harness/runtime/<runtime>/routing-plan.yaml` and scores it.

The runtime runs with only the sandbox's own configuration: no user settings, memory or MCP servers. It may read, search, write and run read-only git commands.

## What is scored

| Measure | Meaning |
|---|---|
| Result | Pass when no required gate is missed, no gate the oracle keeps off is made required, and the work mode matches. |
| Schema | Whether the plan follows `routing-plan.template.yaml`: every key present, every agent classified with a valid state and a reason. |
| Missed required gate | The safety failure. An agent the oracle marks `REQUIRED` was not `REQUIRED`. |
| Unnecessary gate | Over-routing. An agent the oracle marks `NOT_TRIGGERED` or `NOT_APPLICABLE` was `REQUIRED`. |
| Consistency | With `--trials` above 1, how many distinct routing decisions the same scenario produced. |
| Side effects | Files the agent changed other than the routing plan. |
| Cost, turns, time | As reported by the runtime. |

An oracle entry of `CONDITIONAL` accepts any state. `NOT_TRIGGERED` and `NOT_APPLICABLE` are treated as the same outcome.

Results go to `evals/results/<timestamp>-<runtime>/` (not committed): `results.json` plus each routing plan as written.

## Cases

Each directory under `evals/cases/` has a `case.yaml` (the request, in the words a developer would use, and the scenario id) and an optional `files/` overlay. The expected routing is not duplicated here: it comes from the scenario of the same id in `distribution/core/.harness/evals/end-to-end/scenarios/`.

The request never states the work mode, scopes or risk triggers. Classifying the change is part of what is being measured.

## Scope

Covered: the six static-routing scenarios (01 to 06), on Claude Code.

Not covered yet:

- Scenarios 07 to 12 (dynamic escalation, remediation loops, stale gates, conditions, missing evidence, portability). They need a multi-step run with remediation, not a single routing decision.
- Other runtimes. Adding one means adding a driver function to `DRIVERS` in `run.py`.

## Review quality

`run.py` measures which gates are routed. `review.py` measures whether those gates, once run, judge the change correctly.

```bash
python3 evals/review.py --runtime claude                                      # every case, one trial each
python3 evals/review.py --runtime claude --case severity-filter-tenant-leak   # one case
python3 evals/review.py --runtime claude --dry-run                            # build sandboxes, call nothing
python3 evals/review.py --runtime claude --execute                            # install the fixture's dependencies so gates run its checks
python3 evals/review.py --runtime claude --ablate contracts --ablate skills   # the same review with each contract cut to a stub and no skill but harness-run
```

Each directory under `evals/review-cases/` is a change to the fixture. It is either correct (a control, `defect: null`) or carries one planted defect, described in `case.yaml` with the patterns a report must match to count as naming it.

A trial asks the runtime to take the change through `harness-run` up to `route.py ready` without fixing anything. It then reads the gate ledger and the reports.

Without `--execute` nothing in the fixture can be run and the gates judge the change by reading it. With `--execute`, `npm ci` runs once per lockfile into `evals/.cache/` (it needs npm and network access), every sandbox links to that `node_modules`, and the gates may run `npm test`, `npm run typecheck` and `npm run lint`. The planted defects pass all three: they are the kind a green suite does not catch.

| Measure | Meaning |
|---|---|
| Result, defect case | Pass when a gate that demands changes names the defect and the final gate is `PRE_PR_BLOCKED`. |
| Result, control | Pass when no gate demands changes. A gate that does is a false alarm. |
| Gates | Required gates with a result recorded for the current change, out of those routed. A gate that did not run fails the trial. |
| Side effects | Project files changed during a review-only run. |

Naming the defect is decided by a text match on the report. The reports are saved next to `results.json`: read them before trusting a close call.

Each trial also records every event of the run in `<case>-<trial>-trace.jsonl` and prints, per agent, how many requests it made, how full its context got, and how many words it read of each kind of file (agent contracts, skills, harness core, project code, run state), with the heaviest files listed. Use it to decide what to trim: `evals/tracing.py` holds the summary and is covered by the scoring tests.

The sandbox has no dependencies installed, so the agents cannot run tests. The trial measures review by reading, not by execution.

A trial launches one agent per routed gate and costs several times a routing trial.

## Build quality

`review.py` measures the review of a change that already exists. `build.py` measures the change itself: the agent gets a request and the repository, and what it leaves is scored with tests it never saw.

```bash
python3 evals/build.py --runtime claude --arm bare --arm harness   # the same request without and with the harness
python3 evals/build.py --runtime claude --case resolve-incident --trials 2
python3 evals/build.py --solution reference                        # score the cases' own solutions; calls no runtime
python3 evals/build.py --solution naive
```

Each directory under `evals/build-cases/` holds the request (`case.yaml`, with the interface the change must keep), the hidden tests (`hidden/`), a solution that passes all of them (`reference/`) and the files of one that gets the edges wrong (`naive/`). A hidden test whose name starts with `[edge]` covers something the request implies and does not spell out; the others cover what it says.

| Measure | Meaning |
|---|---|
| Said | Hidden tests of what the request says, passed out of those the case has. A test file that does not load counts as all of its tests failed. |
| Edges | The same for the `[edge]` tests. This is where a careful build and a quick one differ. |
| Checks | The project's own tests, type check and lint on what the agent left, before the hidden tests are added. |
| Own tests | Test cases in the test files the agent wrote or changed. |
| Spec | Whether a specification was written under `docs/specs/`. |

In the `harness` arm the request is built with `harness-start` and stops before the review; in the `bare` arm the repository has no harness. Each trial saves its trace and the change it produced next to `results.json`. `--solution` is how the cases check themselves: the reference must pass everything, the naive solution what is said and not every edge. It needs the fixture's dependencies (`npm ci` once, into `evals/.cache/`), so it is not part of CI.

## Tests

```bash
python3 tests/test_eval_scoring.py
```

Covers the scorer and checks that every case maps to a loadable oracle. It does not call any runtime.
