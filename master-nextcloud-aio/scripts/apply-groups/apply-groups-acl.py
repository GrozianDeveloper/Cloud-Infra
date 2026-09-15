#!/usr/bin/env python3
"""Legacy wrapper → instance/maps/permissions/apply-permissions-map.py."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TARGET = Path(__file__).resolve().parents[2] / "instance/maps/permissions/apply-permissions-map.py"


def main() -> int:
    print("use instance/maps/permissions/apply-permissions-map.py", file=sys.stderr)
    return subprocess.call([sys.executable, str(TARGET), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
