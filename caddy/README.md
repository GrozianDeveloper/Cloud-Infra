# Caddy + CrowdSec = Edge

Goal: Single HTTPS entry. HTTP/3 (QUIC) is pinned.

```
Internet --TCP/80, TCP/443, UDP/443--> router --> Caddy
  --> TrueNAS catalog apps via host.docker.internal:<port>
  --> Dockge stacks via container DNS on `proxy` / `nextcloud-aio`
```

## Docs

- [Deploy](docs/deploy.md)
- [Instance](../instance/caddy/Readme.md)
- [Networking](../docs/networking.md)

## Installation

- [Dockge](dockge/Readme.md) stack `caddy`
- [Secrets](../instance/caddy/.env) (source) → `apps/dockge/caddy/.env` (runtime)
- [Docker Compose](docker-compose.yml). Ports `80:80`, `443:443`, `443:443/udp`. `cap_add: NET_ADMIN`.
- HTTP/3: `servers { protocols h1 h2 h3 }` + `Alt-Svc` on every vhost.
- Host UDP buffer: TrueNAS tunables `net.core.rmem_max` / `net.core.rmem_default` = `2500000` (not `/etc/sysctl.d`).
- Nextcloud vhost: no `encode` (large DAV/video).
- Shared volume `caddy_logs` → `/var/log/caddy` for CrowdSec.

## CrowdSec

In-Caddy bouncer (`order crowdsec first`) + engine parsing Caddy JSON logs.

- Collections: `crowdsecurity/caddy`, `http-cve`, `linux`, `whitelist-good-actors`.
- `acquis.yaml` label `type: caddy` — renaming it stops detection.
- Do **not** bind-mount `config.yaml` or a volume over `/etc/crowdsec`.
- LAN / Docker / Netbird (`100.64.0.0/10`) whitelisted. Bans 4h.

## Scripts

| Path | What | Args |
|---|---|---|
| `scripts/ensure-env.py` | Add missing keys to `instance/caddy/.env`. Never overwrite | `KEY=value`… (required) |
| `scripts/push.sh` | Caddyfile, compose, crowdsec, `.env` → Dockge | `--no-env` skip `.env` |
| `scripts/reload.sh` | HUP Caddyfile only | |
| `scripts/restart.sh` | Recreate stack (`.env` / compose). Brief edge blip | |
| `scripts/check.py` | HTTPS GET each `*_DOMAIN`. Optional extra keys as args | |