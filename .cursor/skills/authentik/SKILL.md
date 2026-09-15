---
name: authentik
description: >
  Manage Authentik IdP via reusable scripts (users, groups, OIDC apps, tokens, attributes, generic API).
  Use every time when working on Authentik, SSO, OIDC, forward-auth, user_oidc, or instance/authentik/Readme.md.
  Never recreate curl/python against the Authentik API — run scripts/ instead.
---

# Authentik

**Always use this skill for Authentik work.** Run the scripts below. Do not invent curl, one-off python, or duplicate API clients.

- **URL / Admin**: `https://{AUTH_DOMAIN}/` · `/if/admin/`
- **API**: `https://{AUTH_DOMAIN}/api/v3/` · docs `/api/v4/docs/`
- **Instance providers**: `instance/authentik/Readme.md`
- **Forward auth**: `caddy/README.md`

## Creds

Scripts load defaults (never print them):

| Var | File |
|-----|------|
| `AUTHENTIK_TOKEN` | `instance/authentik/.env` |
| `AUTH_DOMAIN` | `instance/caddy/.env` |

Override when needed: `--token` `--domain` `--connect-host` on any script, or env `AUTHENTIK_TOKEN` / `AUTH_DOMAIN` / `AUTH_CONNECT_HOST`. `--domain` accepts host or URL.

If public DNS does not hit Caddy, scripts pin TLS SNI to `AUTH_DOMAIN` against TrueNAS LAN `:443`.

## Scripts

From repo root. JSON on stdout. Shared helper: `scripts/ak_lib.py` (do not call directly).

```bash
python3 .cursor/skills/authentik/scripts/<script>.py --help
```

| Script | When |
|--------|------|
| `whoami.py` | verify token |
| `list-users.py` `[--search] [--username]` | list users |
| `get-user.py --user <username\|pk>` | one user |
| `create-new-user.py --username --name [--email] [--path users] [--type internal] [--json '{}']` | create user |
| `set-user-attribute.py --user <u> --key K --value V` | merge one attribute (does not wipe others) |
| `set-user-attribute.py --user <u> --json '{"k":"v"}'` | merge attribute object |
| `list-groups.py` `[--search]` | list groups |
| `create-group.py --name [--parent <name\|pk>] [--superuser]` | create group (`--parent` repeatable → `parents`) |
| `add-user-to-group.py --user <u> --group <g>` | add member (`add_user`, not full-list PATCH) |
| `list-apps.py` `[--search]` | list applications |
| `create-oidc-app.py --name --slug --launch-url --redirect-uri URL [--consent implicit\|explicit] [--scopes openid,email,profile]` | new OIDC provider+app (create only) |
| `create-api-token.py --identifier [--description]` | non-expiring API token (prints key once) |
| `api.py METHOD PATH [JSON] [--paginate] [--file body.json]` | **any other endpoint** — use this instead of writing a new script |

Examples:

```bash
python3 .cursor/skills/authentik/scripts/whoami.py
python3 .cursor/skills/authentik/scripts/list-users.py
python3 .cursor/skills/authentik/scripts/create-new-user.py --username user@example.com --name "Full Name"
python3 .cursor/skills/authentik/scripts/add-user-to-group.py --user user@example.com --group "My Group"
python3 .cursor/skills/authentik/scripts/set-user-attribute.py --user akadmin --key nextcloud_user_id --value admin
python3 .cursor/skills/authentik/scripts/api.py GET core/users/me/
python3 .cursor/skills/authentik/scripts/api.py GET providers/oauth2/ --paginate
python3 .cursor/skills/authentik/scripts/api.py PATCH core/users/5/ '{"name":"New Name"}'
```

`create-oidc-app.py`: extra `--redirect-uri` (repeat), `--logout-uri`, `--signing-key`, `--client-id`, `--client-secret`, `--print-secret`. Nextcloud SSO is **not** this script — use bootstrap below.

## Flows / mappings

| Flow | Slug |
|------|------|
| Explicit consent | `default-provider-authorization-explicit-consent` |
| Implicit consent (trusted/internal) | `default-provider-authorization-implicit-consent` |
| Logout | `default-invalidation-flow` |

OIDC scopes: look up live via `api.py GET propertymappings/provider/scope/ --paginate`. Common: `openid`, `email`, `profile`. Signing key name: `authentik Self-signed Certificate`.

## Nextcloud OIDC

Idempotent Authentik side (writes `instance/master-nextcloud-aio/.env.oidc`):

```bash
python3 master-nextcloud-aio/scripts/oidc/authentik-create-nextcloud_oidc.py
```

Map existing NC `admin` account:

```bash
python3 .cursor/skills/authentik/scripts/set-user-attribute.py --user <authentik-username> --key nextcloud_user_id --value admin
```

On the TrueNAS host after AIO Start (`nextcloud-aio-nextcloud` up): `scripts/oidc/apply-oidc.sh` then `scripts/apply-mail.sh`. One-shot compose: `master-nextcloud-aio/scripts/oidc/host-apply-oidc.compose.yaml`. Details: `docs/installation_guide/02-authentik-apps-auth/04-authentik-nextcloud-sso.md`.

## Gotchas

1. List endpoints paginate — wrappers already follow `pagination.next`; `api.py` needs `--paginate`.
2. Do not PATCH a group's full `users` list — use `add-user-to-group.py`.
3. OAuth2 providers need a signing key or JWKS is `{}`.
4. Token `identifier` must be unique.
5. DEFCON 1 — API user/group/app changes are OK; do not print tokens.

## Endpoints (for `api.py`)

| Path | Methods |
|------|---------|
| `core/users/` | GET, POST |
| `core/users/{id}/` | GET, PATCH, DELETE |
| `core/groups/` | GET, POST |
| `core/groups/{pk}/` | GET, PATCH, DELETE |
| `core/groups/{pk}/add_user/` | POST `{"pk": user_pk}` |
| `core/applications/` | GET, POST |
| `core/tokens/` | GET, POST |
| `core/tokens/{identifier}/view_key/` | GET |
| `providers/all/` | GET |
| `providers/oauth2/` | GET, POST |
| `providers/proxy/` | GET, POST |
| `flows/instances/` | GET |
| `stages/all/` | GET |
| `sources/all/` | GET |
| `outposts/instances/` | GET |
| `propertymappings/provider/scope/` | GET, POST |
| `rbac/roles/` | GET |
