# Dockge

Goal: Host non TrueNAS-native apps
eg Nextcloud-AIO, Caddy

## Docs

- [Instance](../instance/dockge/Readme.md)
- Skill: `.cursor/skills/agentskillexchange-skills-dockge-docker-compose-stack-manager/SKILL.md`

## Installation

- TrueNAS App: `dockge`
- Ports: WebUI=31014. Host Network=false
- Storage: Stacks=`apps/dockge`, Data=`apps/dockge/data`

## Scripts

```bash
node .cursor/skills/agentskillexchange-skills-dockge-docker-compose-stack-manager/scripts/dockge-start.mjs list
node .cursor/skills/agentskillexchange-skills-dockge-docker-compose-stack-manager/scripts/dockge-start.mjs status <stack>
```

`start` / `down` change running stacks — confirm first. List/update images: `.cursor/skills/truenas-scale/scripts/dockge-list.mjs` / `dockge-update.mjs`.
