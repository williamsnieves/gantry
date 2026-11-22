# modeling-event-flows

Models accepted event-driven/asynchronous interactions.

Core:

```text
producer
→ event
→ consumer
```

Roadmap-required semantics:

```text
delivery
ordering
retries
deduplication
dead-letter behavior
schema/versioning
ownership
```

Core rule:

```text
event-driven
≠ Kafka
≠ exactly-once
≠ event sourcing
≠ CQRS
```

Output:

```text
event-flow-model.md
```

Next roadmap skill:

```text
modeling-deployment-architecture
```
