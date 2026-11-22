# Check Order and Scope

## Iteration Versus Completion

During implementation, prefer the smallest relevant checks that provide fast feedback.

Before completion, run every required check defined by project policy.

## Typical Dependency-Aware Order

Use only when supported by project configuration:

1. generated artifact or schema preparation;
2. format verification;
3. linting;
4. static analysis or type checking;
5. targeted tests;
6. broader tests;
7. build or packaging;
8. end-to-end or external-service checks;
9. project-specific final verification.

## Scope

Determine:

- changed files;
- affected package or workspace;
- dependency impact;
- shared libraries;
- application boundaries;
- cross-cutting contracts.

Use repository-native affected commands when available.

## Full-Repository Checks

Run full checks when:

- project policy requires them;
- shared contracts changed;
- affected scope cannot be established safely;
- targeted checks pass but integration risk remains material.

Do not use narrow scope to avoid a mandatory gate.
