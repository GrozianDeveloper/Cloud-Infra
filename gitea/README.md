# Gitea

Goal: version control `infra/` and centralize automations (n8n, FileFlows…)

## Docs

- [MCP](MCP.md)
- [Instance](../instance/gitea/Readme.md)
- Runner: [gitea-runner](../gitea-runner/README.md)

## Installation

- TrueNAS App: `gitea`
- Secrets: [Main](../instance/gitea/.env), [OIDC](../instance/gitea/.env.oidc). Email: [SMTP](../instance/email/.env)
- Caddy: `GIT_DOMAIN` → `GIT_UPSTREAM` (no FA; Gitea login)
- Actions: `additional_envs` → `GITEA__ACTIONS__ENABLED=true`

## Scripts

| Path | What |
|---|---|
| `scripts/apply-oidc-host.sh` | Gitea 1.27 has no `/api/v1/admin/auths` — CLI. Name must stay `authentik` |
| `scripts/apply-oidc.py` | API path (unused on 1.27) |
