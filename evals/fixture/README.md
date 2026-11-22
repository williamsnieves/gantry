# Incident Desk

Small multi-tenant incident tracker used as a fixture for harness evaluations.

- `apps/api`: Node + TypeScript HTTP API, PostgreSQL through Prisma.
- `apps/web`: React + TypeScript client.

Every incident belongs to one tenant. Users only see and change incidents of their own tenant. Changing severity is restricted to the `commander` role.

```bash
npm test
npm run typecheck
npm run lint
```
