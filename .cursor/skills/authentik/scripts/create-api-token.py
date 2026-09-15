#!/usr/bin/env python3
"""Create a non-expiring API token and print its key once."""
from __future__ import annotations

import argparse
import sys

from ak_lib import add_common_args, creds_from_args, dump, request


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    add_common_args(p)
    p.add_argument("--identifier", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--user", type=int, help="user pk (default: token owner)")
    args = p.parse_args()
    token, domain = creds_from_args(args)
    body = {
        "identifier": args.identifier,
        "intent": "api",
        "expiring": False,
        "description": args.description,
    }
    if args.user is not None:
        body["user"] = args.user
    created = request("POST", "/core/tokens/", token, domain, body)
    key = request("GET", f"/core/tokens/{args.identifier}/view_key/", token, domain)
    dump({"token": created, "key": key.get("key")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
