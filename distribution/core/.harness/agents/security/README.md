# Security Agent

Independent cross-cutting security gate.

## Core Pipeline

```text
STRIDE
→ Application Security Review
→ Security Control Verification
```

## Primary Skills

```text
threat-modeling-with-stride
reviewing-application-security
verifying-security-controls
```

## Frontend Specialists

```text
reviewing-frontend-security
reviewing-frontend-privacy-and-analytics
```

## Security Knowledge Model

```text
STRIDE
→ what could go wrong

OWASP Top 10:2025
→ broad application-risk classification

MITRE CWE
→ concrete weakness/root cause

OWASP ASVS 5.0.0 / project baseline
→ what control must be verified

evidence
→ whether the control actually works
```

## Critical Rule

```text
planned mitigation
≠ implemented control
≠ verified control
```

and:

```text
NOT_VERIFIED
≠ PASS
```

## Decisions

```text
SECURITY_APPROVED
SECURITY_APPROVED_WITH_CONDITIONS
SECURITY_CHANGES_REQUIRED
SECURITY_BLOCKED_PENDING_DECISION
SECURITY_BLOCKED_PENDING_EVIDENCE
SECURITY_REVIEW_NOT_REQUIRED
```
