# Gramps Web

Goal: Genealogy — family tree. SSO = Authentik only. Multi-tree.

## Docs

- [SSO](docs/sso.md)
- [Deploy](docs/deploy.md)
- [Instance](../instance/gramps-web/Readme.md)

## Installation

- TrueNAS Catalog `gramps-web`
- Secrets: [Main](../instance/gramps-web/.env). [OIDC](../instance/gramps-web/.env.oidc)
- [Caddy](../instance/caddy/.env): `GRAMPS_DOMAIN` → `GRAMPS_UPSTREAM` (`host.docker.internal:{WebUI port}`).
  WebUI port = `30179`.
- Catalog `multi_tree=true` (`TREE=*`). Authentik slug `gramps` (catalog name stays `gramps-web`).

## Scripts

Generic:

| Path | What | Args |
|---|---|---|
| `caddy/scripts/ensure-env.py` | Add missing `instance/caddy/.env` keys | `GRAMPS_DOMAIN=…` `GRAMPS_UPSTREAM=host.docker.internal:30179` |
| `.cursor/skills/truenas-scale/scripts/ensure-datasets.sh` | HostPath + perms | `dataset` or `dataset:uid:gid:mode` |
| `.cursor/skills/truenas-scale/scripts/catalog-install.py` | Catalog install/update | `--app` `--train` `--version` `--values` |

Gramps (values from `instance/gramps-web/.env` + `.env.oidc`):

| Path | What | Args |
|---|---|---|
| `scripts/ensure-env.py` | Missing `SECRET_KEY` / `REDIS_PASSWORD` only | none |
| `scripts/install-catalog.py` | Build catalog values + upsert | `--train` `--version` `--users` `--index` `--thumbs` `--cache` `--media` `--db` `--port` |
