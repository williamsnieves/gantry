# validating-frontend-architecture

Validates implemented frontend code against its already selected architecture profile.

It checks:

```text
dependency direction
feature boundaries
public surfaces
shared ownership
composition
server/client separation
package boundaries
cycles
architecture automation
```

It is profile-aware: Profile A remains lightweight, while Profile B/C add stronger layer and package rules.

The skill reports objective evidence, severity, automation gaps, and smallest remediation targets without redesigning the repository or introducing new tooling.
