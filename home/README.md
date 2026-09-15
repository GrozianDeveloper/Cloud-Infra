# Home Assistant OS

Goal: Family smart-home dashboard

## Docs

- [MCP](MCP.md)
- [Instance](../instance/home/Readme.md)
- Generic extra HA VM: [05-authentik-home-assistant-sso.md](../docs/installation_guide/02-authentik-apps-auth/05-authentik-home-assistant-sso.md)
- Skill: `.agents/skills/home-assistant-best-practices`

## Installation

- Secrets: [Main](../instance/home/.env), [OIDC](../instance/home/.env.oidc)
- Caddy: `HOME_DOMAIN` → `HOME_UPSTREAM` (**no** FA)
- Caddy `proxy` net cannot reach this VM. `home-gw` (socat) on TrueNAS.

## HTTP behind Caddy

Caddy always sends `X-Forwarded-For`. HA requires the **TCP peer** in `http.trusted_proxies`. Peer is TrueNAS LAN (socat), not Docker `172.16.0.0/12`.

If that IP is missing: `https://{HOME_DOMAIN}` → `400`. LAN still works. Then restart Core. Set External URL = `https://{HOME_DOMAIN}`.
