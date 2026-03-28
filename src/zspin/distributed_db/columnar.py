from __future__ import annotations


class ColumnStore:
    def __init__(self) -> None:
        self.columns: dict[str, list[object]] = {}

    def insert(self, row: dict[str, object]) -> None:
        for col, val in row.items():
            self.columns.setdefault(col, []).append(val)

    def scan(self, col: str) -> list[object]:
        return self.columns.get(col, [])
