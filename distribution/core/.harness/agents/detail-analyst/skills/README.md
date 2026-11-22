# Skills

The Detail Analyst agent requires the `analyzing-details` skill.

Recommended layout:

```text
skills/
└── analyzing-details/
    ├── SKILL.md
    ├── references/
    ├── assets/
    └── evals/
```

Do not duplicate the complete skill procedure inside platform adapters.

The portable agent contract should reference the skill by capability name. Each platform adapter is responsible only for making that skill discoverable.
