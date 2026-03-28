from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Snapshot:
    def __init__(self, path: str = "snapshot.json") -> None:
        self.path = Path(path)

    def save(self, data: dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, separators=(",", ":"))

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}

        with self.path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
