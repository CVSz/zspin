from __future__ import annotations

from zspin.distributed_db.truetime import TrueTime
from zspin.raft.node import RaftNode


class TwoPhaseCommit:
    def __init__(self, raft_node: RaftNode, truetime: TrueTime) -> None:
        self.raft = raft_node
        self.tt = truetime

    def prepare(self, txn: object) -> bool:
        _ = txn
        return True

    def commit(self, txn: object) -> dict[str, object]:
        writes = getattr(txn, "writes", [])
        ts = self.tt.now()

        for key, value in writes:
            self.raft.propose(
                {
                    "op": "set",
                    "key": key,
                    "value": value,
                    "ts": ts[1],
                }
            )

        self.tt.after(ts)
        return {"status": "committed", "ts": ts}
