from __future__ import annotations

import queue
import threading
import time
from collections import defaultdict
from collections.abc import MutableMapping
from typing import Any

from zspin.distributed_db.mvcc import MVCCStore
from zspin.kv.revision import Revision


class KVStore:
    def __init__(self, raft: Any, mvcc: MVCCStore, revision: Revision) -> None:
        self.raft = raft
        self.mvcc = mvcc
        self.rev = revision
        self.watchers: MutableMapping[str, list[queue.Queue[dict[str, Any]]]] = defaultdict(list)
        self._watch_lock = threading.Lock()

    def put(self, key: str, value: object) -> dict[str, object]:
        revision = self.rev.next()
        command = {
            "op": "mvcc_write",
            "key": key,
            "value": value,
            "ts": time.time(),
            "rev": revision,
        }

        ok = bool(self.raft.propose(command))
        if ok:
            self._notify_watchers(key, value, revision)
        return {"ok": ok, "revision": revision}

    def get(self, key: str) -> object | None:
        return self.mvcc.read(key, time.time())

    def delete(self, key: str) -> dict[str, object]:
        return self.put(key, None)

    def prefix(self, prefix: str) -> dict[str, object | None]:
        results: dict[str, object | None] = {}
        for key in self.mvcc.data:
            if key.startswith(prefix):
                results[key] = self.get(key)
        return results

    def cas(self, key: str, expected: object, new: object) -> dict[str, object]:
        current = self.get(key)
        if current != expected:
            return {"ok": False, "error": "conflict", "current": current}
        return self.put(key, new)

    def watch(self, key: str, event_queue: queue.Queue[dict[str, Any]]) -> None:
        with self._watch_lock:
            self.watchers[key].append(event_queue)

    def _notify_watchers(self, key: str, value: object, revision: int) -> None:
        event = {"key": key, "value": value, "revision": revision}
        with self._watch_lock:
            for watcher in list(self.watchers.get(key, [])):
                watcher.put(event)
