# Edit Validation

## Validation Sequence

1. Inspect consolidated change state.
2. Confirm artifact dependency completion.
3. Review the final diff across the entire change.
4. Validate OpenSpec syntax and structure.
5. Verify implementation coherence when code exists.
6. Confirm task status truthfulness.
7. Review update-versus-new decision again after the final scope is visible.

## Completion States

### Ready to Continue Implementation

- artifacts are coherent;
- validation passes;
- next incomplete task is clear;
- no blocking decision remains.

### Conditionally Ready

- artifacts are coherent;
- a bounded non-blocking decision remains explicit;
- implementation can safely continue without fabricating it.

### Not Ready

- validation fails;
- artifact contradictions remain;
- task status is false;
- code/spec truth is unresolved;
- the revision actually requires a new change.

## Evidence

Record:

- edited files;
- rationale;
- status/validation/verification results;
- tasks added, removed, reopened, or reordered;
- readiness and next action.
