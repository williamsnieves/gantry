# Reviewer Decision Policy

Use exactly:

```text
READY_FOR_PRE_PR_GATE
READY_FOR_PRE_PR_GATE_WITH_CONDITIONS
NOT_READY_CHANGES_REQUIRED
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
```

## READY_FOR_PRE_PR_GATE

Use when:

- every required gate is present and fresh;
- all applicable normalized gates are PASS/NOT_REQUIRED;
- no specialist blocker exists;
- no unresolved decision/evidence blocker exists;
- no gate contradiction exists;
- no invalid waiver/condition exists.

## READY_FOR_PRE_PR_GATE_WITH_CONDITIONS

Use when:

- all blocking findings are cleared;
- all required gates are present/fresh;
- one or more specialist gates explicitly allow bounded non-blocking conditions;
- condition owner/verification/gate are clear;
- no condition conflicts with another gate.

## NOT_READY_CHANGES_REQUIRED

Use when at least one applicable specialist has proven that changes are required.

Examples:

```text
REQUEST_CHANGES
ARCHITECTURE_CHANGES_REQUIRED
CHANGES_REQUESTED
QA_CHANGES_REQUIRED
PERFORMANCE_CHANGES_REQUIRED
SECURITY_CHANGES_REQUIRED
INFRASTRUCTURE_CHANGES_REQUIRED
Validator FAIL
Detail Analyst NOT READY
```

Use this rather than pending evidence when the defect is already proven.

## BLOCKED_PENDING_DECISION

Use when there is no safe next remediation until an authoritative decision resolves.

Examples:

```text
product behavior
architecture choice
privacy policy
risk acceptance
deployment target
```

A concrete proven blocker elsewhere still takes precedence as `NOT_READY_CHANGES_REQUIRED`.

## BLOCKED_PENDING_EVIDENCE

Use when final integration cannot be completed because:

```text
required gate missing
required report stale
mandatory evidence unavailable
gate contradiction requires verification
change identity mismatch
```

## Precedence

```text
any proven change-required blocker
→ NOT_READY_CHANGES_REQUIRED

else any unresolved authoritative decision
→ BLOCKED_PENDING_DECISION

else any evidence/missing/stale/contradiction blocker
→ BLOCKED_PENDING_EVIDENCE

else any valid non-blocking condition
→ READY_FOR_PRE_PR_GATE_WITH_CONDITIONS

else
→ READY_FOR_PRE_PR_GATE
```

## No Majority Rule

One valid blocker is sufficient.

Reviewer cannot override a specialist decision by counting approvals.

## No Silent Waiver

A waiver/risk acceptance must have explicit authority and scope.

Reviewer records it but does not alter the original specialist verification status.
