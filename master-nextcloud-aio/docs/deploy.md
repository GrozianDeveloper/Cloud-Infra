# Deploy (Dockge on TrueNAS)

Stack dir: `apps/dockge/master-nextcloud-aio/`

```
compose.yaml   # copy of docker-compose.yml
.env           # copy of instance/master-nextcloud-aio/.env — not in git
```

Caddy already created docker networks `proxy` and `nextcloud-aio`. Apache joins `proxy` via `APACHE_ADDITIONAL_NETWORK`. Caddy upstream: `NEXTCLOUD_UPSTREAM` = `nextcloud-aio-apache:11000`.

Upload from repo root:

```bash
node .cursor/skills/truenas-scale/scripts/tn-put.mjs \
  master-nextcloud-aio/docker-compose.yml \
  /mnt/apps/dockge/master-nextcloud-aio/compose.yaml
node .cursor/skills/truenas-scale/scripts/tn-put.mjs \
  instance/master-nextcloud-aio/.env \
  /mnt/apps/dockge/master-nextcloud-aio/.env
```

Start (pulls the AIO image; confirm first):

```bash
node .cursor/skills/agentskillexchange-skills-dockge-docker-compose-stack-manager/scripts/dockge-start.mjs start master-nextcloud-aio
node .cursor/skills/agentskillexchange-skills-dockge-docker-compose-stack-manager/scripts/dockge-start.mjs status master-nextcloud-aio
```

AIO UI: `https://<TrueNAS-LAN-IP>:8081` (self-signed). Save the AIO passphrase.

## HostPath before first `up`

| Dataset | Use |
|---|---|
| `apps/nc-aio` | mastercontainer config volume (must stay named `nextcloud_aio_mastercontainer`) |
| `church_tank/nc-data` | `NEXTCLOUD_DATADIR` — empty on first boot; `33:0` `0750` |
| `church_tank/nc-db-dump` | intended bind for `nextcloud_aio_database_dump` — **not attached** (AIO created a plain Docker volume first; dump lives in `/mnt/.ix-apps/docker/volumes/nextcloud_aio_database_dump/_data`) |
| `church_tank/nc-backup` | Borg location in AIO UI (no env) |
| `apps/` | FAST Local storage (`NEXTCLOUD_FAST_MOUNT`); AIO bind is parent `/mnt` |
| `church_tank/` | ARCHIVE Local storage (`NEXTCLOUD_ARCHIVE_MOUNT`) |
| `fast/media_work` | FileFlows / HandBrake / NC Local **Медиа в Работе** (`quota=300G`). [media-work.md](media-work.md) |

## AIO UI on first Start

Checkboxes this instance wants: **Talk**, Collabora, Imaginary, Fulltextsearch, ClamAV, Talk Recording.

- Domain = `NEXTCLOUD_DOMAIN` (Caddy env).
- Borg location = `/mnt/church_tank/nc-backup`.
- After domain check works: set `SKIP_DOMAIN_VALIDATION=false` and recreate mastercontainer.

## After Nextcloud is up

1. Authentik OIDC: [04-authentik-nextcloud-sso.md](../docs/installation_guide/02-authentik-apps-auth/04-authentik-nextcloud-sso.md)
2. `python3 master-nextcloud-aio/scripts/oidc/authentik-create-nextcloud_oidc.py` (Authentik REST). Map NC admin: `python3 .cursor/skills/authentik/scripts/set-user-attribute.py --user <ak-user> --key nextcloud_user_id --value admin`
3. On host (Dockge one-shot `nc-aio-oidc` from `scripts/oidc/host-apply-oidc.compose.yaml`, or terminal): `scripts/oidc/apply-oidc.sh` then `scripts/apply-mail.sh`. Session-only: `scripts/oidc/apply-session-settings.sh`. Stack must contain those scripts plus `instance/master-nextcloud-aio/.env.oidc` and `instance/email/.env` (or copies next to the scripts).
4. External storage Local → FAST `/mnt/apps`, ARCHIVE `/mnt/church_tank`, **Медиа в Работе** `/mnt/fast/media_work` group `church-media` (`scripts/apply-external-storage.sh`). Changing `NEXTCLOUD_MOUNT` needs mastercontainer recreate, then recreate `nextcloud-aio-nextcloud` (AIO watchdog). One-shot: Dockge stack `nc-aio-apply` from `scripts/host-apply.compose.yaml` (also Deck import). Vanilla `docker compose` rejects Dockge `apps:` — `host-apply.sh` rewrites it to `services:`.

Talk TURN is host `:3478` TCP+UDP (router already forwards). Not via Caddy.
