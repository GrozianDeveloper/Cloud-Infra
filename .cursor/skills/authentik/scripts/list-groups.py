#!/usr/bin/env python3
"""List groups."""
from __future__ import annotations

import argparse
import sys

from ak_lib import add_common_args, creds_from_args, dump, paginate


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    add_common_args(p)
    p.add_argument("--search")
    args = p.parse_args()
    token, domain = creds_from_args(args)
    params = {"search": args.search} if args.search else {}
    groups = paginate("/core/groups/", token, domain, params)
    dump(
        [
            {
                "pk": g.get("pk"),
                "name": g.get("name"),
                "is_superuser": g.get("is_superuser"),
                "parents": g.get("parents") or [],
                "users": g.get("users"),
            }
            for g in groups
        ]
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
