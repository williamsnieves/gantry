# Frontend Code Review Agent

Independent frontend implementation reviewer.

Unlike backend, the current frontend roadmap has no standalone `reviewing-frontend-code` skill.

This agent therefore composes the reusable generic review skills plus focused frontend evidence skills, while keeping:

```text
reviewing-frontend-architecture
```

reserved for the separate Frontend Architecture Review Agent.

## Core Review Modes

```text
auditing-code
reviewing-adversarially
analyzing-details
```

## Conditional Frontend Skills

```text
validating-frontend-architecture
testing-react-components
testing-react-hooks
testing-frontend-adapters
testing-frontend-user-journeys
reviewing-web-accessibility
reviewing-frontend-performance
reviewing-frontend-security
reviewing-frontend-privacy-and-analytics
```

## Role Separation

```text
Validator
→ mechanical checks

Frontend Code Review
→ concrete user/runtime implementation correctness

Frontend Architecture Review
→ ownership, profile, boundaries, proportionality, structural health
```

## Decisions

```text
APPROVE
APPROVE_WITH_NON_BLOCKING_COMMENTS
APPROVE_WITH_CONDITIONS
REQUEST_CHANGES
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
```
