from __future__ import annotations


class MVCCStore:
    def __init__(self) -> None:
        self.data: dict[str, list[tuple[float, object]]] = {}

    def write(self, key: str, value: object, ts: float) -> None:
        versions = self.data.setdefault(key, [])
        versions.append((ts, value))

    def read(self, key: str, ts: float) -> object | None:
        versions = self.data.get(key, [])
        visible = [version for version in versions if version[0] <= ts]
        if not visible:
            return None
        return sorted(visible, key=lambda version: version[0])[-1][1]
