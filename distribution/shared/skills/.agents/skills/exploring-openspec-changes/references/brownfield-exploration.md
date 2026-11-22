# Brownfield Exploration

Use when OpenSpec is introduced into an existing project or specifications are incomplete.

## Rules

- Treat running behavior and accepted project documentation as evidence, not automatically as ideal design.
- Distinguish current behavior from desired behavior.
- Record undocumented invariants discovered in code and tests.
- Do not attempt to document the entire repository before the first change.
- Baseline only the capabilities relevant to the explored change.
- Identify legacy constraints and technical debt separately from change requirements.
- Avoid presenting aspirational architecture as current state.

## Output Additions

Record:

- current behavior source;
- specification coverage gaps;
- legacy constraints;
- candidate baseline capability;
- migration or compatibility implications.
