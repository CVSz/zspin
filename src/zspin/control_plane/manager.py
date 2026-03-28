from __future__ import annotations

from zspin.aiops import AIOpsEngine
from zspin.events import publish_event
from zspin.platform.runtime import Runtime
from zspin.platform.services import Service


class ControlPlane:
    def __init__(self) -> None:
        self.runtime = Runtime()
        self.tenants: dict[str, dict[str, list[dict[str, str]]]] = {}
        self.clusters: dict[str, dict[str, str]] = {
            "cluster-a": {},
            "cluster-b": {},
        }
        self.ai = AIOpsEngine()

    def register_tenant(self, tenant: str) -> None:
        self.tenants.setdefault(tenant, {"services": []})

    def list_tenants(self) -> list[str]:
        return sorted(self.tenants.keys())

    def list_clusters(self) -> list[str]:
        return sorted(self.clusters.keys())

    def deploy(self, service: dict[str, str], tenant: str, cluster: str) -> dict[str, str]:
        if cluster not in self.clusters:
            raise ValueError(f"unknown cluster: {cluster}")

        self.register_tenant(tenant)
        svc_name = service.get("name", "").strip()
        if not svc_name:
            raise ValueError("service name is required")

        result = self.runtime.deploy(Service(svc_name, service.get("type", "api")))

        publish_event(
            "deployments",
            {"tenant": tenant, "service": svc_name, "cluster": cluster},
        )

        decision = self.ai.analyze({"latency": 100, "errors": 0.01})
        self.ai.feedback(decision)

        self.tenants[tenant]["services"].append({"name": svc_name, "cluster": cluster})

        return {
            "status": "deployed",
            "tenant": tenant,
            "cluster": cluster,
            "service": svc_name,
            "runtime": result,
        }
