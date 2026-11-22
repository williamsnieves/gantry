# Documentation Impact Analysis

Map changed concepts to affected documentation without broad rewriting.

## Common Impacts

- Behavior → guides, examples, troubleshooting, screenshots.
- Interface/schema → API reference, clients, migration notes.
- Architecture → diagrams, ownership, data flow, decisions.
- Tooling/workflow → setup, commands, CI, contribution guides.
- Configuration/operations → environment reference, deployment, runbooks, rollback.

Inspect changed files, documentation indexes, references to renamed identifiers, generator configuration, CI checks, and ownership metadata.

Use:

| Changed Concept | Documentation Surface | Action | Evidence |
|---|---|---|---|

Actions: Add, Modify, Remove, Deprecate, Regenerate, No change, Blocked.

No affected surface should disappear silently.
