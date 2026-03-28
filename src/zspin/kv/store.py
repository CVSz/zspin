from __future__ import annotations

import time


class KVStore:
    def __init__(self, raft, mvcc) -> None:
        self.raft = raft
        self.mvcc = mvcc

    def put(self, key: str, value: object) -> bool:
        cmd = {
            "op": "mvcc_write",
            "key": key,
            "value": value,
            "ts": time.time(),
        }
        return bool(self.raft.propose(cmd))

    def get(self, key: str) -> object | None:
        return self.mvcc.read(key, time.time())

    def delete(self, key: str) -> bool:
        return self.put(key, None)
