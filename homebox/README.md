# HomeBox

Goal: Home inventory. SSO = Authentik only.

## Docs

- [SSO](docs/sso.md)
- [Deploy](docs/deploy.md)
- [Instance](../instance/homebox/Readme.md)

## Installation

- TrueNAS App: `homebox`.
- Secrets: [Main](../instance/homebox/.env). [OIDC](../instance/homebox/.env.oidc)
- [Caddy](../instance/caddy/.env): `HOMEBOX_DOMAIN` → `HOMEBOX_UPSTREAM` (`host.docker.internal:{WebUI port}`).
  WebUI port = `30149`..

## Scripts

Generic:

| Path | What | Args |
|---|---|---|
| `caddy/scripts/ensure-env.py` | Add missing `instance/caddy/.env` keys | `HOMEBOX_DOMAIN=…` `HOMEBOX_UPSTREAM=host.docker.internal:30149` |
| `.cursor/skills/truenas-scale/scripts/ensure-datasets.sh` | HostPath + perms | `dataset` or `dataset:uid:gid:mode` |
| `.cursor/skills/truenas-scale/scripts/catalog-install.py` | Catalog install/update | `--app` `--train` `--version` `--values` |

HomeBox (values from `instance/homebox/.env` + `.env.oidc`):

| Path | What | Args |
|---|---|---|
| `scripts/ensure-env.py` | Missing `API_KEY_PEPPER` only | none |
| `scripts/install-catalog.py` | Build catalog values + upsert | `--train` `--version` `--data` `--port` (all required) |
