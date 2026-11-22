# Authoring Guide

## Capability Boundary

Define one coherent capability with a verifiable result.

Do not use a skill for:

- repository-wide constraints;
- general agent roles;
- long-form canonical documentation;
- broad lifecycle orchestration;
- deterministic checks better implemented in tooling.

## Frontmatter

The `name` must match the directory and use lowercase letters, numbers, and hyphens.

The `description` must state:

- what the skill does;
- when it should activate;
- when it should not activate if confusion is likely.

## Runtime Content

Keep only the information required during execution:

- activation boundaries;
- required inputs and context;
- primary procedure;
- decision branches;
- validation;
- failure handling;
- output;
- completion criteria.

Move authoring explanations, detailed methodologies, and evaluation guidance out of `SKILL.md`.

## Context Review

Before publishing, identify:

- content always loaded;
- content loaded conditionally;
- content used only during authoring;
- content used only during evaluation;
- duplicated or removable content.

Every paragraph in `SKILL.md` should change execution behavior.
