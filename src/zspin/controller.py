from __future__ import annotations

from collections.abc import Callable


class Controller:
    def __init__(self, store, reconcile_fn: Callable[[str, object], None]) -> None:
        self.store = store
        self.reconcile_fn = reconcile_fn

    def run(self) -> None:
        for key, value in self.store.store.items():
            self.reconcile_fn(key, value)
