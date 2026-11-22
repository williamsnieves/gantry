# Acceptance Criteria

Acceptance criteria define observable behavior, not implementation preference.

## Qualities

Criteria should be:

- specific;
- testable;
- traceable to the intended outcome;
- independent where practical;
- clear about relevant preconditions and results.

## Coverage

Include as relevant:

- successful behavior;
- validation and error behavior;
- permissions and unauthorized behavior;
- empty or boundary states;
- compatibility;
- non-functional expectations;
- documentation, migration, or operational completion.

## Formats

Use concise bullet criteria or Given–When–Then when scenario structure improves clarity.

Example:

```text
Given [precondition]
When [action]
Then [observable result]
```

## Avoid

- internal file names without confirmed project evidence;
- vague terms such as “works correctly”;
- prescribing tests instead of behavior;
- combining multiple unrelated outcomes in one criterion;
- inventing thresholds, copy, or product policy.
