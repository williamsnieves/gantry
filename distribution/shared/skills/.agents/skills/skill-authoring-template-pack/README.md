# Skill Authoring Template Pack

This package applies progressive disclosure to skill authoring.

## Runtime Layer

`SKILL.md` is the only file loaded when the skill is activated. Keep it concise and operational.

## Conditional Knowledge

Files in `references/` are loaded only when a specific workflow branch requires them.

## Output Assets

Files in `assets/` define substantial output structures without increasing the runtime instructions.

## Evaluation Layer

Files in `evals/` are used to test discovery, procedure, edge cases, output quality, and regressions. They are not part of normal skill execution.

## Authoring Flow

1. Copy this package into the new skill directory.
2. Rename the directory and update frontmatter.
3. Define the capability boundary.
4. Keep the primary workflow in `SKILL.md`.
5. Move detailed methodologies into conditional references.
6. Move substantial output formats into assets.
7. Add evaluation cases.
8. Delete unused placeholder files and sections.
9. Review against the Agent Skills Authoring Standard.
