# designing-frontend-ports

Designs frontend ports around what Domain/Application needs, not provider or browser mechanics.

It covers:

```text
Domain vs Application ownership
repositories
remote data
browser persistence
analytics
clipboard
files
notifications
geolocation
clock / IDs / connectivity
cache semantics
offline sync
subscriptions
errors / not found
cancellation / races
security / privacy
test doubles
```

It prevents endpoint mirroring, generic getJson/request APIs, localStorage/IndexedDB leakage, provider SDK types, analytics `any` payloads, cache-library metadata, vendor cancellation tokens, and god browser-capability interfaces.
