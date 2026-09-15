#!/usr/bin/env python3
"""Create missing keys in instance/gramps-web/.env. Never print secrets."""
from __future__ import annotations

import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".cursor/skills/authentik/scripts"))
from ak_lib import load_env

OUT = ROOT / "instance" / "gramps-web" / ".env"


def main() -> int:
    env = load_env(OUT)
    if not env.get("SECRET_KEY"):
        env["SECRET_KEY"] = secrets.token_urlsafe(48)
    if not env.get("REDIS_PASSWORD"):
        env["REDIS_PASSWORD"] = secrets.token_urlsafe(24)
    if len(env["SECRET_KEY"]) < 32:
        raise SystemExit("SECRET_KEY must be at least 32 characters")
    lines = ["# Gramps Web. Do not commit."]
    for k, v in env.items():
        if v:
            lines.append(f"{k}={v}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print("ok", OUT.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
