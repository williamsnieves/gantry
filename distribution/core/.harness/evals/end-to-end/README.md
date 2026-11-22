# Harness End-to-End Evaluation

End-to-end evaluation package for the portable Gantry harness.

This package validates the complete system:

```text
classification
→ routing
→ handoffs
→ validation
→ specialist fan-out
→ dynamic escalation
→ remediation
→ targeted re-review
→ Detail Analyst
→ Reviewer
→ Final Pre-PR Gate
```

The goal is not to prove that individual prompts look reasonable.

The goal is to test whether the **whole harness behaves correctly as a system**.

## What Is Evaluated

```text
routing precision
risk-trigger detection
unnecessary-gate avoidance
required-gate recall
handoff completeness
specialist ownership
parallelism safety
blocking semantics
dynamic routing
remediation-loop correctness
minimal re-review
gate freshness
Reviewer aggregation
Final Pre-PR correctness
runtime portability
```

## Runtime Scope

The core evaluation is runtime-neutral.

It can later be executed through:

```text
Claude Code
Codex
Cursor
OpenCode
Oh My Pi
```

Runtime-specific evaluations should compare against the same semantic oracle.

## Pass Philosophy

A harness passes only when:

```text
it activates every materially required gate
+
does not activate expensive unrelated gates mechanically
+
preserves blockers
+
passes enough context through handoffs
+
re-runs only invalidated gates
+
reaches the correct terminal pre-PR decision
```

## Files

- `EVALUATION-STRATEGY.md`
- `METRICS.md`
- `E2E-ORACLE.md`
- `PORTABILITY-EVALUATION.md`
- `templates/run-result.template.yaml`
- `templates/evaluation-report.template.md`
- `scenarios/` — canonical end-to-end fixtures.
- `evals/cases.yaml` — machine-readable evaluation catalogue.

## Canonical Scenarios

1. Tiny low-risk frontend behavior change.
2. One-line multi-tenant authorization change.
3. Full-stack medium-risk feature.
4. Brownfield schema migration with mixed versions.
5. Architecture-only design.
6. Test-only remediation.
7. Dynamic Security escalation from Frontend Code Review.
8. Security blocker → remediation → minimal re-review.
9. Stale gate after post-review code change.
10. Valid non-blocking conditions.
11. Missing evidence while independent branches continue.
12. Runtime portability: same semantics across adapters.

## Important

This package does not yet implement a Claude/Codex/OMP adapter.

It creates the **semantic oracle** those adapters will have to satisfy.
