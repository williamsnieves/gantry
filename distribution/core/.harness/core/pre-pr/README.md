# Complete Pre-PR Flow

Portable execution policy for the Loop Engineering Harness.

This package completes roadmap stage:

```text
Build complete pre-PR flow
```

It defines:

```text
parallelism
review ordering
blocking semantics
early stop / continuation
dynamic gate activation
re-review loops
Reviewer integration
final pre-PR gate
```

It consumes the existing portable routing/handoff package:

```text
harness-routing-and-handoffs
```

and does not depend on:

```text
Claude Code
Codex
Cursor
OpenCode
Oh My Pi
```

Those runtimes may execute the flow differently but must preserve its semantics.

## Core Flow

```text
Classify / Route
      ↓
Implementation Stable
      ↓
Validator
      ↓
Specialist Review Fan-Out
      ↓
Dynamic Escalations / Handoffs
      ↓
Targeted Remediation Loop
      ↓
Detail Analyst
      ↓
Reviewer
      ↓
Final Pre-PR Gate
```

Not every agent runs for every change.

The router determines applicability.

## Files

- `PRE-PR-FLOW.md` — canonical state machine.
- `PARALLELISM-POLICY.md` — safe fan-out/fan-in rules.
- `REVIEW-ORDERING-POLICY.md` — dependency-aware ordering.
- `BLOCKING-POLICY.md` — stop/continue semantics.
- `RE-REVIEW-POLICY.md` — minimal invalidation and re-entry.
- `FINAL-PRE-PR-GATE.md` — terminal gate contract.
- `references/gate-result-envelope.md`
- `references/execution-state-model.md`
- `templates/pre-pr-run.template.yaml`
- `templates/final-pre-pr-report.template.md`
- `examples/`
- `evals/cases.yaml`

## Important Distinction

```text
Reviewer
→ integrates specialist gate truth

Final Pre-PR Gate
→ checks that the entire harness run is internally complete,
   fresh, traceable, and allowed to transition to PR creation
```

The final gate does not redo Reviewer analysis.
