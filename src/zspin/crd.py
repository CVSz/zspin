from __future__ import annotations


class Resource:
    def __init__(self, name: str, spec: dict[str, object]) -> None:
        self.name = name
        self.spec = spec
        self.status: dict[str, object] = {}


class ResourceStore:
    def __init__(self) -> None:
        self.resources: dict[str, Resource] = {}

    def apply(self, resource: Resource) -> None:
        self.resources[resource.name] = resource

    def list(self) -> list[Resource]:
        return list(self.resources.values())

    def get(self, name: str) -> Resource | None:
        return self.resources.get(name)
