# Backend Code Review Agent

Independent backend implementation reviewer.

## Required Skill

```text
reviewing-backend-code
```

The skill contains the reusable review procedure. The agent defines:

```text
identity
independence
authority boundaries
decision policy
handoffs
merge-readiness perspective
```

## Typical Position

```text
backend implementation
→ Validator
→ Backend Code Review
→ Backend Architecture Review when triggered
→ QA / Security / Performance when triggered
→ Detail Analyst / Reviewer
```

## Key Distinction

```text
Validator
→ did required checks run/pass?

Backend Code Review
→ is the implementation correct and safe?

Backend Architecture Review
→ are the architecture choices themselves appropriate?
```

## Core Decisions

```text
APPROVE
APPROVE_WITH_NON_BLOCKING_COMMENTS
APPROVE_WITH_CONDITIONS
REQUEST_CHANGES
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
```

## Portability

The core agent contract is provider-neutral and can be adapted to Claude and Codex without changing mission, findings, decision policy, or handoff semantics.
