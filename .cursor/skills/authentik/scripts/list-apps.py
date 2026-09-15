#!/usr/bin/env python3
"""List applications."""
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
    apps = paginate("/core/applications/", token, domain, params)
    dump(
        [
            {
                "pk": a.get("pk"),
                "name": a.get("name"),
                "slug": a.get("slug"),
                "provider": a.get("provider"),
                "provider_type": (a.get("provider_obj") or {}).get("verbose_name"),
                "meta_launch_url": a.get("meta_launch_url"),
            }
            for a in apps
        ]
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
