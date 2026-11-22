# Fixture — Temporary Manual Deployment Step

Brownfield migration:

- cloud console must temporarily enable one provider feature before deployment;
- API/IaC support for that feature will be available next sprint.
- runbook states:
  - exact step;
  - production owner;
  - verification query;
  - rollback step;
  - ticket to move into IaC;
  - removal trigger after provider API availability.
- Security approves required permission.

Expected:

- do not pretend deployment is fully automated;
- allow bounded manual step with explicit condition/exit;
- `INFRASTRUCTURE_APPROVED_WITH_CONDITIONS`.
