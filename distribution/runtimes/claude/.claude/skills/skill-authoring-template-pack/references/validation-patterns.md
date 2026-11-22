# Validation Patterns

Validation must produce observable evidence.

## Standard Loop

```text
execute → validate → correct → re-execute
```

## Validation Definition

For every check, define:

- what is checked;
- how it is checked;
- acceptable evidence;
- response to failure.

## Common Evidence

- successful repository-native command;
- structured findings tied to source locations;
- schema-valid output;
- comparison with accepted criteria;
- updated artifact with traceable changes.

## Completion Guard

A skill must not claim completion when:

- a mandatory check was skipped;
- validation failed;
- evidence is unavailable;
- the output conflicts with a higher-precedence instruction;
- a blocking dependency remains unresolved.
