# Propagation Tracing

Trace each material requirement or decision through the applicable chain:

```text
request → acceptance criteria → specification → design → tasks → implementation → tests → configuration → documentation → operations
```

For each item, identify its source, affected capability, design consequence, implementation surface, validation evidence, and documentation or operational consequence.

Also trace backward: every task should map to approved scope, every diff path should serve an approved requirement, and every new configuration option should have ownership and documentation.

Use a coverage matrix for cross-layer changes. A blank cell must be classified as valid, missing, or not applicable.
