from __future__ import annotations

import time

from zspin.distributed_db.index import SecondaryIndex
from zspin.distributed_db.mvcc import MVCCStore
from zspin.raft.node import RaftNode


class SQLExecutor:
    def __init__(self, mvcc_store: MVCCStore, raft_node: RaftNode, index: SecondaryIndex) -> None:
        self.store = mvcc_store
        self.raft = raft_node
        self.index = index

    def execute(self, plan: dict[str, str]) -> dict[str, object]:
        if plan["op"] == "insert":
            ts = time.time()
            self.store.write(plan["key"], plan["value"], ts)
            self.index.add(plan["key"], plan["value"])
            ok = True
            if hasattr(self.raft, "propose"):
                ok = self.raft.propose({"op": "set", "key": plan["key"], "value": plan["value"]})
            return {"status": "ok" if ok else "not_leader"}

        if plan["op"] == "delete":
            ok = True
            if hasattr(self.raft, "propose"):
                ok = self.raft.propose({"op": "delete", "key": plan["key"]})
            return {"status": "ok" if ok else "not_leader"}

        if plan["op"] == "scan":
            value = self.store.read(plan["key"], time.time())
            return {"value": value}

        return {"error": "unknown"}
