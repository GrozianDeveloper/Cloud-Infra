# Home MCP

Official: https://www.home-assistant.io/integrations/mcp_server/

URL: `{HOME_URL}/api/mcp` (LAN). Enable **Model Context Protocol Server** in HA. This VM listens on **`:80`**.

## Connect

- Config: `.cursor/mcp.json` server `home` (stdio). Wrapper `.cursor/mcp/home.sh` → `npx mcp-remote`.
- PATH: Cursor MCP spawn has no Homebrew. Wrapper sources `.cursor/mcp/path.sh`. Symptom if missing: `exec: npx: not found`.
- Auth: `HOME_MCP_TOKEN` in `instance/home/.env`. `HOME_URL` must include scheme+port.
- Tools only for entities [exposed to Assist](https://www.home-assistant.io/voice_control/voice_remote_expose_devices/).
  - Settings → Voice assistants → Expose (or https://my.home-assistant.io/redirect/voice_assistants).
  - Expose is per-entity. MCP tool list stays empty until at least one is exposed.
- After URL/token change: reload MCP server `home` in Cursor.

## Use when

HA state, Assist tools, to-do lists, lights/covers — same surface as Voice Assist.

## Do not

Put the token in `mcp.json` or docs. Do not put this MCP in `~/.cursor/mcp.json`. Do not send MCP through Caddy/OIDC — LAN token only.
