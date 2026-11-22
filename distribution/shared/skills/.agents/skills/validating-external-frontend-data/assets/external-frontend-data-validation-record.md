# External Frontend Data Validation Record

## Context

- Change/capability:
- Repository/application:
- Architecture profile:
- External source:
- Provider/transport contract:
- HTTP/decode boundary:
- Adapter/repository:
- Application/Domain target:
- Existing validation library:
- Versioning:
- Observability/privacy policy:
- Applicable `AGENTS.md`:
- Designed/implemented by/date:

## Readiness

- External contract known:
- Trust level known:
- Structural importance known:
- Validation policy known:
- Version policy known:
- Error policy known:
- Privacy policy known:
- Initial decision:
- Conditions/blockers:

## Validation Decision

- Decision: VALIDATE_REQUIRED / VALIDATE_RECOMMENDED / VALIDATE_OPTIONAL / RUNTIME_VALIDATION_NOT_REQUIRED / UNKNOWN_REQUIRES_DECISION
- Model status: PROPORTIONATE_VALIDATION / UNDERVALIDATED_BOUNDARY / OVERVALIDATED_BOUNDARY / RUNTIME_VALIDATION_NOT_REQUIRED
- Why:
- Risk if malformed:
- Existing trusted validator upstream:
- Duplicate validation avoided:

## Source Classification

| Source | Trust | Mutation/version risk | Structural importance |
|---|---|---|---|
| API/BFF | | | |
| Third-party SDK | | | |
| localStorage/IndexedDB | | | |
| postMessage | | | |
| imported file/JSON | | | |
| remote config | | | |

## Boundary

```text
external unknown
→ decode
→ validate
→ typed transport contract
→ map
→ Application / Domain
```

- Decode owner:
- Validation owner:
- Mapping owner:
- Schema module:
- Feature schema excluded from common HTTP client:

## External Contract

```text

```

| Field | External type | Required/null/optional | Notes |
|---|---|---|---|
| | | | |

- Provider casing preserved:
- Provider enum values preserved:
- Pagination/version envelope:
- Application semantics not mixed in:

## Unknown Fields

- Policy: ALLOW_UNKNOWN_FIELDS / STRIP_UNKNOWN_FIELDS / REJECT_UNKNOWN_FIELDS / PRESERVE_UNKNOWN_FOR_FORWARD_COMPAT
- Reason:
- Additive API compatibility:
- Security-sensitive exceptions:

## Missing / Null / Optional

| Field | Missing | Null | Empty | Mapping result |
|---|---|---|---|---|
| | | | | |

- Required fields not weakened:
- Defaults:
- Default owner:
- Coercion:

## Enums

| External enum | Known values | Unknown policy | Inward mapping |
|---|---|---|---|
| | | CONTRACT_MISMATCH / MAP_TO_UNKNOWN / PRESERVE_UNKNOWN_VALUE / VERSION_FALLBACK | |

- Silent casts excluded:

## Dates / Numbers

- Timestamp primitive:
- Parseability requirement:
- Timezone:
- Number/integer constraints:
- Finite:
- Unit:
- Business ranges deferred to Domain/backend:

## Versioning

- Version field:
- Known versions:
- Current version:
- Unknown version behavior:
- Backward compatibility:
- Migration owner:

### Migration Flow

```text
raw unknown
→ version detect
→ version-specific validate
→ migrate
→ current contract
→ map inward
```

## Persisted Browser Data

- Applicable:
- Storage source:
- Old-version risk:
- User/extension mutation risk:
- Partial-write risk:
- Schema/version:
- Migration:
- Invalid persisted data recovery:

## postMessage

- Applicable:
- Allowed origin/source policy:
- Message discriminator:
- Payload schema:
- Version:
- Origin validation separate from schema validation:
- Invalid-message behavior:

## Imported/User Data

- Applicable:
- File/JSON type:
- Parse limits:
- Version:
- Structure:
- Sensitive content:
- Full payload logging prohibited:

## HTML / URLs / Security-Sensitive Strings

- External HTML:
- Sanitization required separately:
- External URLs:
- Allowlist/security review:
- Validation not treated as XSS/security proof:

## Library Policy

- Existing library:
- Reused:
- New library introduced:
- If none, custom validator justification:
- Validator-specific errors kept Infrastructure-local:
- No global schema framework introduced:

## Failure Semantics

| Failure | Stable semantic |
|---|---|
| malformed JSON | HTTP-client/decode failure |
| schema mismatch | CONTRACT_MISMATCH / MALFORMED_EXTERNAL_DATA |
| unsupported version | UNSUPPORTED_VERSION |
| unknown enum | |
| invalid persisted data | |

- Raw validator error not exposed:
- Raw provider payload not exposed:
- Domain/Application object creation prevented:

## Observability

- Source/category:
- Schema/version:
- Field path:
- Expected type:
- Received type only:
- Correlation ID:
- App version:
- Full payload logging:
- PII/secrets redacted:
- User-facing details excluded:

## Performance

- Payload size:
- Frequency:
- Schema complexity:
- Full vs partial validation:
- Revalidation duplication:
- Lazy validation justified:
- Validation cache required:
- Measurement evidence:

## Mapping

| External field | Validated transport type | Inward field/type |
|---|---|---|
| | | |

- Validation before mapping:
- Provider semantics stay outward:
- Domain validation remains separate:

## Focused Tests

| Case | Expected |
|---|---|
| valid payload | accepted and mapped |
| missing required field | contract mismatch |
| wrong primitive | contract mismatch |
| null vs missing | policy preserved |
| unknown field | configured policy |
| unknown enum | configured policy |
| malformed nested object | mismatch |
| unsupported version | unsupported version |
| legacy version | validate + migrate |
| safe observability | no raw sensitive payload |

## Contract Drift

- Provider drift history:
- Mismatch telemetry:
- Escalation owner:
- Schema weakening prohibited without decision:
- Compatibility strategy:

## Over/Undervalidation Audit

- Type assertion after JSON:
- unchecked localStorage:
- unchecked postMessage:
- provider enum cast:
- `any` into component:
- duplicate validation across layers:
- giant unused schema:
- strict unknown rejection without need:
- fallback `{}`:
- internal constants unnecessarily validated:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
