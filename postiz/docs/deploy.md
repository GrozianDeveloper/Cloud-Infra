# Deploy (Dockge on TrueNAS)

Stack dir: `apps/dockge/postiz/`

```
compose.yaml          # copy of docker-compose.yml
dynamicconfig/development-sql.yaml
.env                  # copy of instance/postiz/.env — not in git
```

HostPath (create before first `up`):

| Dataset | Container | uid |
|---------|-----------|-----|
| `apps/postiz/config` | `/config` | 1000 |
| `apps/postiz/uploads` | `/uploads` | 1000 |
| `apps/postiz/postgres` | Postgres data | 70 |
| `apps/postiz/redis` | Redis data | 999 |
| `apps/postiz/temporal-pg` | Temporal Postgres | 999 |
| `apps/postiz/temporal-es` | Elasticsearch | 1000 |

```bash
python3 postiz/scripts/ensure-env.py
bash .cursor/skills/truenas-scale/scripts/ensure-datasets.sh \
  apps/postiz \
  apps/postiz/config:1000:1000:0750 \
  apps/postiz/uploads:1000:1000:0750 \
  apps/postiz/postgres:70:70:0700 \
  apps/postiz/redis:999:999:0750 \
  apps/postiz/temporal-pg:999:999:0700 \
  apps/postiz/temporal-es:1000:1000:0750
python3 instance/maps/auth_apps/apply.py postiz
python3 postiz/scripts/ensure-env.py
bash postiz/scripts/push.sh
node .cursor/skills/agentskillexchange-skills-dockge-docker-compose-stack-manager/scripts/dockge-start.mjs start postiz
bash caddy/scripts/push.sh
bash caddy/scripts/reload.sh
# after healthy:
python3 instance/maps/map-postiz/apply.py
```

Compose key is `services:`. Joins external network `proxy`. No Traefik. No Temporal UI.

OIDC redirect: `https://{POSTIZ_DOMAIN}/settings`. Creds: `instance/postiz/.env.oidc` (never overwrite existing).
