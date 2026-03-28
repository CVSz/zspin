from __future__ import annotations


class SecondaryIndex:
    def __init__(self) -> None:
        self.index: dict[object, set[str]] = {}

    def add(self, key: str, value: object) -> None:
        self.index.setdefault(value, set()).add(key)

    def search(self, value: object) -> list[str]:
        return list(self.index.get(value, []))
