from __future__ import annotations


class BillingEngine:
    PRICING = {
        "deploy": 0.01,
        "cpu": 0.001,
    }

    def calculate(self, usage: dict[str, float]) -> float:
        total = 0.0
        total += usage.get("deploys", 0.0) * self.PRICING["deploy"]
        total += usage.get("cpu", 0.0) * self.PRICING["cpu"]
        return round(total, 4)
