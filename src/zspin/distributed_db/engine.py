from __future__ import annotations

from zspin.distributed_db.columnar import ColumnStore
from zspin.distributed_db.geo import RegionManager
from zspin.distributed_db.index import SecondaryIndex
from zspin.distributed_db.mvcc import MVCCStore
from zspin.distributed_db.sharding import ShardManager
from zspin.distributed_db.snapshot import Snapshot
from zspin.distributed_db.truetime import TrueTime
from zspin.distributed_db.tx2pc import TwoPhaseCommit
from zspin.distributed_db.vector import VectorIndex
from zspin.distributed_db.wal import WAL
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
        self.wal = WAL(path=f"{self.raft.node_id}.wal")
        self.snapshot = Snapshot(path=f"{self.raft.node_id}_snapshot.json")
        self.index = SecondaryIndex()
        self.executor = SQLExecutor(self.store, raft_node, self.index)
        self.shards = ShardManager()
        self.optimizer = CostBasedOptimizer()
        self.dist_exec = DistributedExecutor(self.shards, self.executor)
        self.tt = TrueTime()
        self.geo = RegionManager()
        self.txn_mgr = TwoPhaseCommit(raft_node, self.tt)
        self.columnar = ColumnStore()
        self.vector = VectorIndex()
        if hasattr(self.raft, "sm") and hasattr(self.raft.sm, "register_handler"):
            self.raft.sm.register_handler("mvcc_write", self._apply_mvcc_write)
        self._load_snapshot()
        self._replay_wal()

    def query(self, sql: str) -> dict[str, object]:
        try:
            plan = self.parser.parse(sql)
            logical = self.planner.plan(plan)

            plans = [logical]
            if logical["op"] == "scan":
                plans.append({"op": "index_lookup", "key": logical["key"]})

            best = self.optimizer.choose(plans)
            return self.dist_exec.execute(best)
        except Exception as exc:
            return {"error": str(exc)}

    def _apply_mvcc_write(self, command: dict[str, object]) -> None:
        key = str(command["key"])
        value = command["value"]
        ts = float(command["ts"])
        self.wal.append({"op": "mvcc_write", "key": key, "value": value, "ts": ts})
        self.store.write(key, value, ts)
        self.index.add(key, value)

    def apply(self, command: dict[str, object]) -> dict[str, object]:
        if command.get("op") == "mvcc_write":
            if self.raft.state == "leader" and not bool(command.get("_replicated", False)):
                accepted = self.raft.propose(command)
                return {"status": "proposed" if accepted else "rejected"}
            self._apply_mvcc_write(command)
            return {"status": "applied"}

        return {"status": "ignored"}

    def snapshot_now(self) -> None:
        self.snapshot.save(self.store.data)

    def _load_snapshot(self) -> None:
        snapshot_data = self.snapshot.load()
        for key, versions in snapshot_data.items():
            if not isinstance(versions, list):
                continue
            for item in versions:
                if not isinstance(item, list | tuple) or len(item) != 2:
                    continue
                ts, value = item
                self.store.write(str(key), value, float(ts))
                self.index.add(str(key), value)

    def _replay_wal(self) -> None:
        for record in self.wal.replay():
            if record.get("op") != "mvcc_write":
                continue
            key = str(record["key"])
            value = record["value"]
            ts = float(record["ts"])
            self.store.write(key, value, ts)
            self.index.add(key, value)
