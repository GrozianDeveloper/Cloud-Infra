# Tandoor Recipes

Goal: Recipe manager

## Docs

- [SSO](docs/sso.md) - Authentik only
- [Deploy](docs/deploy.md)
- [Instance-specific Docs](../instance/tandoor-recipes/Readme.md)

## Installation

- Secrets: [Main](../instance/tandoor-recipes/.env). [OIDC](../instance/tandoor-recipes/.env.oidc)
- [Caddy](../instance/caddy/.env): `TANDOOR_RECIPES_DOMAIN` → `TANDOOR_RECIPES_UPSTREAM` (`host.docker.internal:{WebUI port}`).
WebUI port = `30290`

## Scripts

Generic (no defaults — pass every value):

| Path | What | Args |
|---|---|---|
| `caddy/scripts/ensure-env.py` | Add missing `instance/caddy/.env` keys | `TANDOOR_RECIPES_DOMAIN=…` `TANDOOR_RECIPES_UPSTREAM=host.docker.internal:30290` |
| `.cursor/skills/truenas-scale/scripts/ensure-datasets.sh` | HostPath datasets + perms | `dataset` or `dataset:uid:gid:mode` |
| `.cursor/skills/truenas-scale/scripts/catalog-install.py` | Catalog install/update from JSON | `--app` `--train` `--version` `--values` |

Tandoor (OIDC/Django values from `instance/tandoor-recipes/.env` + `.env.oidc`):

| Path | What | Args |
|---|---|---|
| `scripts/install-catalog.py` | Build catalog values + upsert | `--train` `--version` `--static` `--media` `--db` `--port` (all required) |
| `scripts/inspect_sso.py` | Dump Site + OIDC app shape (no secrets) | run inside recipes container |
| `scripts/host-migrate.compose.yaml` | One-shot `manage.py migrate` | Dockge one-shot |
| `scripts/sso-debug.compose.yaml` | SSO logs + inspect | Dockge one-shot |
| `scripts/debug-logs.compose.yaml` | Recipes container logs | Dockge one-shot |