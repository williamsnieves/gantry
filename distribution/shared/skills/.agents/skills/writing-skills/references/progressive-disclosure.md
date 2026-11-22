# Progressive Disclosure

## Loading Model

- Metadata is used for discovery.
- `SKILL.md` is loaded after activation.
- Additional files are loaded only when needed.
- Scripts may execute without their source being loaded into context.
- Evaluation files never belong in normal runtime context.

## Placement Rules

Keep in `SKILL.md`:

- core procedure;
- decision boundaries;
- validation;
- output;
- completion criteria.

Move to `references/`:

- conditional methodologies;
- large standards;
- domain-specific branches;
- detailed examples.

Move to `assets/`:

- substantial report formats;
- schemas;
- templates used as output material.

Move to `scripts/`:

- fragile, repetitive, deterministic operations.

Move to `evals/`:

- prompts;
- fixtures;
- expected outputs;
- run records.

## Navigation

- Link every reference directly from `SKILL.md`.
- State when each reference should be read.
- Avoid reference-to-reference chains.
- Add a contents section to long references.
- Keep `SKILL.md` below 500 lines and preferably far smaller for frequently used skills.

## Context Audit

Record:

- always-loaded content;
- conditionally loaded content;
- executable content;
- evaluation-only content;
- unnecessary content to remove.
