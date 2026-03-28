from __future__ import annotations

import json
from pathlib import Path

from zspin.raft.state_machine import StateMachine


class Snapshot:
    def __init__(self, path: str | Path = "snapshot.json") -> None:
        self.path = Path(path)

    def save(self, state_machine: StateMachine, last_included_index: int, last_included_term: int) -> None:
        payload = {
            "kv": state_machine.kv,
            "last_included_index": last_included_index,
            "last_included_term": last_included_term,
        }
        self.path.write_text(json.dumps(payload), encoding="utf-8")

    def load(self) -> dict[str, object]:
        if not self.path.exists():
            return {"kv": {}, "last_included_index": -1, "last_included_term": 0}
        return json.loads(self.path.read_text(encoding="utf-8"))
