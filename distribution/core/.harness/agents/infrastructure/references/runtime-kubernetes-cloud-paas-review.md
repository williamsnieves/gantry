# Runtime, Kubernetes, Cloud, and PaaS Review

## Runtime

Check:

```text
startup
shutdown
health
configuration
secrets
resource use
network exposure
logs/metrics
```

## Kubernetes

Only when present.

Inspect relevant:

```text
workload controller
Service/Ingress/Gateway
ServiceAccount/RBAC
ConfigMap/Secret
resources
probes
security context
network policy
rollout
termination
autoscaling
storage
```

Do not add every Kubernetes primitive.

## Cloud

Review actual accepted provider/service.

Do not substitute AWS/GCP/Azure services by preference.

Check actual:

```text
IAM
network
region/residency
service limits
backup/recovery
logging
runtime config
```

## PaaS

Vercel/Railway/etc. still have infrastructure semantics:

```text
environment variables
preview/prod separation
build/runtime settings
domains
deployment protection
logs
rollback
persistent-state limitations
background-job limitations
```

Platform convenience does not eliminate operational risk.
