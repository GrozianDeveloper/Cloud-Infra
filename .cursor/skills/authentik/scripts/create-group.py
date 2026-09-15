#!/usr/bin/env python3
"""Create a group. Repeat --parent for multiple parents (Authentik 2025.12+)."""
from __future__ import annotations

import argparse
import sys

from ak_lib import add_common_args, creds_from_args, dump, find_group, request


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    add_common_args(p)
    p.add_argument("--name", required=True)
    p.add_argument("--parent", action="append", default=[], help="parent name or pk (repeatable)")
    p.add_argument("--superuser", action="store_true")
    args = p.parse_args()
    token, domain = creds_from_args(args)
    parents = [find_group(token, domain, ident)["pk"] for ident in args.parent]
    body = {"name": args.name, "is_superuser": args.superuser, "parents": parents}
    dump(request("POST", "/core/groups/", token, domain, body))
    return 0


if __name__ == "__main__":
    sys.exit(main())
