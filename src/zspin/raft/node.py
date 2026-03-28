from __future__ import annotations

from typing import Any

from zspin.raft.cluster import PeerClient
from zspin.raft.log import LogEntry, RaftLog
from zspin.raft.snapshot import Snapshot
from zspin.raft.state import PersistentState
from zspin.raft.state_machine import StateMachine


class RaftNode:
    def __init__(self, node_id: str, peers: list[str], state_path: str | None = None) -> None:
        self.node_id = node_id
        self.peer_addresses = peers
        self.clients: list[PeerClient] = []
        self.state = "follower"

        self.state_store = PersistentState(path=state_path or f"{self.node_id}_raft_state.json")
        self.term = self.state_store.term
        self.voted_for = self.state_store.voted_for

        self.log = RaftLog()
        self.sm = StateMachine()
        self.snapshot = Snapshot(path=f"{self.node_id}_snapshot.json")

        self.next_index: dict[str, int] = {}
        self.match_index: dict[str, int] = {}

    def attach_clients(self, clients: list[PeerClient]) -> None:
        self.clients = clients

    def become_leader(self) -> None:
        self.state = "leader"
        next_idx = len(self.log.entries)
        for client in self.clients:
            self.next_index[client.address] = next_idx
            self.match_index[client.address] = -1

    def append_entry(self, command: dict[str, Any]) -> None:
        self.log.append(LogEntry(term=self.term, command=command))

    def propose(self, command: dict[str, Any]) -> bool:
        if self.state != "leader":
            return False

        self.append_entry(command)
        self.send_heartbeat()
        self.update_commit_index()
        self.log.apply(self.sm)
        return True

    def send_heartbeat(self) -> None:
        for client in self.clients:
            peer_addr = client.address
            start = self.next_index.get(peer_addr, len(self.log.entries))
            prev_index = start - 1
            prev_term = self.log.entries[prev_index].term if prev_index >= 0 else 0
            pending = self.log.entries[start:]

            payload_entries = [entry.command for entry in pending]
            success, match_idx = client.append_entries(
                term=self.term,
                leader_id=self.node_id,
                prev_index=prev_index,
                prev_term=prev_term,
                entries=payload_entries,
                leader_commit=self.log.commit_index,
            )

            if success:
                self.match_index[peer_addr] = match_idx
                self.next_index[peer_addr] = match_idx + 1
            else:
                self.next_index[peer_addr] = max(0, start - 1)
                if self.next_index[peer_addr] == 0:
                    snapshot_data = self.snapshot.load()
                    client.install_snapshot(self.term, self.node_id, snapshot_data)

    def update_commit_index(self) -> None:
        if not self.log.entries:
            return

        majority = (len(self.clients) + 1) // 2 + 1
        for index in range(self.log.commit_index + 1, len(self.log.entries)):
            votes = 1
            for replicated_idx in self.match_index.values():
                if replicated_idx >= index:
                    votes += 1
            if votes >= majority and self.log.entries[index].term == self.term:
                self.log.commit_to(index)

    def handle_append_entries(
        self,
        term: int,
        leader_id: str,
        prev_index: int,
        prev_term: int,
        entries: list[dict[str, object]],
        leader_commit: int,
    ) -> tuple[bool, int]:
        del leader_id

        if term < self.term:
            return False, len(self.log.entries) - 1

        if term > self.term:
            self.term = term
            self.state_store.set_term(term)
            self.voted_for = None

        self.state = "follower"

        if not self.log.match(prev_index, prev_term):
            return False, len(self.log.entries) - 1

        self.log.delete_conflicts(prev_index)
        for command in entries:
            self.log.append(LogEntry(term=term, command=command))

        if leader_commit > self.log.commit_index:
            self.log.commit_to(leader_commit)
        self.log.apply(self.sm)

        return True, len(self.log.entries) - 1

    def request_vote(self, term: int, candidate_id: str, last_log_index: int, last_log_term: int) -> bool:
        if term < self.term:
            return False

        if term > self.term:
            self.term = term
            self.voted_for = None
            self.state_store.set_term(term)

        if self.voted_for not in (None, candidate_id):
            return False

        current_last_index = len(self.log.entries) - 1
        current_last_term = self.log.entries[current_last_index].term if current_last_index >= 0 else 0
        candidate_is_up_to_date = (last_log_term, last_log_index) >= (current_last_term, current_last_index)

        if not candidate_is_up_to_date:
            return False

        self.voted_for = candidate_id
        self.state_store.vote_for(candidate_id)
        return True

    def take_snapshot(self) -> None:
        last_idx = self.log.commit_index
        last_term = self.log.entries[last_idx].term if last_idx >= 0 else 0
        self.snapshot.save(self.sm, last_included_index=last_idx, last_included_term=last_term)
        if last_idx >= 0:
            self.log.entries = self.log.entries[last_idx + 1 :]
        self.log.commit_index = -1
        self.log.last_applied = -1

    def install_snapshot(self, term: int, leader_id: str, snapshot_data: dict[str, object]) -> bool:
        del leader_id

        if term < self.term:
            return False

        if term > self.term:
            self.term = term
            self.state_store.set_term(term)

        self.state = "follower"
        self.sm.kv = dict(snapshot_data.get("kv", {}))
        self.log.entries = []
        self.log.commit_index = -1
        self.log.last_applied = -1
        return True

    def add_peer(self, peer: str) -> None:
        if peer not in self.peer_addresses:
            self.peer_addresses.append(peer)

    def remove_peer(self, peer: str) -> None:
        self.peer_addresses = [p for p in self.peer_addresses if p != peer]
        self.next_index.pop(peer, None)
        self.match_index.pop(peer, None)
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
