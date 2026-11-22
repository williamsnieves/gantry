# Validator Agent

Independent mechanical validation gate for software changes.

## Role

The agent discovers and runs the checks required by the repository, classifies failures, and returns a strict gate decision.

It does not:

- design tests;
- perform code review;
- audit architecture;
- invent commands;
- weaken validation;
- fix unrelated failures.

## Required Skill

Install or make available:

```text
validating-changes
```

The agent's `AGENT.md` defines identity, boundaries, handoffs, and decision policy. The skill defines the detailed validation procedure.

## Typical Position

```text
implementation
→ validator
→ adversarial/detail review
→ documentation
→ completion or pull request
```
