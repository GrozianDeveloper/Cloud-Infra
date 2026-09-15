#!/usr/bin/env python3
"""Print TrueNAS catalog app states. Exit 1 if named apps are not RUNNING."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".cursor/skills/truenas-scale/scripts"))
from tn import tn


def _state(rec: dict) -> str:
    st = rec.get("state")
    if isinstance(st, dict):
        return str(st.get("state") or st.get("status") or "")
    return str(st or "")


def main() -> int:
    want = sys.argv[1:]
    recs = tn("app.query", [])
    if not isinstance(recs, list):
        raise SystemExit("app.query: expected list")
    by_name = {str(r.get("name")): r for r in recs if isinstance(r, dict)}
    names = want or sorted(by_name)
    bad = 0
    for name in names:
        rec = by_name.get(name)
        if not rec:
            print(name, "MISSING")
            bad += 1
            continue
        st = _state(rec)
        print(name, st)
        if want and st.upper() != "RUNNING":
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
