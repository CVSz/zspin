from __future__ import annotations


class ScoringScheduler:
    def __init__(self) -> None:
        self.nodes = {
            "node-a": {"cpu": 0.5, "latency": 50},
            "node-b": {"cpu": 0.2, "latency": 100},
        }

    def score(self, node: dict[str, float]) -> float:
        return node["cpu"] * 0.7 + node["latency"] * 0.3

    def select(self) -> str:
        return min(self.nodes, key=lambda n: self.score(self.nodes[n]))
