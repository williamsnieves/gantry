# Handoff Protocol

## Purpose

Move the minimum complete context from one agent to another without forcing the receiver to rediscover the whole change.

A handoff is not:

```text
"Security, please review this."
```

A valid handoff says exactly:

```text
why the receiver is activated
what evidence exists
what question/decision is owned by the receiver
what output is required
what blocks progress
```

## Portable Handoff Envelope

Use fields equivalent to:

```yaml
handoff_protocol_version:
handoff_id:
change_identity:
from:
to:
reason:
trigger:
scope:
source_findings:
authoritative_context:
evidence:
known_facts:
unknowns:
requested_action:
expected_output:
blocking_status:
reentry_condition:
```

See:

```text
templates/handoff-envelope.template.yaml
```

## Required Fields

### `handoff_id`

Stable identifier.

Recommended:

```text
HO-001
HO-002
```

### `change_identity`

Commit/diff/spec/change identifier covered by the handoff.

### `from`

Agent/skill/orchestrator producing the handoff.

### `to`

Exact owner.

Do not use:

```text
someone
team
reviewer
```

when a known harness agent owns it.

### `reason`

Why this receiver is needed.

### `trigger`

The routing/risk trigger that activated the handoff.

Examples:

```text
SECURITY: multi-tenant authorization
INFRASTRUCTURE: schema rollout
PERFORMANCE: measured p95 regression
```

### `scope`

Exact affected surface.

### `source_findings`

IDs from the producing agent.

Do not copy findings without IDs when stable IDs exist.

### `authoritative_context`

Only authoritative requirements/ADRs/policies relevant to the receiver.

### `evidence`

Exact evidence already gathered.

Examples:

```text
file/line
test result
trace
query plan
architecture diagram
CI artifact
runtime config
```

### `known_facts`

Facts already established.

### `unknowns`

Do not hide uncertainty.

### `requested_action`

One clear action.

Examples:

```text
verify control
decide architecture
evaluate scenario coverage
rerun validator command
```

### `expected_output`

Use the receiver's normal output contract.

### `blocking_status`

Use:

```text
BLOCKING
NON_BLOCKING
CONDITIONAL
UNKNOWN_PENDING_RECEIVER
```

The sender must not downgrade a receiver-owned blocker.

### `reentry_condition`

What evidence/result allows upstream flow to resume.

## Handoff Quality Rule

The receiver should not need to ask:

```text
what changed?
where?
why am I here?
what finding triggered this?
what decision do you need from me?
```

If those are unclear, the handoff is incomplete.

## Minimal Context

Do not dump the entire repository/chat.

Pass:

```text
authoritative context
+
affected scope
+
trigger evidence
+
source findings
+
expected output
```

The receiver may fetch surrounding repository context as required.

## Evidence, Not Conclusions

Good:

```text
Security:
BCR-004 shows update query lacks organization predicate.
Authenticated org is available at request context.
Please evaluate exploitability/control requirement.
```

Bad:

```text
Security:
This is definitely a critical vulnerability.
```

when sender does not own security severity.

## Specialist Ownership

Sender may describe facts.

Receiver owns domain interpretation.

Examples:

```text
Code Review
→ passes implementation evidence
→ Security owns security disposition

Performance
→ passes CPU saturation evidence
→ Infrastructure owns runtime configuration change

QA
→ passes impossible-to-isolate testability evidence
→ Architecture Review owns structural decision
```

## Handoff Chains

A finding may create a chain:

```text
QA
→ Code Review / Implementation
→ Validator
→ QA re-check
→ Reviewer
```

Record each step rather than hiding the chain.

## No Circular Handoffs

If agents bounce the same unresolved question:

```text
A → B → A
```

without new evidence, route to:

```text
authoritative decision owner
```

or mark:

```text
BLOCKED_PENDING_DECISION
```

## Handoff Updating

When new evidence appears, create an updated handoff/version.

Do not silently mutate old evidence.

## Runtime Serialization

Allowed:

```text
Markdown
YAML
JSON
tool payload
OMP swarm message
Claude subagent prompt
Codex task
Cursor/OpenCode task
```

Semantic fields must remain equivalent.
