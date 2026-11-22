---
name: enriching-user-stories
description: Analyzes and enriches incomplete software user stories, tickets, feature requests, or change descriptions with implementation-relevant context, acceptance criteria, constraints, risks, and open questions. Use before specification or planning when the input may be ambiguous or incomplete. Do not use to invent product decisions or implement the change.
---

# Enriching User Stories

## Purpose

Turn an incomplete software change request into a clearer, implementation-oriented input while preserving the original intent and exposing unresolved decisions.

## Use When

- A ticket, story, feature request, or change description lacks implementation-relevant detail.
- Acceptance criteria are vague, incomplete, or untestable.
- The request must be prepared for specification-driven development.
- Missing context, constraints, dependencies, or non-functional requirements may block planning.

## Do Not Use When

- The request is already an accepted specification and only needs implementation.
- The task is to explore an OpenSpec change; use the OpenSpec exploration capability.
- The task is to make product decisions without an authorized decision-maker.
- The task is to review code or validate an implementation.

## Inputs

- Original story, ticket, or change request.
- Available project context, specifications, architecture, and applicable `AGENTS.md`.
- Optional external ticket source when explicitly available.
- Optional scope, product constraints, and known decisions.

## Required Context

1. Preserve the original request verbatim or by a faithful reference.
2. Read the nearest applicable `AGENTS.md`.
3. Inspect only the project documentation needed to evaluate the request.
4. Distinguish confirmed facts from assumptions and unresolved decisions.
5. Do not require an external tracker when the user already provided the request content.

## Workflow

1. **Acquire:** Identify the authoritative request source and confirm that its content is available.
2. **Understand:** Summarize the problem, intended outcome, actors, and affected behavior.
3. **Assess:** Evaluate completeness using the readiness dimensions.
4. **Classify gaps:** Separate blockers, non-blocking clarifications, assumptions, risks, and out-of-scope discoveries.
5. **Enrich:** Produce the smallest complete enhancement supported by available evidence.
6. **Define acceptance:** Add observable acceptance criteria and relevant failure or edge cases.
7. **Check readiness:** Assign a readiness status and explain what remains unresolved.
8. **Report:** Preserve the original, provide the enhanced version, and expose every assumption or open question.

## Decision Points

```text
If the original request content is unavailable:
    stop and request the content or an available source.
Else if a product or architecture decision is required and unsupported:
    record it as a blocking open question; do not invent it.
Else if the missing detail can be discovered from canonical project sources:
    retrieve and cite that context.
Else:
    enrich with confirmed information and mark remaining uncertainty explicitly.
```

## Validation

Verify that:

- the enhanced version preserves the original intent;
- no unsupported product or architecture decision is presented as fact;
- acceptance criteria are observable;
- blockers and assumptions are explicit;
- relevant testing, documentation, security, performance, and operational impacts are considered;
- the readiness decision matches the unresolved gaps.

## Output

Use `assets/enriched-story-template.md`.

## Completion Criteria

- [ ] Original input is preserved.
- [ ] Problem and intended outcome are clear.
- [ ] Relevant readiness dimensions were assessed.
- [ ] Acceptance criteria are testable.
- [ ] Facts, assumptions, risks, and questions are separated.
- [ ] No decision was fabricated.
- [ ] Readiness status and next action are explicit.

## References

- Read `references/readiness-dimensions.md` while assessing completeness.
- Read `references/gap-classification.md` when classifying missing information.
- Read `references/acceptance-criteria.md` when creating or repairing acceptance criteria.
- Read `references/context-retrieval.md` only when project context must be discovered.
