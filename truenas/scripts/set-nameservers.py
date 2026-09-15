#!/usr/bin/env python3
"""Set TrueNAS DNS nameservers. No defaults. ns1 = AdGuard on this host."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".cursor/skills/truenas-scale/scripts"))
from tn import tn


def main() -> int:
    p = argparse.ArgumentParser(description="Update TrueNAS nameserver1..3")
    p.add_argument("ns1", help="primary (AdGuard LAN IP)")
    p.add_argument("ns2", nargs="?", default="", help="secondary (router)")
    p.add_argument("ns3", nargs="?", default="", help="tertiary")
    args = p.parse_args()
    data = {"nameserver1": args.ns1, "nameserver2": args.ns2, "nameserver3": args.ns3}
    tn("network.configuration.update", [data])
    print("nameservers", args.ns1, args.ns2 or "-", args.ns3 or "-")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
