# Portable Harness Runtime Invariants

This repository uses the portable Loop Engineering Harness.

Authoritative contracts:

```text
.harness/core/
.harness/agents/
.agents/skills/
```

`.omp/` contains runtime adapters only.

Always preserve these invariants:

- `change size != change risk`.
- Route the smallest complete gate set.
- Never skip a materially REQUIRED gate.
- Main OMP session owns routing, task fan-out, dynamic activation, remediation waves, and fan-in.
- Specialist project agents under `.omp/agents/` do not spawn nested workers.
- All workers in one review wave inspect the same stable change identity.
- Independent read-only gates may run concurrently.
- Missing required evidence is not PASS.
- A specialist blocker cannot be averaged away.
- A dynamic trigger must be resolved before Reviewer.
- After remediation, rerun only materially invalidated gates.
- Reviewer runs after all REQUIRED gates are terminal.
- Only `PRE_PR_PASS` or `PRE_PR_PASS_WITH_CONDITIONS` allows PR transition.
- Any material post-gate edit makes readiness stale.

For meaningful implementation/review/release work, use `/harness-run`.
