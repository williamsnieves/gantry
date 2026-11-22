# Omission and Inconsistency

## Omission
A required element is absent or incomplete, such as a schema change without migration, specified error behavior without implementation, or new configuration without documentation.

## Inconsistency
Two representations cannot both be correct, such as a spec saying optional while the schema requires the field, or tasks assuming synchronous behavior while design is asynchronous.

## Partial Propagation
A decision appears in some affected layers but not others.

## Observation
A supported improvement that is not required by the current contract.

## Question
A material detail whose approved answer is unavailable.

Before reporting, confirm the detail is required, not supplied by framework or generated behavior, not explicitly deferred, and not owned by another artifact. Do not convert preference into defect.
