# Review Boundaries

## In Scope

- defects introduced or exposed by the target change;
- contract violations;
- material security, correctness, reliability, performance, or compatibility risks;
- missing safeguards necessary for the claimed behavior;
- test gaps only when tied to a concrete unprotected failure mode.

## Out of Scope

- unrelated repository debt;
- formatting or lint already enforced by tools;
- personal style preferences;
- speculative redesign without a demonstrated defect;
- broad dependency-health assessment;
- dead-code inventory;
- implementation of fixes.

## Existing Issues

Report an existing issue only when the change:

- materially worsens it;
- relies on it;
- makes it reachable;
- claims to solve it but does not.

Otherwise record it separately or omit it.

## Review Economy

Prefer a small number of high-signal findings over exhaustive commentary.

A clean review with no findings is valid when the change withstands challenge.
