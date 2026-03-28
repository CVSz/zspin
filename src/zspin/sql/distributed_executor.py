from __future__ import annotations

from zspin.distributed_db.sharding import ShardManager
from zspin.sql.executor import SQLExecutor


class DistributedExecutor:
    def __init__(self, shard_manager: ShardManager, local_executor: SQLExecutor) -> None:
        self.shards = shard_manager
        self.local = local_executor

    def execute(self, plan: dict[str, str]) -> dict[str, object]:
        key = plan.get("key", "")
        shard, node = self.shards.get_shard(key)

        if node == "node1":
            if plan["op"] == "index_lookup":
                plan = {"op": "scan", "key": key}
            return self.local.execute(plan)

        return {"remote_node": node, "shard": shard, "result": "ok"}
