# Proof of concept report: template

Copy this file into the evidence directory, one per product. Fill it from the saved evidence. Leave a cell empty when the evidence does not say; do not fill it from memory.

## Run

| | |
|---|---|
| Product and stack | |
| Date | |
| Gantry version (`gantry --version`) and commit | |
| Runtime and version | |
| Lead model | |
| `.harness/models.yaml` | |
| Install flags | |
| Arms run | harness / harness and control |

## Installation and onboarding

| Step | Result | Notes |
|---|---|---|
| `gantry install` | | files written, anything refused |
| `gantry doctor` | | each finding and whether its `fix:` line was enough |
| `gantry inspect --write` after the first request | | checks listed, checks missing |
| `/harness-onboard` | | questions asked; statements in `docs/conventions.md` that are wrong |

## Per request

One row per request and arm.

| Request | Arm | Lane (expected) | Triggers declared | Gates run: decision | Reruns | Final gate | Checks | Spec: criteria | Questions | Interventions | Cost USD | Minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | |

## Acceptance

One row per request and arm, from the evaluator.

| Request | Arm | Said passed / total | Edges passed / total | Cannot tell |
|---|---|---|---|---|
| | | | | |

## Failed edges

One row per failed edge. "Where it got through" is one of: not in the specification; the gate for that risk was not routed; the gate ran and passed it; the gate found it and the fix was wrong; no harness (bare or control arm).

| Request | Arm | Edge | Risk | Where it got through | Evidence |
|---|---|---|---|---|---|
| | | | | | |

## What the gates found

One row per finding that made a gate return something other than a pass.

| Request | Gate | Finding | Real defect? | In `acceptance.md`? | Fixed? |
|---|---|---|---|---|---|
| | | | | | |

## Friction

One row each time the harness refused something, the builder looped, or the builder misread an instruction.

| Request | What happened (quote the message) | Was the harness right? | How it ended |
|---|---|---|---|
| | | | |

## What was read

| Request | Skills read | Contracts read | Notes |
|---|---|---|---|
| | | | |

## Totals

| | Harness | Control |
|---|---|---|
| Said passed / total | | |
| Edges passed / total | | |
| Defects stopped by a gate before the commit | | n/a |
| Gate findings that were not defects | | n/a |
| Requests that ended blocked | | |
| Operator interventions | | |
| Cost USD | | |
| Hours | | |

## Reading

Answer each in two or three sentences, naming the requests that support it.

1. Did it work from nothing, or into existing code, on this stack? What had to be fixed by hand?
2. Which failed edges would a specification or a gate have been expected to stop, and why did it not?
3. Which gate findings changed the product for the better, and which were noise?
4. Where did the harness cost time without changing the result?
5. What should change in the harness before the next run?
