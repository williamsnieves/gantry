# Frontend Security Review Record

## Context

- Application/feature:
- Repository:
- Framework/version:
- Rendering model:
- Auth/session model:
- Backend authorization model:
- Threat model:
- Application-security review:
- Control baseline:
- Applicable `AGENTS.md`:
- Reviewer/date:

## Scope

- Included:
- Excluded:
- Browser origins:
- Third parties:
- Sensitive data:
- Privileged actions:
- Evidence available:
- Blockers:

## Browser Attack Surface

| Surface | Untrusted source | Sensitive sink/action | Trust boundary |
|---|---|---|---|
| | | | |

## Findings

| ID | Status | Severity | Surface | Required handoff |
|---|---|---|---|---|
| | | | | |

### FE-SEC-001 — [Title]

- Status: CONFIRMED / LIKELY_REQUIRES_VALIDATION / DEFENSE_IN_DEPTH / FALSE_POSITIVE / NOT_APPLICABLE
- Surface:
- Source:
- Sink/storage/action:
- Attacker control:
- Preconditions:
- Exploit path:
- Impact:
- Frontend root cause:
- Required frontend remediation:
- Required backend/infra remediation:
- `reviewing-application-security` required:
- STRIDE threat:
- Control verification:
- Evidence:
- Negative test:
- Residual risk:

## Roadmap Evaluation — dangerouslySetInnerHTML

- Occurrences:
- Data source:
- Attacker-controlled:
- Sanitizer:
- Sanitizer policy:
- Rendering context:
- URL protocols:
- SVG/MathML:
- Post-sanitization mutation:
- CSP:
- Malicious fixture:
- Result:

## Roadmap Evaluation — localStorage Token

- Token in localStorage:
- Token type:
- Bearer/replayable:
- Lifetime:
- Scope:
- Refresh token:
- Rotation:
- Logout/revocation:
- XSS exposure:
- Third-party script exposure:
- Alternative session architecture:
- Accepted risk:
- Result:

## Roadmap Evaluation — Secret Environment Variable

| Variable | Client-visible | Intended public | Secret privilege | Result |
|---|---|---|---|---|
| | | | | |

- Build bundle inspected:
- Runtime config inspected:
- Source maps:
- Server-only secret location:
- Logging:
- Result:

## Roadmap Evaluation — Redirect Handling

- Input:
- Source: query / API / storage / provider
- Destination policy:
- Same-origin/internal:
- Structural URL parsing:
- Allowlist:
- Dangerous schemes:
- Protocol-relative URLs:
- OAuth/OIDC:
- Negative external-host test:
- Result:

## Roadmap Evaluation — File Upload

- Accepted file types:
- Client size check:
- Client MIME:
- Filename rendering:
- Preview:
- SVG/HTML active content:
- Object URL:
- Metadata:
- Server size enforcement:
- Server content validation:
- Storage ACL:
- Download authorization:
- Parser/resource limits:
- Frontend checks treated as UX:
- Result:

## Roadmap Evaluation — Third-Party Script

- Provider/script:
- Purpose:
- Origin:
- Dynamic/static:
- User-controlled URL:
- Version/change control:
- DOM access:
- Storage/token access:
- Sensitive data access:
- CSP:
- SRI:
- iframe/sandbox option:
- Consent/privacy handoff:
- Failure behavior:
- Supply-chain review:
- Result:

## XSS / DOM Sink Inventory

| Sink | Source | Sanitized/escaped | Exploitability |
|---|---|---|---|
| | | | |

- innerHTML:
- outerHTML:
- insertAdjacentHTML:
- document.write:
- DOMParser:
- markdown/raw HTML:
- URL sinks:
- eval/new Function:
- framework escaping relied upon:

## Sensitive Data Exposure

- Hydration payload:
- API overfetching:
- browser storage:
- DOM:
- URL/query/hash:
- source maps:
- console logs:
- telemetry:
- provider credentials:
- internal stack traces:
- private IDs:

## Authentication / Session Boundary

- Cookie/session:
- HttpOnly:
- Secure:
- SameSite:
- browser-readable token:
- URL token:
- logout cleanup:
- query cache cleanup:
- shared-device persistence:
- CSRF model:
- Required backend handoff:

## Authorization Boundary

| Capability | Frontend UX check | Server authority evidence | Result |
|---|---|---|---|
| | | | |

- Route guards:
- Hidden/disabled controls:
- Client-controlled role:
- Tenant identifier:
- Resource ownership:
- Cache tenant dimension:
- Backend authorization required:

## Redirect / Navigation Inventory

| Source | Destination sink | Policy | Negative test |
|---|---|---|---|
| | | | |

## postMessage / iframe / popup

- Applicable:
- targetOrigin:
- event.origin:
- event.source:
- runtime schema:
- sandbox:
- allow permissions:
- sensitive data:
- privileged action:

## Browser Storage

| Store | Data | Sensitive | Runtime validated | Cleanup |
|---|---|---|---|---|
| localStorage | | | | |
| sessionStorage | | | | |
| IndexedDB | | | | |
| service worker cache | | | | |

## CSP / Browser Security Mechanisms

- CSP:
- script-src:
- unsafe-inline:
- unsafe-eval:
- object-src:
- base-uri:
- frame-ancestors:
- Trusted Types:
- Referrer-Policy:
- defense-in-depth only:
- verification handoff:

## Dependency / Runtime Supply Chain

- Runtime third-party scripts:
- CDN dependencies:
- HTML sanitizer dependency:
- package executing sensitive browser behavior:
- abandoned/unmaintained:
- lockfile/trusted registry:
- generic SCA handoff:

## Application Security Handoff

| Frontend finding | OWASP/CWE classification needed | Root cause |
|---|---|---|
| | | |

## Control Verification Handoff

| Control | Evidence required |
|---|---|
| | |

## Threat Model Handoff

- New trust boundary:
- New provider:
- New cross-origin flow:
- New auth flow:
- Threat model update:

## Security Tests

| Risk | Boundary | Negative fixture |
|---|---|---|
| | unit/component/browser/E2E | |

## Over/Under-Review Audit

- all env vars treated secret:
- all unsafe HTML auto-failed:
- all localStorage auto-critical:
- route guard treated as auth:
- true secret shipped:
- unsafe redirect:
- long-lived token ignored:
- arbitrary script URL:
- active upload preview:
- Decision: PROPORTIONATE_FRONTEND_SECURITY_REVIEW / OVERCLASSIFIED_FRONTEND_RISK / FRONTEND_SECURITY_REVIEW_TOO_GENERIC

## Final Decision

- Decision:
- Critical findings:
- Required frontend remediation:
- Required backend/infra remediation:
- Required application-security classification:
- Required control verification:
- Required threat-model update:
- Residual risk:
