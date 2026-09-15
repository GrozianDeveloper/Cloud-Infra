# Gramps Web

## Authentik

- slug = `gramps`
- bind group = `gramps`
- Redirect (regex): `https://{GRAMPS_DOMAIN}/api/oidc/callback/.*`
- grant_types = `authorization_code`, `refresh_token`
- Scopes: `openid email profile groups`

## This NAS

- Catalog `gramps-web`. Domain: `GRAMPS_DOMAIN` → `GRAMPS_UPSTREAM` (`host.docker.internal:30179`)
- Multi-tree (`TREE=*`). First tree via API after local owner (see `gramps-web/docs/sso.md`)
- HostPath: `apps/gramps-{users,index,thumbs,cache}` uid **0**; `church_tank/gramps-{media,db}` uid **0**
- Creds: `instance/gramps-web/.env` + `.env.oidc`
