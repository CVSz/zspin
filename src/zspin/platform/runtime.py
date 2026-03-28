from __future__ import annotations

from .services import Service


class Runtime:
    def deploy(self, service: Service) -> str:
        return f"Deploying {service.name}"

    def scale(self, service: Service, replicas: int) -> str:
        return f"Scaling {service.name} to {replicas}"
