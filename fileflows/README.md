# FileFlows

Goal: Automate-simplify file conversions

## Docs

- [Extensions](docs/extensions.md)
- [Instance](../instance/fileflows/Readme.md)

## Installation

- - TrueNAS App: `fileflows`. Caddy: `FILEFLOWS_DOMAIN` → `FILEFLOWS_UPSTREAM` + Authentik FA
- DB: SQLite in `apps/fileflows/data` (no Postgres sidecar)
- Flow elements from plugins in `data/Plugins/*.ffplugin`
- Plugin catalog: `https://fileflows.com/api/plugin?version=<FileFlowsVersion>` (no `version` → 412)
- Env: `FF_EULA_ACCEPTED=Yes`. First-run must install plugins (Basic, Video, Image, …)
