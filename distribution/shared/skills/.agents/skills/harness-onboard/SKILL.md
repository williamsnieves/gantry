---
name: harness-onboard
description: Describe how this project is built so every later run and reviewer starts from the same conventions. Use once after installing the harness, and again when the project's structure or stack changes. In an existing project it reads the code and records its conventions; in a new one it settles them with the user.
---

# Harness Onboard

The output is one short file, `docs/conventions.md`. It belongs to the project, not to the harness: the user can edit it, and it stays if the harness is removed.

1. Read `.harness/project.yaml`. It says whether the project is new or existing (`kind`), its stack, its layout and its check commands. If it is missing, ask the user to run `gantry inspect --write` and stop.
2. If `docs/conventions.md` already exists, update it: keep what is still true and what the user wrote, change only what the project contradicts.
3. Follow the section for the project's `kind`, then finish.

## Existing project (`kind: brownfield`)

The code is the authority. Describe what it does; do not propose what it should do.

- Read the documents listed under `docs` in `.harness/project.yaml`. Link to them instead of repeating them.
- For each of the largest directories under `layout`, read two or three representative source files and one test.
- Write only what at least two files show. One file is an instance, not a convention.
- Where the code does two things for the same job, name both under Open questions. Do not pick one.

## New project (`kind: greenfield`)

There is no code to learn from, so the decisions are the user's.

- Ask in one message, and only for what the user has not already said: what is being built and for whom, the constraints (languages the team knows, where it will run, systems it must work with), and whether they have a stack in mind. Five questions at most, each with a proposed default the user can accept with a yes.
- Write the conventions from the answers. Mark a line `(proposed)` when it is your default and the user has not confirmed it.
- Do not create project code in this step unless the user asks. Once the project has its tooling, the user runs `gantry inspect --write` so the check commands are recorded.

## The file

Use these headings, in this order, and stay under 600 words. After each statement about existing code, name a file that shows it, in backticks.

```markdown
# Project conventions

## Structure
Where the files of a new feature go, and what each top-level directory is for.

## Patterns
How a request or user action travels through the code; how errors, validation and data access are done.

## Tests
Where tests live, how they are named, what they replace with doubles, how to run one.

## Do not
What this codebase consistently avoids.

## Open questions
What the code or the user has not settled.
```

## Finish

Run `python3 .harness/bin/conventions.py check` and fix what it reports. Then show the user the file and tell them it is theirs to correct.
