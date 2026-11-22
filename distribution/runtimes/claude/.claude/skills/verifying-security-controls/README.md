# verifying-security-controls

Cross-cutting security evidence/verification skill.

Default selected application-security baseline when the project uses it:

```text
OWASP ASVS 5.0.0
```

But exact control IDs and wording must come from the project's approved ASVS source.

Core statuses:

```text
PASS
FAIL
NOT_APPLICABLE
NOT_VERIFIED
```

Core rule:

```text
implemented intent
≠
verified security control
```

This skill prevents unsupported conformance claims and keeps risk acceptance separate from verification status.
