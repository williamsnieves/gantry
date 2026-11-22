# Final Pre-PR Gate

## Purpose

Provide the final portable harness transition:

```text
reviewed change
→ allowed / not allowed to proceed to PR creation
```

The final gate verifies execution integrity.

## The gate is computed

```text
python3 .harness/bin/route.py ready --runtime <runtime>
```

It reads the routing plan and the results recorded with `route.py gate`, and applies the rules below to the current content of the change: a required gate with no result, a stale result, a changed report, or a blocking decision gives `PRE_PR_BLOCKED`. The agent does not declare the outcome.

It does not replace Reviewer.

## Inputs

Required:

```text
current change identity
final routing plan
gate-result set
Reviewer report
condition ledger
waiver/risk-acceptance ledger
dynamic-trigger ledger
Validator evidence
```

Optional:

```text
PR metadata draft
release notes
deployment notes
```

PR metadata is not required for engineering readiness unless project policy says otherwise.

## Final Decisions

Use exactly:

```text
PRE_PR_PASS
PRE_PR_PASS_WITH_CONDITIONS
PRE_PR_FAIL
PRE_PR_BLOCKED
```

## PRE_PR_PASS

Require all:

```text
Reviewer = READY_FOR_PRE_PR_GATE
all REQUIRED routed gates present
all required results fresh
no unresolved dynamic trigger
no pending decision/evidence
Validator evidence current
change identity matches reviewed state
no invalid waiver
```

## PRE_PR_PASS_WITH_CONDITIONS

Require:

```text
Reviewer = READY_FOR_PRE_PR_GATE_WITH_CONDITIONS
```

and every condition is:

```text
explicitly non-blocking for PR
owned
verifiable
not expired
not contradicted by another gate
```

The final report must carry conditions forward.

## PRE_PR_FAIL

Use when:

```text
Reviewer = NOT_READY_CHANGES_REQUIRED
```

or a final integrity check reveals a proven change-required blocker.

This means:

```text
remediation required
```

not merely missing information.

## PRE_PR_BLOCKED

Use when:

```text
Reviewer = BLOCKED_PENDING_DECISION
Reviewer = BLOCKED_PENDING_EVIDENCE
required gate missing/stale
dynamic trigger unresolved
change identity mismatch
required final evidence unavailable
```

## Final Integrity Checks

### 1. Identity

```text
current change identity
==
Reviewer-reviewed identity
```

or a documented safe derivative with freshness proof.

### 2. Routing Completeness

Every:

```text
REQUIRED
```

gate must be terminal.

### 3. Dynamic Routing Completeness

Every dynamically activated gate must be resolved.

### 4. Reviewer Consistency

Final gate must not contradict Reviewer.

It may only become stricter if final integrity evidence is missing/stale.

### 5. Validator Freshness

Required mechanical evidence must cover the current identity.

### 6. Conditions

Carry every valid condition forward.

Do not silently drop them.

### 7. Waivers

Require explicit authority/scope.

Do not turn specialist FAIL into PASS.

### 8. Artifacts

Required harness artifacts/reports must be available or referenced.

## Final Report

Use:

```text
templates/final-pre-pr-report.template.md
```

## Output Envelope

Recommended:

```yaml
pre_pr_flow_version:
change_identity:
decision:
reviewer_decision:
required_gates:
conditions:
residual_risks:
waivers:
final_checks:
pr_creation_allowed:
```

`pr_creation_allowed`:

```text
true
```

only for:

```text
PRE_PR_PASS
PRE_PR_PASS_WITH_CONDITIONS
```

unless external project policy further restricts it.

## Runtime Adapter

Adapters may map:

```text
PRE_PR_PASS
→ enable/create PR action
```

but the portable core does not create the PR.

## Post-Gate Mutation

If files/config/tests change after final gate:

```text
final gate becomes stale
```

Return to routing/invalidation logic.

No silent post-gate edits.
