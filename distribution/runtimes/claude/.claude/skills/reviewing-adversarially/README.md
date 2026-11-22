# reviewing-adversarially

Challenges a specific software change by attempting to falsify its guarantees.

## Core Boundary

This skill is a focused review, not a broad audit, mechanical validation pass, or implementation workflow.

## Typical Targets

- pull requests;
- high-risk implementations;
- authorization changes;
- payment and data-integrity flows;
- retries and idempotency;
- migrations and compatibility;
- reliability-sensitive designs.

## Key Rules

- Start from contracts and invariants.
- Use realistic adversarial triggers.
- Trace complete execution paths.
- Inspect existing controls before reporting.
- Prefer a few high-signal findings.
- Separate severity from confidence.
- Never modify code.

## Provenance

Adapted from the approved LIDR `adversarial-review` reference in the roadmap.
