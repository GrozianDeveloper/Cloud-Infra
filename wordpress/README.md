# WordPress

Goal: Public web site

## Docs

- [Instance](../instance/wordpress/Readme.md)

## Installation

- Secrets: [OIDC](../instance/wordpress/.env.oidc)
- Caddy: `WORDPRESS_DOMAIN` → `WORDPRESS_UPSTREAM` + `X-Forwarded-Proto https`
- Public pages stay public. Enforce Privacy off.

## Scripts

| Path | What |
|---|---|
| `scripts/force-public-url.php` | strips LAN hosts and `:ports`; DB `home`/`siteurl` = `WORDPRESS_DOMAIN` |
| `scripts/apply-oidc.sh` | OpenID Connect Generic; `host` = NAS sidecar. Settings from `instance/wordpress/.env.oidc` |
