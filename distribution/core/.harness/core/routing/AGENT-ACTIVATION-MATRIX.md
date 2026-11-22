# Agent Activation Matrix

Legend:

```text
R = generally REQUIRED
C = CONDITIONAL / trigger-based
N = normally NOT_APPLICABLE
P = project-policy dependent
```

This matrix is a routing aid, not a substitute for trigger analysis.

| Change Type | Validator | Detail Analyst | B Code | B Arch | F Code | F Arch | QA | Perf | Security | Infra | Reviewer |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Docs only | C | C | N | N | N | N | C | N | N | N | C |
| Architecture only | N | C | N | C | N | C | N | C | C | C | C |
| Backend small behavioral | R | R | R | C | N | N | R | C | C | C | R |
| Frontend small behavioral | R | R | N | N | R | C | R | C | C | C | R |
| Full-stack behavioral | R | R | R | C | R | C | R | C | C | C | R |
| Security-sensitive backend | R | R | R | C | N | N | R | C | R | C | R |
| Security-sensitive frontend | R | R | N | N | R | C | R | C | R | C | R |
| DB/schema migration | R | R | R | C/R | N/C | N/C | R | C | C | R | R |
| CI/CD only | R | R/C | N | N | N | N | C | C | C | R | R |
| Infrastructure runtime change | R | R | C | C | C | C | C | C | C | R | R |
| Test-only remediation | R | C | C | N/C | C | N/C | R | N/C | C | N/C | R |
| Performance remediation | R | R | C | C | C | C | R/C | R | C | C | R |
| Security remediation | R | R | C | C | C | C | R/C | C | R | C | R |

## Interpretation Rules

### `C`

Activate only when a material trigger exists.

Example:

```text
small frontend copy change
→ Performance C
→ NOT_TRIGGERED
```

### `C/R`

Usually conditional, but becomes required for the described risk.

Example:

```text
schema migration changes transaction/data ownership
→ Backend Architecture Review REQUIRED
```

## Agent-Specific Trigger Summary

### Validator

Triggers:

```text
implementation changed
tests changed
build/config changed
release artifacts changed
```

### Detail Analyst

Triggers:

```text
pre-PR readiness
cross-artifact propagation
style/convention/spec/config/documentation completeness
```

### Backend Code Review

Triggers:

```text
backend production behavior changed
backend test-only change affecting behavior evidence may be conditional
```

### Backend Architecture Review

Triggers:

```text
ownership
ports/adapters
transaction/idempotency
eventing
migration seam
architecture drift
```

### Frontend Code Review

Triggers:

```text
frontend user/runtime behavior changed
```

### Frontend Architecture Review

Triggers:

```text
profile
vertical-slice ownership
state/composition
shared abstractions
styling architecture
testability architecture
```

### QA

Triggers:

```text
accepted behavior changed
test evidence changed
critical regression risk
```

### Performance

Triggers:

```text
accepted target
measured regression
capacity/load
large-data/performance-sensitive path
```

### Security

Triggers:

```text
trust boundary
auth/authz
tenant
secret
sensitive data
provider
webhook
browser security/privacy
IAM/network
```

### Infrastructure

Triggers:

```text
CI/CD
IaC
runtime/cloud
deployment
migration rollout
secrets/IAM/network implementation
observability
```

### Reviewer

Triggers:

```text
move toward final harness pre-PR readiness
```
