# designing-software-system

End-to-end requirements + software architecture orchestrator.

Primary responsibility:

```text
select the smallest complete architecture-skill graph
```

Canonical flow:

```text
requirements
→ architecture drivers
→ candidate architectures
→ trade-offs
→ ADRs
→ selected models
→ STRIDE
→ architecture validation
→ accepted Architecture Package
→ OpenSpec / implementation planning
```

Do not run every skill mechanically.

Roadmap examples:

```text
Small internal CRUD
→ skip unnecessary event/state/DFD/deployment complexity

Payment platform
→ state + sequences + DFD + event + deployment + STRIDE + explicit reliability/security evidence
```

Output:

```text
software-system-orchestration-plan.md
```

This completes the Requirements Engineering + Software Architecture roadmap.
