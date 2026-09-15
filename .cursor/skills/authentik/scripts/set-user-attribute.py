#!/usr/bin/env python3
"""Merge attributes onto a user (does not wipe existing keys)."""
from __future__ import annotations

import argparse
import json
import sys

from ak_lib import (
    add_common_args,
    creds_from_args,
    deep_merge,
    dump,
    find_user,
    parse_json_arg,
    request,
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    add_common_args(p)
    p.add_argument("--user", required=True, help="username or pk")
    p.add_argument("--key", help="top-level attribute key")
    p.add_argument("--value", help="value (JSON if parseable, else string)")
    p.add_argument("--json", help='merge object, e.g. {"nextcloud_user_id":"admin"}')
    args = p.parse_args()
    if not args.key and not args.json:
        raise SystemExit("need --key/--value or --json")
    token, domain = creds_from_args(args)
    user = find_user(token, domain, args.user)
    attrs = dict(user.get("attributes") or {})
    extra = parse_json_arg(args.json)
    if extra:
        if not isinstance(extra, dict):
            raise SystemExit("--json must be an object")
        attrs = deep_merge(attrs, extra)
    if args.key is not None:
        if args.value is None:
            raise SystemExit("--value required with --key")
        try:
            val = json.loads(args.value)
        except json.JSONDecodeError:
            val = args.value
        attrs[args.key] = val
    out = request(
        "PATCH",
        f"/core/users/{user['pk']}/",
        token,
        domain,
        {"attributes": attrs},
    )
    dump({"pk": out.get("pk"), "username": out.get("username"), "attributes": out.get("attributes")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
