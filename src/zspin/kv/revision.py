from __future__ import annotations

import threading


class Revision:
    """Monotonic revision counter for linearized writes."""

    def __init__(self) -> None:
        self._current = 0
        self._lock = threading.Lock()

    def next(self) -> int:
        with self._lock:
            self._current += 1
            return self._current

    @property
    def current(self) -> int:
        with self._lock:
            return self._current
