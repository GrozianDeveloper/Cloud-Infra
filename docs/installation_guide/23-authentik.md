# Authentik

Catalog. After AdGuard + Caddy. [authentik/README.md](../../authentik/README.md). Skill: `.cursor/skills/authentik/SKILL.md` — never ad-hoc curl.

## Install

- HostPath `apps/authentik/{data,db,certs,template}` (db uid **999**, others **568**).
- HTTP host port; HTTPS disabled. `AUTH_DOMAIN` / `AUTHENTIK_UPSTREAM` in `instance/caddy/.env`.
- SMTP: `instance/email/.env`.
- API token → `instance/authentik/.env` (`AUTHENTIK_TOKEN`). First admin user.

Brand + outpost `authentik_host` = public `https://{AUTH_DOMAIN}` ([instance/authentik/Readme.md](../../instance/authentik/Readme.md)).

SSO / maps: [02.4](02-authentik-apps-auth/02.4-groups-map.md). NAS apply = existing app scripts (`gitea/scripts/apply-oidc-host.sh`, `wordpress/scripts/apply-oidc.sh host`, `caddy/scripts/reload.sh`, Nextcloud occ helpers) — not a first-install-only wrapper.
