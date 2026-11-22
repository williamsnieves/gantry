# Discovery and Frontmatter

## Frontmatter

Use only the portable required fields:

```yaml
---
name: skill-name
description: Use when [concrete triggers, symptoms, artifacts, or lifecycle conditions].
---
```

## Name

The name must:

- match the directory;
- use lowercase letters, numbers, and hyphens;
- remain under platform limits;
- describe the activity;
- avoid vague names;
- avoid reserved vendor terms.

Prefer consistent action-oriented or gerund naming.

## Description

The description exists for discovery.

It should:

- be written in third person;
- state when the skill applies;
- include realistic trigger vocabulary;
- describe symptoms or context rather than implementation steps;
- distinguish adjacent capabilities;
- remain concise.

Do not summarize the workflow in the description. A workflow summary can become a shortcut that causes the agent to skip `SKILL.md`.

## Evaluation

Test discovery independently with:

- direct positive prompts;
- implicit positive prompts;
- near-match negatives;
- adjacent-skill negatives;
- ambiguous prompts requiring material context.

Treat false activation and missed activation as separate failures.
