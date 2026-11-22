# validating-external-frontend-data

Decides when frontend runtime validation is necessary and validates external contracts before mapping them inward.

Typical flow:

```text
external unknown
→ decode
→ runtime validate
→ typed transport contract
→ map
→ Application / Domain
```

It covers APIs/BFFs, third-party SDKs, localStorage/IndexedDB, postMessage, imported files, remote config, contract versioning, enum drift, safe errors, redacted observability, validation-library policy, performance, and migrations.

It explicitly rejects treating TypeScript assertions as runtime validation and does not introduce a new schema library when the repository already has an approved one.
