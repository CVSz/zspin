from __future__ import annotations

from zspin.distributed_db.index import SecondaryIndex
from zspin.distributed_db.mvcc import MVCCStore
from zspin.distributed_db.sharding import ShardManager
from zspin.raft.node import RaftNode
from zspin.sql.distributed_executor import DistributedExecutor
from zspin.sql.executor import SQLExecutor
from zspin.sql.optimizer import CostBasedOptimizer
from zspin.sql.parser import SQLParser
from zspin.sql.planner import QueryPlanner


class Database:
    def __init__(self, raft_node: RaftNode) -> None:
        self.raft = raft_node
        self.parser = SQLParser()
        self.planner = QueryPlanner()
        self.store = MVCCStore()
        self.index = SecondaryIndex()
        self.executor = SQLExecutor(self.store, raft_node, self.index)
        self.shards = ShardManager()
        self.optimizer = CostBasedOptimizer()
        self.dist_exec = DistributedExecutor(self.shards, self.executor)

    def query(self, sql: str) -> dict[str, object]:
        plan = self.parser.parse(sql)
        logical = self.planner.plan(plan)

        plans = [logical]
        if logical["op"] == "scan":
            plans.append({"op": "index_lookup", "key": logical["key"]})

        best = self.optimizer.choose(plans)
        return self.dist_exec.execute(best)
