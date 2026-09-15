#!/usr/bin/env python3
"""Create an internal user."""
from __future__ import annotations

import argparse
import sys

from ak_lib import add_common_args, creds_from_args, dump, parse_json_arg, request


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    add_common_args(p)
    p.add_argument("--username", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--email")
    p.add_argument("--path", default="users")
    p.add_argument("--type", default="internal")
    p.add_argument("--inactive", action="store_true")
    p.add_argument("--json", help="extra fields merged into POST body")
    args = p.parse_args()
    token, domain = creds_from_args(args)
    body = {
        "username": args.username,
        "name": args.name,
        "email": args.email or args.username,
        "is_active": not args.inactive,
        "type": args.type,
        "path": args.path,
    }
    extra = parse_json_arg(args.json)
    if extra:
        body.update(extra)
    dump(request("POST", "/core/users/", token, domain, body))
    return 0


if __name__ == "__main__":
    sys.exit(main())
