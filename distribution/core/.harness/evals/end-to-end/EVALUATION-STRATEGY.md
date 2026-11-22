# End-to-End Evaluation Strategy

## Objective

Test the harness as an orchestrated engineering system.

Do not evaluate only:

```text
prompt quality
individual agent eloquence
number of findings
```

Evaluate:

```text
did the system make the right engineering decisions?
```

## Evaluation Layers

### Layer 1 — Classification

Does the harness correctly identify:

```text
work mode
scope
risk triggers
```

Failure examples:

```text
architecture-only classified as implementation
one-line auth change classified as low-risk because tiny
test-only remediation treated as full production change
```

### Layer 2 — Routing

Does the harness select the smallest complete gate set?

Measure both:

```text
missed required gates
unnecessary gates
```

Both matter.

### Layer 3 — Handoffs

When one agent activates another, does the receiver get:

```text
reason
trigger
scope
source finding
authoritative context
evidence
unknowns
requested action
expected output
re-entry condition
```

### Layer 4 — Execution / Parallelism

Does the harness:

```text
fan out independent read-only reviews
respect prerequisites
avoid reviewing moving targets
avoid skipping gates when runtime lacks parallelism
```

### Layer 5 — Blocking

Does the harness correctly distinguish:

```text
changes required
pending decision
pending evidence
conditions
advisories
not required
```

### Layer 6 — Dynamic Routing

Does new evidence activate new gates?

Example:

```text
Frontend Code Review
→ detects PII analytics
→ Security REQUIRED
```

### Layer 7 — Remediation

Does the system order fixes by dependency?

Preferred:

```text
decision
→ architecture/root cause
→ implementation
→ tests
→ specialist verification
```

### Layer 8 — Re-Review

Does the system re-run only invalidated gates?

Over-rerunning is a quality/cost defect.

Under-rerunning is a safety defect.

### Layer 9 — Reviewer

Does Reviewer:

```text
preserve specialist blockers
detect stale results
detect contradictions
preserve conditions
consolidate root causes
```

without redoing specialist work?

### Layer 10 — Final Pre-PR Gate

Does the run end in the correct terminal state?

```text
PRE_PR_PASS
PRE_PR_PASS_WITH_CONDITIONS
PRE_PR_FAIL
PRE_PR_BLOCKED
```

## Test Modes

### Static Oracle Evaluation

Feed a scenario and inspect the produced plan/result against expected semantics.

### Simulated Multi-Agent Evaluation

Use fixture specialist outputs and test orchestrator transitions.

### Live Runtime Evaluation

Later adapters run actual agents in:

```text
Claude Code
Codex
Cursor
OpenCode
Oh My Pi
```

and compare semantic results against the oracle.

## Determinism

The harness need not produce identical prose.

It must produce equivalent semantics:

```text
gate set
trigger reasons
blocking class
handoff ownership
re-review set
terminal decision
```

## Failure Categories

```text
MISCLASSIFICATION
MISSED_GATE
UNNECESSARY_GATE
BAD_HANDOFF
OWNERSHIP_VIOLATION
UNSAFE_PARALLELISM
WRONG_BLOCKING_CLASS
MISSED_DYNAMIC_TRIGGER
BAD_REMEDIATION_ORDER
UNDER_REREVIEW
OVER_REREVIEW
STALE_GATE_ACCEPTED
BLOCKER_DOWNGRADED
CONDITION_DROPPED
WRONG_FINAL_GATE
RUNTIME_SEMANTIC_DRIFT
```

## Evaluation Rule

A severe safety failure outweighs several efficiency wins.

Examples:

```text
missed Security gate
blocker downgraded
stale gate accepted
PRE_PR_PASS with unresolved blocker
```

are critical harness defects.
