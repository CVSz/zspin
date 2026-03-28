from __future__ import annotations

import time


class KVStore:
    def __init__(self) -> None:
        self.store: dict[str, object] = {}
        self.log: list[dict[str, object]] = []

    def put(self, key: str, value: object) -> None:
        entry = {"key": key, "value": value, "ts": time.time()}
        self.log.append(entry)
        self.store[key] = value

    def get(self, key: str) -> object | None:
        return self.store.get(key)

    def history(self) -> list[dict[str, object]]:
        return self.log
