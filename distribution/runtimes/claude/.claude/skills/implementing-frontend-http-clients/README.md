# implementing-frontend-http-clients

Implements or evolves the approved frontend HTTP abstraction inside Infrastructure.

It covers the roadmap evaluations:

```text
token injection
abort signal
malformed JSON
401 handling
retry policy
file upload
streaming response
```

It also handles base URL, common headers, decoding, stable transport errors, correlation IDs, safe observability, server/client lifecycle, timeouts, status normalization, and migration from repeated raw fetch.

It does not perform repository mapping, Domain logic, runtime provider-schema validation, React state, navigation, or server-state caching.
