# Change Classification

## Purpose

Describe what kind of work is being performed before activating agents.

Routing uses:

```text
work mode
+
change scopes
+
risk triggers
```

Do not route from file extensions alone.

## Work Modes

### DISCOVERY

Understanding an existing system or requirement.

Typical outputs:

```text
context
risks
unknowns
requirements questions
```

No implementation gate should be assumed.

### ARCHITECTURE_ONLY

Requirements/system/backend/frontend/deployment architecture work without implementation.

Potential gates:

```text
architecture skills
STRIDE
architecture validation
```

Implementation Code Review/QA/Validator may be not applicable.

### IMPLEMENTATION

Production code/config/test implementation.

This is the normal review-gate flow.

### REVIEW_ONLY

Review existing implementation without modifying it.

Activate only requested/applicable review gates.

### REMEDIATION

Fix known findings.

Routing should include the owner plus only invalidated re-review gates.

### MIGRATION

Brownfield/schema/platform/architecture migration.

This often adds:

```text
architecture
QA
security
infrastructure
```

depending on risk.

### RELEASE_ONLY

Deployment/release/configuration work without new application implementation.

Infrastructure/Security/Validator may dominate.

## Change Scopes

A change can contain multiple scopes.

```text
DOCUMENTATION
REQUIREMENTS
SOFTWARE_ARCHITECTURE
BACKEND
FRONTEND
FULL_STACK
DATA
DATABASE
API_CONTRACT
EVENTING
SECURITY
PERFORMANCE
INFRASTRUCTURE
CI_CD
DEPLOYMENT
MIGRATION
OBSERVABILITY
TEST_ONLY
CONFIGURATION
DEPENDENCY
```

## Scope Rules

### BACKEND

Use when changing:

```text
domain/application behavior
backend adapters
HTTP/API implementation
persistence
provider integration
server-side authorization
```

### FRONTEND

Use when changing:

```text
React/UI behavior
frontend hooks/state
frontend adapters
browser interactions
styling affecting behavior
```

### FULL_STACK

Use only when one accepted behavior crosses frontend/backend or multiple independently deployable application layers.

Do not mark full-stack merely because the repository contains both.

### SOFTWARE_ARCHITECTURE

Use for system-level choices:

```text
service boundaries
data ownership
events
deployment topology
cross-system trade-offs
```

### INFRASTRUCTURE

Use for:

```text
IaC
cloud/PaaS
Kubernetes
runtime configuration
IAM/network
```

### CI_CD

Use for build/test/deploy workflow mechanics.

### MIGRATION

Use when old and new states coexist or staged compatibility matters.

### TEST_ONLY

Use when production behavior is unchanged and only tests/evidence are modified.

This may still require:

```text
QA
Validator
Reviewer
```

but not every Code Review specialist.

## Size Is Metadata, Not Routing Authority

Optional size:

```text
TINY
SMALL
MEDIUM
LARGE
```

may help context budgeting.

It must not determine gate activation by itself.

Example:

```text
1-line tenant predicate
→ HIGH security risk

2,000-line generated CSS update
→ potentially LOW behavioral risk
```

## Multi-Scope Example

```text
scopes:
  - BACKEND
  - DATABASE
  - MIGRATION
  - INFRASTRUCTURE

risks:
  - DATA_INTEGRITY
  - ROLLBACK
  - SECURITY
```

The router composes gates from all applicable triggers.
