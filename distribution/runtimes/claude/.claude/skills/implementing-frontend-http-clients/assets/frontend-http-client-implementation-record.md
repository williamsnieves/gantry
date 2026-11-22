# Frontend HTTP Client Implementation Record

## Context

- Change/repository:
- Existing HTTP abstraction:
- Transport library:
- Runtime: browser/server/isomorphic:
- Base URL policy:
- Authentication policy:
- Header policy:
- Retry policy:
- Cancellation policy:
- Runtime-validation policy:
- Observability policy:
- Security/privacy policy:
- Applicable `AGENTS.md`:
- Implemented by/date:

## Readiness

- Shared HTTP client required:
- Existing library approved:
- Auth policy known:
- Error taxonomy known:
- Retry policy known:
- Upload requirements:
- Streaming requirements:
- Initial decision:
- Conditions/blockers:

## HTTP API

```text

```

- Primary request method:
- Convenience methods:
- Response modes:
- Provider/business methods excluded:

## Request Contract

| Field | Type | Purpose |
|---|---|---|
| method | | |
| path/url | | |
| query | | |
| headers | | |
| body | | |
| signal | | |
| timeout | | |
| response mode | | |

- React/Domain/Use Case types excluded:
- Endpoint-specific semantics excluded:

## Base URL / Environment

- Base URL source:
- Environment handling:
- Feature code does not choose URL:
- Client/server differences:
- Secrets excluded from client bundle:

## Authentication

- Mechanism:
- Token/cookie provider:
- Request-time lookup:
- Public unauthenticated requests:
- Token rotation:
- Refresh policy:
- Infinite refresh loop prevented:
- Tokens redacted:

## Headers

| Header | Owner | Injected when |
|---|---|---|
| | HTTP client / adapter | |

- JSON Content-Type conditional:
- Multipart boundary not manually set:
- Sensitive headers redacted:

## Query / Body Serialization

- Arrays:
- booleans:
- null/undefined:
- dates:
- JSON:
- FormData:
- binary:
- Domain classes not serialized directly:

## Response Modes

| Mode | Behavior |
|---|---|
| json | |
| text | |
| empty | |
| blob | |
| arrayBuffer | |
| stream | |

## Decode Behavior

- Empty 2xx:
- Malformed JSON:
- Wrong content type:
- Body consumed once:
- Runtime validation owner:

## Error Taxonomy

| Condition | Stable kind | Metadata |
|---|---|---|
| network | NETWORK | |
| timeout | TIMEOUT | |
| 401 | UNAUTHENTICATED | |
| 403 | FORBIDDEN | |
| 404 | NOT_FOUND | |
| 409 | CONFLICT | |
| 429 | RATE_LIMITED | |
| 5xx | SERVER | |
| malformed payload | MALFORMED_RESPONSE | |
| cancellation | CANCELLED | |
| unknown | UNKNOWN | |

- Raw vendor errors excluded:
- Raw sensitive body excluded:
- Provider semantic mapping deferred to adapters:

## 401 / Auth Flow

- Policy:
- Refresh flow:
- Session invalidation owner:
- React/router behavior excluded:

## Cancellation

- Caller signal:
- Transport propagation:
- Timeout signal composition:
- Stable cancellation result:
- Cleanup:
- Vendor cancellation normalized:

## Retry

- Classification:
- Retryable methods:
- Retryable failures:
- Max attempts:
- Backoff:
- Jitter:
- Retry-After:
- Cancellation stops retries:
- Unsafe POST retry disabled:
- Idempotency requirement:
- Duplicate retry layers checked:

## Correlation / Observability

- Request/correlation ID:
- Propagation:
- Response ID:
- Duration:
- Method/status:
- Retry count:
- Sanitized path:
- Token/cookie/body redaction:
- Logger/telemetry owner:

## File Upload

- Required:
- Input:
- Multipart/binary:
- Content-Type behavior:
- Auth:
- Cancellation:
- Progress:
- Retry:
- Provider field names remain adapter-owned:

## Streaming

- Required:
- Stream type:
- Consumer contract:
- Chunk behavior:
- Cancellation:
- Cleanup:
- Decode owner:
- Provider semantic mapping remains adapter-owned:

## Server / Client Lifecycle

- Client classification:
- Browser singleton safe:
- Token lookup request-time:
- Server per-request context:
- Request/user mutable state not captured globally:
- Cookie/header propagation:

## Migration / Direct Fetch Exceptions

| Location | Raw fetch/vendor use | Decision | Reason |
|---|---|---|---|
| | | migrate / accepted isolated adapter | |

## Focused Tests

| Case | Expected |
|---|---|
| token injection | current token injected safely |
| token rotation | no stale capture |
| auth disabled | no auth header |
| abort signal | CANCELLED |
| malformed JSON | MALFORMED_RESPONSE |
| 401 | accepted unauthenticated policy |
| network failure | NETWORK |
| timeout | TIMEOUT |
| retryable GET | bounded retry |
| unsafe POST | no automatic retry |
| cancellation during backoff | stops retry |
| file upload | correct multipart/binary |
| streaming | chunks + cancellation |
| correlation/redaction | safe observability |

## Test Boundary

- Mock/test server:
- Transport substitution:
- Virtual clock:
- No arbitrary sleeps:
- Business mapping excluded:

## Security / Privacy Audit

- Token logging:
- Cookie logging:
- Query secrets:
- Body logging:
- PII:
- Server secrets:
- CORS assumptions:
- CSRF policy:
- Credential mode:

## Anti-Pattern Audit

- Feature-specific endpoint methods:
- Repository semantics in client:
- Domain mapping:
- React state:
- Router navigation:
- Toast/UI behavior:
- Provider schemas:
- Hidden retries:
- Global mutable interceptors:
- Vendor error leakage:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
