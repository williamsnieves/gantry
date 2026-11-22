# Task Planning

## Purpose

Tasks make the approved change executable without replacing engineering judgment.

## Qualities

Tasks should be:

- ordered;
- concrete;
- independently checkable where practical;
- traceable to specs or design;
- small enough to show progress;
- broad enough to avoid meaningless microsteps.

## Coverage

Include as relevant:

- implementation;
- tests;
- migrations;
- generated artifacts;
- documentation;
- observability;
- rollout or feature flags;
- security review;
- performance validation;
- cleanup and compatibility work.

## Dependencies

Express ordering when one task depends on another.

Do not mark tasks complete during change creation.

## Avoid

- speculative work outside scope;
- vague tasks such as “implement feature”;
- file-level instructions unsupported by project evidence;
- duplicating acceptance criteria as tasks;
- omitting validation and documentation work.
