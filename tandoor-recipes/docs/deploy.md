# Deploy 


## Catalog values

- `TZ` — host timezone
- `recipes.db_password` / `recipes.secret_key` — from `instance/tandoor-recipes/.env` (`DATABASE_PASSWORD`, `SECRET_KEY`)
- `recipes.allowed_hosts` — domain + `127.0.0.1` + `localhost` (healthcheck)
- `recipes.postgres_image_selector` — leave default
- `network.web_port` — published `30290`
- `storage.*.type` — `host_path` for staticfiles, mediafiles, postgres_data
- `additional_envs` — see [docs/sso.md](docs/sso.md)

## Caddy / DNS

- `instance/caddy/.env`: `TANDOOR_RECIPES_DOMAIN`, `TANDOOR_RECIPES_UPSTREAM`
- Caddy `header_up Host` + `X-Forwarded-Proto https`.
- Add Adguard rewrite. Public A/AAAA required for ACME.

## Order

```bash
bash .cursor/skills/truenas-scale/scripts/ensure-datasets.sh \
  fast/tandoor-static:0:0:0755 \
  church_tank/tandoor-media:0:0:0755 \
  apps/tandoor-db:999:999:0700
python3 caddy/scripts/ensure-env.py \
  TANDOOR_RECIPES_DOMAIN=<host> \
  TANDOOR_RECIPES_UPSTREAM=host.docker.internal:30290
# public DNS + AdGuard
python3 instance/maps/permissions/apply.py
python3 instance/maps/auth_apps/apply.py tandoor-recipes
# apply writes missing instance/tandoor-recipes/.env.oidc keys only
python3 tandoor-recipes/scripts/install-catalog.py \
  --train community --version 1.2.44 \
  --static /mnt/fast/tandoor-static \
  --media /mnt/church_tank/tandoor-media \
  --db /mnt/apps/tandoor-db \
  --port 30290
# Caddyfile vhost → bash caddy/scripts/push.sh && bash caddy/scripts/restart.sh
# (reload/HUP is not enough for new .env keys)
# wait healthy (first boot must run migrate; if `auth_user` missing see docs/sso.md)
# manage.py inside the recipes image is /opt/recipes/venv/bin/python
# set Django Site.domain to TANDOOR_RECIPES_DOMAIN (default example.com)
```

OIDC env after Authentik app exists. Catalog recreate if `SOCIALACCOUNT_PROVIDERS` JSON changes.

## Effects

- Users in closure of `tandoor-recipes` can SSO. Others: Authentik deny.
- Login form hidden. Break-glass: `https://{TANDOOR_RECIPES_DOMAIN}/accounts/login/?form=1`. Recover also: `docker exec` into recipes container (`venv/bin/python`).
- Spaces/households: create in Tandoor UI. Owner = `space.created_by` (needed for `/api/household/` and invite links). Django superuser is not enough.
