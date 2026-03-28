from __future__ import annotations

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

        self.tenants[tenant]["services"].append({"name": svc_name, "cluster": cluster})

        return {
            "status": "deployed",
            "tenant": tenant,
            "cluster": cluster,
            "service": svc_name,
            "runtime": result,
        }
