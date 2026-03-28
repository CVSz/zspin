from __future__ import annotations

import threading
import time

from zspin.kv.store import KVStore


class LeaseManager:
    def __init__(self, store: KVStore, interval_seconds: float = 1.0) -> None:
        self.store = store
        self.interval_seconds = interval_seconds
        self._leases: dict[str, float] = {}
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def grant(self, key: str, ttl_seconds: float) -> float:
        expire_at = time.time() + ttl_seconds
        with self._lock:
            self._leases[key] = expire_at
        return expire_at

    def revoke(self, key: str) -> None:
        with self._lock:
            self._leases.pop(key, None)

    def _loop(self) -> None:
        while True:
            now = time.time()
            with self._lock:
                expired = [key for key, expires_at in self._leases.items() if expires_at <= now]

            for key in expired:
                self.store.delete(key)
                self.revoke(key)

            time.sleep(self.interval_seconds)
