# Traceability and Idempotency

Synchronization should be repeatable without duplicating behavior.

## Traceability

For each delta, record:

- source change;
- source delta location;
- target main spec;
- operation type;
- resulting requirement or scenario;
- status.

## Idempotency

A second synchronization attempt should result in:

- no duplicate requirements;
- no repeated removals;
- no destructive rename;
- an explicit already-synchronized or no-op result.

## Coverage Matrix

Use a matrix when multiple capabilities are affected:

| Source Delta | Operation | Target Spec | Result |
|---|---|---|---|

Every approved delta should have exactly one terminal result:

- applied;
- already represented;
- intentionally deferred;
- blocked by conflict.

No delta may disappear silently.
