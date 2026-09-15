# Deploy (Dockge on TrueNAS)

Stack dir: `apps/dockge/caddy/`

```
compose.yaml          # copy of docker-compose.yml
Caddyfile
.env                  # copy of instance/caddy/.env — not in git
crowdsec/acquis.yaml
crowdsec/profiles.yaml
crowdsec/whitelist.yaml
```

Compose creates named networks `proxy` and `nextcloud-aio` and volumes `caddy_data`, `caddy_config`, `caddy_logs`, `caddy_crowdsec_data` on first `up`. Other Dockge stacks join those names as `external: true`.

After copying files, start the stack in Dockge (`caddy`). CrowdSec must be healthy before Caddy (`depends_on` + healthcheck).

Helpers (creds from `instance/truenas/.env` / Dockge login; not printed):

```bash
python3 caddy/scripts/ensure-env.py KEY=value   # missing keys only
bash caddy/scripts/push.sh
bash caddy/scripts/reload.sh
node .cursor/skills/agentskillexchange-skills-dockge-docker-compose-stack-manager/scripts/dockge-start.mjs status caddy
```

Do not recreate catalog apps as compose!

## HTTP/3 — make sure all four true

Caddy serves `h1 h2 h3`. Browsers need a first HTTP/2 response (`Alt-Svc: h3=":443"`) before they switch to QUIC. Missing any hop → stay on h2.

| Layer | What |
|-------|------|
| Caddyfile | `servers` + `servers :443 { protocols h1 h2 h3 }` and `Alt-Svc` on every vhost |
| Compose | `443:443/udp` **and** `443:443/tcp`; `cap_add: NET_ADMIN` |
| Router | UDP **and** TCP 443 → TrueNAS host ([01-router-portforward.md](../../docs/installation_guide/01-router-portforward.md)) |
| Host | TrueNAS **Tunables** `net.core.rmem_max` and `net.core.rmem_default` = `2500000` |

Do **not** use `/etc/sysctl.d` on SCALE — it does not persist. System → Tunables (SYSCTL), or API `tunable.create`.

Verify (from a phone hotspot; macOS `/usr/bin/curl` has no `--http3`):

```bash
curl -sI https://auth.church.giize.com | grep -i alt-svc
# expect: alt-svc: h3=":443"
curl -sI --http3 https://auth.church.giize.com | head
# first line HTTP/3 if the client supports it
```

No UDP/443 on the router → `Alt-Svc` is advertised but QUIC never connects. No `443/udp` on the container → Caddy never binds the QUIC socket.

# Build Checklist

1. Deploy Caddy via Dockge (`apps/dockge/caddy`). Confirm stack running.
2. Tunables `rmem_max` / `rmem_default` = 2500000.
3. Confirm catalog apps have the published ports in `instance/caddy/.env`.
4. Forward router TCP 80, TCP 443, **UDP 443**, Netbird STUN 30417, AIO Talk **TCP+UDP 3478**.
5. Split-horizon DNS.
6. Gate WUD/Dockge with Authentik; disable Dockge built-in auth.
7. `curl -sI https://auth… | grep alt-svc` then `curl --http3` from a client that supports h3.

# Troubleshooting

| Symptom | Cause |
|---------|-------|
| `curl --http3` fails, `--http2` works | UDP/443 missing on router, host firewall, or compose |
| `failed to sufficiently increase receive buffer` | tunables `rmem_max`/`rmem_default` = 2500000 |
| CrowdSec restart loop | volume or `config.yaml` mounted over `/etc/crowdsec` |
| Caddy crash: `server block without any key` | new `{$APP_DOMAIN}` in Caddyfile but container env stale. `restartStack` does not reload `.env`. `bash caddy/scripts/push.sh && bash caddy/scripts/restart.sh` (deploy/recreate) |
| `Additional property apps is not allowed` | top-level must be `services:`; health wait is `service_healthy` |
| `.env: unexpected character (` | markdown in stack `.env` must be `#` comments |
| `Found multiple config files` | leftover `docker-compose.yml` next to `compose.yaml` — compose uses `compose.yaml` |
| 502 to Authentik / n8n / NocoDB / WP | published port changed — update `*_UPSTREAM` in `instance/caddy/.env` and stack `.env` |
| 502 to Nextcloud / Grafana / WUD | container not on `proxy` / `nextcloud-aio` |
| Authentik loop | FA stacked on an OIDC app (Grafana, Nextcloud) |
| Netbird agents fail | gRPC `h2c://` path or `NETBIRD_MGMT_UPSTREAM` wrong |
| CrowdSec silent | acquis `type` renamed, or `caddy_logs` not shared |
| Home HTTPS `502` | `home-gw` down, or `HOME_LAN_PORT` ≠ HA listen port |