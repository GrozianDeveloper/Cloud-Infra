# TrueNAS-Scale

Secrets: `instance/truenas/.env` (`TRUENAS_URL`, `TRUENAS_API_KEY`, `TRUENAS_LAN` / `HOST_LAN_IP`).

Caddy owns host **TCP 80, TCP & UDP 443**.
TrueNAS Web UI: HTTP 880, HTTPS 8443.

SYSCTL tunables (persist): `python3 truenas/scripts/apply-tunables.py net.core.rmem_max=2500000 net.core.rmem_default=2500000`

### Media Team

- `fast/media_work`

### App datasets (HostPath)

- Each app: `instance/{app}/Readme.md`
- Create: `bash .cursor/skills/truenas-scale/scripts/ensure-datasets.sh dataset` or `dataset:uid:gid:mode`
- Postiz: `apps/postiz/{config,uploads,postgres,redis,temporal-pg,temporal-es}`
- Tandoor: `fast/tandoor-static`, `church_tank/tandoor-media`, `apps/tandoor-db` (postgres uid 999)
- HomeBox: `apps/homebox` (uid 568)
- Gramps: `apps/gramps-{users,index,thumbs,cache}`, `church_tank/gramps-{media,db}` (uid 0)

### Docker (TrueNAS Apps pool, hidden)

Dataset `apps/ix-apps` mounts at `/mnt/.ix-apps`. Docker graph: `apps/ix-apps/docker` → `/mnt/.ix-apps/docker`.

AIO named volumes: `/mnt/.ix-apps/docker/volumes/nextcloud_aio_*`. Details: [master-nextcloud-aio](../../master-nextcloud-aio/README.md).

## Pool

Assume dataset `Generic` if not specified otherwise.

| Pool Name | Layout | For what | Examples of use |
|---|---|---|---|
| apps | Stripe (SATA SSD) | Working app data | Apps config, Docker |
| church_tank | Stripe (HDD) | Archive files | Nextcloud user files |
| fast | Stripe (NVMe 500G) | media work in progress | `fast/media_work` (300G quota) |

- Disks: [`../hardware.md`](../hardware.md)
