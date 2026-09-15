# List of installed apps & TrueNAS Paths

| App | Storage Paths | Notes |
|---|---|---|
| [Dockge](dockge/Readme.md) | Stacks=`apps/dockge`, Data=`apps/dockge/data` | |
| [Caddy](caddy/Readme.md) | Dockge `apps/dockge/caddy` | secrets `instance/caddy/.env` |
| [Netbird Server](netbird-server/Readme.md) | Data=`apps/netbird_s/data`, Config=`apps/netbird_s/config` | |
| [Authentik](authentik/Readme.md) | `apps/authentik/{data,db,certs,template}` | |
| [Nextcloud-AIO](master-nextcloud-aio/Readme.md) | see that Readme | |
| [Nextcloud MCP](nextcloud-mcp/Readme.md) | `apps/nextcloud-mcp` | |
| [n8n](n8n/Readme.md) | Data=`apps/n8n/data` | |
| [Gitea](gitea/Readme.md) | Config=`apps/gitea/config`, Data=`church_tank/gitea_data` | |
| [Gitea Act Runner](gitea-runner/Readme.md) | Data=`apps/gitea-runner` | uid `568:568` |
| [FileFlows](fileflows/Readme.md) | `apps/fileflows/{data,logs,temp}`, `fast/media_work` | |
| [HandBrake](handbrake/Readme.md) | `apps/handbrake-web/data`, `fast/media_work` | |
| [Postiz](postiz/Readme.md) | `apps/postiz/{config,uploads,postgres,redis,temporal-pg,temporal-es}` | |
| [Home](home/Readme.md) | HA OS VM | separate Proxmox VM |
| [WordPress](wordpress/Readme.md) | Data=`apps/wordpress/data`, MariaDB=`apps/wordpress/mariadb` | |
| [NocoDB](nocodb/Readme.md) | | Caddy FA |
| [AdGuard Home](adguardhome/Readme.md) | Config=`apps/adguardhome` | |
| [Tandoor Recipes](tandoor-recipes/Readme.md) | Static=`fast/tandoor-static`, Media=`church_tank/tandoor-media`, Postgres=`apps/tandoor-db` | uid **999**, catalog **Automatic Permissions** |
| [HomeBox](homebox/Readme.md) | Data=`apps/homebox` | uid **568**, catalog OIDC |
| [Gramps Web](gramps-web/Readme.md) | Users/index/thumbs/cache=`apps/gramps-*`, Media=`church_tank/gramps-media`, DB=`church_tank/gramps-db` | uid **0**, multi-tree |
| [TrueNAS](truenas/Readme.md) | | |
| [Proxmox](proxmox/Readme.md) | | |
| [Home stub](home/Readme.md) | | church HA later |
| [Email](email/Readme.md) | | shared SMTP |

# `instance/{app_name}/` contents

- Doc: `Readme.md`
- Secrets: `.env`, `.env.oidc`…
