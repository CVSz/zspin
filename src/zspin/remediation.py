from __future__ import annotations

from typing import Callable


class RemediationEngine:
    """Simple self-healing action router for known issue types."""

    def __init__(self) -> None:
        self.actions: dict[str, Callable[[dict], dict[str, object]]] = {
            "high_cpu": self.scale_service,
            "crash_loop": self.restart_service,
            "unhealthy": self.restart_service,
        }

    def run(self, issue: dict) -> dict[str, object]:
        issue_type = issue.get("type")

        if issue_type in self.actions:
            return self.actions[issue_type](issue)

        return {"status": "ignored", "reason": "no action"}

    def scale_service(self, issue: dict) -> dict[str, object]:
        service = issue.get("service")
        return {
            "action": "scale",
            "service": service,
            "replicas": 2,
            "status": "simulated",
        }

    def restart_service(self, issue: dict) -> dict[str, object]:
        service = issue.get("service")
        return {
            "action": "restart",
            "service": service,
            "status": "simulated",
        }
