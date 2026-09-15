# Router port forwarding

Forward WAN ports to this host's LAN IP (`HOST_LAN_IP` / `TRUENAS_LAN` in `instance/truenas/.env`).

See [networking.md](../networking.md).

UDP/443 is required for HTTP/3. Caddy advertises `Alt-Svc: h3=":443"` on every vhost; if the router only forwards TCP, browsers never switch. See [caddy/README.md](../../caddy/README.md#http3--all-four-must-be-true).

Talk Recording does NOT need a router forward: AIO keeps the recording container (`:1234`) inside the docker network and Nextcloud reaches it by internal DNS.

## Steps (example: TP-Link Archer-style UI)

Any router with static DHCP + virtual servers works. Names of menus differ.

1. Reserve a static DHCP lease for this host's MAC.
2. Add one virtual-server / port-forward row per [networking.md](../networking.md#router-port-forwarding) line.
3. If the UI treats TCP and UDP as separate rows, add each protocol as its own row.
4. If this host's LAN IP changes, update `HOST_LAN_IP` / `TRUENAS_LAN` in `instance/truenas/.env`.
5. Disable `SIP ALG`, `UPnP` (optional), and any "block ICMP" / "DoS protection" that may break STUN or QUIC.

## Host (TrueNAS SCALE)

UI is on **880 / 8443** so Caddy can own **80 / 443**. Published Docker ports are allowed inbound by default.

QUIC UDP buffer — persist as **System → Tunables** (SYSCTL), not `/etc/sysctl.d`:

- `net.core.rmem_max=2500000`
- `net.core.rmem_default=2500000`

See [caddy/README.md](../../caddy/README.md#http3--all-four-must-be-true).

## Verify

From an outside network (e.g. phone hotspot). macOS stock `curl` has no `--http3`.

```
curl -sI https://{AUTH_DOMAIN} | grep -i alt-svc
curl -sI --http3 https://{AUTH_DOMAIN} | head   # needs an h3-capable curl
curl -vI https://{NEXTCLOUD_DOMAIN}
nc -vz {NETBIRD_DOMAIN} 443
nc -vz {NEXTCLOUD_DOMAIN} 3478
nmap -sU -p 443 {AUTH_DOMAIN}        # HTTP/3
nmap -sU -p 3478 {NEXTCLOUD_DOMAIN}  # AIO Talk
nmap -sU -p 30417 {NETBIRD_DOMAIN}   # Netbird STUN (catalog default)
```
