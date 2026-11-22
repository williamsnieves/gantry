# Brownfield Auditing

Use for legacy systems, incomplete documentation, or uncertain ownership.

## Strategy

- map critical paths before broad scanning;
- identify runtime and deployment boundaries;
- distinguish legacy constraints from accidental complexity;
- use tests and production behavior as evidence, not as proof of ideal design;
- sample high-risk modules before extrapolating;
- record undocumented invariants;
- avoid recommending full rewrites without comparative evidence.

## Debt Classification

Separate:

- active defect;
- latent risk;
- intentional legacy constraint;
- obsolete compatibility layer;
- documentation gap;
- migration prerequisite.

## Remediation

Prefer:

- containment;
- characterization tests;
- incremental boundary extraction;
- removal after reachability proof;
- staged dependency upgrades;
- observability before risky change.

Record areas that could not be understood confidently.
