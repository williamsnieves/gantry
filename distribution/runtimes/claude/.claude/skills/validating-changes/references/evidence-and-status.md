# Evidence and Status

## Per-Check Record

For each check, capture:

- name;
- exact command;
- working directory or scope;
- source of the command;
- start and end or duration when available;
- exit code;
- relevant output;
- status;
- failure classification;
- rerun relationship.

## Status Values

Use:

- Passed
- Failed — introduced
- Failed — pre-existing
- Failed — environmental
- Failed — flaky
- Failed — unknown
- Not run
- Not applicable

## Overall Status

### Passed

Every applicable blocking check passed.

### Conditionally passed

Use only when project policy explicitly allows a known non-blocking pre-existing or environmental limitation.

### Failed

At least one applicable blocking check failed or a mandatory check could not run.

## Honesty Rules

Do not say:

- tests pass when only a subset ran;
- build passes when compilation was skipped;
- validation is complete when a mandatory service was unavailable;
- tests are good because they passed.
