# Tool-Assisted Detection

Tools identify candidates, not deletion authorization.

## Tool Categories

Use repository-supported or authorized tools:

- compiler unused-symbol checks;
- import graph analyzers;
- unused export analyzers;
- unused dependency analyzers;
- bundle analyzers;
- coverage tools;
- linkers and tree-shaking reports;
- framework-specific route or registration inspection.

## Procedure

1. Discover existing commands and configuration.
2. Record version, scope, entry points, and exclusions.
3. Run without auto-fix or destructive flags.
4. Normalize and deduplicate candidates.
5. Inspect every candidate against project conventions.
6. Preserve raw evidence separately from final classification.

## Common False Positives

- reflection;
- plugins;
- framework registration;
- test-only utilities;
- package exports;
- generated code;
- platform-specific files;
- migration hooks;
- configuration-selected modules.

## Coverage Warning

Unexecuted code is not necessarily dead. Coverage measures observed execution under a test or runtime sample, not total reachability.
