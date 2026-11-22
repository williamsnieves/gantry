---
name: skill-name
description: Performs [specific capability]. Use when [positive trigger conditions]. Do not use when [negative triggers or adjacent capability].
---

# Skill Title

## Purpose

[State one bounded outcome.]

## Use When

- [Concrete trigger.]
- [Concrete trigger.]

## Do Not Use When

- [Excluded case; use `other-skill` instead.]
- [Case outside this skill's authority or scope.]

## Inputs

- `[required-input]`: [Format and constraints.]
- `[optional-input]`: [Default behavior.]

Do not invent missing required inputs.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Inspect [canonical request, specification, diff, or target artifact].
3. Load only the references required by the selected workflow branch.

## Workflow

1. Establish scope and applicable constraints.
2. Classify the task and select the correct branch.
3. Execute the bounded procedure.
4. Validate the result.
5. Correct failures within scope and re-run validation.
6. Report evidence, blockers, skipped checks, and residual risks.

## Decision Points

```text
If [condition A]:
    follow branch A and read `references/[reference-a].md`.
Else if [condition B]:
    follow branch B and read `references/[reference-b].md`.
Else if required context is missing:
    stop and report the blocker.
Else:
    follow the default procedure.
```

## Validation

The skill MUST verify:

- [Correctness check.]
- [Completeness check.]
- [Consistency or project-native check.]

The skill MUST NOT claim completion when required evidence is missing or validation fails.

## Failure Handling

- Stop before unsafe or unauthorized action.
- Preserve failure evidence.
- Distinguish pre-existing failures from introduced failures.
- Do not weaken checks, fabricate context, or silently expand scope.

## Output

Use `assets/output-template.md` when a structured report is required.

## Completion Criteria

- [ ] The task was within scope.
- [ ] Required context was obtained.
- [ ] The correct branch was executed.
- [ ] Validation passed or blockers were reported.
- [ ] Evidence and residual risks were recorded.

## References

- Read `references/[reference-a].md` only when [condition A].
- Read `references/[reference-b].md` only when [condition B].

## Scripts

- Run `scripts/[script-name]` only when [deterministic operation is required].
