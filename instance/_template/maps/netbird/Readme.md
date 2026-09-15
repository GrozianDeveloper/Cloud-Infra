# NetBird

## Goal

Pointwise VPN: overlay groups, Networks, domain/CIDR resources, port policies. Authentik `name` ↔ NetBird `from_authentik` / permissions `netbird.group` + `netbird.network`.

Three Networks share nothing (groups, resources, policies, router groups). Same physical LAN (`TRUENAS_LAN` subnet) does not merge them.

## Files

[`map.yaml`](map.yaml). Empty sections skipped.

## How to read

| Section | What |
|---------|------|
| `groups` | NetBird group `name`. `from_authentik` = Authentik group (docs + IdP). `res-*` / `routers-*` are not Authentik |
| `networks` | Container per environment |
| `resources` | Destinations. `address` = FQDN or CIDR. `lan_ip` / `mac` / `uuid` = docs only |
| `policies` | Source user groups → dest `res-*` groups, ports. `bidirectional: false` |
| `routers` | `peer_groups` per network. `enabled: false` until a peer exists. Do not share peers across networks |
| `nameservers` | Empty on purpose |

`*-vpn` groups: overlay identity, no resource policy.

Peers are not in the map.

## Routing peer

A NetBird client on church LAN. Overlay packets go to that peer; it forwards to LAN IPs listed as resources in **that** Network only.

- `local-infra/lan` → LAN CIDR → cameras (and any LAN IP) by IP
- `cloud-infra` → only Proxmox / TrueNAS / Dockge / Nextcloud Master FQDNs + listed ports
- `real_estate` → only Geo PC Moonlight ports

`local-infra/lan` can reach TrueNAS / PVE / Geo PC by IP. Do not give that group to people who must not hit those hosts. That is physical LAN, not a shared NetBird object.

Do not use a true exit node (`0.0.0.0/0`) — that would NAT all internet through church.

Prefer a routing peer that is **not** TrueNAS or Proxmox: UI/SSH to those hosts stay “through” the resource. If the peer **is** TrueNAS, TrueNAS UI/SSH need an extra peer-to-peer policy (input chain).

## DNS

No NetBird nameservers (not primary, not match-domain). Public Caddy FQDNs stay on public DNS.

VPN-only names are **domain resources**. Client with a policy gets that name via the routing peer DNS forwarder. Routing peer must resolve them (AdGuard rewrite — `todo/netbird/after-map-apply.md`).

FQDNs and LAN IPs: `map.yaml` + `instance/truenas/.env` / `instance/proxmox/.env`. Do not duplicate values here.

## Apply

Never delete. PAT: `instance/netbird-server/.env` (`NETBIRD_API_TOKEN`). Domain: `instance/caddy/.env` `NETBIRD_DOMAIN`.

Do not apply until review. Routers stay disabled (no peers).

```bash
python3 instance/maps/netbird/apply.py
python3 instance/maps/netbird/apply.py groups,networks
python3 instance/maps/netbird/apply.py --dump --force-dump
```

`--dump` overwrites this file. Requires `--force-dump`.

## Effects

Creates missing groups / networks / resources / policies. Existing names left as-is. Disabled routers skipped. Peers unchanged.

## Related

[Maps index](../index.md) · [permissions](../permissions/Readme.md) · [todo](../../../todo/netbird/after-map-apply.md)
