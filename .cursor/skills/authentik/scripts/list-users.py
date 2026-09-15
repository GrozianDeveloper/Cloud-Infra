#!/usr/bin/env python3
"""List users (paginated)."""
from __future__ import annotations

import argparse
import sys

from ak_lib import add_common_args, creds_from_args, dump, paginate


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    add_common_args(p)
    p.add_argument("--search")
    p.add_argument("--username")
    args = p.parse_args()
    token, domain = creds_from_args(args)
    params = {}
    if args.search:
        params["search"] = args.search
    if args.username:
        params["username"] = args.username
    users = paginate("/core/users/", token, domain, params)
    dump(
        [
            {
                "pk": u.get("pk"),
                "username": u.get("username"),
                "name": u.get("name"),
                "email": u.get("email"),
                "is_active": u.get("is_active"),
                "is_superuser": u.get("is_superuser"),
                "path": u.get("path"),
                "groups": [g.get("name") for g in (u.get("groups_obj") or [])],
                "attributes": u.get("attributes") or {},
            }
            for u in users
        ]
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
