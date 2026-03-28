from __future__ import annotations


class MultiClusterScheduler:
    def select_cluster(self, service: dict[str, str], clusters: dict[str, dict[str, str]]) -> str:
        _ = service
        if not clusters:
            raise ValueError("no clusters available")
        return sorted(clusters.keys())[0]
