# Sync Validation

## Validation Sequence

1. Inspect the main-spec diff.
2. Confirm delta-to-main coverage.
3. Run OpenSpec validation.
4. Re-open or render affected main specs.
5. Search for duplicate or contradictory requirements.
6. Confirm unaffected content remains stable.
7. Check that change artifacts still explain the synchronized result.
8. Report archival readiness.

## Ready for Archival

Use when:

- all approved deltas have terminal results;
- main specs validate;
- no unresolved conflict remains;
- implementation verification requirements are satisfied according to project policy;
- the change can be understood historically after archival.

## Not Ready

Use when:

- validation fails;
- a delta is missing;
- requirements are duplicated;
- modified behavior remains contradictory;
- approved truth is unresolved;
- the active change still requires editing.

## Evidence

Record:

- sync command or action;
- affected main specs;
- final diff;
- validation result;
- delta coverage matrix;
- readiness decision.
