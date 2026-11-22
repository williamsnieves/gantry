---
name: validating-changes
description: Runs and reports the repository-native mechanical validation required for a software change, including formatting, linting, static analysis, type checks, tests, builds, and project-specific checks. Use before review, pull request creation, or completion claims. Do not use to judge test quality, review architecture, assess code style beyond tooling, or fix unrelated failures.
---

# Validating Changes

## Purpose

Establish whether a software change preserves repository integrity by discovering and executing the applicable project-native validation commands and reporting reproducible evidence.

## Use When

- A change must be checked before review or pull request creation.
- An implementation loop needs mechanical pass or fail evidence.
- The project requires format, lint, type, test, build, schema, or generated-artifact validation.
- A failure must be classified as pre-existing or introduced by the current change.

## Do Not Use When

- The request is to evaluate whether tests are well designed or sufficiently comprehensive.
- The request is a code, architecture, security, performance, or detail review.
- The task is to implement the change.
- The task is to weaken or bypass validation.
- The task is to repair unrelated repository failures.

## Inputs

- Current working tree or change diff.
- Applicable `AGENTS.md`.
- Project manifests, scripts, CI workflows, and tool configuration.
- Optional baseline branch, commit, or previous validation evidence.
- Optional explicit validation scope.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Inspect repository manifests, scripts, task runners, and CI before choosing commands.
3. Determine affected workspaces, packages, applications, and generated artifacts.
4. Preserve user-authored changes and existing failure evidence.
5. Do not invent commands, flags, paths, or required services.
6. Do not treat successful test execution as proof of test quality.

## Workflow

1. **Discover:** Build the validation matrix from repository-native sources.
2. **Scope:** Determine fast iteration checks and mandatory completion checks.
3. **Prepare:** Identify environment requirements, services, generated artifacts, and safe execution constraints.
4. **Execute:** Run applicable checks in dependency-aware order.
5. **Capture:** Record commands, exit codes, relevant output, duration, and scope.
6. **Classify failures:** Determine introduced, pre-existing, environmental, flaky, or unknown status when evidence permits.
7. **Correct within scope:** When authorized, fix only failures caused by the current change and rerun affected checks.
8. **Escalate:** Report blockers and residual risk for checks that cannot run or remain failing.
9. **Summarize:** Produce the validation report and final mechanical status.

## Decision Points

```text
If project-native commands cannot be discovered:
    stop and report the missing validation contract.
Else if a check requires unavailable infrastructure:
    record it as not run with exact requirements and residual risk.
Else if a failure is clearly introduced by the current change:
    correct it when implementation authority exists, then rerun.
Else if a failure is pre-existing and unrelated:
    preserve evidence, do not expand scope, and report it separately.
Else if failure ownership is unclear:
    classify as unknown and gather minimal comparison evidence.
```

## Validation

The skill itself must verify that:

- commands came from repository evidence;
- every applicable required check has a terminal status;
- no failed or skipped check is described as passing;
- exit codes and relevant output are preserved;
- rerun results replace stale results;
- the final status reflects the strictest blocking check;
- test-quality claims are excluded.

## Output

Use `assets/change-validation-report.md`.

## Completion Criteria

- [ ] Validation matrix is evidence-based.
- [ ] Scope and command order are defined.
- [ ] Every applicable check ran or has an explicit not-run reason.
- [ ] Failures are classified when evidence permits.
- [ ] Introduced failures were corrected and rerun when authorized.
- [ ] Pre-existing failures did not silently expand scope.
- [ ] Final status and residual risks are explicit.
- [ ] No claim about test quality was made.

## References

- Read `references/command-discovery.md` before constructing the validation matrix.
- Read `references/check-order-and-scope.md` when selecting check order and affected scope.
- Read `references/failure-classification.md` when any check fails.
- Read `references/environment-and-services.md` when checks require infrastructure or credentials.
- Read `references/evidence-and-status.md` before producing the final result.
