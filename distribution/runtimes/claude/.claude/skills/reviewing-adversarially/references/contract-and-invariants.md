# Contract and Invariants

An adversarial review starts with what must remain true.

## Contract Sources

Use, in precedence order:

1. applicable instructions;
2. accepted specifications or active change artifacts;
3. acceptance criteria;
4. public interfaces and schemas;
5. documented architecture and operational contracts;
6. existing tests and implementation behavior.

Tests and current code are evidence, not automatically the desired contract.

## Invariant Categories

Identify as relevant:

- authorization and tenant isolation;
- uniqueness and idempotency;
- atomicity and consistency;
- ordering and monotonicity;
- data validation and integrity;
- compatibility;
- bounded resource use;
- retry and recovery behavior;
- privacy and secret handling;
- observability;
- lifecycle and cleanup.

## Claimed Guarantees

Translate vague claims into falsifiable statements.

Example:

```text
Claim: Order creation is idempotent.
Invariant: Repeating the same authorized request key produces at most one committed order and a stable response.
```

## Ambiguity

When the intended contract is unclear:

- record the ambiguity;
- do not invent a guarantee;
- assess whether the ambiguity itself blocks approval.
