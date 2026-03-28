from __future__ import annotations

import json
from pathlib import Path


class WAL:
    def __init__(self, path: str = "raft.log") -> None:
        self.path = Path(path)

    def append(self, entry: dict[str, object]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def read_all(self) -> list[dict[str, object]]:
        try:
            with self.path.open(encoding="utf-8") as f:
                return [json.loads(line) for line in f]
        except FileNotFoundError:
            return []
