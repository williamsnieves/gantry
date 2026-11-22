# Context Retrieval

Use project sources to resolve discoverable facts before asking the user.

## Retrieval Order

1. Applicable `AGENTS.md`.
2. Accepted specifications or active change records.
3. Architecture and development documentation.
4. Existing implementation and adjacent tests.
5. Project configuration and CI.
6. External ticket source only when explicitly available and needed.

## Retrieval Boundaries

Retrieve only context that can materially change:

- scope;
- behavior;
- architecture constraints;
- acceptance criteria;
- risk;
- readiness.

Do not scan the entire repository without a concrete information need.

## Evidence

Record the source of project-specific facts in the final enrichment.

When sources conflict:

- follow instruction precedence;
- report the conflict;
- do not silently select a convenient interpretation.
