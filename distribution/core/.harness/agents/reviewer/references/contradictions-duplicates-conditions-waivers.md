# Contradictions, Duplicates, Conditions, and Waivers

## Contradictions

A contradiction exists when two gates make incompatible factual claims about the same reviewed state.

Examples:

```text
Security:
tenant authorization missing

Code Review:
tenant authorization explicitly verified
```

or:

```text
Infrastructure:
browser E2E never ran

QA:
browser E2E proves focus restoration
```

Do not pick one silently.

Route to evidence owner(s).

## Duplicate Findings

Classify:

```text
SAME_ROOT_CAUSE
SAME_SYMPTOM
DEPENDENT_FINDING
DISTINCT_FINDING
```

Example:

```text
missing tenant authorization
├── code correctness
├── security exploitability
└── QA regression evidence
```

One root cause, three valid specialist responsibilities.

Consolidate the remediation story, not the specialist evidence.

## Conditions

A valid condition is:

```text
explicit
non-blocking now
bounded
owned
verifiable
```

If a specialist marked the issue blocking, Reviewer cannot convert it into a condition.

## Waivers

Require:

```text
authority
scope
reason
duration/review trigger if applicable
```

A waiver does not change facts such as:

```text
control FAIL
test not run
migration irreversible
```

It changes only authorized disposition when policy permits it.
