#!/usr/bin/env python3
"""Upsert TrueNAS SYSCTL tunables. Idempotent. Args: VAR=VALUE [VAR=VALUE...]"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".cursor/skills/truenas-scale/scripts"))
from tn import call_job, tn


def _pairs(argv: list[str]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for a in argv:
        if "=" not in a or a.strip().startswith("#"):
            raise SystemExit(f"bad arg: {a}")
        k, v = a.split("=", 1)
        k, v = k.strip(), v.strip()
        if not k or not v:
            raise SystemExit(f"bad arg: {a}")
        out.append((k, v))
    return out


def main() -> int:
    if not sys.argv[1:]:
        print("Usage: apply-tunables.py VAR=VALUE [VAR=VALUE...]", file=sys.stderr)
        return 1
    rows = tn("tunable.query", [])
    if not isinstance(rows, list):
        raise SystemExit("tunable.query: expected list")
    by_var = {str(t.get("var")): t for t in rows if isinstance(t, dict)}
    for var, value in _pairs(sys.argv[1:]):
        rec = by_var.get(var)
        if rec:
            tid = rec.get("id")
            if rec.get("value") == value and rec.get("enabled") is True:
                print("ok", var)
                continue
            call_job("tunable.update", [tid, {"value": value, "enabled": True}])
            print("updated", var)
            continue
        call_job(
            "tunable.create",
            {
                "type": "SYSCTL",
                "var": var,
                "value": value,
                "enabled": True,
                "update_initramfs": False,
            },
        )
        print("created", var)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
