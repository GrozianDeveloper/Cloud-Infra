# Authentik

Goal: IDP & SSO — single place to manage all users

## Docs

- [Instance](../instance/authentik/Readme.md)
- Maps: [Applications](../instance/maps/auth_apps/Readme.md), [Permissions](../instance/maps/permissions/Readme.md)
- Skill: `.cursor/skills/authentik/SKILL.md` — run `scripts/`, do not recreate curl

## Installation

- TrueNAS App
- Secrets: [API](../instance/authentik/.env). Domains: [Caddy](../instance/caddy/.env). Email: [SMTP](../instance/email/.env)
- Ports: HTTP=30140, HTTPS=Disabled. Domain=`AUTHENTIK_DOMAIN`. Mount Docker Socket = TRUE
- Storage: `apps/authentik/{data,db,certs,template}`. Automatic Permissions=true
  - `data`, `certs`, `template`: uid/gid `568`
  - `db`: uid/gid `999`, POSIX, snapdir hidden
- Start AdGuard before this app. TrueNAS `nameserver1` is AdGuard. If AdGuard is down, `app.start` hangs on image pull.
- Chart `1.3.39` wants GHCR `server:2026.8.1`. That tag was missing; local `2026.8.0` tagged as `2026.8.1`. Installed pin: `2026.8.0`.
- TrueNAS apply (Gitea OIDC CLI, WP plugin, NC occ groups/folders, Caddy HUP): Dockge stack `host-apply-auth`.
