# TrueNAS SCALE

Official install: [TrueNAS SCALE docs](https://www.truenas.com/docs/scale/). Prefer **bare metal** if no Proxmox.

## Already installed

`TRUENAS_URL`, `TRUENAS_API_KEY`, `TRUENAS_LAN` / `HOST_LAN_IP` → `instance/truenas/.env`. HTTPS required for API keys.

## Our choices (not the vendor wizard)

- UI **880 / 8443** so Caddy owns **80 / 443**.
- HostPath, never IxVolumes.
- Tunables: `python3 truenas/scripts/apply-tunables.py` ([13](13-pools-datasets.md), [caddy HTTP/3](../../caddy/docs/deploy.md)).
- After AdGuard: `python3 truenas/scripts/set-nameservers.py` — `nameserver1` = this host (AdGuard), `nameserver2` = router.

PVE guest: pass disks through; GPU vfio if media apps. App docs: [truenas/README.md](../../truenas/README.md).
