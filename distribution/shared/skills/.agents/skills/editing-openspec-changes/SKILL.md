---
name: editing-openspec-changes
description: Revises an active OpenSpec change when new information, implementation feedback, scope refinement, or corrected decisions require updates to its planning artifacts. Use when the same underlying intent remains valid. Do not use when the intent fundamentally changes, a new independent scope emerges, the change only needs specification synchronization, or implementation is the primary task.
...
---

# Editing OpenSpec Changes

## Purpose

Update an active OpenSpec change as a coherent living plan while preserving intent, propagating consequences across dependent artifacts, and detecting when the work should become a new change instead.

## Use When

- A proposal, specification, design, task list, or custom artifact needs revision.
- Implementation revealed a mistaken assumption or missing task.
- Scope is being narrowed or clarified without changing the underlying goal.
- A technical approach changes while the intended outcome remains the same.
- Code and change artifacts have drifted and the correct direction must be determined.

## Do Not Use When

- The problem or intent has fundamentally changed.
- The new work can complete independently from the active change.
- The request is to create a new change.
- The request is only to merge delta specs into main specs.
- The request is primarily to implement tasks or verify completed implementation.
- The change is ready only for archival.

## Inputs

- Active change identifier or path.
- Requested revision or newly discovered evidence.
- Current OpenSpec configuration and artifact dependency graph.
- Existing change artifacts.
- Relevant implementation, tests, and project documentation when drift is involved.
- Applicable `AGENTS.md`.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Inspect the entire active change, not only the named artifact.
3. Inspect project OpenSpec configuration, schema, templates, context, and rules.
4. Identify completed and incomplete implementation tasks.
5. Inspect code only when the requested revision depends on implementation reality.
6. Preserve a distinction between confirmed changes, proposed revisions, and unresolved decisions.

## Workflow

1. **Understand the revision:** State what changed, why, and the supporting evidence.
2. **Classify update versus new change:** Confirm the underlying intent remains the same.
3. **Assess impact:** Identify every artifact, capability, task, and implementation area affected.
4. **Choose the source of truth:** When code and artifacts disagree, determine which reflects the approved desired behavior.
5. **Edit the primary artifact:** Make the smallest coherent revision.
6. **Propagate consequences:** Update all dependent artifacts and task ordering.
7. **Reconcile implementation state:** Preserve valid completed work, reopen or add tasks when required, and record obsolete work.
8. **Validate:** Run OpenSpec status, inspection, validation, and verification when available.
9. **Report:** Document changed artifacts, implementation impact, readiness, and any recommendation for a new change.

## Decision Points

```text
If the intent or problem has fundamentally changed:
    stop and recommend creating a new change.
Else if the new scope can complete independently:
    recommend a separate change and preserve the current one.
Else if the same goal is being refined:
    edit the active change in place.
If code and artifacts disagree:
    determine which side reflects the approved desired behavior before editing either.
If the underlying idea is still unclear:
    return to OpenSpec exploration.
```

## Validation

Verify that:

- the update-versus-new decision is justified;
- the primary revision is supported by evidence;
- every dependent artifact was reviewed;
- proposal, specs, design, tasks, and custom artifacts remain consistent;
- completed task state is still truthful;
- obsolete, new, reordered, or reopened tasks are explicit;
- code/spec drift is reconciled or reported;
- OpenSpec validation succeeds;
- no independent scope is hidden inside the active change.

## Output

Use `assets/openspec-change-edit-report.md`.

## Completion Criteria

- [ ] The same-intent condition is confirmed.
- [ ] Revision evidence is recorded.
- [ ] Impacted artifacts and capabilities are identified.
- [ ] The primary artifact is updated.
- [ ] Dependent artifacts and tasks are reconciled.
- [ ] Implementation drift is handled when relevant.
- [ ] Validation passes.
- [ ] Readiness and next action are explicit.

## References

- Read `references/update-versus-new.md` before deciding whether to edit in place.
- Read `references/artifact-impact-propagation.md` while propagating revisions.
- Read `references/tasks-as-living-plan.md` when task status or ordering changes.
- Read `references/code-artifact-reconciliation.md` when implementation and artifacts disagree.
- Read `references/edit-validation.md` before completion.
