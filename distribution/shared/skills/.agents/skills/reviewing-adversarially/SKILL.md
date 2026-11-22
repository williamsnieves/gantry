---
name: reviewing-adversarially
description: Portable engineering capability `reviewing-adversarially`. Use when the
  harness or a specialist agent explicitly requires this named capability.
---
# Reviewing Adversarially

## Purpose

Challenge a specific change as if it will fail under hostile inputs, partial failures, concurrency, misuse, and unexpected operating conditions, and report only evidence-backed defects or material risks.

## Use When

- A pull request or implementation needs a rigorous final challenge.
- A high-risk change affects money, identity, permissions, data integrity, reliability, or external systems.
- Mechanical validation passed but correctness confidence remains insufficient.
- The reviewer must test the change's assumptions rather than merely summarize it.
- A design or implementation claims safety, idempotency, atomicity, compatibility, or resilience.

## Do Not Use When

- The task is a repository-wide audit.
- The task is only to run format, lint, type checks, tests, or builds.
- The task is to implement fixes.
- The task is an architecture review without a concrete change.
- The task is to produce stylistic preferences, speculative concerns, or exhaustive low-value comments.

## Inputs

- Target diff, pull request, implementation, or design.
- Intended behavior, specifications, acceptance criteria, or OpenSpec change.
- Applicable `AGENTS.md`.
- Relevant tests, validation evidence, architecture context, and operational constraints.
- Optional threat model, incident history, or risk priorities.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Establish the intended behavior and explicit invariants.
3. Inspect the entire relevant diff and necessary surrounding code.
4. Review validation and test evidence without assuming passing checks prove correctness.
5. Identify trust boundaries, irreversible operations, and critical failure paths.
6. Do not modify code.

## Workflow

1. **Establish contract:** Extract intended outcomes, invariants, exclusions, and claimed guarantees.
2. **Map attack surface:** Identify inputs, state transitions, dependencies, trust boundaries, concurrency, and external effects.
3. **Generate adversarial hypotheses:** Form concrete ways the change could violate the contract.
4. **Trace execution:** Follow each hypothesis through code, configuration, tests, and runtime behavior.
5. **Attempt falsification:** Use counterexamples, boundary cases, failure injection reasoning, and targeted checks.
6. **Triage:** Reject unsupported concerns and group symptoms by root cause.
7. **Assess impact:** Calibrate severity, likelihood, blast radius, and recoverability.
8. **Recommend remediation:** Propose the smallest effective fix and verification.
9. **Conclude:** State whether the change is acceptable, conditionally acceptable, or blocked.

## Adversarial Lenses

Apply only relevant lenses:

- malformed, missing, duplicated, stale, or reordered inputs;
- unauthorized or cross-tenant access;
- replay, retry, and idempotency failures;
- partial success and rollback failure;
- concurrency, races, deadlocks, and stale state;
- timeout, cancellation, and resource exhaustion;
- dependency failure and inconsistent external responses;
- migration and backward-compatibility breaks;
- logging, observability, and secret exposure;
- unsafe defaults and configuration drift;
- recovery, restart, and duplicate processing;
- unexpected scale and algorithmic amplification.

## Decision Points

```text
If a concern cannot be tied to a concrete contract, path, or realistic trigger:
    omit it or record it as a question.
If the issue is already prevented by a verified guard:
    do not report it.
If multiple failures share one root cause:
    report the root cause once with affected manifestations.
If a critical exploit or irreversible data-loss path is credible:
    report it first and recommend blocking release.
If the review requires broad repository health analysis:
    route to auditing-code.
```

## Finding Requirements

Every finding must include:

- stable identifier;
- severity;
- confidence;
- violated contract or invariant;
- affected location;
- adversarial trigger;
- execution path or evidence;
- impact;
- why existing controls are insufficient;
- smallest remediation;
- verification strategy.

## Validation

Verify that:

- every finding attempts to falsify a stated or implied contract;
- the trigger is realistic;
- relevant guards and tests were inspected;
- severity and confidence are independent;
- duplicate symptoms are consolidated;
- style preferences and unrelated debt are excluded;
- no code changes were made;
- the final verdict matches unresolved findings.

## Output

Use `assets/adversarial-review-report.md`.

## Completion Criteria

- [ ] Intended contract and invariants are explicit.
- [ ] Critical surfaces and failure paths were mapped.
- [ ] Relevant adversarial lenses were applied.
- [ ] Findings satisfy the evidence contract.
- [ ] False positives and duplicates were removed.
- [ ] Each blocking finding has remediation and verification.
- [ ] Strengths and effective controls are acknowledged.
- [ ] Final verdict and residual risk are explicit.

## References

- Read `references/contract-and-invariants.md` before generating hypotheses.
- Read `references/adversarial-lenses.md` while challenging the change.
- Read `references/falsification-methods.md` when validating hypotheses.
- Read `references/finding-calibration.md` before reporting findings.
- Read `references/review-boundaries.md` to keep the review focused.
