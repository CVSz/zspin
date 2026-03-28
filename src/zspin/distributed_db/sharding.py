from __future__ import annotations


class ShardManager:
    def __init__(self) -> None:
        self.shards: dict[str, dict[str, object]] = {
            "shard-1": {"range": ("a", "m"), "node": "node1"},
            "shard-2": {"range": ("n", "z"), "node": "node2"},
        }

    def get_shard(self, key: str) -> tuple[str | None, str | None]:
        for shard, meta in self.shards.items():
            start, end = meta["range"]
            if start <= key <= end:
                return shard, str(meta["node"])
        return None, None

    def rebalance(self) -> dict[str, str]:
        return {"status": "rebalanced"}
