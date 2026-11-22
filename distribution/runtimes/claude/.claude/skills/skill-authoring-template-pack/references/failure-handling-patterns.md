# Failure Handling Patterns

## Blocking Failures

Stop when:

- required context is unavailable;
- instructions conflict materially;
- authorization is missing;
- execution would be unsafe;
- validation cannot be performed.

## Recoverable Failures

1. Preserve evidence.
2. Determine whether the failure is pre-existing or introduced.
3. Correct only issues within scope.
4. Re-run the affected validation.
5. Report remaining limitations.

## Prohibited Recovery

Do not:

- weaken tests or validation;
- suppress meaningful errors;
- fabricate missing context;
- perform destructive actions silently;
- expand the task to hide a failure.
