---
name: analyzing-details
description: Performs a meticulous, traceable analysis of a specific software change, specification, design, task plan, or implementation to detect omissions, inconsistencies, incomplete propagation, boundary mistakes, and overlooked operational details. Use when the main direction is accepted but completeness must be challenged. Do not use for broad code audits, hostile exploit-oriented review, mechanical validation, or implementation.
---

# Analyzing Details

## Purpose

Inspect a bounded software artifact or change at high resolution to identify missing details, mismatched assumptions, incomplete propagation, and small inconsistencies that could become implementation, review, release, or maintenance defects.

## Use When

- A specification, design, task plan, pull request, or implementation needs a completeness review.
- The main solution is accepted, but edge behavior and propagation must be checked.
- A change crosses multiple layers, files, workspaces, contracts, or lifecycle states.
- Reviewers suspect omissions rather than a fundamentally wrong approach.

## Do Not Use When

- The task is a broad repository health audit.
- The task is to aggressively falsify security or reliability guarantees.
- The task is only to run lint, tests, type checks, or builds.
- The task is to implement missing work.
- The task is to invent requirements that were never approved.

## Inputs

- Target artifact, diff, change, design, task plan, or implementation.
- Original request, accepted specifications, acceptance criteria, or OpenSpec artifacts.
- Applicable `AGENTS.md`.
- Relevant interfaces, schemas, tests, documentation, configuration, and operational context.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Establish the authoritative intent and expected outcome.
3. Define the exact analysis boundary.
4. Inspect the target and every directly affected contract or artifact.
5. Trace only dependencies that can materially change completeness.
6. Separate confirmed omissions, inconsistencies, observations, and open questions.
7. Do not modify files.

## Workflow

1. **Anchor:** Identify the authoritative request, specification, and expected result.
2. **Inventory:** Enumerate affected artifacts, layers, actors, states, data, and interfaces.
3. **Trace propagation:** Follow each requirement and decision through dependent artifacts and implementation surfaces.
4. **Inspect boundaries:** Examine validation, empty states, errors, retries, permissions, lifecycle, compatibility, and cleanup.
5. **Compare representations:** Check whether request, specs, design, tasks, code, tests, configuration, and documentation agree.
6. **Find omissions:** Detect expected elements that are missing, partial, or left implicit.
7. **Find inconsistencies:** Detect contradictions, naming drift, incompatible assumptions, and stale references.
8. **Assess materiality:** Distinguish release-impacting gaps from minor observations.
9. **Recommend correction:** Define the smallest required update and where it belongs.
10. **Report:** Produce a detail-analysis report with coverage, findings, questions, and readiness.

## Decision Points

```text
If a detail is required by an authoritative source but absent:
    report an omission.
If two authoritative representations disagree:
    report an inconsistency and identify the decision needed.
If the detail is merely a possible enhancement:
    record it as an observation, not a defect.
If the expected behavior is not defined:
    record an open question; do not invent it.
If hostile failure analysis is needed:
    route to reviewing-adversarially.
If repository-wide risk assessment is needed:
    route to auditing-code.
```

## Finding Requirements

Every actionable finding must include:

- stable identifier;
- type;
- materiality;
- confidence;
- authoritative expectation;
- affected artifact or location;
- observed state;
- missing or inconsistent detail;
- consequence;
- smallest correction;
- verification approach.

## Output

Use `assets/detail-analysis-report.md`.

## Completion Criteria

- [ ] Authoritative intent and scope are explicit.
- [ ] Affected surfaces were inventoried.
- [ ] Requirements and decisions were traced through dependent artifacts.
- [ ] Relevant boundary and lifecycle details were inspected.
- [ ] Omissions and inconsistencies satisfy the evidence contract.
- [ ] Questions and optional observations are separated from defects.
- [ ] Corrections and verification are actionable.
- [ ] Readiness and limitations are explicit.

## References

- Read `references/analysis-framing.md` before defining the review boundary.
- Read `references/propagation-tracing.md` while following requirements and decisions.
- Read `references/detail-dimensions.md` for domain-specific completeness prompts.
- Read `references/omission-and-inconsistency.md` when classifying findings.
- Read `references/materiality-and-readiness.md` before producing the verdict.
- Read `references/artifact-specific-checks.md` only for the artifact types present.
