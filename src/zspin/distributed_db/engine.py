from __future__ import annotations

from zspin.raft.node import RaftNode
from zspin.sql.executor import SQLExecutor
from zspin.sql.parser import SQLParser


class Database:
    def __init__(self, raft_node: RaftNode) -> None:
        self.raft = raft_node
        self.parser = SQLParser()
        self.executor = SQLExecutor(raft_node.sm, raft_node)

    def query(self, sql: str) -> dict[str, object]:
        plan = self.parser.parse(sql)
        return self.executor.execute(plan)
