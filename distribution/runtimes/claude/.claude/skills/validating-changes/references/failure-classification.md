# Failure Classification

Classify a failing check only when evidence supports the conclusion.

## Introduced

Evidence shows the current change caused the failure.

Actions:

- correct within scope when authorized;
- rerun the affected check;
- rerun downstream checks invalidated by the fix.

## Pre-Existing

The same failure exists on the chosen baseline or is supported by reliable prior evidence.

Actions:

- preserve comparison evidence;
- do not repair unrelated work unless requested;
- report whether it blocks project policy.

## Environmental

The failure results from unavailable services, credentials, permissions, platform dependencies, resource limits, or setup.

Actions:

- record exact requirement;
- distinguish environment failure from code failure;
- identify what must run elsewhere.

## Flaky

Use only when repeated execution or established project evidence demonstrates nondeterminism.

Do not label an unexplained failure flaky after a single rerun.

## Unknown

Use when evidence cannot establish ownership.

Actions:

- gather minimal additional evidence;
- avoid false attribution;
- report residual risk.

## Comparison Safety

Do not discard the user's working tree or overwrite changes to construct a baseline.
