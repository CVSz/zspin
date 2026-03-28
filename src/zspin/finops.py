from __future__ import annotations


class FinOpsEngine:
    """Cost optimization helpers for platform resources."""

    def analyze(self, resources: list[dict]) -> list[dict[str, str]]:
        report: list[dict[str, str]] = []
        for resource in resources:
            if resource.get("cpu", 0) < 5 and resource.get("uptime", 0) > 3600:
                report.append(
                    {
                        "service": str(resource.get("name")),
                        "issue": "idle",
                        "recommendation": "scale_to_zero",
                    }
                )
        return report

    def estimate_cost(self, resources: list[dict]) -> float:
        return float(sum(resource.get("cost_per_hour", 0) for resource in resources))
