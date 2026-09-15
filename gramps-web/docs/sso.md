# Gramps Web ↔ Authentik (OIDC)

- Login: Authentik OIDC. Gate = Group Binding `gramps`.
- Custom provider id in Gramps = `custom`. Redirect regex: `https://{GRAMPS_DOMAIN}/api/oidc/callback/.*`
- Env names are `GRAMPSWEB_*` (catalog additional_envs). Booleans lowercase `true`/`false`.
- `OIDC_ISSUER` = Authentik `issuer` from discovery (not the well-known URL). Trailing slash must match.

Official: [Gramps OIDC](https://www.grampsweb.org/install_setup/oidc/), [multi-tree](https://www.grampsweb.org/install_setup/multi-tree/).

## Authentik

App slug `gramps`. Bind group `gramps` only. Map: [`auth_apps/map.yaml`](../../instance/maps/auth_apps/map.yaml).

Scopes: `openid email profile groups` (`groups` = role mapping).

## Gramps env

| Name | Why |
|------|-----|
| `GRAMPSWEB_BASE_URL` | `https://{GRAMPS_DOMAIN}` |
| `GRAMPSWEB_OIDC_ENABLED` | `true` |
| `GRAMPSWEB_OIDC_ISSUER` | issuer from discovery |
| `GRAMPSWEB_OIDC_CLIENT_ID` / `GRAMPSWEB_OIDC_CLIENT_SECRET` | `instance/gramps-web/.env.oidc` |
| `GRAMPSWEB_OIDC_NAME` | `Authentik` |
| `GRAMPSWEB_OIDC_SCOPES` | `openid email profile groups` |
| `GRAMPSWEB_OIDC_ROLE_CLAIM` | `groups` |
| `GRAMPSWEB_OIDC_GROUP_OWNER` | `gramps` — set **before** first OIDC login |
| `GRAMPSWEB_OIDC_AUTO_REDIRECT` | `true` |
| `GRAMPSWEB_OIDC_DISABLE_LOCAL_AUTH` | `false` — keep local for site-admin / break-glass |

Do not enable Google/Microsoft providers (role-mapping bug when mixed with custom).

## Multi-tree (this instance)

One Authentik user ↔ one Gramps account ↔ **one** tree. Several people **can** share one tree. One person cannot SSO into a second tree with the same Authentik user (needs a second IdP identity).

OIDC login URL includes `tree=<tree_id>`. Empty install has **no** trees → OIDC cannot bootstrap.

1. Local owner (no tree) — catalog first-run / `user add`. Site admin cannot OIDC.
2. `POST /api/trees/` as that owner → first tree (UUID id). This is the Family tree.
3. Family SSO with that `tree` id. Role `Owner` because `gramps` is in the `groups` claim (`OIDC_GROUP_OWNER=gramps`).
4. Extra trees later: same API. Hide frontend register (`hideRegisterLink`) — register cannot pick a tree.

Tree membership is Gramps, not the permissions map.
