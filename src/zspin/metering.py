from __future__ import annotations

from zspin.tenant import TenantManager

tenant_manager = TenantManager()


def record_deploy(tenant: str) -> None:
    tenant_manager.add_usage(tenant, "deploys", 1)


def record_cpu(tenant: str, amount: float) -> None:
    tenant_manager.add_usage(tenant, "cpu", amount)


def get_usage(tenant: str) -> dict[str, float]:
    return tenant_manager.get_usage(tenant)
