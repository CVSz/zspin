from __future__ import annotations

from typing import Any

import requests


def send(node_url: str, cmd: dict[str, Any]) -> dict[str, Any]:
    try:
        return requests.post(node_url, json=cmd, timeout=2).json()
    except Exception:
        return {"error": "node unreachable"}
