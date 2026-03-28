from __future__ import annotations


class RegionManager:
    def __init__(self) -> None:
        self.regions: dict[str, list[str]] = {
            "us-east": ["node1"],
            "eu-west": ["node2"],
            "ap-south": ["node3"],
        }

    def get_replicas(self, key: str) -> list[str]:
        _ = key
        return [node for nodes in self.regions.values() for node in nodes]
