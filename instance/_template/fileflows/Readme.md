# FileFlows

## Authentik

- slug = `fileflows`
- Caddy forward_auth + Embedded Outpost
- bind group = `fileflows`

## This NAS

- Server port `19200`
- HostPath: Data=`apps/fileflows/data`, Logs=`apps/fileflows/logs`, Temp=`apps/fileflows/temp`, Additional: `fast/media_work` → `/media/work`
- GPU: PCI from `instance/hardware.md` (passed to TrueNAS)
