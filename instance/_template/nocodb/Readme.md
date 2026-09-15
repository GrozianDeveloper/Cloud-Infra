# NocoDB

## Authentik

- slug = `nocodb`
- Caddy `authentik_forward_auth`. Community has no SSO.
- bind group = `nocodb`

## This NAS

- Domain keys: `NOCODB_DOMAIN` → `NOCODB_UPSTREAM` in `instance/caddy/.env`
