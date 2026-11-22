# Detail Analyst Readiness Policy

## READY

Use only when:

- authoritative sources agree;
- every materially affected surface is reviewed;
- required propagation is complete;
- no blocking or high-materiality finding remains;
- unresolved observations are optional.

## CONDITIONALLY READY

Use only when:

- remaining details are explicit and non-blocking;
- ownership and follow-up are assigned;
- no undefined behavior must be invented;
- proceeding will not create irreversible rework or unsafe release.

## NOT READY

Use when:

- source truth conflicts;
- requirements are incomplete;
- implementation or task propagation is materially missing;
- migration, compatibility, generated, testing, documentation, or operations work is absent;
- task completion state is false;
- affected scope cannot be established.

## Decision Discipline

The agent must not lower materiality merely to allow progress.

The agent must also avoid blocking on optional polish, future enhancements, or explicitly deferred scope.
