# Severity and Prioritization

Severity and confidence are independent.

## Severity

### Critical

Credible risk of catastrophic security exposure, irreversible data loss, widespread outage, or immediate unsafe release.

### High

Major correctness, security, reliability, or performance impact affecting important flows with plausible activation.

### Medium

Meaningful defect or debt with bounded impact, lower likelihood, workaround, or limited scope.

### Low

Localized improvement, minor risk, or maintainability issue without significant current impact.

### Informational

Useful context, strength, or non-actionable observation.

## Confidence

Use:

- High;
- Medium;
- Low.

A critical but low-confidence suspicion is not a confirmed critical defect.

## Priority Inputs

Rank by:

- severity;
- likelihood;
- blast radius;
- exploitability or trigger frequency;
- detectability;
- remediation cost;
- dependency order;
- strategic value.

## Action Plan

Group into:

1. contain immediately;
2. fix before release;
3. schedule next;
4. monitor or investigate;
5. accept explicitly.
