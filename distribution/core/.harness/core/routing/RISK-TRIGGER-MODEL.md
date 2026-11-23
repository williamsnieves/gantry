# Risk Trigger Model

## Principle

Agent activation is trigger-based, not checklist-based.

Use:

```text
scope
+
accepted requirements
+
changed trust/behavior boundaries
+
known findings
```

## Risk Dimensions

```text
BEHAVIORAL
ARCHITECTURE
SECURITY
DATA_INTEGRITY
MIGRATION
PERFORMANCE
INFRASTRUCTURE
COMPATIBILITY
USER_IMPACT
OPERABILITY
```

Risk dimensions are qualitative routing signals, not fake numeric precision.

## Trigger Vocabulary

### BEHAVIORAL

```text
new user/business behavior
changed validation
changed state transition
error/recovery behavior
multi-step workflow
browser-only interaction
```

Usually activates:

```text
relevant Code Review
QA
```

### ARCHITECTURE

```text
new module/service boundary
new port/adapter abstraction
new shared/global state ownership
new transaction owner
new event architecture
new deployment topology
new compatibility seam
```

Activates relevant Architecture Review.

### SECURITY

The change alters how the system decides who may do what:

```text
authentication or authorization logic
tenant-isolation rule
privilege or role
```

or it opens something new:

```text
public entry point
webhook
file upload/download
redirect/callback
third-party script/provider
rendering of user-generated HTML
IAM/network exposure
```

or it newly stores, logs or sends:

```text
sensitive/personal data
secret
analytics/privacy-relevant data
```

Activates Security unless an explicit specialist policy says review not required.

Do not activate merely because the code runs behind authentication or reads tenant-scoped data. A validated parameter added to an existing protected endpoint, with its access rules unchanged, is not a Security trigger. A one-line change to the access rule itself is.

### DATA_INTEGRITY

```text
database write semantics
financial/destructive operation
idempotency
concurrency
lost-update risk
schema constraint
data ownership
```

Usually activates:

```text
Backend Code Review
QA
```

and sometimes:

```text
Backend Architecture Review
Security
Infrastructure
```

### MIGRATION

```text
schema migration
dual read/write
backfill
compatibility facade
old/new version coexistence
platform migration
```

Usually activates:

```text
Architecture Review
QA
Infrastructure
```

plus Security/Performance if relevant.

### PERFORMANCE

```text
accepted latency/throughput/CWV/bundle/memory target
measured regression
large data growth
load/capacity requirement
known performance-sensitive path
```

Activates Performance.

Do not activate merely because code contains a loop.

### INFRASTRUCTURE

```text
IaC
CI/CD
cloud runtime
Kubernetes
new environment variable/secret
deployment strategy
health/readiness
backup/recovery
autoscaling
```

Activates Infrastructure.

### COMPATIBILITY

```text
public API change
event/schema version
mixed-version deployment
client/server rollout order
backward compatibility
```

Activates QA and appropriate Code/Architecture/Infrastructure gates.

### USER_IMPACT

```text
critical path
revenue/entitlement
destructive action
authentication
accessibility-critical interaction
```

Raises QA/review depth without automatically activating unrelated agents.

### OPERABILITY

```text
background job
queue/worker
reconciliation
alerting
runbook
startup/shutdown
recovery
```

May activate Infrastructure and Architecture Review.

## Risk Escalation

Routing may escalate when an agent discovers new scope.

Example:

```text
Backend Code Review
→ discovers tenant-boundary issue
→ SECURITY trigger activated
```

The router must support dynamic activation.

## Risk De-Escalation

Do not mechanically retain specialists after evidence proves they are not applicable.

Example:

```text
Performance trigger suspected
→ no target/symptom and specialist returns PERFORMANCE_REVIEW_NOT_REQUIRED
```

Record it as NOT_REQUIRED, not missing.

## Unknowns

Unknown material behavior should not be converted into risk guesses.

Use:

```text
PENDING_DECISION
PENDING_EVIDENCE
```

and route to the decision/evidence owner.
