# Nextcloud AIO

## Authentik

- slug = `nextcloud`
- bind group = `cloud`
- `user_oidc`. Entitlements = map slugs. Closure mapping on provider.
- Redirects: `/apps/user_oidc/code` and `/index.php/apps/user_oidc/code`
- Creds: `instance/master-nextcloud-aio/.env.oidc`

## This NAS

- Mastercontainer UI host `:8081` (LAN). Public: Caddy → `nextcloud-aio-apache:11000`
- Talk TURN/STUN: host `:3478` TCP+UDP (not Caddy)
- Env: `instance/master-nextcloud-aio/.env`. Mail: `instance/email/.env`

| Path | For what |
|---|---|
| `apps/nc-aio` | mastercontainer config |
| `church_tank/nc-data` | `NEXTCLOUD_DATADIR` (uid 33, `0750`) |
| `church_tank/nc-backup` | Borg in AIO UI |
| `church_tank/nc-db-dump` | intended dump HostPath — unused |
| `/mnt/.ix-apps/docker/volumes/nextcloud_aio_*` | AIO named volumes |

`NEXTCLOUD_MOUNT=/mnt` → FAST `/mnt/apps`, ARCHIVE `/mnt/church_tank`, media `/mnt/fast/media_work`.
