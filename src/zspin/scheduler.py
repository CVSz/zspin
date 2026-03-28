from __future__ import annotations

from .crd import Resource


class Scheduler:
    def __init__(self) -> None:
        self.nodes = ["node-a", "node-b"]

    def schedule(self, resource: Resource) -> str:
        return self.nodes[hash(resource.name) % len(self.nodes)]
