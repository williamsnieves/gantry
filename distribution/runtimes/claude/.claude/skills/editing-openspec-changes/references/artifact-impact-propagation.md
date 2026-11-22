# Artifact Impact Propagation

A change artifact is editable at any time, but revisions may invalidate dependent artifacts.

## Impact Questions

For every revision, ask:

- Does the proposal scope or rationale change?
- Does behavior change?
- Are capabilities added, modified, removed, or renamed?
- Does the technical direction still support the behavior?
- Do tasks still represent the required work?
- Do validation, migration, documentation, rollout, security, or operations change?
- Does a custom artifact depend on the edited artifact?

## Common Propagation

### Proposal Revision

Review:

- delta specs;
- design;
- tasks;
- scope exclusions.

### Specification Revision

Review:

- design feasibility;
- implementation tasks;
- tests and validation;
- compatibility and migration.

### Design Revision

Review:

- tasks;
- risks;
- operational work;
- specification assumptions accidentally tied to the old design.

### Task Revision

Confirm that tasks still trace to approved specs and design.

## Minimal Coherent Edit

Do not rewrite unrelated content.

Update all material consequences, even when the requested edit names only one file.
