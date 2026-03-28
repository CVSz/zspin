from __future__ import annotations


class SLOEngine:
    def __init__(self) -> None:
        self.targets = {
            "availability": 0.99,
            "latency_ms": 200,
        }

    def evaluate(self, metrics: dict) -> list[str]:
        violations: list[str] = []

        if metrics.get("availability", 1) < self.targets["availability"]:
            violations.append("availability")

        if metrics.get("latency_ms", 0) > self.targets["latency_ms"]:
            violations.append("latency")

        return violations
