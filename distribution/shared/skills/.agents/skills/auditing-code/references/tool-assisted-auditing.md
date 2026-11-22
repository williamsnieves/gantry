# Tool-Assisted Auditing

Tools generate evidence and candidates, not final findings.

## Potential Tools

Use only repository-supported or authorized tools:

- compiler and type checker;
- linters and static analyzers;
- dependency and vulnerability scanners;
- dead-code and unused-dependency analyzers;
- complexity or duplication tools;
- test and coverage tools;
- profilers and query analyzers;
- secret scanners.

## Procedure

1. Discover existing configuration and commands.
2. Run within declared scope.
3. Preserve command, version, configuration, and output.
4. Triage candidates against source and project context.
5. Deduplicate by root cause.
6. Report only verified findings or explicitly labeled tool candidates.

## Restrictions

- Do not install arbitrary scanners without authorization.
- Do not report database entries without checking applicability.
- Do not equate coverage percentage with test quality.
- Do not treat lint preference as a production defect.
- Do not delete code solely because a tool calls it unused.
