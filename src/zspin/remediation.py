from __future__ import annotations

from typing import Callable

from .platform.runtime import Runtime
from .platform.services import Service


class RemediationEngine:
    """Self-healing action router for known issue types."""

    def __init__(self) -> None:
        self.runtime = Runtime()
        self.actions: dict[str, Callable[[dict], dict[str, object]]] = {
            "high_cpu": self.scale_service,
            "crash_loop": self.restart_service,
            "unhealthy": self.restart_service,
            "scale": self.scale_service,
            "restart": self.restart_service,
        }

    def run(self, issue: dict) -> dict[str, object]:
        issue_type = issue.get("type")

        if issue_type in self.actions:
            return self.actions[issue_type](issue)

        return {"status": "ignored", "reason": "no action"}

    def scale_service(self, issue: dict) -> dict[str, object]:
        service_name = issue.get("service", "api")
        replicas = int(issue.get("replicas", 2))
        service = Service(service_name, "api")
        output = self.runtime.scale(service, replicas)
        return {
            "action": "scale",
            "service": service_name,
            "replicas": replicas,
            "status": "executed",
            "runtime_output": output,
        }

    def restart_service(self, issue: dict) -> dict[str, object]:
        service_name = issue.get("service", "api")
        service = Service(service_name, "api")
        output = self.runtime.restart(service)
        return {
            "action": "restart",
            "service": service_name,
            "status": "executed",
            "runtime_output": output,
        }
