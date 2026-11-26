---
name: harness-ship
description: Ship a reviewed change and close the loop on it. Use when the review has passed and the change is about to be merged, released or deployed, and again after it is in production, or when a shipped change is rolled back or causes an incident.
---

# Harness Ship

The review decided whether the change is right. This decides whether it can leave, and writes down what happened when it did. You do not deploy anything the user has not asked you to deploy.

## 1. Before it leaves

```bash
python3 .harness/bin/release.py check --runtime <runtime>
```

- `RELEASE_BLOCKED`: resolve each blocker it lists. A missing rollout is written in the specification, in a `## Rollout` section: the order things are deployed in, how the change is verified in production, and how it is undone. Write only what the project's own files support (its CI, migrations and deployment configuration); ask the user for what they do not show. Editing the specification changes the change: rerun `harness-run` as its step 10 says.
- `RELEASE_READY_WITH_CONDITIONS`: put every condition in the pull request description, unchanged. A condition is for a person to decide; do not resolve it by rewording it.
- `RELEASE_READY`: go on.

The pull request description states what the change does, the conditions, the `pillar:` lines of `route.py ready` unchanged, and the rollout when there is one.

## 2. Merge and deploy

Merging and deploying follow the project's own process. Do them only when the user asks, with the commands in `.harness/project.yaml` or the project's CI. Never skip a check to get a change out.

## 3. After it is out

Verify it the way the rollout says. With no rollout, run the project's checks against what was shipped and confirm the behavior the specification describes. Then record the outcome:

```bash
python3 .harness/bin/release.py record --outcome SHIPPED --change "<pull request or version>"
```

Record `SHIPPED` only for something you or the user saw working in production. If nobody has verified it, say so and record nothing.

## 4. When it goes wrong

A rollback or an incident is recorded with what happened, and with the risk that was not declared when the change was routed, if there was one:

```bash
python3 .harness/bin/release.py record --outcome INCIDENT --change "<reference>" \
  --note "<what users saw, in one sentence>" --missed <DIMENSION>
```

`python3 .harness/bin/route.py vocabulary` lists the dimensions. Leave `--missed` out when every relevant risk was declared and the reviewers still passed it; say that in the note instead.

Then fix it as `REMEDIATION` work with the `harness-start` skill, starting from a test that fails the way production did.

When a missed risk was recorded, run `python3 .harness/bin/learn.py propose` and show the user what it prints. It proposes a rule that routes that risk whenever a later change touches the same code. The user decides the path it applies to and whether to add it; run the `learn.py add` command only with their answer, and never write `docs/learned.md` yourself.

## Rules

- The record states what happened, not what was intended. Do not record an outcome you did not observe.
- `docs/releases.md` is the project's memory of what got past the review. Do not edit earlier lines.
