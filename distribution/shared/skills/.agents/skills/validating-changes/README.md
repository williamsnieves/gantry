# validating-changes

Runs repository-native mechanical validation for a software change.

## Boundary

This skill confirms whether required checks execute and pass. It does not determine whether tests are meaningful, whether architecture is sound, or whether the code is well designed.

## Typical Checks

- format;
- lint;
- static analysis or type checking;
- tests;
- build;
- schema and generated-artifact consistency;
- project-specific CI gates.

## Core Rules

- Discover commands; never invent them.
- A skipped check is not a pass.
- Preserve evidence.
- Separate introduced, pre-existing, environmental, flaky, and unknown failures.
- Do not fix unrelated failures.
