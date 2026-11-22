# Routing Policy

## Purpose

Select the smallest complete set of agents required for the current work.

Core target:

```text
minimum sufficient gate graph
+
complete risk coverage
```

Not:

```text
run every agent
```

## Applicability States

Every known agent is classified as:

```text
REQUIRED
CONDITIONAL
NOT_APPLICABLE
NOT_TRIGGERED
ALREADY_SATISFIED
BLOCKED
```

### REQUIRED

Must run before the current target gate can complete.

### CONDITIONAL

Trigger exists but execution depends on evidence/decision produced by another step.

### NOT_APPLICABLE

The agent's domain is outside the change.

### NOT_TRIGGERED

The domain exists but no material trigger requires specialist review.

### ALREADY_SATISFIED

A fresh compatible result already covers the current change identity.

### BLOCKED

Agent cannot run meaningfully until a decision/evidence prerequisite exists.

## Routing Inputs

The router receives:

```text
work_mode
change_identity
scopes
accepted_behavior
architecture_profile / system profile if applicable
risk_triggers
known_findings
existing_fresh_gate_results
project policies
```

## Routing Output

Produce:

```text
routing_plan_version
change_identity
classification
risk_triggers
agents
reason_for_each_agent
required_inputs
expected_outputs
minimal_dependencies
deferred_policy_questions
```

Use:

```text
templates/routing-plan.template.yaml
```

## Routing Algorithm

### 1. Establish Work Mode

```text
DISCOVERY
ARCHITECTURE_ONLY
IMPLEMENTATION
REVIEW_ONLY
REMEDIATION
MIGRATION
RELEASE_ONLY
```

### 2. Classify Scopes

Use one or more change scopes.

### 3. Identify Risk Triggers

Use `RISK-TRIGGER-MODEL.md`.

### 4. Apply Base Agent Rules

#### Validator

`REQUIRED` for implementation/remediation/release changes when repository-native mechanical checks exist.

May be `NOT_APPLICABLE` for pure early architecture/discovery work.

#### Detail Analyst

Normally `REQUIRED` before final Reviewer for meaningful implementation/release work.

May be omitted for isolated early architecture work.

#### Relevant Code Review

Backend Code Review when backend implementation changed.

Frontend Code Review when frontend implementation changed.

#### Architecture Reviews

Only when architecture triggers exist or project policy requires the gate.

Do not activate because a codebase uses architecture.

#### QA

Required for meaningful behavior changes or test-evidence remediation.

May be `NOT_TRIGGERED` for documentation-only/non-behavioral changes if policy permits.

#### Performance

Activate only from performance triggers.

#### Security

Activate from security/trust/privacy triggers.

#### Infrastructure

Activate from infrastructure/release/runtime triggers.

#### Reviewer

Required only when the work is moving toward the harness pre-PR integration path.

Not required for isolated architecture exploration unless explicitly requested.

## Architecture-Only Routing

Example:

```text
work_mode: ARCHITECTURE_ONLY
scopes:
  - SOFTWARE_ARCHITECTURE

agents:
  backend-code-review: NOT_APPLICABLE
  frontend-code-review: NOT_APPLICABLE
  qa: NOT_APPLICABLE
  validator: NOT_APPLICABLE
```

Use architecture skills/orchestration instead of forcing implementation agents.

Security/STRIDE may still activate if trust boundaries are being designed.

## Frontend-Only Implementation

Baseline candidates:

```text
Validator
Frontend Code Review
QA
Detail Analyst
Reviewer
```

Add:

```text
Frontend Architecture Review
Performance
Security
Infrastructure
```

only when triggered.

## Backend-Only Implementation

Baseline candidates:

```text
Validator
Backend Code Review
QA
Detail Analyst
Reviewer
```

Add relevant specialist gates only when triggered.

## Full-Stack Implementation

Usually:

```text
Validator
Backend Code Review
Frontend Code Review
QA
Detail Analyst
Reviewer
```

Architecture Reviews are still trigger-based.

Do not activate both architecture reviews merely because both layers changed.

## Migration Routing

Migration frequently activates:

```text
relevant Code Review
relevant Architecture Review
QA
Infrastructure
Validator
Detail Analyst
Reviewer
```

Security/Performance only when their triggers exist.

## Test-Only Remediation

Typical:

```text
QA
Validator
Reviewer
```

Add Code Review only if production behavior/code also changed.

Detail Analyst may activate if test/spec propagation was the original gap.

## Dynamic Routing

Agents may emit:

```text
new_trigger
required_handoff
gate_escalation
```

Example:

```text
Frontend Code Review
→ finds PII sent to analytics
→ activate Security
```

The router appends the agent with a reason.

Do not silently broaden scope without recording the trigger source.

## Existing Fresh Results

If a compatible gate already exists for the same change identity:

```text
ALREADY_SATISFIED
```

Do not rerun it.

Freshness rules are ultimately owned by Reviewer/re-review policy.

## Routing Is Not Ordering

This document determines:

```text
what must run
```

It intentionally does not fully determine:

```text
what runs in parallel
exact review sequence
blocker precedence
```

Those are the next roadmap artifacts.

Only minimum dependencies are defined in `GATE-DEPENDENCY-CONTRACT.md`.

## Runtime Independence

Router output must be identical in meaning whether executed by:

```text
Claude Code
Codex
Cursor
OpenCode
Oh My Pi
```

Runtime adapters may change only execution mechanics.
