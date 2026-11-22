# Authoring Methodology

## Contents

1. Classification
2. Capability boundary
3. Degree of freedom
4. Skill structure
5. Authoring cycle
6. Review questions

## 1. Classification

Before writing, classify the intended content:

| Content | Destination |
|---|---|
| Durable non-obvious constraint | `AGENTS.md` |
| Canonical explanation | Documentation |
| Reusable procedure | Skill |
| Specialized role | Agent |
| Ordered orchestration | Workflow |
| Repeated workflow with exit conditions | Loop |
| Mechanical enforcement | Tooling |

Reject the skill proposal when another artifact is more appropriate.

## 2. Capability Boundary

A skill should have:

- one recognizable purpose;
- concrete activation conditions;
- explicit exclusions;
- one stable output contract;
- observable completion criteria.

Do not create skills for one-off solutions, project anecdotes, generic knowledge, or mechanical constraints.

## 3. Degree of Freedom

Choose instruction precision according to risk:

- **High:** multiple valid approaches; context determines the best path.
- **Medium:** a preferred pattern exists but parameters vary.
- **Low:** sequence is fragile, destructive, or consistency-critical; prefer a script.

## 4. Skill Structure

Keep runtime behavior in `SKILL.md`:

- purpose and boundaries;
- inputs and required context;
- workflow and branches;
- validation and failure handling;
- output and completion.

Extract only material that is conditional, substantial, or executable.

## 5. Authoring Cycle

### RED

Create an evaluation before writing or changing the skill. Capture the failure:

- wrong activation;
- skipped step;
- unsafe shortcut;
- missing evidence;
- unnecessary context;
- incorrect output.

### GREEN

Write the minimum guidance needed to correct the observed failure.

Do not add hypothetical rules without evidence.

### REFACTOR

After the evaluation passes:

- remove repetition;
- compress examples;
- clarify branches;
- extract conditional detail;
- convert fragile repeated logic into scripts;
- rerun all cases.

## 6. Review Questions

- Does every paragraph change execution?
- Can the agent already infer this?
- Is the skill teaching judgment rather than duplicating tooling?
- Is the activation boundary distinguishable from adjacent skills?
- Is success observable?
- Does the skill load only the context needed for the current branch?
