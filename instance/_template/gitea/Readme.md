# Gitea

## Authentik

- slug = `gitea`
- bind group = `gitea`
- Auth source name in Gitea **must** be `authentik`
- Redirect: `https://{GIT_DOMAIN}/user/oauth2/authentik/callback`
- Entitlement `gituser`
- Creds: `instance/gitea/.env.oidc`

## This NAS

- WebUI `30008`, SSH `30009`
- Config=`apps/gitea/config`, Data=`church_tank/gitea_data`, Postgres=ixVolume (future: `apps/gitea/db`)
- Secrets: `instance/gitea/.env` (`GITEA_ACCESS_TOKEN`, `GITEA_HOST`, `RUNNER_REGISTRATION_TOKEN`)
- Email: `instance/email/.env`
