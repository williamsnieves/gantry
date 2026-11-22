# Infrastructure Decision Policy

Use exactly:

```text
INFRASTRUCTURE_APPROVED
INFRASTRUCTURE_APPROVED_WITH_CONDITIONS
INFRASTRUCTURE_CHANGES_REQUIRED
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
INFRASTRUCTURE_REVIEW_NOT_REQUIRED
```

## INFRASTRUCTURE_APPROVED

Use when:

- infrastructure implementation aligns with accepted architecture;
- deployment mechanics are safe enough;
- required security/performance constraints are respected;
- rollback/recovery is adequate for scope;
- required operational evidence is available;
- no blocking drift/manual hidden state remains.

## INFRASTRUCTURE_APPROVED_WITH_CONDITIONS

Use for bounded non-blocking operational conditions explicitly allowed by policy.

Examples:

- production observation required after staged rollout;
- temporary manual step with named owner and removal trigger;
- non-blocking alert/dashboard completed before full traffic;
- restore drill required before a later production milestone.

Conditions must be explicit and verifiable.

## INFRASTRUCTURE_CHANGES_REQUIRED

Use when infrastructure/pipeline/runtime implementation itself must change.

Typical reasons:

- unsafe CI secret exposure;
- excessive deployment permissions;
- destructive IaC action not accepted;
- public exposure contradicts architecture/security;
- wrong environment/artifact can be deployed;
- migration order unsafe;
- no safe rollout/rollback for required risk level;
- health/readiness configuration causes unsafe traffic;
- accepted topology not implemented;
- resource/configuration evidence demonstrates operational failure.

## BLOCKED_PENDING_DECISION

Use when infrastructure cannot be reviewed because an authoritative architecture/product/security decision is unresolved.

Examples:

- target cloud/runtime undecided;
- region/residency undecided but required now;
- rollout strategy depends on unresolved compatibility requirement;
- acceptable downtime/rollback policy unknown;
- architecture must decide queue/cache/store topology.

Do not choose silently.

## BLOCKED_PENDING_EVIDENCE

Use when required operational evidence is unavailable.

Examples:

- IaC plan unavailable;
- CI execution artifact unavailable;
- production runtime config inaccessible;
- required rollback/restore evidence missing;
- security IAM evidence unavailable;
- performance sizing evidence required but absent.

## INFRASTRUCTURE_REVIEW_NOT_REQUIRED

Use when no material infrastructure/delivery surface is affected and policy does not require this gate.

## Precedence

```text
demonstrable unsafe infrastructure change
→ INFRASTRUCTURE_CHANGES_REQUIRED

otherwise unresolved authoritative decision
→ BLOCKED_PENDING_DECISION

otherwise mandatory evidence unavailable
→ BLOCKED_PENDING_EVIDENCE

otherwise bounded permitted conditions
→ INFRASTRUCTURE_APPROVED_WITH_CONDITIONS

otherwise review not triggered
→ INFRASTRUCTURE_REVIEW_NOT_REQUIRED

otherwise
→ INFRASTRUCTURE_APPROVED
```
