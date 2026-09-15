# HomeBox

## Authentik

- slug = `homebox`
- bind group = `homebox`
- Redirect (strict): `https://{HOMEBOX_DOMAIN}/api/v1/users/login/oidc/callback`
- grant_types = `authorization_code`, `refresh_token`
- Scopes: `openid email profile`

## This NAS

- Catalog `homebox`. Domain: `HOMEBOX_DOMAIN` → `HOMEBOX_UPSTREAM` (`host.docker.internal:30149`)
- HostPath `apps/homebox` uid **568**. Creds: `instance/homebox/.env` + `.env.oidc`
