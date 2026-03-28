from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any, Iterator


class WAL:
    def __init__(self, path: str = "zspin.wal") -> None:
        self.path = Path(path)
        self._lock = threading.Lock()

    def append(self, record: dict[str, Any]) -> None:
        line = json.dumps(record, separators=(",", ":"))
        with self._lock:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(f"{line}\n")

    def replay(self) -> Iterator[dict[str, Any]]:
        if not self.path.exists():
            return

        with self._lock:
            with self.path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    if not line.strip():
                        continue
                    yield json.loads(line)
