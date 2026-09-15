# Caddy + CrowdSec

Dockge stack. Single HTTPS entry. [caddy/docs/deploy.md](../../caddy/docs/deploy.md).

## Order

1. `proxy` + `nextcloud-aio` networks (compose on first `up`).
2. `python3 caddy/scripts/ensure-env.py KEY=value` — missing keys only.
3. `bash caddy/scripts/push.sh` then start stack `caddy`. CrowdSec healthy before Caddy.
4. Tunables already from [13](13-pools-datasets.md).
5. Router: [01](01-router-portforward.md).

```bash
python3 caddy/scripts/check.py
```

LAN `dig {APP}_DOMAIN` must be `TRUENAS_LAN`.
