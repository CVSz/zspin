from __future__ import annotations


class IntelligentRemediation:
    def decide(self, issue: dict[str, object], slo_violations: list[str]) -> dict[str, str]:
        if "availability" in slo_violations:
            return {"type": "restart", "priority": "high"}

        if "latency" in slo_violations:
            return {"type": "scale", "priority": "medium"}

        return {"type": str(issue.get("type", "unknown")), "priority": "low"}
