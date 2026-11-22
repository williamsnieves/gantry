---
name: updating-documentation
description: Updates project documentation after an approved software change by identifying affected documentation surfaces, grounding every edit in current code and specifications, removing stale guidance, and validating commands, examples, links, and terminology. Do not use to invent behavior or manually patch generated docs.
...
---

# Updating Documentation

## Purpose

Keep technical and project documentation accurate after approved behavior, architecture, interfaces, configuration, tooling, or operations change.

## Use When

- Implemented or specified behavior makes documentation stale.
- APIs, schemas, commands, configuration, migrations, runbooks, or examples changed.
- A completed change requires documentation before handoff or release.
- Documentation drift must be corrected.

## Do Not Use When

- Behavior or decisions remain unresolved.
- The task is unrelated rewriting or marketing copy.
- The task is review-only.
- A generated file would be edited instead of its source.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Identify the approved source of truth.
3. Discover documentation structure, ownership, generation, and style rules.
4. Inspect current docs before selecting edits.
5. Verify commands, paths, fields, examples, links, and defaults.
6. Leave unrelated documentation unchanged.

## Workflow

1. Understand the approved change.
2. Discover affected documentation surfaces.
3. Classify each as add, modify, remove, deprecate, regenerate, no change, or blocked.
4. Identify audience and purpose.
5. Make the smallest complete grounded edits.
6. Reconcile terminology, links, paths, examples, diagrams, and cross-references.
7. Update generated documentation through its source and native generator.
8. Run applicable documentation validation.
9. Confirm stale guidance is removed and unrelated content is stable.
10. Produce the update report.

## Decision Points

```text
If behavior is not approved:
    stop or route back to specification.
If documentation is generated:
    update its source and regenerate.
If a command or example cannot be verified:
    report it as blocked; do not fabricate it.
If a surface is unaffected:
    leave it unchanged.
```

## Validation

Verify that:

- every edit is evidence-based;
- affected surfaces have terminal outcomes;
- obsolete guidance is removed or deprecated;
- commands and examples are verified;
- links and references are valid;
- generated output matches its source;
- terminology is consistent;
- unrelated rewrites were avoided.

## Output

Use `assets/documentation-update-report.md`.

## Completion Criteria

- [ ] Approved source behavior identified.
- [ ] Documentation impact mapped.
- [ ] Affected docs updated in the correct locations.
- [ ] Examples, commands, links, and references validated.
- [ ] Generated docs handled through their source.
- [ ] Drift removed or deprecated.
- [ ] Validation and residual gaps reported.

## References

- Read `references/documentation-impact-analysis.md` before selecting files.
- Read `references/documentation-standards.md` while editing.
- Read `references/examples-and-command-validation.md` for executable material.
- Read `references/generated-documentation.md` for generated outputs.
- Read `references/documentation-drift-and-removal.md` for stale content.
- Read `references/documentation-validation.md` before completion.
