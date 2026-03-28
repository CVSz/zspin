from __future__ import annotations

from zspin.intelligence import IntelligentRemediation
from zspin.policy import PolicyEngine
from zspin.remediation import RemediationEngine
from zspin.slo import SLOEngine


class AlertHandler:
    def __init__(self) -> None:
        self.engine = RemediationEngine()
        self.policy = PolicyEngine()
        self.slo = SLOEngine()
        self.ai = IntelligentRemediation()

    def handle(self, alert: dict) -> dict[str, object]:
        mapped = self.map_alert(alert)

        metrics = {
            "availability": 0.97,
            "latency_ms": 300,
        }
        slo_violations = self.slo.evaluate(metrics)
        decision = self.ai.decide(mapped, slo_violations)

        action = {
            "action": decision["type"],
            "service": mapped.get("service"),
            "error_rate": 0.2,
        }

        if not self.policy.evaluate(action):
            return {"status": "blocked_by_policy", "action": action}

        mapped["type"] = decision["type"]
        return self.engine.run(mapped)

    def map_alert(self, alert: dict) -> dict[str, str]:
        name = alert.get("alert")

        if name == "HighCPU":
            return {"type": "high_cpu", "service": "api"}

        if name == "ServiceDown":
            return {"type": "unhealthy", "service": "api"}

        return {"type": "unknown", "service": "api"}
