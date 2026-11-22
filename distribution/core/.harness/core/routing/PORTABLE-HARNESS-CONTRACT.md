# Portable Harness Contract

## Purpose

Define the boundary between the reusable engineering harness and runtime-specific execution adapters.

The harness core must be able to move between agent runtimes without rewriting engineering logic.

## Layer Model

```text
┌──────────────────────────────────────────────┐
│ Runtime Adapters                             │
│ Claude Code / Codex / Cursor / OpenCode /   │
│ Oh My Pi / future runtimes                  │
└──────────────────────────────────────────────┘
                     ↑
┌──────────────────────────────────────────────┐
│ Harness Orchestration                        │
│ routing / handoffs / later: parallelism,     │
│ ordering, blocking, pre-PR gate              │
└──────────────────────────────────────────────┘
                     ↑
┌──────────────────────────────────────────────┐
│ Agents                                       │
│ Validator / Reviews / QA / Performance /     │
│ Security / Infrastructure / Reviewer /       │
│ Detail Analyst                               │
└──────────────────────────────────────────────┘
                     ↑
┌──────────────────────────────────────────────┐
│ Portable Engineering Core                    │
│ AGENTS.md / skills / standards / OpenSpec / │
│ architecture / templates / evals             │
└──────────────────────────────────────────────┘
```

## Portable Core MUST Own

```text
engineering rules
skill semantics
agent missions
agent authority boundaries
routing semantics
risk triggers
gate applicability
handoff schemas
finding/evidence contracts
decision vocabularies
evaluation cases
```

## Runtime Adapter MUST Own

Only runtime mechanics:

```text
agent declaration syntax
skill discovery paths
subagent invocation
tool permissions
context injection
parallel execution mechanism
session/process management
structured-output transport
runtime/model selection
hooks/events
MCP wiring
CLI/SDK invocation
```

## Portable Core MUST NOT Depend On

```text
Claude-specific subagent syntax
Codex-specific agent syntax
Cursor-specific rule syntax
OpenCode-specific agent syntax
Oh My Pi swarm/workflow syntax
provider-specific model names
runtime-specific directory layouts
runtime-specific hooks
runtime-specific task IDs
```

## Runtime Adapter MUST NOT Redefine

```text
what Security means
what QA means
what Validator means
which finding is blocking
what evidence counts as PASS
agent handoff semantics
risk triggers
specialist decision vocabularies
```

Adapters translate; they do not reinterpret.

## Agent Contract

Every portable agent definition must expose:

```text
id
mission
activation triggers
inputs
outputs
authority
forbidden actions
decision vocabulary
handoff requirements
re-entry requirements
```

The runtime adapter may map that contract into its own agent/subagent format.

## Skill Contract

Skills remain runtime-neutral wherever possible.

A skill package should define:

```text
description
procedure
inputs
outputs
references
assets
evals
```

Runtime adapters may install/discover the skill from different paths.

## Gate Contract

Every gate returns:

```text
gate_id
scope
change_identity
original_decision
findings
conditions
evidence
handoffs
reentry_requirements
```

Do not normalize specialist decisions inside runtime adapters.

## Handoff Contract

All agent-to-agent transfers use a portable envelope defined by:

```text
HANDOFF-PROTOCOL.md
```

The runtime may serialize it as:

```text
Markdown
YAML
JSON
tool payload
task message
swarm message
```

but semantic fields remain equivalent.

## Routing Contract

The core router returns a runtime-neutral plan:

```text
change classification
risk triggers
agent applicability
reason for activation
required inputs
expected outputs
dependencies
deferred decisions
```

The runtime adapter decides how to execute that plan.

## Model Routing

Model selection belongs outside engineering semantics.

Good:

```text
agent: security
reasoning_profile: deep
```

Adapter/runtime policy:

```text
deep → model/provider chosen here
```

Bad:

```text
Security Agent = fixed model name
```

inside the portable core.

## Runtime Capability Gaps

If a runtime cannot support an execution feature:

```text
parallel subagents
persistent agents
hooks
MCP
structured messages
```

the adapter must degrade execution mechanics without weakening engineering gates.

Example:

```text
parallel unavailable
→ execute sequentially
```

not:

```text
parallel unavailable
→ skip Security
```

## Compatibility Principle

The same routing input should produce the same semantic agent set across runtimes.

Allowed differences:

```text
execution order where semantically safe
parallel vs sequential execution
model/provider
tooling
formatting
```

Not allowed:

```text
different required security gate
different QA standard
different blocking interpretation
```

## Versioning

Portable contracts should be versioned independently from adapters.

Recommended:

```text
harness_contract_version
routing_policy_version
handoff_protocol_version
adapter_version
```

This allows runtime adapters to evolve without silently changing engineering behavior.
