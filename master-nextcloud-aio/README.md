# Nextcloud AIO

Goal: Center point of all apps — integrated with Nextcloud

## Docs

- [Deploy](docs/deploy.md)
- [Instance](../instance/master-nextcloud-aio/Readme.md)
- MCP: [nextcloud-mcp](../nextcloud-mcp/README.md)
- SSO: [04-authentik-nextcloud-sso.md](../docs/installation_guide/02-authentik-apps-auth/04-authentik-nextcloud-sso.md)

## Installation

- Dockge stack. Mastercontainer UI on host `:8081` (LAN). Public: Caddy → `nextcloud-aio-apache:11000`
- Secrets: [Main](../instance/master-nextcloud-aio/.env), [OIDC](../instance/master-nextcloud-aio/.env.oidc). Mail: [SMTP](../instance/email/.env)
- Talk TURN/STUN: host `:3478` TCP+UDP (not via Caddy)
- Compose binds `apps/nc-aio` → mastercontainer config. Dump volume `nextcloud_aio_database_dump` is a Docker volume on `apps/ix-apps/docker` (HostPath `church_tank/nc-db-dump` did not attach). Borg path is **AIO UI**, not env.

Dockge stack dir `apps/dockge/master-nextcloud-aio/` is compose + `.env` only. AIO then creates sibling containers via docker.sock.

AIO named volumes (not HostPaths):

- `nextcloud_aio_nextcloud` — NC install (`config.php`, `apps/`, `custom_apps/`)
- `nextcloud_aio_database` — Postgres
- `nextcloud_aio_database_dump` — SQL dump. AIO created this volume first; compose bind to `nc-db-dump` is ignored
- `nextcloud_aio_redis`, `nextcloud_aio_apache`, `nextcloud_aio_elasticsearch`, `nextcloud_aio_harp`

AIO exposes **one** host tree via `NEXTCLOUD_MOUNT`. Extra binds on the mastercontainer do **not** reach Nextcloud.

## External storage

1. Dataset exists on the host (HostPath).
2. Path is under `NEXTCLOUD_MOUNT`. Wider tree = recreate mastercontainer, then recreate `nextcloud-aio-nextcloud`.
3. Perms: NC www-data is uid **33**. On a **shared** dataset add an ACL for uid 33 — do **not** `chown -R 33:0` (breaks other apps). Dedicated `nc-data` is `chown 33:0` + `chmod 750`.
4. After first start: enable **External storage support**. Then Administration → External storage → **Local**, or `scripts/apply-external-storage.sh`.

SMB/S3 mounts do not use `NEXTCLOUD_MOUNT`.

## Talk

HPB/TURN: AIO UI **Talk** checkbox on first Start. HPB/signaling: docker network only. TURN/STUN: host TCP+UDP 3478, bypass Caddy. Recording: AIO UI, no WAN port.

## Optional containers (AIO UI)

Collabora, Imaginary, Fulltextsearch, ClamAV, Talk Recording. Collabora seccomp left on. NVIDIA: `NEXTCLOUD_ENABLE_NVIDIA_GPU` — omit if GPU is not passed to Docker.

## Scripts

| Dir | What |
|---|---|
| `scripts/oidc/` | Authentik OIDC app + `user_oidc` + session |
| `scripts/optimizations/` | ClamAV after-upload |
| `scripts/` | mail, host-apply, external-storage, groups ACL |
