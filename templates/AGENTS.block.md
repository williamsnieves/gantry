<!-- LOOP-ENGINEERING-HARNESS:START -->
# Loop Engineering Harness

This repository uses the portable Loop Engineering Harness.

Authoritative portable contracts:

```text
.harness/core/
.harness/agents/
.harness/evals/
```

Portable Agent Skills:

```text
.agents/skills/
```

Runtime adapters may also install runtime-native agent/rule directories.

Core invariants:

- Classify work mode, scope, and material risk before selecting gates.
- `change size != change risk`.
- Run the smallest complete gate set.
- Never skip a materially REQUIRED specialist gate.
- Keep specialist ownership explicit.
- Review agents do not implement fixes.
- All reviewers in one wave inspect the same stable change identity.
- New material risk becomes a dynamic routing trigger.
- A specialist blocker cannot be averaged away.
- Missing required evidence is not PASS.
- After remediation, rerun only materially invalidated gates.
- Reviewer runs after all REQUIRED specialist gates are terminal.
- Only `PRE_PR_PASS` or `PRE_PR_PASS_WITH_CONDITIONS` permits transition to PR creation.
- Any material post-gate edit invalidates final readiness.

Project harness configuration:

```text
.harness/harness.config.yaml
```
<!-- LOOP-ENGINEERING-HARNESS:END -->
