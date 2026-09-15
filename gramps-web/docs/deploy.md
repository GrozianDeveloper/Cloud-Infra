# Deploy

## Catalog values

- `TZ` — host timezone
- `gramps.redis_password` / `gramps.app_key` — `REDIS_PASSWORD`, `SECRET_KEY` in `instance/gramps-web/.env` (`SECRET_KEY` ≥ 32 chars)
- `gramps.multi_tree` — `true` (chart sets `TREE=*` + `MEDIA_PREFIX_TREE`; do not duplicate in additional_envs)
- `gramps.disable_telemetry` — leave default (off) unless you decide otherwise
- `network.web_port` — published `30179`
- `storage.*.type` — `host_path` for **all** keys (no ixVolume): `users`, `index`, `thumbnail_cache`, `cache`, `media`, `grampsdb`
- `additional_envs` — see [sso.md](sso.md)

Catalog web/celery run as **root** (uid 0). Redis 568 (bundled, no extra HostPath).

## Caddy / DNS

- `instance/caddy/.env`: `GRAMPS_DOMAIN`, `GRAMPS_UPSTREAM`
- Caddy `header_up Host` + `X-Forwarded-Proto https`. No FA.
- Host is outside the church wildcard → AdGuard rewrite **and** public A/AAAA (ACME).

## Order

```bash
python3 gramps-web/scripts/ensure-env.py
bash .cursor/skills/truenas-scale/scripts/ensure-datasets.sh \
  apps/gramps-users:0:0:0750 \
  apps/gramps-index:0:0:0750 \
  apps/gramps-thumbs:0:0:0750 \
  apps/gramps-cache:0:0:0750 \
  church_tank/gramps-media:0:0:0755 \
  church_tank/gramps-db:0:0:0750
python3 caddy/scripts/ensure-env.py \
  GRAMPS_DOMAIN=<host> \
  GRAMPS_UPSTREAM=host.docker.internal:30179
# public DNS + AdGuard
python3 instance/maps/permissions/apply.py
python3 instance/maps/auth_apps/apply.py gramps
# apply writes missing instance/gramps-web/.env.oidc keys only
python3 gramps-web/scripts/install-catalog.py \
  --train community --version 1.4.4 \
  --users /mnt/apps/gramps-users \
  --index /mnt/apps/gramps-index \
  --thumbs /mnt/apps/gramps-thumbs \
  --cache /mnt/apps/gramps-cache \
  --media /mnt/church_tank/gramps-media \
  --db /mnt/church_tank/gramps-db \
  --port 30179
# Caddyfile vhost → bash caddy/scripts/push.sh && bash caddy/scripts/restart.sh
# local owner → POST /api/trees/ → family OIDC with that tree id ([sso.md](sso.md))
```

OIDC env after Authentik app exists. Catalog recreate if issuer/client/`TREE` changes.

## Effects

- Users in closure of `gramps` can SSO. Others: Authentik deny.
- First OIDC logins become Gramps **Owner** (`OIDC_GROUP_OWNER=gramps`).
- Local password stays for site-admin / break-glass. Do not disable until a local owner exists and the first tree is created.
