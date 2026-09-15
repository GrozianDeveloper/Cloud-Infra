# HomeBox ↔ Authentik (OIDC)

- Login: Authentik OIDC. Gate = Group Binding `homebox`.
- Redirect (strict): `https://{HOMEBOX_DOMAIN}/api/v1/users/login/oidc/callback`
- Issuer must match Authentik `/.well-known/openid-configuration` `issuer` **exactly** (trailing slash). Copy from discovery; do not invent.
- Authentik must answer discovery **before** HomeBox starts, or UI shows `OIDC provider not available`. Restart HomeBox after Authentik is up.

Official: [HomeBox OIDC](https://homebox.software/en/quick-start/configure/oidc/).

## Authentik

App slug `homebox`. Bind group `homebox` only. Map: [`auth_apps/map.yaml`](../../instance/maps/auth_apps/map.yaml).

Scopes: `openid email profile`. Do **not** set `HBOX_OIDC_ALLOWED_GROUPS` (Authentik bind is the gate; extra group filter would miss ancestor names unless `groups` scope + exact name).

## HomeBox env

Catalog `homebox.additional_envs` (values from secrets, never in git):

| Name | Why |
|------|-----|
| `HBOX_OIDC_ENABLED` | `true` |
| `HBOX_OIDC_ISSUER_URL` | `issuer` from discovery (not the well-known URL) |
| `HBOX_OIDC_CLIENT_ID` / `HBOX_OIDC_CLIENT_SECRET` | `instance/homebox/.env.oidc` |
| `HBOX_OPTIONS_TRUST_PROXY` | `true` (Caddy HTTPS) |
| `HBOX_OPTIONS_HOSTNAME` | `HOMEBOX_DOMAIN` only — no `https://` |
| `HBOX_OIDC_AUTO_REDIRECT` | `true` |
| `HBOX_OPTIONS_ALLOW_LOCAL_LOGIN` | `false`. Break-glass: set `true`, recreate catalog, local user |
| `HBOX_OIDC_VERIFY_EMAIL` | omit / `false` — Authentik may send `email_verified=false` |

## Inventory (groups / collections)

OIDC does **not** put users in a shared inventory. First login without an invite = empty private inventory.

1. One family member (Богдан) SSO first → that inventory is the house inventory.
2. Profile → invite link.
3. Others open the **invite URL**, then Authentik. Do not SSO the main URL first.

Shared membership is HomeBox UI, not the permissions map.
