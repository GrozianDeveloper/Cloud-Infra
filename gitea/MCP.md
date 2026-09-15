# Gitea MCP

Official server: https://gitea.com/gitea/gitea-mcp  
Workspace: `.cursor/mcp/gitea.sh` → binary `.cursor/mcp/bin/gitea-mcp` (gitignored).

## Connect

- Config: `.cursor/mcp.json` server `gitea` (stdio).
- Auth: `GITEA_ACCESS_TOKEN` from `instance/gitea/.env` (admin PAT).
- Host: `GITEA_HOST` in that env (LAN `http://<truenas>:30008`). `GIT_DOMAIN` HTTPS if DNS (AdGuard) works on this machine.
- First clone / other Mac: `bash .cursor/mcp/install-gitea-mcp.sh`

## Use when

Repos, issues, PRs, files, branches, tags, releases, Actions, wiki, packages, notifications on this Gitea.

## Do not

Put the token in `mcp.json` or docs. Do not point `--host` at gitea.com — this instance only.
