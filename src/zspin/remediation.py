from __future__ import annotations

from dataclasses import dataclass

from .platform.runtime import Runtime


@dataclass(frozen=True)
class Service:
    name: str


class RemediationEngine:
    """Maps issue types to actionable runtime remediation."""

    def __init__(self) -> None:
        self.runtime = Runtime()

    def run(self, issue: dict[str, object]) -> dict[str, object]:
        issue_type = str(issue.get("type", "unknown"))
        service_name = str(issue.get("service", "api"))
        service = Service(name=service_name)

        if issue_type == "high_cpu":
            output = self.runtime.scale(service, replicas=2)
            return {"action": "scale", "service": service_name, "output": output.strip()}

        if issue_type == "unhealthy":
            output = self.runtime.deploy(service)
            return {"action": "redeploy", "service": service_name, "output": output.strip()}

        return {"action": "noop", "service": service_name, "reason": f"unsupported issue '{issue_type}'"}
