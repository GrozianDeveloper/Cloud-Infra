# Caddy (this NAS)

Secrets: `instance/caddy/.env` — `{APP}_DOMAIN` / `{APP}_UPSTREAM` source of truth. Runtime copy: `apps/dockge/caddy/.env`.

Home: `proxy` net cannot reach the HA VM. `home-gw` (socat, host net) → `HOME_LAN:HOME_LAN_PORT`. Do not router-forward the gw port. See `instance/home/Readme.md`.