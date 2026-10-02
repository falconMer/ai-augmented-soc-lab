#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from soc_backend.reader import read_recent_alerts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read and normalize recent Wazuh JSON alerts."
    )
    parser.add_argument(
        "--file",
        default="/var/ossec/logs/alerts/alerts.json",
        help="Path to Wazuh alerts.json",
    )
    parser.add_argument(
        "--last",
        type=int,
        default=5,
        help="Number of newest matching alerts to display",
    )
    parser.add_argument(
        "--rule",
        action="append",
        default=[],
        help="Rule ID to include; repeat this option for multiple rule IDs",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        alerts, stats = read_recent_alerts(
            args.file,
            limit=args.last,
            rule_ids=args.rule,
        )
    except PermissionError:
        print(
            f"Permission denied reading {args.file}. "
            "Grant the current user read access rather than running the backend as root.",
            file=sys.stderr,
        )
        return 2
    except FileNotFoundError:
        print(f"Alert file not found: {args.file}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(json.dumps({"stats": stats}, indent=2))
    for alert in alerts:
        print(json.dumps(alert.to_dict(), indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
