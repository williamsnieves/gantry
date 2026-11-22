# Frontend Adapter Testing Record

## Context

- Adapter:
- Port:
- Repository/application:
- External/storage system:
- Approved HTTP/storage abstraction:
- Runtime validation:
- Auth/refresh policy:
- Cancellation policy:
- Offline policy:
- IndexedDB/storage version:
- Provider sandbox/emulator:
- Test runner:
- Applicable `AGENTS.md`:
- Tested by/date:

## Boundary Strategy

- Strategy: MSW / TEST_SERVER / CONTRACT_FIXTURE / BROWSER_STORAGE_RUNTIME / INDEXEDDB_EMULATOR_OR_REAL_BROWSER / PROVIDER_EMULATOR / PROVIDER_SANDBOX / OTHER
- Why:
- Real adapter is SUT:
- Adapter mocked:
- Fetch internals mocked:
- Faithfulness limitations:

## Port Semantics

| Operation | Success | Absence | Stable failures | Cancellation |
|---|---|---|---|---|
| | | | | |

## External Contract

- Endpoint/store:
- Method/operation:
- Request type:
- Response/storage type:
- Runtime schema:
- Version:
- Provider enums:
- Date formats:
- Nullability:
- Pagination:

## Request Mapping

| Input | External representation | Evidence |
|---|---|---|
| | | |

- Path:
- Method:
- Query:
- Body:
- Headers:
- Tenant/resource identifiers:
- Sensitive header logging avoided:

## Inbound Mapping

| External field | Inward field/value | Mapping rule |
|---|---|---|
| | | |

- Raw payload leakage:
- Provider enum leakage:
- Invalid date policy:
- Unknown enum policy:
- Null/missing policy:

## 404 Roadmap Case

- Endpoint/operation:
- External 404:
- Port semantic:
- Result/error:
- Why not global undefined mapping:
- Evidence:

## Malformed Payload Roadmap Case

- Malformed fixture:
- JSON decode vs schema mismatch:
- Runtime validation:
- Stable error:
- Invalid data crosses inward:
- Evidence:

## Error Matrix

| Technical event | Stable inward semantic | Covered |
|---|---|---|
| 401 | | |
| 403 | | |
| 404 | | |
| 409 | | |
| 429 | | |
| 5xx | | |
| network/offline | | |
| timeout | | |
| cancellation | | |
| malformed payload | | |
| corrupt storage | | |

## Cancellation

- Accepted signal:
- Propagated through:
- Technical abort:
- Stable cancellation:
- Distinct from timeout/network:
- Arbitrary delay/sleep:
- Evidence:

## Auth Refresh Roadmap Case

- Applicable:
- Owner: HTTP_CLIENT / ADAPTER / SESSION_LAYER
- Initial 401:
- Refresh:
- Retry:
- Refresh failure:
- Max retry:
- Infinite loop prevented:
- Concurrent refresh behavior:
- Cancellation during refresh:
- Adapter-specific coverage vs HTTP-client detailed coverage:

## Offline Roadmap Case

- Applicable:
- Offline semantic: OFFLINE_WITH_LOCAL_DATA / OFFLINE_NO_DATA / OFFLINE_QUEUED / OFFLINE_UNAVAILABLE / PROJECT_EQUIVALENT
- Authoritative source:
- Local provisional state:
- Queue:
- Ordering:
- Duplicate prevention:
- Reconciliation owner:
- Pure remote behavior:
- Evidence:

## Browser Storage

- Applicable:
- Storage:
- Key:
- Serialization:
- Missing:
- Corrupt JSON:
- Schema version:
- Quota/unavailable:
- SSR unavailable:
- Cleanup:
- Trusted/untrusted validation:

## IndexedDB Roadmap Case

- Applicable:
- Runtime: real browser / fake-indexeddb / emulator / other approved
- DB name/version:
- Object stores:
- Round trip:
- Missing record:
- Mapping:
- Date/enum/null:
- Migration:
- Corrupt/legacy:
- Transaction failure:
- Atomicity:
- Blocked upgrade:
- Connection cleanup:
- Plain-object mock avoided:

## Provider Sandbox Roadmap Case

- Applicable:
- Provider:
- Sandbox/test project:
- Credentials source:
- Production credentials used:
- Test resource namespace:
- Seed/create:
- Cleanup:
- Stable provider shape verified:
- Stable auth verified:
- Error case:
- Contract drift detection:
- CI trigger:
- Network/rate-limit/cost policy:
- Status: SANDBOX_NOT_CONFIGURED / SANDBOX_SKIPPED_BY_POLICY / SANDBOX_AVAILABLE / SANDBOX_UNAVAILABLE / SANDBOX_CONTRACT_PASS / SANDBOX_CONTRACT_FAIL

## Shared Port Contract Suite

- Multiple implementations:
- Shared semantic suite:
- Implementations:
- Absence:
- Stable errors:
- Ordering/pagination:
- Cancellation:
- Provider leakage:
- Technical behavior kept adapter-specific:

## Test Layering

| Behavior | Boundary |
|---|---|
| pure mapper | mapper unit |
| HTTP integration | MSW/test server |
| storage lifecycle | browser/emulator |
| provider compatibility | sandbox |
| Application orchestration | Use Case test |
| hook/cache state | hook/server-state test |
| UI interaction | component test |

## Security / Privacy

- Test-only tokens:
- Production resources:
- PII in fixtures:
- Sensitive logs:
- Sensitive storage:
- Sanitized provider errors:

## Isolation / Cleanup

- MSW handlers reset:
- Server stopped:
- DB deleted/reset:
- Storage cleared:
- Open IndexedDB connections closed:
- Sandbox resources removed:
- Parallel resource collision avoided:

## Roadmap Evaluation Summary

### 404
- Result:
- Evidence:

### Malformed Payload
- Result:
- Evidence:

### Auth Refresh
- Result:
- Evidence:

### Offline State
- Result:
- Evidence:

### IndexedDB Mapping
- Result:
- Evidence:

### Provider Sandbox
- Result:
- Evidence:

## Execution Evidence

- Focused command:
- Result:
- Adapter suite:
- Result:
- Browser/storage suite:
- Result:
- Sandbox suite:
- Result:
- Duration:
- Flakiness:

## Over/Under-Testing Audit

- Adapter mocked:
- Fetch mocked instead of MSW:
- Plain object as IndexedDB:
- Happy path only:
- Missing malformed payload:
- Missing cancellation:
- Missing storage migration:
- Sandbox overused:
- Sandbox missing where critical:
- Decision: FAITHFUL_ADAPTER_TEST_BOUNDARY / OVERMOCKED_ADAPTER_TEST / BOUNDARY_TOO_EXPENSIVE / SANDBOX_POLICY_REQUIRED

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
