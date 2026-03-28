from __future__ import annotations

import math


class VectorIndex:
    def __init__(self) -> None:
        self.vectors: dict[str, list[float]] = {}

    def add(self, key: str, vec: list[float]) -> None:
        self.vectors[key] = vec

    def search(self, query: list[float], top_k: int = 3) -> list[tuple[str, list[float]]]:
        def dist(a: list[float], b: list[float]) -> float:
            return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

        ranked = sorted(self.vectors.items(), key=lambda item: dist(query, item[1]))
        return ranked[:top_k]
