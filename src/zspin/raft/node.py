from __future__ import annotations

import random
import time


class RaftNode:
    def __init__(self, node_id: str, peers: list[str]) -> None:
        self.node_id = node_id
        self.peers = peers
        self.term = 0
        self.voted_for: str | None = None
        self.log: list[object] = []
        self.state = "follower"
        self.last_heartbeat = time.time()

    def become_leader(self) -> None:
        self.state = "leader"
        print(f"[{self.node_id}] became leader (term {self.term})")

    def become_follower(self, term: int) -> None:
        self.state = "follower"
        self.term = term
        self.voted_for = None

    def request_vote(self) -> None:
        self.term += 1
        votes = 1

        for _peer in self.peers:
            if random.random() > 0.5:
                votes += 1

        if votes > len(self.peers) // 2:
            self.become_leader()

    def append_entry(self, entry: object) -> None:
        self.log.append(entry)

    def run(self) -> None:
        while True:
            if self.state == "leader":
                self.send_heartbeat()
                time.sleep(1)
            else:
                if time.time() - self.last_heartbeat > random.uniform(2, 5):
                    self.request_vote()
                time.sleep(1)

    def send_heartbeat(self) -> None:
        print(f"[{self.node_id}] heartbeat (term {self.term})")
