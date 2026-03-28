"""In-memory usage metering for demo purposes."""

from __future__ import annotations

from collections import defaultdict

usage_db: dict[str, dict[str, int]] = defaultdict(dict)


def meter(user_id: str, action: str) -> None:
    usage_db[user_id][action] = usage_db[user_id].get(action, 0) + 1
