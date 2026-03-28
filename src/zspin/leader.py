from __future__ import annotations

import time
import uuid


class LeaderElection:
    def __init__(self, lease_duration: int = 5) -> None:
        self.leader_id: str | None = None
        self.lease_expiry = 0.0
        self.id = str(uuid.uuid4())
        self.lease_duration = lease_duration

    def try_acquire(self) -> bool:
        now = time.time()

        if not self.leader_id or now > self.lease_expiry:
            self.leader_id = self.id
            self.lease_expiry = now + self.lease_duration
            return True

        return self.leader_id == self.id

    def renew(self) -> None:
        if self.leader_id == self.id:
            self.lease_expiry = time.time() + self.lease_duration
