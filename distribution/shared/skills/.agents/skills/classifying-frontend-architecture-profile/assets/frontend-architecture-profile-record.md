# Frontend Architecture Profile Record

## Context

- Change/capability:
- Classification scope: FEATURE / CAPABILITY / APPLICATION / PACKAGE / WORKSPACE
- Repository/workspace:
- Application/package:
- Owning team:
- Accepted behavior:
- Frontend standard application record:
- Applicable `AGENTS.md`:
- Existing architecture decisions:
- Classified by/date:

## Readiness

- Behavior scope:
- Ownership resolved:
- Authority resolved:
- Consumer evidence:
- Evolution constraints:
- Initial decision:
- Conditions/blockers:

## Current Architecture

- Current profile:
- Current folder shape:
- Capability ownership:
- Public entry points:
- State/data strategy:
- Rendering model:
- Test boundaries:
- Deployment/release boundary:
- Current pain or risk:

## Behavior and Complexity

- User intentions:
- Client-owned invariants:
- State transitions:
- Offline behavior:
- Optimistic behavior:
- Reconciliation/conflicts:
- Undo/redo/editor lifecycle:
- Shared UI surfaces:
- Complexity: LOW / MODERATE / HIGH
- Evidence:

## Authority

- Classification: SERVER_AUTHORITATIVE / CLIENT_AUTHORITATIVE / SHARED_OR_RECONCILED_AUTHORITY / PRESENTATIONAL_ONLY / UNKNOWN
- Server-owned rules:
- Client-owned rules:
- Reconciled state:
- Duplication risk:
- Decision required:

## Consumers and Ownership

| Consumer | Real/committed/speculative | Required contract | Owner |
|---|---|---|---|
| | | | |

- Reuse classification:
- Platform boundary:
- Public package need:
- Independent release/versioning:
- Deep-import risk:

## Domain Layer Decision

- Status:
- Candidate rules/state:
- Why Domain is required or not justified:
- Pure testability:
- Backend-authority duplication risk:
- Conditions:

## Application Layer Decision

- Status:
- User intentions:
- React-independent orchestration:
- Shared UI entry points:
- Cancellation/failure needs:
- Conditions:

## Port and Adapter Decision

| Dependency | Semantic boundary | Port justified | Adapter owner |
|---|---|---|---|
| | | | |

- Generic/technical abstractions rejected:
- Existing shared infrastructure reused:

## Profile Comparison

| Dimension | Profile A fit | Profile B fit | Profile C fit | Evidence |
|---|---|---|---|---|
| Business/client rules | | | | |
| Consumers | | | | |
| Authority | | | | |
| Offline/reconciliation | | | | |
| Public contracts | | | | |
| Independent evolution | | | | |
| Test boundaries | | | | |
| Deployment/versioning | | | | |

## Overengineering Challenge

- Ceremonial Domain/Application layers:
- One-call Use Case:
- Generic ports:
- Speculative shared/package extraction:
- Unneeded factories/indirection:
- Backend-shape mimicry:

## Under-Structuring Challenge

- Rules trapped in components/hooks:
- Duplicated intentions:
- Browser/provider leakage:
- Pure behavior only testable through UI:
- Shared state with unclear ownership:
- Package/application deep imports:

## Selected Profile

- Selection:
- Confidence:
- Rationale:
- Why lighter profile is insufficient:
- Why heavier profile is unnecessary:

## Required Structure and Boundaries

```text

```

- Required folders:
- Public entry points:
- Dependency direction:
- Feature-local boundaries:
- Package boundaries:
- Test boundaries:
- Explicitly unnecessary folders:

## Current-to-Target Delta

- Migration decision:
- Files/capability affected:
- Compatibility:
- Unrelated structure excluded:
- Conditions:

## Deferred Complexity

| Not justified now | Reason |
|---|---|
| | |

## Scaling Triggers

| Trigger | Profile/boundary to reconsider | Evidence required |
|---|---|---|
| | | |

## Deviations

| Deviation | Scope | Risk | Owner | Exit condition |
|---|---|---|---|---|
| | | | | |

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
