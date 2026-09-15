# Postiz

## Authentik

- slug = `postiz`
- bind group = `postiz`
- Redirect: `https://{POSTIZ_DOMAIN}/settings`
- Creds: `instance/postiz/.env.oidc`

## This NAS

- Dockge stack `postiz`. Image `ghcr.io/gitroomhq/postiz-app:v2.23.0`
- HostPath `apps/postiz/{config,uploads,postgres,redis,temporal-pg,temporal-es}`
- Secrets: `instance/postiz/.env` + `.env.oidc`. Map SQL: `instance/postiz/postiz-apply.sql`
- Email from `instance/email/.env`
- Workspaces: [`../maps/map-postiz`](../maps/map-postiz/Readme.md)
