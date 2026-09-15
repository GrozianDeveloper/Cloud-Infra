# Authentik Applications & Providers

## Goal

• Create/update Authentik Application + Provider only. 
• This script doesnt apply to App-side SSO (occ, Gitea CLI, HA plugin, NetBird UI) — AI creates this manualy, by reading this YAML + `{app}/` docs.

## Files

[`map.yaml`](map.yaml) — list of apps.

## How to read

`type`: `oauth2` | `proxy` | `stub`. `{NAME}` in URLs = key from `instance/caddy/.env`. `secrets:` = env **keys** in `file:`, never values. Write missing keys; never overwrite existing client_id/secret. Never print secrets.

```yaml
- name: Home
  slug: home
  type: oauth2
  launch: "https://{HOME_DOMAIN}"
  bind_groups:
    - home
  provider:
    name: home
    client_type: confidential
    consent: implicit
    grant_types: [authorization_code, refresh_token]
    scopes: [openid, email, profile, groups, offline_access]
    redirects:
      - matching: strict
        kind: authorization
        url: "https://{HOME_DOMAIN}/auth/oidc/callback"
  secrets:
    file: instance/home/.env.oidc
    client_id: HOME_OIDC_CLIENT_ID
    client_secret: HOME_OIDC_CLIENT_SECRET
    discovery: HOME_OIDC_DISCOVERY
```

## Apply

Never delete groups & data. Creds: `instance/authentik/.env` + `instance/caddy/.env`.

```bash
python3 instance/maps/auth_apps/apply.py
python3 instance/maps/auth_apps/apply.py home nextcloud
```

Binds `bind_groups` only (Authentik includes child-group members). No `app-access-group-closure`. Proxy apps attach to Embedded Outpost. Gitea extra entitlement `gituser`.

OAuth2 `grant_types` from the map (default `authorization_code`, `refresh_token`). Empty on the live provider → Authentik `invalid_request` / malformed authorize.

## Effects

Application + Provider created/updated. Target apps themselves unchanged.

## Related

[Maps index](../index.md) · [permissions](../permissions/Readme.md) · [Authentik skill](../../../.cursor/skills/authentik/SKILL.md)
