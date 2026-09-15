#!/usr/bin/env python3
"""HTTPS GET each instance/caddy/.env *_DOMAIN. Exit 1 on connect/5xx."""
from __future__ import annotations

import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".cursor/skills/authentik/scripts"))
from ak_lib import load_env

CTX = ssl._create_unverified_context()


def main() -> int:
    caddy = load_env(ROOT / "instance" / "caddy" / ".env")
    keys = sys.argv[1:] or sorted(k for k in caddy if k.endswith("_DOMAIN") and caddy.get(k))
    if not keys:
        print("no *_DOMAIN in instance/caddy/.env", file=sys.stderr)
        return 1
    bad = 0
    for k in keys:
        host = caddy.get(k) or ""
        if not host:
            print(k, "MISSING")
            bad += 1
            continue
        url = f"https://{host}/"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
                print(k, resp.status)
                if resp.status >= 500:
                    bad += 1
        except urllib.error.HTTPError as e:
            print(k, e.code)
            if e.code >= 500:
                bad += 1
        except OSError as e:
            print(k, "FAIL", type(e).__name__)
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
