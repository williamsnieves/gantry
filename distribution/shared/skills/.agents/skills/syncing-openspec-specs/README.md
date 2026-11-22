# syncing-openspec-specs

Synchronizes approved change delta specifications into canonical main specs.

## Core Boundaries

- It does not edit unresolved change intent.
- It does not implement code.
- It does not archive the change.
- It preserves unrelated canonical behavior.
- It must be idempotent and traceable.

## Typical Sequence

```text
editing or implementation complete
→ syncing-openspec-specs
→ validation and verification
→ archival workflow
```

## Provenance

Based on the approved LIDR `openspec-sync-specs` reference, mandatory OpenSpec task guidance, and the selected OpenSpec workflow documentation from the roadmap.
