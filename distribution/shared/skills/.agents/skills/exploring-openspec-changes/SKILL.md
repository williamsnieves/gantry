---
name: exploring-openspec-changes
description: Investigates an unclear or risky software change before an OpenSpec change is created. Use when the problem, scope, current behavior, affected capabilities, or solution trade-offs require codebase and specification discovery. Do not use to create OpenSpec artifacts, edit an active change, or implement code.
...
---

# Exploring OpenSpec Changes

## Purpose

Turn an initial problem or enriched request into an evidence-based OpenSpec exploration brief that supports a decision to create a new change, continue an existing change, or stop without creating artifacts.

## Use When

- The problem is known but the correct solution is not.
- Requirements or scope remain unclear.
- The codebase or existing specifications must be understood first.
- Multiple approaches need comparison against the actual project.
- A proposed change may overlap an active OpenSpec change.
- The work may be larger, smaller, or different from the initial request.

## Do Not Use When

- The desired behavior and approach are already sufficiently clear for change creation.
- The task is to create proposal, specification, design, or task artifacts.
- The task is to edit an existing active change.
- The task is to implement or validate code.
- The task is only to enrich a user story without OpenSpec investigation.

## Inputs

- Original or enriched change context.
- Available acceptance criteria, constraints, questions, and assumptions.
- Applicable `AGENTS.md`.
- Existing OpenSpec configuration, specifications, and active changes.
- Relevant project code and documentation.

## Required Context

1. Preserve the initial request and any enrichment handoff.
2. Read the nearest applicable `AGENTS.md`.
3. Confirm that OpenSpec is present or explicitly intended for the project.
4. Inspect relevant existing specs and active changes before recommending a new change.
5. Inspect only the code and documentation required to answer concrete exploration questions.
6. Separate project evidence, inference, proposed decisions, and open questions.

## Workflow

1. **Frame:** State the problem, desired outcome, known constraints, and unanswered questions.
2. **Discover OpenSpec state:** Locate configuration, relevant specifications, and related active changes.
3. **Inspect current behavior:** Trace the smallest relevant code, data, interfaces, tests, and documentation.
4. **Refine the problem:** Confirm or correct the initial understanding using evidence.
5. **Identify affected capabilities:** Map behavior to existing or new specification capabilities.
6. **Develop options:** Produce viable approaches without prematurely committing to one.
7. **Compare trade-offs:** Evaluate options against project architecture, risk, scope, and verification needs.
8. **Recommend a next action:** Create a new change, continue or edit a related change, explore further, or stop.
9. **Prepare handoff:** Produce the exploration brief without creating OpenSpec artifacts.

## Decision Points

```text
If the request is already clear and no investigation is needed:
    recommend direct handoff to change creation.
Else if a related active change owns the same intent:
    recommend continuing or editing that change.
Else if the problem is unsupported by project evidence:
    report the mismatch and stop or request clarification.
Else if material decisions remain unresolved:
    mark the exploration conditionally ready or not ready.
Else:
    recommend creating a new change and provide the handoff context.
```

## Validation

Verify that:

- current-state claims are grounded in project sources;
- related specs and active changes were considered;
- options are genuinely distinct and viable;
- trade-offs relate to the actual project;
- the recommendation follows from the evidence;
- unresolved decisions remain explicit;
- no OpenSpec artifact or production code was created or modified.

## Output

Use `assets/openspec-exploration-brief.md`.

## Completion Criteria

- [ ] Initial context is preserved.
- [ ] Current behavior is supported by evidence.
- [ ] Relevant specs and active changes are identified.
- [ ] Affected capabilities are mapped.
- [ ] Options and trade-offs are documented when needed.
- [ ] Recommendation and readiness are explicit.
- [ ] Creation handoff inputs are complete enough for the next skill.
- [ ] No OpenSpec artifacts or code were written.

## References

- Read `references/exploration-methodology.md` for the investigation procedure.
- Read `references/openspec-state-discovery.md` when inspecting OpenSpec configuration, specs, and changes.
- Read `references/option-analysis.md` when multiple approaches require comparison.
- Read `references/handoff-readiness.md` before recommending change creation.
- Read `references/brownfield-exploration.md` only when the repository predates OpenSpec or has incomplete specifications.
