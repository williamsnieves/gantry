# Candidate Classification

## Status Definitions

### Used

A valid internal or external path reaches the candidate.

### Conditionally Used

Usage depends on configuration, platform, tenant, feature flag, environment, or rare runtime state.

### Externally Consumed

The candidate is part of a public, downstream, operational, or integration contract.

### Generated or Managed

The candidate is produced, updated, or referenced by a generator, framework, migration system, or vendor process.

### Deprecated but Active

Removal is intended, but current compatibility or consumer evidence still requires it.

### Removal Candidate

Evidence supports that no valid internal, dynamic, operational, generated, or external consumer requires it.

### Unknown

Available evidence cannot establish safe classification.

## Confidence

Use:

- High: multiple independent signals and complete entry-point coverage;
- Medium: strong static evidence but limited dynamic or external evidence;
- Low: incomplete graph, convention risk, or missing consumer inventory.

## Value

Estimate likely removal benefit:

- reduced attack surface;
- smaller artifact or bundle;
- lower maintenance burden;
- fewer dependencies;
- reduced cognitive complexity;
- simplified migration.

Do not inflate value without measurable or plausible impact.
