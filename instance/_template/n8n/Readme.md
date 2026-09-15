# n8n

## Authentik

- slug = `n8n`
- bind group = `n8n`
- Redirect: `https://{N8N_DOMAIN}/rest/sso/oidc/callback`
- Native SSO needs Enterprise — leave off. **No FA** (breaks MCP OAuth).
- Creds: `instance/n8n/.env.oidc`

## This NAS

- WebUI `30109` (Caddy only). Users: `https://{N8N_DOMAIN}`
- Data=`apps/n8n/data`, Postgres=ixVolume
- Email: `instance/email/.env`
