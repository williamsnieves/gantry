---
name: writing-skills
description: Use when creating a new agent skill, revising an existing skill, investigating unreliable skill activation, reducing skill context usage, or verifying a skill before adoption.
...
---

# Writing Skills

## Purpose

Create or revise one bounded, discoverable, context-efficient, and evaluated agent skill.

## Use When

- A reusable capability needs a new skill.
- An existing skill triggers incorrectly or is difficult to follow.
- A skill needs progressive disclosure, validation, or regression coverage.
- An external skill is being adapted after its adoption review.

## Do Not Use When

- The content is a repository-wide rule, agent role, canonical document, workflow, loop, or deterministic check.
- The request is only to execute an existing skill.

## Required Inputs

- Capability or observed failure.
- Intended triggers and exclusions.
- Target platforms and models.
- Applicable `AGENTS.md` and skill standards.
- Existing skill files when revising.

## Workflow

1. **Classify:** Confirm the artifact belongs in a skill and define one coherent capability.
2. **RED:** Create a baseline evaluation that exposes the missing behavior, unreliable discovery, or current failure.
3. **Design:** Define triggers, exclusions, inputs, procedure, evidence, output, and completion criteria.
4. **GREEN:** Write the smallest skill that makes the failing case pass.
5. **Disclose progressively:** Keep runtime-critical guidance in `SKILL.md`; move conditional methodology to `references/`, substantial formats to `assets/`, deterministic operations to `scripts/`, and tests to `evals/`.
6. **Evaluate:** Test positive, negative, and ambiguous discovery; procedure branches; missing context; failures; safety; output quality; and context efficiency.
7. **REFACTOR:** Remove duplication and obvious explanation, close demonstrated gaps, and rerun the full evaluation set.
8. **Report:** Record evidence, unresolved limitations, compatibility notes, and production-readiness status.

## Validation

The skill is valid only when:

- frontmatter and directory names match;
- discovery cases pass;
- every meaningful procedure branch is tested;
- validation evidence is required before completion;
- irrelevant references are not loaded;
- known regressions pass;
- platform assumptions are explicit.

Do not mark a skill production-ready without a failing baseline or documented equivalent evidence, followed by passing evaluations.

## Output

Use `assets/skill-authoring-report.md`.

## Completion Criteria

- [ ] Capability boundary is correct.
- [ ] Baseline failure is recorded.
- [ ] Runtime instructions are concise.
- [ ] Progressive disclosure is applied.
- [ ] Evaluation cases pass.
- [ ] Safety and portability are reviewed.
- [ ] Final status and remaining risks are recorded.

## References

- Read `references/authoring-methodology.md` when creating or substantially restructuring a skill.
- Read `references/discovery-and-frontmatter.md` when naming, writing descriptions, or debugging activation.
- Read `references/progressive-disclosure.md` when organizing files or reducing context.
- Read `references/testing-methodology.md` before creating or changing evaluation cases.
- Read `references/discipline-skills.md` only for skills that enforce non-negotiable behavior.
