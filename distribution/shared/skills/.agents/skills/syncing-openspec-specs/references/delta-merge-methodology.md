# Delta Merge Methodology

## Goal

Produce the complete canonical behavior that should remain after the change.

## Added Behavior

- Insert the new requirement into the correct capability.
- Preserve project ordering and naming conventions.
- Avoid duplicating equivalent existing behavior.
- Include all required scenarios.

## Modified Behavior

- Identify the exact canonical requirement being changed.
- Replace or revise the complete intended requirement context.
- Preserve unaffected scenarios and constraints.
- Do not append a fragment that leaves contradictory old behavior.

## Removed Behavior

- Confirm removal is explicit and approved.
- Remove only the targeted requirement or scenario.
- Review references, dependencies, and compatibility implications.
- Do not remove broader capability content accidentally.

## Renamed Behavior

- Preserve semantics unless the change also modifies them.
- Update identifiers, headings, references, and related scenarios consistently.
- Distinguish pure rename from behavioral modification.

## No-Op or Equivalent Delta

If the main spec already contains equivalent approved behavior:

- do not duplicate it;
- record the delta as already represented;
- verify wording differences do not hide semantic differences.

## Final-State Review

Read the resulting main specification as a standalone source of truth. It must not require the archived delta to be understandable.
