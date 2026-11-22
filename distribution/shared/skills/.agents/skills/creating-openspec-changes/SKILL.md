---
name: creating-openspec-changes
description: Creates and validates a new OpenSpec change from a clear request or completed exploration handoff. Use when intent, scope, affected capabilities, and material decisions are sufficiently ready to produce the planning artifacts required by the project's configured OpenSpec workflow. Do not use for exploration, editing an active change, implementation, synchronization, or archival.
...
---

# Creating OpenSpec Changes

## Purpose

Create a correctly scaffolded, internally consistent, and validated OpenSpec change using the project's configured schema, profile, artifact dependencies, templates, context, and rules.

## Use When

- An exploration brief recommends creating a new change.
- A sufficiently clear request can proceed directly to OpenSpec planning.
- The project requires proposal, specification, design, task, or custom planning artifacts before implementation.
- The intended work does not belong to an active change.

## Do Not Use When

- The problem or approach still requires investigation.
- The same intent belongs to an active OpenSpec change.
- The request is to revise an existing change.
- The request is to implement, verify, sync, or archive a change.
- OpenSpec adoption or configuration has not been established and the user has not authorized setup work.

## Inputs

- Original or enriched request.
- Optional OpenSpec exploration brief.
- Confirmed intent, scope, exclusions, and affected capabilities.
- Known decisions, constraints, risks, and validation expectations.
- Applicable `AGENTS.md`.
- Project OpenSpec configuration and available commands.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Inspect the current OpenSpec configuration, schema, profile, templates, context, and per-artifact rules.
3. Inspect relevant main specifications and active changes.
4. Confirm that this work requires a new change.
5. Determine artifact dependencies from the configured workflow rather than assuming a fixed sequence.
6. Preserve unresolved decisions explicitly instead of inventing them.

## Workflow

1. **Verify readiness:** Confirm that the input can support change creation.
2. **Discover workflow:** Determine the configured OpenSpec creation path and required artifacts.
3. **Resolve ownership:** Confirm no active change already owns the same intent.
4. **Name the change:** Select a concise, stable, unique change name.
5. **Scaffold officially:** Use the available OpenSpec creation action or CLI scaffolding; do not manually create the change directory.
6. **Create artifacts:** Follow configured dependency order, templates, project context, and per-artifact rules.
7. **Reconcile artifacts:** Ensure proposal, behavioral deltas, design, tasks, and custom artifacts agree.
8. **Validate:** Run available OpenSpec status, inspection, and validation commands.
9. **Review:** Check readiness for implementation and report unresolved items.

## Decision Points

```text
If material intent, scope, or architecture decisions are unresolved:
    stop or return to exploration.
Else if an active change owns the same intent:
    route to editing or continuing that change.
Else if the project uses the core propose path:
    use the configured propose action.
Else if the project uses an expanded or custom workflow:
    scaffold the change and create artifacts in dependency order.
Else:
    inspect available OpenSpec commands and configuration before proceeding.
```

## Validation

Verify that:

- official scaffolding created the change metadata;
- the change name and location follow project conventions;
- every required artifact exists;
- artifact dependency status is complete;
- proposal intent and scope match the input;
- specifications describe behavior and scenarios;
- design records technical decisions and constraints where required;
- tasks are ordered, actionable, and traceable;
- artifacts do not contradict each other or relevant main specs;
- unresolved blockers are explicit;
- OpenSpec validation succeeds.

## Output

Use `assets/openspec-change-creation-report.md`.

## Completion Criteria

- [ ] New-change ownership is confirmed.
- [ ] Official scaffolding was used.
- [ ] Configured artifacts were created in valid dependency order.
- [ ] Project templates, context, and rules were respected.
- [ ] Artifacts are mutually consistent.
- [ ] Validation passed.
- [ ] Remaining decisions and risks are explicit.
- [ ] The change is ready or conditionally ready for implementation review.

## References

- Read `references/workflow-discovery.md` before choosing commands or artifact order.
- Read `references/artifact-authoring.md` while creating planning artifacts.
- Read `references/specification-deltas.md` when writing added, modified, or removed behavior.
- Read `references/task-planning.md` when creating implementation tasks.
- Read `references/readiness-and-validation.md` before completion.
- Read `references/brownfield-change-creation.md` only when main specification coverage is incomplete.
