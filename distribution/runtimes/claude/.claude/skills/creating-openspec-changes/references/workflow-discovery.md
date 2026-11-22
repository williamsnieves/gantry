# Workflow Discovery

## Principle

OpenSpec workflows are schema-driven and may differ by project. Do not hardcode one artifact sequence or command set.

## Inspect

Determine:

- project OpenSpec root;
- `openspec/config.yaml` or equivalent configuration;
- selected schema;
- installed profile and available actions;
- artifact definitions;
- dependency graph;
- templates;
- project context;
- per-artifact rules;
- active changes and naming conventions.

## Creation Paths

Common paths include:

- a one-step propose action that creates all planning artifacts;
- an explicit new-change action followed by incremental continuation;
- an explicit new-change action followed by fast-forward creation;
- a customized schema with different artifacts or dependencies.

Use the path actually available in the project.

## Scaffolding Guardrail

Never create a new directory directly under the changes location as a substitute for official scaffolding.

Use the supported OpenSpec action or CLI that initializes the change and its metadata.

After scaffolding, verify:

- the change directory exists;
- change metadata exists;
- the selected schema is correct;
- status inspection recognizes the change.
