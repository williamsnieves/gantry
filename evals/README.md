# Scenario runner

Runs the harness against a real agent runtime and scores what the agent decided. Use it to get a baseline before changing skills, contracts or routing, and to compare after.

```bash
python3 evals/run.py --runtime claude                              # all scenarios, one trial each
python3 evals/run.py --runtime claude --scenario small-frontend    # one scenario
python3 evals/run.py --runtime claude --trials 3                   # consistency across repeated runs
python3 evals/run.py --runtime claude --dry-run                    # build sandboxes, call nothing
python3 evals/run.py --rescore evals/results/<run>                 # re-score saved plans, call nothing
```

The first measurement is recorded in [BASELINE.md](BASELINE.md).

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

- Scenarios 07 to 12 (dynamic escalation, remediation loops, stale gates, conditions, missing evidence, portability). They need a multi-step run with specialist agents, not a single routing decision.
- Whether the gates, once routed, find real defects.
- Other runtimes. Adding one means adding a driver function to `DRIVERS` in `run.py`.

## Tests

```bash
python3 tests/test_eval_scoring.py
```

Covers the scorer and checks that every case maps to a loadable oracle. It does not call any runtime.
