from __future__ import annotations

from .services import Service


def deploy(service: Service) -> dict[str, object]:
    return {
        "status": "deployed",
        "service": service.to_dict(),
    }
