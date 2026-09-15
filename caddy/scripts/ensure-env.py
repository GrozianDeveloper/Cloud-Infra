#!/usr/bin/env python3
"""Add KEY=value to instance/caddy/.env. Never overwrite."""
from __future__ import annotations

import sys
from pathlib import Path


def repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "instance").is_dir() and (parent / "Readme.md").is_file():
            return parent
    raise SystemExit("repo root not found")


def main() -> int:
    if not sys.argv[1:]:
        print("Usage: ensure-env.py KEY=value [KEY=value...]", file=sys.stderr)
        return 1
    pairs: list[tuple[str, str]] = []
    for a in sys.argv[1:]:
        if "=" not in a or a.strip().startswith("#"):
            print(f"bad arg: {a}", file=sys.stderr)
            return 1
        k, v = a.split("=", 1)
        k = k.strip()
        if not k:
            print(f"bad arg: {a}", file=sys.stderr)
            return 1
        pairs.append((k, v))
    caddy = repo_root() / "instance" / "caddy" / ".env"
    text = caddy.read_text() if caddy.exists() else ""
    have = {
        line.split("=", 1)[0].strip()
        for line in text.splitlines()
        if "=" in line and not line.strip().startswith("#")
    }
    add = [f"{k}={v}" for k, v in pairs if k not in have]
    if not add:
        print("caddy env ok")
        return 0
    if text and not text.endswith("\n"):
        text += "\n"
    caddy.write_text(text + "\n".join(add) + "\n")
    print("caddy env +", *[a.split("=", 1)[0] for a in add])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
