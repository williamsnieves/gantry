---
name: syncing-openspec-specs
description: Reconciles an active or completed OpenSpec change's delta specifications with the project's main specifications. Use when approved added, modified, removed, or renamed behavior must be reflected in the canonical spec set before or during archival. Do not use to create or edit the change, implement code, validate test quality, or archive the change itself.
---

# Syncing OpenSpec Specs

## Purpose

Apply approved specification deltas from an OpenSpec change to the canonical main specifications without losing unrelated behavior, duplicating requirements, or hiding unresolved conflicts.

## Use When

- A change contains specification deltas that must update the main specs.
- The project requires spec synchronization before archival.
- Main specs and change specs have drifted during implementation.
- A completed change must leave canonical behavior documentation accurate.

## Do Not Use When

- The change intent, design, or tasks still require editing.
- The request is to create a new change.
- The request is to implement or validate code.
- The request is to archive the change after synchronization.
- No approved specification delta exists.

## Inputs

- Active or completed change identifier.
- Change delta specifications.
- Current main specifications.
- OpenSpec configuration, schema, profile, and available sync commands.
- Applicable `AGENTS.md`.
- Optional implementation evidence when spec truth is disputed.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Inspect the entire change and its current validation state.
3. Inspect the relevant main specifications before applying any delta.
4. Determine the supported sync action or CLI from project configuration.
5. Confirm that each delta is approved and still represents the desired behavior.
6. Identify concurrent or previously synchronized changes affecting the same capability.

## Workflow

1. **Verify preconditions:** Confirm the change and its deltas are valid enough to synchronize.
2. **Discover sync behavior:** Determine project-specific commands, schema rules, and archival expectations.
3. **Map capabilities:** Match each change delta to its canonical main specification.
4. **Classify operations:** Identify added, modified, removed, renamed, unchanged, and conflicting behavior.
5. **Preview merge:** Determine the resulting canonical requirements before writing.
6. **Resolve conflicts:** Preserve unrelated behavior and stop when approved truth is unclear.
7. **Apply synchronization:** Use the supported OpenSpec sync action or perform the schema-compliant merge.
8. **Validate main specs:** Run OpenSpec validation and inspect the resulting canonical specification set.
9. **Verify traceability:** Confirm every approved delta was applied exactly once.
10. **Report:** Record changed specs, conflicts, evidence, and archival readiness.

## Decision Points

```text
If the change artifacts or delta specs are invalid:
    return to editing the active change.
Else if a delta conflicts with a newer approved main-spec change:
    stop and resolve the source of truth.
Else if a delta was already synchronized:
    do not duplicate it; verify equivalence and record no-op status.
Else if the project provides an official sync action:
    use it and inspect the resulting diff.
Else:
    apply the configured schema semantics manually and validate.
```

## Validation

Verify that:

- every synchronized delta maps to the correct capability;
- added behavior appears once;
- modified behavior replaces the intended requirement without losing unrelated scenarios;
- removed behavior is absent only where approved;
- renamed behavior preserves semantics and references;
- unaffected main-spec content remains unchanged;
- no unresolved conflict is silently merged;
- the resulting main specs validate;
- the change remains traceable to the canonical result.

## Output

Use `assets/openspec-sync-report.md`.

## Completion Criteria

- [ ] Preconditions are satisfied.
- [ ] Every delta is classified and mapped.
- [ ] Conflicts and already-synced behavior are handled explicitly.
- [ ] Canonical specs contain the intended resulting behavior.
- [ ] Unrelated behavior is preserved.
- [ ] Validation passes.
- [ ] Traceability is recorded.
- [ ] Archival readiness is reported without archiving.

## References

- Read `references/sync-preconditions.md` before modifying main specs.
- Read `references/delta-merge-methodology.md` while applying added, modified, removed, or renamed behavior.
- Read `references/conflict-resolution.md` when main specs and deltas disagree.
- Read `references/traceability-and-idempotency.md` before completion.
- Read `references/sync-validation.md` for the final validation sequence.
