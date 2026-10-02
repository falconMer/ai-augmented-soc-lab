from __future__ import annotations

import json
from collections import deque
from pathlib import Path
from typing import Iterable

from .models import NormalizedAlert
from .normalizer import normalize_wazuh_alert


def read_recent_alerts(
    path: str | Path,
    *,
    limit: int = 5,
    rule_ids: Iterable[str] | None = None,
) -> tuple[list[NormalizedAlert], dict[str, int]]:
    """Read the newest matching alerts from Wazuh's JSON-lines alert file.

    The file is scanned line-by-line instead of loaded into memory. Only the
    newest requested number of matching normalized alerts are retained.
    """

    if limit < 1:
        raise ValueError("limit must be at least 1")

    wanted = {str(rule_id) for rule_id in rule_ids or []}
    recent: deque[NormalizedAlert] = deque(maxlen=limit)

    lines_seen = 0
    matching_lines = 0
    malformed_lines = 0

    with Path(path).open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            lines_seen += 1
            if not line.strip():
                continue

            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                malformed_lines += 1
                continue

            rule = raw.get("rule") if isinstance(raw, dict) else None
            rule_id = (
                str(rule.get("id"))
                if isinstance(rule, dict) and rule.get("id") is not None
                else None
            )

            if wanted and rule_id not in wanted:
                continue

            matching_lines += 1
            recent.append(normalize_wazuh_alert(raw))

    stats = {
        "lines_seen": lines_seen,
        "matching_lines": matching_lines,
        "malformed_lines": malformed_lines,
        "returned": len(recent),
    }
    return list(recent), stats
