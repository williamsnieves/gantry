# Proof of concept: three products, three stacks

The measurements in [../BASELINE.md](../BASELINE.md) used small, precise requests on one TypeScript fixture, and every arm passed every case. They cannot say whether the harness helps on the work it was made for: a product built from nothing, from requests written the way a person writes them, on a stack the harness was not developed against.

This document is the protocol for finding out. One agent builds three small products with the harness; a person or a second agent then checks each against criteria the builder never saw.

## What it should answer

1. **Does it work from nothing?** Install, onboard and build in an empty repository, on Python and on TypeScript.
2. **Does it work on code it did not write?** Install into a Go service built without it.
3. **Does a vague request end up right?** Each request hides at least one risk it does not mention. Does the build handle it, and if not, does a gate catch it?
4. **Does the risk reach the right reviewer?** Lane and gates per request, against what the criteria expect.
5. **Does it get in the way?** Every time the harness blocks, loops or confuses the agent, and whether it was right to.
6. **What does it cost?** Money, time and the number of times a person had to step in.
7. **Are the skills ever read?** None was in the build measurement.

## The products

| Product | Stack | Starts as | What it stresses |
|---|---|---|---|
| [Turnos](products/turnos/brief.md): appointment booking API for clinics | Python, FastAPI, SQLite, pytest, ruff, mypy | Empty repository, harness from the first commit | Tenant isolation, concurrency, a migration over existing data, the learning loop |
| [Cuentas claras](products/cuentas-claras/brief.md): shared expenses web app | TypeScript, React front end, Node API, vitest, ESLint | Empty repository, harness from the first commit | Front-end states and accessibility, money arithmetic, a refactoring |
| [Relay](products/relay/brief.md): webhook delivery service | Go, standard library, SQLite | Built **without** the harness, then the harness is installed | Installing into existing code, security of outbound requests, infrastructure |

Each product directory has two files:

- `brief.md`: the requests, in order. This is all the builder sees of the product.
- `acceptance.md`: what each request must end up doing, the lane and gates it should get, and the traps. **The builder must never see it.** Keep the product repositories outside this repository so it is not on the builder's disk path.

## Roles

- **Operator** (a person, or an agent that follows this file): creates the repositories, gives the requests one at a time, answers the builder, saves the evidence.
- **Builder** (the coding agent under test): receives one request per session and nothing else.
- **Evaluator** (a person or a second agent, never the builder's session): after a stage, runs the product and checks `acceptance.md` against its behaviour.

## Rules for the operator

1. **One request, one fresh session.** Paste the request text unchanged. Do not add hints, and do not mention a trap.
2. **Answer questions with the builder's own assumption.** `harness-start` asks with the answer it would assume; reply "use what you assume" to every one. Write down each question.
3. **Approve a design after reading it.** In the `DESIGN` lane the builder waits. Read the specification, approve it as it is, and note what you would have changed.
4. **Never fix anything yourself.** If the builder ends with a failing check or a blocked gate, tell it once "finish it"; if it still ends blocked, record that and move on.
5. **After each request:** the change is committed to `main` and tagged `req-<id>` (ask the builder to commit if it did not; record that you had to). Then copy `.harness/runtime/` and the session transcript into the evidence directory, because the next change overwrites the gate ledger.
6. **Nothing leaves the machine.** No remote, no push, no real credentials or personal data in any product.
7. **Pin the model and say which.** The same lead model for every request of every product. Record the contents of `.harness/models.yaml`.

## Setup

Requirements: `git`, `python3`, Node 20 or later, Go 1.22 or later, `uv` or `pip`, and the agent runtime. Hooks exist only on Claude Code, so run the three products there first; repeating one product on another runtime is a useful second pass.

```bash
GANTRY=/path/to/gantry           # this repository
POC=~/gantry-poc                 # outside this repository
mkdir -p $POC/evidence && cd $POC
```

**Turnos and Cuentas claras** (harness from the first commit):

```bash
mkdir turnos && cd turnos && git init -b main && git commit --allow-empty -m "Start"
$GANTRY/gantry.sh install --runtime claude --stage mvp --scope backend --project .   # --scope fullstack for cuentas-claras
$GANTRY/gantry.sh doctor --project .
git add -A && git commit -m "Install the harness"
```

Then, in the agent, run `/harness-onboard` and answer its questions with the stack named in the brief and its defaults for the rest. Commit `docs/conventions.md`.

The first request creates the project's tooling. After it, run `gantry inspect --write --project .` and commit, so `.harness/project.yaml` lists the checks; the builder cannot edit that file. Record what the harness did during that first request, when no check existed yet.

**Relay** (harness arrives later): create the repository the same way but do not install anything. Give requests C1 to C4 with the bare prompt below. Tag `bare-done`, evaluate stage 1, then:

```bash
$GANTRY/gantry.sh install --runtime claude --stage product --scope backend --project .
$GANTRY/gantry.sh doctor --project .      # record every finding and its fix line
```

Run `/harness-onboard` (it reads the code this time), commit, and continue with C5 onwards.

### Prompts

With the harness:

```text
/harness-start <request text>
```

When it finishes with the review passed, in the same session: `/harness-ship`, then "commit it to main". There is no deployment: record `SHIPPED` once the evaluator has seen the request working.

Without the harness (Relay stage 1, and the control arm):

```text
<request text>
Build this in this repository. Run the tests, lint and type checks before you finish, and commit.
```

To keep cost and a transcript per request on Claude Code, run headless from the product directory:

```bash
claude -p "<prompt>" --model <lead model> --output-format stream-json --verbose > $POC/evidence/<product>/req-<id>.jsonl
```

A headless run cannot be answered. Use it for the bare prompt; for harness requests use an interactive session, or add to the prompt "No one can answer: use your assumptions, and a design you write is approved for this run", and record that you did.

### Control arm (recommended for one product, optional for the rest)

Stage 2 of every product starts from a tagged commit. Branch `control` from that tag and give the same stage 2 requests with the bare prompt. Same starting code, same requests, one arm with the harness and one without: this is the only comparison in the protocol where the harness is the only difference.

## What to record

Fill one row of [REPORT.md](REPORT.md) per request, from the evidence and not from memory:

| Field | Where it comes from |
|---|---|
| Lane, work mode, triggers | `routing-plan.yaml` in the saved `.harness/runtime/` |
| Gates routed, each decision, reruns | `gates.json` in the same directory |
| Final gate | `python3 .harness/bin/route.py ready --runtime claude`, before committing |
| Checks | `python3 .harness/bin/check.py status` |
| Specification written, criteria count | `docs/specs/` at the request's tag |
| Questions asked, design approvals | Operator's notes |
| Skills and contracts read | The transcript: every `Read` of a path under `.agents/skills/` or `.harness/agents/` |
| Cost, time, turns | The runtime's own report (`/cost`, or the last event of the transcript) |
| Operator interventions | Every message other than the request, "use what you assume", an approval, `/harness-ship` and "commit it" |
| Friction | Each time the harness refused, looped or was misread: quote the message, and say whether the refusal was correct |
| Acceptance | The evaluator's result, below |

## Evaluation

After each stage, the evaluator gets the product repository at the stage's tag and that product's `acceptance.md`, in a session that has never seen the build. It starts the product as its README says and checks every item from outside: HTTP requests, the browser, the command line. It does not read the code to decide a result; it may read it afterwards to explain a failure.

Each item is `pass`, `fail` or `cannot tell`, with the command or steps that showed it. Items are of two kinds, as in the build measurement:

- **said**: what the request states.
- **edge**: what the request does not state and a careful engineer would still handle. Each names the risk trigger it belongs to, in the words of `route.py vocabulary`; `no trigger` marks an edge no gate is routed for.

For every failed edge, the report says where it could have been stopped: the specification did not mention it, the gate for that risk was not routed, the gate ran and passed it, or the gate found it and the fix was wrong.

## Reading the result

Decide what the outcomes would mean before running anything:

- **The harness earns its cost** if, in the control comparison, it ships fewer failed edges than the bare arm, or its gates stop defects the bare arm ships; and the operator interventions stay near zero.
- **The harness is neutral** if both arms pass the same items, as in every measurement so far. Then its cost multiple is the result, and the next question is which parts can go.
- **The harness hurts** if the builder ends blocked on a correct change, a gate rejects for something that is not a defect, or a stack makes a step fail (no check detected, a hook that misfires). Each of these is a defect to fix before anything else, and worth more than the scores.

Three products and one run each will not prove any of these; they show where to look. Report counts, never percentages, and name every failed item.

## Cost

No run of this size has been measured. Extrapolating from the fixture (a small request built with the harness cost 0.4 to 1.3 USD, and a full review 1.4 to 3 USD, on the lead model with Sonnet gates), 24 requests land between 50 and 150 USD, and larger requests may exceed that. Run one product first, read its report, and decide on the other two with a real number.
