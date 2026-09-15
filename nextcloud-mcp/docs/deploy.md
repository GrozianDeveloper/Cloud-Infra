# Deploy (Dockge on TrueNAS)

Stack dir: `apps/dockge/nextcloud-mcp/`

```
compose.yaml   # copy of docker-compose.yml
.env           # copy of instance/nextcloud-mcp/.env — not in git
```

Data HostPath: `apps/nextcloud-mcp` (uid **1000**, mode `0750`). Create dataset before first `up`.

Compose key is `services:` (Dockge compose on this host rejects `apps:`).

Upload from repo root:

```bash
node .cursor/skills/truenas-scale/scripts/tn-put.mjs \
  nextcloud-mcp/docker-compose.yml \
  /mnt/apps/dockge/nextcloud-mcp/compose.yaml
node .cursor/skills/truenas-scale/scripts/tn-put.mjs \
  instance/nextcloud-mcp/.env \
  /mnt/apps/dockge/nextcloud-mcp/.env
```

Start (pulls GHCR image; confirm first):

```bash
node .cursor/skills/agentskillexchange-skills-dockge-docker-compose-stack-manager/scripts/dockge-start.mjs start nextcloud-mcp
node .cursor/skills/agentskillexchange-skills-dockge-docker-compose-stack-manager/scripts/dockge-start.mjs status nextcloud-mcp
```

Probe from this Mac: `curl http://192.168.0.35:31800/health/ready`
