# Deploy

## Catalog values

- `TZ` — host timezone
- `homebox.api_key_pepper` — `API_KEY_PEPPER` in `instance/homebox/.env`. Stable; rotate = all API keys die
- `run_as.user` / `run_as.group` — `568`
- `network.web_port` — published `30149`
- `storage.data.type` — `host_path` (`/mnt/apps/homebox`)
- `additional_envs` — see [sso.md](sso.md)

SQLite lives under `/data` (do not change `HBOX_STORAGE_DATA`).

## Caddy / DNS

- `instance/caddy/.env`: `HOMEBOX_DOMAIN`, `HOMEBOX_UPSTREAM`
- Caddy `header_up Host` + `X-Forwarded-Proto https`. No FA.
- Host is outside the church wildcard → AdGuard rewrite **and** public A/AAAA (ACME). Same as Tandoor recipes host.

## Order

```bash
python3 homebox/scripts/ensure-env.py
bash .cursor/skills/truenas-scale/scripts/ensure-datasets.sh \
  apps/homebox:568:568:0750
python3 caddy/scripts/ensure-env.py \
  HOMEBOX_DOMAIN=<host> \
  HOMEBOX_UPSTREAM=host.docker.internal:30149
# public DNS + AdGuard
python3 instance/maps/permissions/apply.py
python3 instance/maps/auth_apps/apply.py homebox
# apply writes missing instance/homebox/.env.oidc keys only
python3 homebox/scripts/install-catalog.py \
  --train community --version 1.1.11 \
  --data /mnt/apps/homebox \
  --port 30149
# Caddyfile vhost → bash caddy/scripts/push.sh && bash caddy/scripts/restart.sh
```

OIDC env after Authentik app exists. Catalog recreate if issuer/client changes.

## Effects

- Users in closure of `homebox` can SSO. Others: Authentik deny.
- Local login off. Break-glass: `HBOX_OPTIONS_ALLOW_LOCAL_LOGIN=true` then catalog update.
- Shared house inventory: invite link (see [sso.md](sso.md)).
