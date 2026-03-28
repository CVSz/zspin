from __future__ import annotations


class Service:
    def __init__(self, name: str, service_type: str) -> None:
        self.name = name
        self.type = service_type

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "type": self.type}
