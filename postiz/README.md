# Postiz

Goal: Social scheduling. SSO = Authentik only.

## Docs

- [Proxmox Script](https://community-scripts.org/scripts?q=postiz&preview=postiz)
- [Deploy](docs/deploy.md)
- [MCP](MCP.md)
- [Instance](../instance/postiz/Readme.md)
- Workspaces: [map-postiz](../instance/maps/map-postiz/Readme.md)

## Installation

- Dockge stack `postiz`. No host `:4007`. (would break API/MCP).
- Secrets: [Main](../instance/postiz/.env), [OIDC](../instance/postiz/.env.oidc). Email: [SMTP](../instance/email/.env)
- Caddy: `POSTIZ_DOMAIN` → `POSTIZ_UPSTREAM` (`postiz:5000` on `proxy`)
- Do not set `DISABLE_REGISTRATION=true` (kills OIDC).
- Bundled Postgres + Redis + Temporal (needed since v2.12). No Temporal UI.

## Scripts

| Path | What |
|---|---|
| `scripts/ensure-env.py` | Create missing keys in `instance/postiz/.env` |
| `scripts/push.sh` | Compose + env → Dockge |
| `scripts/host-apply-map.sh` | Apply `instance/postiz/postiz-apply.sql` on NAS |
