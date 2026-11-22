# testing-external-service-adapters

Tests provider-specific Infrastructure adapters using the strongest safe available evidence:

```text
pure mapping
→ protocol/contract
→ official emulator/test mode
→ real sandbox
```

It covers mapping, semantic failures, authentication, retries, rate limits, timeouts, idempotency, ambiguous outcomes, async states, redaction, lifecycle, cleanup, and honest product/provider/environment failure classification.
