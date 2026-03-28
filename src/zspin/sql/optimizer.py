from __future__ import annotations


class CostBasedOptimizer:
    def estimate_cost(self, plan: dict[str, str]) -> int:
        if plan["op"] == "scan":
            return 10
        if plan["op"] == "index_lookup":
            return 1
        return 100

    def choose(self, plans: list[dict[str, str]]) -> dict[str, str]:
        return min(plans, key=self.estimate_cost)
