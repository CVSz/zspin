from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class LogEntry:
    term: int
    command: dict[str, Any]


class RaftLog:
    def __init__(self) -> None:
        self.entries: list[LogEntry] = []
        self.commit_index = -1
        self.last_applied = -1

    def append(self, entry: LogEntry) -> None:
        self.entries.append(entry)

    def match(self, index: int, term: int) -> bool:
        if index < 0:
            return True
        if index >= len(self.entries):
            return False
        return self.entries[index].term == term

    def delete_conflicts(self, index: int) -> None:
        self.entries = self.entries[: index + 1]
        if self.commit_index > index:
            self.commit_index = index
        if self.last_applied > index:
            self.last_applied = index

    def commit_to(self, index: int) -> None:
        self.commit_index = min(index, len(self.entries) - 1)

    def apply(self, state_machine: "StateMachine") -> None:
        while self.last_applied < self.commit_index:
            self.last_applied += 1
            state_machine.apply(self.entries[self.last_applied].command)


from zspin.raft.state_machine import StateMachine
