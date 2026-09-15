# HandBrake Web

## Authentik

- Caddy forward_auth (same pattern as FileFlows)

## This NAS

- WebUI host `31116` → container `9999`
- Data=`apps/handbrake-web/data` → `/data`, Video=`fast/media_work` → `/video`
- GPU: PCI from `instance/hardware.md` (passed to TrueNAS)
