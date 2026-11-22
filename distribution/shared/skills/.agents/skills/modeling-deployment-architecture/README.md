# modeling-deployment-architecture

Models runtime topology and infrastructure placement.

Roadmap-required concerns:

```text
regions / zones
compute
load balancers / gateways
databases
queues
object stores
caches
external providers
network / trust boundaries
observability
secrets
failover
```

Core rule:

```text
C4
→ logical runtime structure

Deployment
→ where/how that structure runs
```

Do not invent infrastructure to make a diagram look complete.

Output:

```text
deployment-architecture-model.md
```

With this skill, Phase D — Architecture diagrams/models is complete.

Next roadmap phase:

```text
Phase E — Security + architecture validation
19. reuse threat-modeling-with-stride
20. validating-architecture-design
```
