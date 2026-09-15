#!/usr/bin/env python3
"""Create missing keys in instance/homebox/.env. Never print secrets."""
from __future__ import annotations

import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".cursor/skills/authentik/scripts"))
from ak_lib import load_env

OUT = ROOT / "instance" / "homebox" / ".env"


def main() -> int:
    env = load_env(OUT)
    if not env.get("API_KEY_PEPPER"):
        env["API_KEY_PEPPER"] = secrets.token_urlsafe(48)
    lines = ["# HomeBox. Do not commit."]
    for k, v in env.items():
        if v:
            lines.append(f"{k}={v}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print("ok", OUT.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
