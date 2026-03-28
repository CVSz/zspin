from __future__ import annotations

import time

from .mvcc import MVCCStore


class Transaction:
    def __init__(self, store: MVCCStore) -> None:
        self.store = store
        self.start_ts = time.time()
        self.writes: list[tuple[str, object]] = []

    def read(self, key: str) -> object | None:
        return self.store.read(key, self.start_ts)

    def write(self, key: str, value: object) -> None:
        self.writes.append((key, value))

    def commit(self) -> bool:
        commit_ts = time.time()
        for key, value in self.writes:
            self.store.write(key, value, commit_ts)
        return True

    def rollback(self) -> None:
        self.writes = []
