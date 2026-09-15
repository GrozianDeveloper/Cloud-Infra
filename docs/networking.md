# Networking

Port forwarding → Caddy (HTTP/3) → TrueNAS catalog apps (host ports) and Dockge stacks (`proxy`).

Domains and upstreams: `instance/caddy/.env` (`{APP}_DOMAIN`, `{APP}_UPSTREAM`). Live brand/outpost: `instance/authentik/Readme.md`.

```mermaid
flowchart TD
    INET[Internet] -->|"TCP 80/443 + UDP 443"| RTR[Router / Firewall]
    RTR -->|"80/443 TCP+UDP → Caddy"| CADDY[Caddy<br/>h1+h2+h3, CrowdSec]

    LocalDNS[Local DNS] --> CADDY

    CADDY -->|"{APP}_DOMAIN"| Application[<b>Application</b><br/>"{APP}_UPSTREAM"]

    LAN[LAN Device] -->|host port| DCK[LAN-only app]

    DCK -.manages.-> CADDY
    DCK -.manages.-> NCAIO
    RTR -.UDP STUN + Talk TURN.-> DIRECT[Bypass Caddy]
```

## Core Principle

One HTTP(S) entry: **TCP 80 + TCP 443 + UDP 443 → Caddy**.

- **TrueNAS catalog / custom apps** (Authentik, n8n, NocoDB, WordPress, Netbird-Server, Gitea, FileFlows, HandBrake Web): isolated `ix-*` networks, published host ports. Caddy uses `host.docker.internal:<port>`.
- **Dockge stacks** (Caddy itself, Nextcloud-AIO, Postiz, optional extras): shared `proxy` (and `nextcloud-aio`). Caddy uses container DNS.
- Authentik `forward_auth` (Caddy snippet): apps with no native SSO (FileFlows, HandBrake Web, JDownloader, NocoDB). Do **not** FA apps that use OIDC or native login (Home Assistant, Nextcloud, n8n, WordPress, Gitea).
- **Extra HA OS VM(s)** (optional): Caddy `{HA_DOMAIN}` → `{HA_UPSTREAM}` (HA HTTP port). MCP stays on LAN. Each extra VM is its own OIDC app. See [05-authentik-home-assistant-sso.md](installation_guide/02-authentik-apps-auth/05-authentik-home-assistant-sso.md). This instance: [home/README.md](../home/README.md).

UDP/443 is HTTP/3. Without it clients stay on h2. STUN/TURN are not HTTP — see Router Port Forwarding.

Read: [caddy/README.md](../caddy/README.md).

## Public URL vs host port

Catalog apps stay published on the TrueNAS host so Caddy can reach `host.docker.internal:<port>`. Router does **not** forward those ports. Users use `https://{APP}_DOMAIN` (no port).

TrueNAS portals always show `http://<lan-ip>:<port>` — ignore them.

Apps that build their own links must be told the Caddy URL, or they append the host port (MCP OAuth resource mismatch):

| App | Public URL field |
|-----|------------------|
| n8n | `N8N_WEBHOOK_URL` / `N8N_EDITOR_BASE_URL` / `N8N_MCP_BASE_URL` (`n8n/README.md`) |
| Gitea | chart `root_url` |
| WordPress | `WP_HOME` / `WP_SITEURL` + `force-public-url.php` |
| NocoDB | chart `public_url` |
| Netbird | chart `netbird_address` |
| Authentik | brand + outpost `authentik_host` (`instance/authentik/Readme.md`) |

Do not unpublish catalog ports — Caddy would 502.

## Router Port Forwarding

| External port | Protocol | Destination | Notes |
|---|---|---|---|
| 80 | TCP | TrueNAS host:80 (Caddy) | ACME HTTP-01 + redirect |
| 443 | TCP/UDP | TrueNAS host:443 (Caddy) | HTTP/1.1 & HTTP/2 + HTTP/3 — required |
| 30417 | UDP/TCP | TrueNAS host:30417 | Netbird STUN (catalog default) |
| 3478 | UDP/TCP | TrueNAS host:3478 | Nextcloud Talk TURN/STUN |

Host LAN IP: `HOST_LAN_IP` / `TRUENAS_LAN` in `instance/truenas/.env`.

## Docker Network (`proxy`)

Created by the Caddy stack on first `up` (`name: proxy`). Other Dockge stacks join with `external: true`. Also creates `nextcloud-aio` (empty until AIO). Catalog apps do not join `proxy`.

Forwards to `{APP}_UPSTREAM`. Eg `WORDPRESS_UPSTREAM`.

## DNS

- Public A/AAAA for forwarded domains.
- Split-horizon wildcard → TrueNAS host IP (`TRUENAS_LAN`).
- TrueNAS `nameserver1` = AdGuard on this host; `nameserver2` = router. Start AdGuard before other catalog apps — otherwise Docker Hub/GHCR pulls stall (~20 min) and `app.start` fails with `Timed out waiting for response`.

A hostname outside the main wildcard needs its own AdGuard rewrite **and** public A/AAAA (else ACME never issues a cert).

LAN clients must use **only** AdGuard (`TRUENAS_LAN:53`). Extra resolvers (`1.1.1.1`, router DNS) return the public A. Then LAN→WAN IP→router→Caddy (hairpin) and transfers sit at ~100 Mbps / ~13 MB/s both ways. Check: `dig +short {APP}_DOMAIN` must be `TRUENAS_LAN`, not the WAN IP.

## Rate limit & CrowdSec

- `secured` snippet: Caddy `rate_limit`. Off on Nextcloud and Netbird.
- CrowdSec in-Caddy bouncer + `type: caddy` logs. LAN/Docker/Netbird ranges whitelisted. Do not overlay `/etc/crowdsec` with an empty volume.
