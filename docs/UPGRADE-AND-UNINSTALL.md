# Upgrade and Uninstall

## Managed-file state

The CLI stores:

```text
.harness/install-state.json
```

with every harness-owned file and its SHA-256.

This lets `gantry` distinguish:

```text
safe managed upgrade
local modification
unmanaged existing project file
```

## Upgrade model

For v1, reinstall the newer distribution with the same runtime selection.

If a managed file was locally edited, the installer refuses to overwrite it unless `--force` is used.

## Runtime uninstall

Example:

```bash
./gantry.sh uninstall --runtime cursor --project .
```

This removes only files owned by the Cursor runtime overlay.

Shared core and skills remain for other runtimes.

## Full uninstall

```bash
./gantry.sh uninstall   --runtime all   --purge-shared   --project .
```

Locally modified managed files are preserved unless `--force` is supplied.
