# Code and Artifact Reconciliation

Use when implementation has started or manual code changes caused drift.

## Determine the Approved Truth

### Artifacts Are Correct, Code Drifted

- preserve the artifacts;
- add or reopen implementation tasks;
- fix code later through the implementation workflow.

### Code Is Correct, Artifacts Are Stale

Use only when the code reflects an approved decision or accepted reality.

- update behavioral deltas;
- update design if the technical direction changed;
- update tasks and completion state;
- validate coherence before archival.

### Neither Is Clearly Approved

- stop;
- record the conflict;
- obtain a decision or return to exploration.

## Verification

Use the project's available OpenSpec verification capability when present to identify:

- incomplete tasks;
- behavior mismatch;
- design inconsistency;
- undocumented implementation changes.

Do not silently treat accidental code as the desired specification.
