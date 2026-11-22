# Portable Harness Baseline Evaluation

## Result

**PASS — contract-level end-to-end consistency.**

This is a semantic/design baseline, not a live runtime benchmark.

- Scenarios evaluated: 12
- Contract-consistent scenarios: 12
- Safety-critical failures: 0

## Scenario Results

| Scenario | Result | Terminal expectation | Notes |
|---|---|---|---|
| `small-frontend` | PASS | `PRE_PR_PASS` | Correct minimal frontend gate set; no unnecessary specialist gates. |
| `tiny-multitenant-auth` | PASS | `N/A_STATIC_ROUTE` | Security remains required despite tiny diff size. |
| `fullstack-medium` | PASS | `N/A_STATIC_ROUTE` | Backend/Frontend Code Review + QA route correctly; specialist extras remain trigger-based. |
| `schema-migration` | PASS | `N/A_STATIC_ROUTE` | Architecture + QA + Infrastructure required for mixed-version migration. |
| `architecture-only` | PASS | `N/A_ARCH_ONLY` | Implementation gates correctly omitted; architecture/security skills remain available. |
| `test-only-remediation` | PASS | `N/A_REMEDIATION_ROUTE` | QA + Validator + Reviewer selected without mechanical architecture rerun. |
| `dynamic-security` | PASS | `N/A_DYNAMIC` | Dynamic privacy/security trigger is represented and required before fan-in. |
| `security-remediation-loop` | PASS | `PRE_PR_PASS` | Minimal re-review preserves Code Review + Security + QA + Validator and avoids unrelated reruns. |
| `stale-gate` | PASS | `PRE_PR_BLOCKED` | Stale Security approval is rejected and requires focused re-review. |
| `valid-conditions` | PASS | `PRE_PR_PASS_WITH_CONDITIONS` | Valid non-blocking conditions survive Reviewer and final gate. |
| `local-evidence-block` | PASS | `PRE_PR_BLOCKED` | Independent branches may continue, but missing required QA evidence blocks final transition. |
| `runtime-portability` | PASS_CONTRACT_ONLY | `ADAPTER_PENDING` | Semantic equivalence requirements are defined; live adapters not yet available. |

## What This Baseline Proves

The current portable contracts are internally consistent across classification, routing, handoffs, parallelism constraints, blocker precedence, dynamic activation, remediation/re-review, Reviewer integration, and final pre-PR semantics.

In particular, the baseline preserves the safety invariants:

```text
tiny change ≠ low risk
one specialist blocker ≠ majority approval
stale approval ≠ current approval
missing required evidence ≠ pass
runtime without parallelism ≠ skipped gates
remediation ≠ rerun every agent
```

## What It Does Not Prove Yet

It does not yet prove that a real runtime/model reliably follows these contracts. The next stage must execute the same oracle through the first runtime adapter and measure semantic drift, handoff loss, unnecessary agent activations, re-review inflation, latency, token use, and cost.

## Next Evaluation Target

```text
Claude Code adapter
→ run canonical 12 scenarios
→ compare against E2E oracle
→ measure runtime-specific efficiency
```
