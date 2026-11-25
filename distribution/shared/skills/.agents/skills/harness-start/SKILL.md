---
name: harness-start
description: Start a piece of work the right way for its risk. Use when the user asks for a feature, a fix, a migration or any change to build, before writing code. It settles what is being asked, decides how much must be written down first, and builds it in tested slices that the harness-run review can then judge.
---

# Harness Start

You build; the harness decides how much has to be settled first and checks the result. Small safe changes go straight to code. Risky ones get a specification the user approves.

## 1. Understand

- Read `docs/conventions.md` and `.harness/project.yaml` when they exist. If `docs/conventions.md` is missing, say so once and suggest the `harness-onboard` skill; do not stop for it.
- Read the code the request touches.
- Ask the user only what would change what you build, in one message, five questions at most, each with the answer you would assume. If nothing is unclear, ask nothing.

## 2. Pick the lane

Run `python3 .harness/bin/route.py vocabulary`, choose the work mode and every risk trigger the request causes, then run:

```bash
python3 .harness/bin/route.py lane --work-mode <MODE> --trigger "<DIMENSION>=<what in the request causes it>"
```

Follow the lane it prints. Do not choose a lighter one because the change looks small.

- `DIRECT`: go to step 4.
- `SPEC`: write the specification (step 3), show the user its acceptance criteria, and continue.
- `DESIGN`: write the specification with its `## Design`, show it to the user and wait for their approval before any code.
- `NONE`: nothing is being built; answer or review instead.

## 3. Specify

Write `docs/specs/<short-name>.md` with these headings, under 800 words:

```markdown
# <What changes, in a few words>

## Problem
Who needs what, and why now.

## Behavior
- AC-1: <something a test or a person can observe>
- AC-2: ...

## Out of scope
What a reader might expect and will not get.

## Design
(DESIGN lane only.) What was chosen, what was rejected and why, and how to undo it.

## Slices
1. <a thin end-to-end piece that works on its own> (AC-1)
2. ... (AC-2, AC-3)

## Open questions
None, or what is still undecided.
```

Each slice cuts through every layer it needs and can be reviewed alone; a slice is not "the backend" followed by "the frontend". Then run `python3 .harness/bin/spec.py check docs/specs/<short-name>.md --lane <LANE>` and fix what it reports.

## 4. Build

One slice at a time, in order:

1. Write the test for the slice's criteria and run it. It must fail for the right reason: a test that has never failed proves nothing.
2. Write the code that makes it pass, following `docs/conventions.md`.
3. Run the commands under `checks` in `.harness/project.yaml`. Do not start the next slice with one failing.

In the `DIRECT` lane there are no criteria: change the code, keep the existing tests passing, and add a test when you fix a defect.

If building shows the specification was wrong, change the specification first and tell the user what changed.

## 5. Review

Run the `harness-run` skill. When there is a specification, pass it to the plan with `--behavior-source docs/specs/<short-name>.md`: it is what the reviewers judge the change against.
