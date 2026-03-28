"""Analytics helpers."""

from __future__ import annotations

from usage import usage_db


def get_stats(user_id: str) -> dict[str, int]:
    return usage_db.get(user_id, {})
