from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class RaftPeer(Protocol):
    def handle_append_entries(
        self,
        term: int,
        leader_id: str,
        prev_index: int,
        prev_term: int,
        entries: list[dict[str, object]],
        leader_commit: int,
    ) -> tuple[bool, int]:
        ...

    def install_snapshot(self, term: int, leader_id: str, snapshot_data: dict[str, object]) -> bool:
        ...


@dataclass(slots=True)
class PeerClient:
    address: str
    peer: RaftPeer

    def append_entries(
        self,
        term: int,
        leader_id: str,
        prev_index: int,
        prev_term: int,
        entries: list[dict[str, object]],
        leader_commit: int,
    ) -> tuple[bool, int]:
        return self.peer.handle_append_entries(
            term=term,
            leader_id=leader_id,
            prev_index=prev_index,
            prev_term=prev_term,
            entries=entries,
            leader_commit=leader_commit,
        )

    def install_snapshot(self, term: int, leader_id: str, snapshot_data: dict[str, object]) -> bool:
        return self.peer.install_snapshot(term=term, leader_id=leader_id, snapshot_data=snapshot_data)


class LocalCluster:
    """Simple in-process peer registry used by the demo CLI and tests."""

    def __init__(self) -> None:
        self._peers: dict[str, RaftPeer] = {}

    def register(self, address: str, peer: RaftPeer) -> None:
        self._peers[address] = peer

    def clients_for(self, addresses: list[str]) -> list[PeerClient]:
        clients: list[PeerClient] = []
        for address in addresses:
            peer = self._peers.get(address)
            if peer is not None:
                clients.append(PeerClient(address=address, peer=peer))
        return clients
