# Finding Calibration

## Severity

### Critical

Credible path to catastrophic data loss, severe security compromise, widespread outage, or irreversible unsafe release.

### High

Major contract violation in an important flow with plausible activation and substantial impact.

### Medium

Material defect with bounded impact, lower likelihood, or a practical workaround.

### Low

Localized defect or resilience gap with limited operational impact.

### Informational

Verified strength, defense-in-depth opportunity, or non-blocking observation.

## Confidence

Use:

- High: path and trigger are directly demonstrated or strongly proven;
- Medium: code path is clear but triggering conditions are partly inferred;
- Low: material concern with incomplete evidence.

## Blocking Policy

A finding blocks approval when:

- project policy says so;
- severity and likelihood make release unsafe;
- the core contract is not met;
- evidence is missing for a claimed critical guarantee.

## Finding Quality Test

A reviewer should be able to answer:

- What exact promise fails?
- Under what trigger?
- Through what path?
- What is the consequence?
- What control was expected?
- How can the fix be verified?
