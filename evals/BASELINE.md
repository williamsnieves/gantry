# Baseline

First live measurement of the harness, taken before any slimming or enforcement work. Later runs are compared against this.

- Harness: commit `bee4128` (v1 content with the integrity fixes and the Gantry rename).
- Runtime: Claude Code 2.1.330, model `claude-fable-5-2`, no user settings, memory or MCP servers.
- Date: 2026-11-22. One trial per scenario, so nothing here says how repeatable each result is.

| Scenario | Result | Plan follows template | Turns | Cost | Seconds |
|---|---|---|---|---|---|
| small-frontend | pass | yes | 10 | $0.79 | 51 |
| tiny-multitenant-auth | pass | yes | 13 | $0.92 | 66 |
| fullstack-medium | fail: Security made required | yes | 17 | $0.92 | 64 |
| schema-migration | fail: plan is not valid YAML | no | 13 | $1.03 | 83 |
| architecture-only | pass | yes | 14 | $0.98 | 82 |
| test-only-remediation | pass | yes | 9 | $0.77 | 53 |

Totals: 4 of 6 passed, no required gate was missed in any scored plan, $5.40, 398 seconds. Across the six trials the agent read about 1.8 million cached input tokens and wrote about 37,000 output tokens, only to decide which gates apply.

## What the failures show

**schema-migration.** The agent wrote `evidence: Incident gains required \`priority: number\`.` as an unquoted YAML value, which does not parse. The routing decision could not be read at all. A plan that is hand-written YAML can break on any colon in free text.

**fullstack-medium.** The agent required Security because the change adds a query parameter to an endpoint and rewrites the `where` clause of a tenant-scoped query. `RISK-TRIGGER-MODEL.md` lists "multi-tenancy" and "public entry point" as Security triggers, so the agent followed the contract. The scenario oracle says Security is not triggered for a medium full-stack feature with an API change. The contract and its own oracle disagree; this is not clearly an agent error.

## Other observations

- **Trigger entries have no defined shape.** The template shows `risk_triggers: []`. Every plan wrote mappings instead of names, with keys that vary between runs (`trigger`, `triggers`, `evidence`, `source`). The scorer reads the `dimension` key.
- **Scopes drift from the oracle vocabulary.** Two plans listed `SECURITY` as a scope, and one omitted `API_CONTRACT`.
- **No side effects.** No trial changed a file other than the routing plan, and every plan was written to the expected path.
