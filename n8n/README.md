# n8n

Goal: Main place for all automations (FileFlows, Home Assistant, FreeShow)

## Docs

- [MCP](MCP.md)
- [Instance](../instance/n8n/Readme.md)

## Installation

- Secrets: [OIDC](../instance/n8n/.env.oidc). Email: [SMTP](../instance/email/.env)
- Caddy: `N8N_DOMAIN` → `N8N_UPSTREAM`. Users never use host `:30109`.
- additional_envs (catalog cannot override chart `N8N_PROTOCOL` / `N8N_HOST` / `N8N_PORT`):
  - `N8N_WEBHOOK_URL` = `https://{N8N_DOMAIN}/`
  - `N8N_EDITOR_BASE_URL` = `https://{N8N_DOMAIN}`
  - `N8N_MCP_BASE_URL` = `https://{N8N_DOMAIN}`
  - `N8N_PROXY_HOPS` = `1`
- Runner Mode = Internal
- Native SSO needs Enterprise — leave off. **No FA**.
