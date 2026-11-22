# Brownfield Change Creation

Use when the project predates OpenSpec or main specs do not fully describe relevant existing behavior.

## Rules

- Baseline only the existing behavior needed to express the current change.
- Distinguish current behavior from the desired delta.
- Use code, tests, and accepted documentation as evidence.
- Do not attempt a repository-wide specification migration.
- Record legacy constraints separately from desired requirements.
- Preserve backward compatibility unless the change explicitly modifies it.
- Add tasks for necessary baseline, migration, or compatibility work.

## Blocking Condition

If the current behavior cannot be established sufficiently to write an unambiguous delta, return to exploration.
