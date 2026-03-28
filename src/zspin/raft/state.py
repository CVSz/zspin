from __future__ import annotations

import json
from pathlib import Path


class PersistentState:
    """Stores Raft term/vote metadata on disk."""

    def __init__(self, path: str | Path = "raft_state.json") -> None:
        self.path = Path(path)
        self.term = 0
        self.voted_for: str | None = None
        self.load()

    def save(self) -> None:
        payload = {"term": self.term, "voted_for": self.voted_for}
        self.path.write_text(json.dumps(payload), encoding="utf-8")

    def load(self) -> None:
        if not self.path.exists():
            return

        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.term = int(data.get("term", 0))
        self.voted_for = data.get("voted_for")

    def set_term(self, term: int) -> None:
        self.term = term
        self.voted_for = None
        self.save()

    def vote_for(self, candidate_id: str | None) -> None:
        self.voted_for = candidate_id
        self.save()
