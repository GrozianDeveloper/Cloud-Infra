# n8n MCP — instance-level

Official: https://docs.n8n.io/connect/connect-to-n8n-mcp-server

URL: `https://{N8N_DOMAIN}/mcp-server/http`  
OAuth metadata: `/.well-known/oauth-protected-resource/mcp-server/http`

## Connect

- Config: `.cursor/mcp.json` server `n8n`. Cursor type must be `streamable-http` (not `http`) + `https://{N8N_DOMAIN}/mcp-server/http`. OAuth in the browser.
- Public URL must match metadata exactly (`https`, no host port). See `n8n/README.md` additional_envs.
- Do not put n8n in `~/.cursor/mcp.json`. A leftover `http://…:30109` URL causes resource mismatch.
- Enable MCP on workflows that should be visible (Settings → MCP access).

## Do not

Point MCP at `http://…:30109`. That is the TrueNAS host port for Caddy, not the public URL. Resource mismatch if the client uses the domain and n8n advertises `:30109`.
