# Providers & Apps

Maps: `[../maps/index.md](../maps/index.md)`. Apply: `instance/maps/permissions/apply.py` + `instance/maps/auth_apps/apply.py`. Nextcloud: `instance/maps/permissions/apply-permissions-map.py`. Procedure: `[docs/installation_guide/02-authentik-apps-auth/02.4-groups-map.md](../../docs/installation_guide/02-authentik-apps-auth/02.4-groups-map.md)`.

Secrets: `instance/authentik/.env` (API token). Domains: `instance/caddy/.env`. Per-app OIDC: `instance/{app}/.env.oidc`.

Live:


| App                                 | Type                  | Slug              | Bind group                                | Creds                                     | notes                                               |
| ----------------------------------- | --------------------- | ----------------- | ----------------------------------------- | ----------------------------------------- | --------------------------------------------------- |
| Nextcloud                           | OIDC (`user_oidc`)    | `nextcloud`       | `cloud`                                   | `instance/master-nextcloud-aio/.env.oidc` | Entitlements = map slugs                            |
| FileFlows / HandBrake / JDownloader | Proxy FA              | same              | `fileflows` / `handbrake` / `jdownloader` |                                           | **authentik Embedded Outpost**.                     |
| Home                                | OIDC stub             | `home`            | `home`                                    | `instance/home/.env.oidc`                 | Church HA later                                     |
| Home                        | OIDC                  | `home`    | `homeм`                     | `instance/home/.env.oidc`         | Not the `home` stub                                 |
| WordPress                           | OIDC                  | `wordpress`       | `wordpress/admin_panel`                   | `instance/wordpress/.env.oidc`            | Plugin OpenID Connect Generic                       |
| Gitea                               | OIDC                  | `gitea`           | `gitea`                                   | `instance/gitea/.env.oidc`                | Auth source name `authentik`. Entitlement `gituser` |
| n8n                                 | OIDC library only     | `n8n`             | `n8n`                                     | `instance/n8n/.env.oidc`                  | Currently, do not enable n8n SSO (Enterprise).      |
| NetBird                             | OIDC                  | `netbird`         | `netbird`                                 | `instance/netbird-server/.env.oidc`       | Keep embedded Dex. UI: extra Generic OIDC.          |
| Postiz                              | OIDC                  | `postiz`          | `postiz`                                  | `instance/postiz/.env.oidc`               | Redirect `/settings`.                               |
| Tandoor Recipes                     | OIDC (django-allauth) | `tandoor-recipes` | `tandoor-recipes`                         | `instance/tandoor-recipes/.env.oidc`      |                                                     |
| HomeBox                             | OIDC                  | `homebox`         | `homebox`                                 | `instance/homebox/.env.oidc`              | Redirect `/api/v1/users/login/oidc/callback`. Invite for shared inventory. |
| Gramps Web                          | OIDC                  | `gramps`          | `gramps`                                  | `instance/gramps-web/.env.oidc`           | Redirect regex `/api/oidc/callback/.*`. Multi-tree. |
| FreeShow                            | Application only      | `freeshow`        | `freeshow`                                |                                           | Currently, no provider / Caddy                      |


• [auth_apps map](../maps/auth_apps/Readme.md)

# Outpost / brand (browser redirects)

- Brand + Embedded Outpost `authentik_host` = `https://{AUTH_DOMAIN}` (not `authentik-default`)
- Without this, FA apps redirect to LAN `https://{TRUENAS_LAN}:30141` (self-signed).

Service account `netbird-svc` (app password) may still be used if NetBird UI IdP sync is configured. Creds: `instance/netbird-server/.env.oidc`.

API: always `.cursor/skills/authentik` scripts (`SKILL.md`). Token: `instance/authentik/.env` (`AUTHENTIK_TOKEN`). Do not ad-hoc curl.

NAS apply: `gitea/scripts/apply-oidc-host.sh`, `wordpress/scripts/apply-oidc.sh host`, `caddy/scripts/reload.sh`, Nextcloud occ helpers.