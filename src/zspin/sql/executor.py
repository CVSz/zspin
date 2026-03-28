from __future__ import annotations

from zspin.raft.node import RaftNode
from zspin.raft.state_machine import StateMachine


class SQLExecutor:
    def __init__(self, state_machine: StateMachine, raft_node: RaftNode) -> None:
        self.sm = state_machine
        self.raft = raft_node

    def execute(self, plan: dict[str, str]) -> dict[str, object]:
        if plan["type"] == "insert":
            ok = self.raft.propose({"op": "set", "key": plan["key"], "value": plan["value"]})
            return {"status": "ok" if ok else "not_leader"}

        if plan["type"] == "delete":
            ok = self.raft.propose({"op": "delete", "key": plan["key"]})
            return {"status": "ok" if ok else "not_leader"}

        if plan["type"] == "select":
            return {"value": self.sm.kv.get(plan["key"])}

        return {"error": "unknown"}
