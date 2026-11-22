# Safe Removal Planning

The analysis recommends removal; a later implementation performs it.

## Removal Unit

Define:

- exact symbols, files, modules, dependencies, or paths;
- coupled configuration;
- tests and fixtures;
- documentation;
- generated artifacts;
- migration or compatibility requirements.

## Removal Strategies

### Direct Removal

Use only for high-confidence, low-blast-radius candidates with strong validation.

### Staged Deprecation

Use when external or uncommon consumers may exist:

1. mark deprecated;
2. add usage telemetry or warnings;
3. communicate migration;
4. wait through an agreed window;
5. remove after evidence.

### Feature Disablement

Disable through configuration before deleting implementation when rollback or rare use is a concern.

### Branch or Release Staging

Separate high-risk removals from unrelated feature work.

## Proof Plan

Specify:

- pre-removal baseline;
- mechanical checks;
- targeted and broader tests;
- build or packaging checks;
- runtime smoke tests;
- telemetry or log observation;
- rollback trigger and mechanism.

## Dependencies

Remove or update:

- imports;
- exports;
- configuration;
- dependency declarations;
- docs;
- ownership metadata;
- tests that only preserve obsolete behavior.

Do not delete useful characterization tests until replacement behavior is protected.
