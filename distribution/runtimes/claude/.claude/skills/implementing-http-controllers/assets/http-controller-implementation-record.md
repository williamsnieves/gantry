# HTTP Controller Implementation Record

## Context

- Change ID:
- Endpoint:
- Framework:
- Controller/handler:
- Use Case:
- Application Request DTO:
- Application Response DTO:
- Public contract/schema:
- Authentication policy:
- Error mapping owner:

## Readiness

- Route/method resolved:
- Success response resolved:
- Error contract resolved:
- Auth/tenant boundary resolved:
- Idempotency resolved:
- Conditions/blockers:

## HTTP Contract

- Method:
- Path:
- Version:
- Content type:
- Success status:
- Success body:
- Headers:
- Async semantics:

## Transport Inputs

| Source | Field | Type/shape | Required | Application field |
|---|---|---|---|---|
| | | | | |

## Trusted Context

- Actor:
- Tenant:
- Roles/scopes:
- Correlation:
- Idempotency:
- Untrusted fields rejected:

## Request Mapping

1.
2.
3.

## Use Case Invocation

- Use Case:
- Invocation count:
- Dependencies called directly by controller:
- Expected result:

## Success Mapping

| Application result | HTTP status | Body | Headers |
|---|---|---|---|
| | | | |

## Error Mapping

| Semantic condition | HTTP status | Public code/body | Logging |
|---|---|---|---|
| | | | |

## Security Review

- Authentication:
- Operation authorization owner:
- Tenant spoofing:
- Body/query limits:
- Mass assignment:
- Sensitive data:
- CSRF/CORS/rate limit ownership:
- Error redaction:

## Tests

| Test | Level | Expected evidence |
|---|---|---|
| | | |

## Schema and Compatibility

- OpenAPI/schema updated:
- Required/optional/nullability:
- Consumer compatibility:
- Generated artifacts:
- Version/deprecation:

## Thinness Audit

- Repository calls:
- Provider calls:
- Domain mutation:
- Business validation:
- Transaction ownership:
- Use Case chaining:
- Technical error parsing:

## Final Status

- Decision:
- Remaining blockers:
- Residual risks:
- Required follow-up:
