# Readiness and Validation

## Validation Sequence

1. Inspect change status.
2. Confirm all required planning artifacts are complete.
3. Run the project's OpenSpec validation command.
4. Inspect the rendered or summarized change.
5. Perform a cross-artifact consistency review.
6. Record unresolved decisions and implementation risks.

## Ready

Use when:

- all required artifacts are complete;
- no blocking decision remains;
- behavioral scope is testable;
- tasks cover implementation and validation;
- validation succeeds.

## Conditionally Ready

Use when implementation may begin but explicit, bounded decisions remain that do not invalidate the core change.

## Not Ready

Use when:

- intent or ownership is unclear;
- required artifacts are missing;
- specs are not testable;
- design conflicts with specs;
- tasks omit material work;
- validation fails.

## Evidence

Record:

- scaffold command or action;
- status output;
- validation command and result;
- created artifacts;
- readiness decision.
