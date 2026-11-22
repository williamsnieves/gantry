# Conflict Resolution

A conflict exists when the delta and current main spec cannot both be applied without ambiguity or contradiction.

## Common Causes

- another change already modified the same requirement;
- the main spec evolved after the active change was created;
- implementation feedback changed the approved outcome;
- duplicate capabilities describe overlapping behavior;
- a removal targets behavior now required elsewhere;
- renamed requirements have diverged.

## Resolution Sequence

1. Identify the conflicting requirements and their provenance.
2. Determine chronological and approval context.
3. Inspect related active and archived changes.
4. Establish the currently approved desired behavior.
5. Update the active change when its delta is stale.
6. Re-run synchronization only after the conflict is resolved.

## Prohibited Resolution

Do not:

- concatenate contradictory requirements;
- prefer the newest text without checking approval;
- delete unrelated main-spec behavior;
- silently reinterpret a modified delta;
- use implementation accident as authority.

## Escalation

If approved truth remains unclear, stop and report the exact decision required.
