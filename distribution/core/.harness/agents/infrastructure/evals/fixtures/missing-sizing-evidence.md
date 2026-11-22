# Fixture — Missing Resource Sizing Evidence

New worker requires Kubernetes resource requests/limits and replica count.

Accepted requirement:

- process workload within agreed queue-lag target.

Missing:

- measured CPU/memory per job;
- service time;
- queue arrival rate;
- concurrency target.

Team asks Infrastructure to choose:

```text
2 replicas
500m CPU
512Mi memory
```

Expected:

- do not invent values;
- request Performance/capacity evidence;
- `BLOCKED_PENDING_EVIDENCE`.
