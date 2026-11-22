# Reviewer Agent Inputs

Reviewer is primarily an integration agent.

It does not need a new specialist review skill.

## Consumed Agent Outputs

```text
Validator
Detail Analyst
Backend Code Review
Backend Architecture Review
Frontend Code Review
Frontend Architecture Review
QA
Performance
Security
Infrastructure
```

## Supporting Generic Skills

When available, Reviewer may use narrowly:

```text
analyzing-details
reviewing-adversarially
```

only to challenge integration consistency, not to redo specialist reviews.

## Important Rule

```text
Reviewer
≠
another code/security/QA/architecture review
```

Its reusable procedure is the gate integration contract contained in `AGENT.md` and `references/`.
