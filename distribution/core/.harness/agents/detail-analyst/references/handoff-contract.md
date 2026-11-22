# Detail Analyst Handoff Contract

Every handoff should allow the recipient to act without repeating the whole analysis.

## Required Fields

- recipient or workflow;
- authoritative source;
- affected artifact or location;
- finding identifier;
- missing or inconsistent detail;
- materiality;
- smallest correction;
- verification method;
- blocked downstream work.

## Routing

### Enrichment

For missing user-story facts, rules, actors, or acceptance behavior.

### Exploration

For unclear options, architecture direction, or scope decisions.

### OpenSpec Editing

For proposal, spec, design, or task corrections.

### Implementation

For missing code, tests, migration, generated output, configuration, or operational work.

### Validator

For absent mechanical evidence.

### Documentation

For stale guides, examples, runbooks, references, or diagrams.

### Adversarial Review

For accepted but high-risk guarantees that need falsification.

## Rule

Do not hand off a vague statement such as “review edge cases.” Name the exact missing condition, affected path, and expected verification.
