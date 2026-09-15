# NetBird Server

Goal: Host VPNs. Dashboard + combined server.

## Docs

- [Network Map](../instance/maps/netbird/Readme.md)
- [Instance](../instance/netbird-server/Readme.md)
- [NetBird Authentik](https://docs.netbird.io/selfhosted/identity-providers/authentik)
- [OIDC install notes](../docs/installation_guide/02-authentik-apps-auth/02.1-authentik-netbird-oidc.md)

## Installation

- Caddy: `NETBIRD_UPSTREAM`, `NETBIRD_MGMT_UPSTREAM` in `instance/caddy/.env`
- Caddy splits gRPC/`/api`/`/relay` **and `/oauth2*`** (embedded Dex) to mgmt; SPA to web. STUN stays on host.
  - Missing `/oauth2*` → SPA 404 → login **Unauthenticated** / dead Logout.
- WAN: STUN `30417` only. Relay is Caddy `/relay` on 443. No Coturn.
- Keep `embedded_idp=true`. **Do not** set `embedded_idp=false` — chart drops client id ([netbird#5335](https://github.com/netbirdio/netbird/issues/5335)).
- Path A: Dex stays. NetBird UI → Identity Providers → Generic OIDC → Authentik issuer `https://AUTH_DOMAIN/application/o/netbird/`. Disable local login.
- Secrets: [OIDC](../instance/netbird-server/.env.oidc). PAT: [instance/netbird-server/.env](../instance/netbird-server/.env)
