# Decision Patterns

Use explicit branches when the procedure changes materially.

## Binary Branch

```text
If [condition]:
    execute branch A.
Else:
    execute branch B.
```

## Ordered Classification

```text
If [highest-priority condition]:
    execute branch A.
Else if [secondary condition]:
    execute branch B.
Else:
    execute the default branch.
```

## Blocking Context

```text
If [mandatory input] is unavailable:
    stop and report the missing input.
```

## Conditional Reference Loading

```text
If [specialized case]:
    read `references/specialized-methodology.md`.
```

Do not hide important decisions in prose. Do not create branches without defining how the condition is established.
