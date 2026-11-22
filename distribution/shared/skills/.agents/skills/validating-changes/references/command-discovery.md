# Command Discovery

## Sources

Discover commands in this order:

1. applicable `AGENTS.md`;
2. package or build manifests;
3. repository scripts and task runners;
4. CI workflows and required status checks;
5. contributing or development documentation;
6. tool configuration.

## Build a Matrix

Record:

| Check | Command | Source | Scope | Required |
|---|---|---|---|---|

Common categories:

- formatting;
- linting;
- static analysis;
- type checking;
- unit tests;
- integration tests;
- contract tests;
- end-to-end tests;
- build or packaging;
- schema or migration validation;
- generated-code consistency;
- documentation validation;
- security checks required by CI.

## Guardrails

- Do not translate a CI step into a different local command without evidence.
- Do not assume common script names.
- Do not install tools merely because a command is missing.
- Do not run destructive maintenance commands as validation.
