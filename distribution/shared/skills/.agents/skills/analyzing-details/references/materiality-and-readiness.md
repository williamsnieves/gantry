# Materiality and Readiness

Materiality levels:

- Blocking: prevents safe implementation, review, release, synchronization, or archival.
- High: likely to cause incorrect behavior, security exposure, data problems, compatibility failure, or major rework.
- Medium: bounded defect, incomplete behavior, operational gap, or maintenance risk.
- Low: localized incompleteness with limited impact.
- Informational: non-blocking observation or strength.

Confidence is High, Medium, or Low.

Readiness:

- Ready: no blocking or high-materiality unresolved detail remains.
- Conditionally ready: only bounded, owned, non-blocking details remain.
- Not ready: authoritative sources conflict, required behavior is missing, affected layers are unknown, or material questions remain.
