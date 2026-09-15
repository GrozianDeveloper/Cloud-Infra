# Proxmox VE

Install **only if** extra VMs (HA OS, more guests) or later several physical nodes. Else bare-metal TrueNAS ([12](12-truenas.md)).

Official ISO: [proxmox.com/downloads](https://www.proxmox.com/en/downloads). This repo does not replace that guide.

## Already installed

`PVE_URL`, token → `instance/proxmox/.env` (`PVE_URL`, `PVE_TOKEN_ID`, `PVE_TOKEN_SECRET`, `PVE_VERIFY_SSL=false` if self-signed). UI `:8006`. MCP: [proxmox/MCP.md](../../proxmox/MCP.md).

## This repo’s extras

- Disk split: hypervisor `local-lvm` vs disks passed through to TrueNAS. Note in [instance/hardware.md](../../instance/hardware.md).
- IOMMU / vfio for GPU. Not Primary GPU. Pass GPU to the TrueNAS VM if FileFlows/HandBrake.
- VM IDs in [instance/Readme.md](../../instance/Readme.md) (this instance: TrueNAS `100`, extra HA as needed).

App docs: [proxmox/README.md](../../proxmox/README.md).
