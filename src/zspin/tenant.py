from __future__ import annotations


class TenantManager:
    def __init__(self) -> None:
        self.data: dict[str, dict[str, dict[str, float] | list[dict[str, str]]]] = {}

    def ensure(self, tenant: str) -> None:
        if tenant not in self.data:
            self.data[tenant] = {
                "services": [],
                "usage": {"deploys": 0.0, "cpu": 0.0},
            }

    def add_usage(self, tenant: str, key: str, value: float) -> None:
        self.ensure(tenant)
        usage = self.data[tenant]["usage"]
        assert isinstance(usage, dict)
        usage[key] = float(usage.get(key, 0.0)) + value

    def get_usage(self, tenant: str) -> dict[str, float]:
        self.ensure(tenant)
        usage = self.data[tenant]["usage"]
        assert isinstance(usage, dict)
        return usage.copy()
