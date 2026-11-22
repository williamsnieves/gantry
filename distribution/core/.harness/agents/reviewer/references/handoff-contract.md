# Reviewer Handoff Contract

Every handoff must include:

- Reviewer integration finding / blocker ID;
- source specialist gate(s);
- source finding/decision IDs;
- current normalized state;
- exact owner;
- required next action;
- exact specialist re-review required;
- Validator rerun requirement;
- re-entry condition to Reviewer.

## To Implementation

Use when a specialist has already proven a code/config/test/infra change is required.

Reviewer does not invent a different fix.

## To Specialist Gate

Use when:

```text
report stale
contradiction
remediation invalidated review
specialist evidence missing
```

Name exact re-review scope.

## To Validator

Use when mechanical evidence must be rerun after remediation.

Do not ask Validator to decide quality/security/architecture.

## To Product / Architecture / Governance

Use when an authoritative decision blocks safe remediation.

## Final Pre-PR Handoff

When ready, provide:

```text
change identity
applicable gate matrix
conditions
residual risk
required final checks
```

Do not create/merge the PR.

## Rule

Avoid:

```text
"rerun reviews"
"fix blockers"
"check everything again"
```

Specify the minimal invalidated gate set.
