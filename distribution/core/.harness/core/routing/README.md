# Harness Routing and Handoffs

Portable routing layer for the Loop Engineering Harness.

This package answers two questions:

```text
Which agents should run for this change?
```

and:

```text
What exact context/evidence must move between agents?
```

It deliberately does **not** yet define the final global:

```text
parallelism policy
review ordering policy
blocking policy
final pre-PR gate
```

Those are the next roadmap stages.

## Goals

The routing layer must work for:

```text
small changes
medium changes
large changes
frontend-only work
backend-only work
architecture-only work
infrastructure-only work
full-stack work
partial implementation
new projects
brownfield projects
```

and remain portable across:

```text
Claude Code
Codex
Cursor
OpenCode
Oh My Pi
other future runtimes
```

## Core Model

```text
Change
→ classify scope
→ identify risk triggers
→ determine required/conditional gates
→ create routing plan
→ dispatch agents
→ exchange typed handoffs
→ specialist outputs
```

Runtime-specific adapters may execute this plan differently, but they must not change its semantics.

## Files

- `PORTABLE-HARNESS-CONTRACT.md` — invariant core vs runtime adapters.
- `ROUTING-POLICY.md` — routing algorithm and activation semantics.
- `CHANGE-CLASSIFICATION.md` — change scopes and work modes.
- `RISK-TRIGGER-MODEL.md` — risk dimensions and triggers.
- `AGENT-ACTIVATION-MATRIX.md` — when each agent is required/conditional/not applicable.
- `HANDOFF-PROTOCOL.md` — typed context/evidence transfer.
- `GATE-DEPENDENCY-CONTRACT.md` — only the minimum dependency constraints required for valid routing.
- `templates/routing-plan.template.yaml`
- `templates/handoff-envelope.template.yaml`
- `examples/` — representative routing plans.
- `evals/cases.yaml` — routing/handoff evaluation cases.

## Key Principle

```text
change size
≠
change risk
```

A one-line authorization change may activate more gates than a large low-risk UI refactor.

## Portability Principle

```text
Portable Core
→ decides what must happen

Runtime Adapter
→ decides how the selected runtime executes it
```

Never put project engineering policy inside an Oh My Pi, Claude, Codex, Cursor, or OpenCode-specific orchestration file.
