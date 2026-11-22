# Gate Result Envelope

Every agent result should be representable as:

```yaml
gate_result_version:
run_id:
wave_id:
gate_id:
change_identity:
reviewed_scope:
original_decision:
normalized_execution_class:
findings:
conditions:
evidence:
dynamic_triggers:
handoffs:
invalidates:
reentry_requirements:
started_at:
completed_at:
```

## `original_decision`

Never discard specialist vocabulary.

## `normalized_execution_class`

Allowed:

```text
PASS
PASS_WITH_CONDITIONS
CHANGES_REQUIRED
PENDING_DECISION
PENDING_EVIDENCE
NOT_REQUIRED
```

## `dynamic_triggers`

New routing signals discovered during execution.

## `invalidates`

Optional explicit statement that another gate's earlier evidence may now be stale.

The orchestrator/reviewer validates the claim.

## Runtime Independence

The envelope may be transported as JSON/YAML/Markdown/tool payload.

Semantics remain portable.
