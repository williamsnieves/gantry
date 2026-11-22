---
name: auditing-code
description: Performs a systematic, evidence-based audit of a codebase, subsystem, or change across correctness, security, type safety, performance, maintainability, dependencies, and dead-code risk. Use for pre-release audits, technical-debt assessments, legacy-system reviews, or focused quality investigations. Do not use for routine mechanical validation, implementation, or speculative style commentary.
...
---

# Auditing Code

## Purpose

Produce a prioritized, reproducible audit of software risks and improvement opportunities without confusing tool output, preferences, or unsupported suspicion with confirmed defects.

## Use When

- A subsystem or repository needs a structured quality audit.
- A release or migration requires broader risk assessment.
- Technical debt must be identified and prioritized.
- Security, performance, correctness, type safety, dependencies, or dead-code risk require investigation.
- A brownfield project needs an evidence-based health assessment.

## Do Not Use When

- The task is only to run format, lint, tests, or builds.
- The task is to implement fixes.
- The task is a narrow adversarial review of a specific diff.
- The task is only to locate dead code.
- The request is primarily architecture design rather than audit.

## Inputs

- Audit target and boundaries.
- Applicable `AGENTS.md`.
- Relevant source, tests, manifests, configuration, documentation, and CI.
- Optional change diff, release criteria, threat model, or risk priorities.
- Optional runtime or production evidence.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Define included and excluded scope before scanning.
3. Discover the project architecture, runtime boundaries, and native tooling.
4. Inspect existing validation evidence before reproducing checks.
5. Separate confirmed findings, probable risks, observations, and questions.
6. Do not modify code unless the user separately authorizes remediation.

## Workflow

1. **Scope and baseline:** Define goals, boundaries, critical paths, and available evidence.
2. **Architecture and flow:** Understand entry points, trust boundaries, data flow, ownership, and failure paths.
3. **Correctness and type safety:** Inspect invariants, error handling, state transitions, concurrency, contracts, and unsafe typing.
4. **Security and dependency risk:** Inspect authorization, validation, secrets, injection, exposure, dependency use, and unsafe defaults.
5. **Performance and resource behavior:** Inspect algorithmic cost, I/O, queries, caching, memory, lifecycle, and backpressure.
6. **Maintainability and dead-code risk:** Inspect complexity, duplication, obsolete paths, unused dependencies, coupling, testability, and documentation drift.
7. **Validate findings:** Reproduce or triangulate evidence and reject unsupported findings.
8. **Prioritize:** Rank findings by severity, likelihood, blast radius, and remediation cost.
9. **Report:** Produce findings, strengths, limitations, and an ordered action plan.

## Decision Points

```text
If a suspected issue cannot be supported by code, tests, configuration, runtime evidence, or a reliable tool:
    record it as a question or omit it.
If a finding is outside the declared scope:
    record it separately without expanding the audit silently.
If a tool reports a candidate issue:
    inspect the underlying code before promoting it to a finding.
If removal safety requires dedicated reachability analysis:
    route the candidate to analyzing-dead-code.
If the audit uncovers an immediate critical security exposure:
    report it first and recommend containment before lower-priority work.
```

## Finding Requirements

Every actionable finding must contain:

- stable identifier;
- concise title;
- category;
- severity;
- confidence;
- affected location;
- evidence;
- impact;
- trigger or reproduction path;
- recommended remediation;
- verification approach;
- scope relationship.

## Validation

Verify that:

- every finding is evidence-backed;
- severity reflects realistic impact and likelihood;
- duplicate symptoms are grouped by root cause;
- strengths and existing controls are acknowledged;
- tool findings were manually interpreted;
- no code changes were made;
- audit limitations and uninspected areas are explicit.

## Output

Use `assets/code-audit-report.md`.

## Completion Criteria

- [ ] Scope and exclusions are explicit.
- [ ] Critical architecture and flows were understood.
- [ ] All applicable audit dimensions were considered.
- [ ] Findings meet the evidence contract.
- [ ] Severity and confidence are separated.
- [ ] False positives and duplicate symptoms were removed.
- [ ] An ordered remediation plan exists.
- [ ] Limitations and residual risk are recorded.

## References

- Read `references/audit-planning.md` before beginning the audit.
- Read `references/finding-evidence.md` when promoting observations to findings.
- Read `references/severity-and-prioritization.md` when ranking findings.
- Read `references/audit-dimensions.md` for dimension-specific prompts.
- Read `references/tool-assisted-auditing.md` when using scanners or static-analysis tools.
- Read `references/brownfield-auditing.md` only for legacy or poorly documented systems.
