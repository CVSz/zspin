from __future__ import annotations

import queue
import time

from zspin.distributed_db.mvcc import MVCCStore
from zspin.kv.lease import LeaseManager
from zspin.kv.revision import Revision
from zspin.kv.store import KVStore


class StubRaft:
    def __init__(self, mvcc: MVCCStore) -> None:
        self.mvcc = mvcc

    def propose(self, command: dict[str, object]) -> bool:
        self.mvcc.write(str(command["key"]), command["value"], float(command["ts"]))
        return True


def test_put_get_prefix_and_cas() -> None:
    mvcc = MVCCStore()
    store = KVStore(StubRaft(mvcc), mvcc, Revision())

    put_result = store.put("/registry/pods/default/nginx", {"name": "nginx"})
    assert put_result["ok"] is True
    assert put_result["revision"] == 1

    assert store.get("/registry/pods/default/nginx") == {"name": "nginx"}

    store.put("/registry/pods/default/api", {"name": "api"})
    prefixed = store.prefix("/registry/pods")
    assert set(prefixed) == {
        "/registry/pods/default/nginx",
        "/registry/pods/default/api",
    }

    conflict = store.cas("/registry/pods/default/nginx", {"name": "wrong"}, {"name": "new"})
    assert conflict["ok"] is False

    updated = store.cas("/registry/pods/default/nginx", {"name": "nginx"}, {"name": "new"})
    assert updated["ok"] is True
    assert store.get("/registry/pods/default/nginx") == {"name": "new"}


def test_watch_notifications_and_lease_expiry() -> None:
    mvcc = MVCCStore()
    store = KVStore(StubRaft(mvcc), mvcc, Revision())

    events: queue.Queue[dict[str, object]] = queue.Queue()
    watched_key = "/registry/pods/default/ttl"
    store.watch(watched_key, events)

    store.put(watched_key, {"phase": "running"})
    event = events.get(timeout=1)
    assert event["key"] == watched_key
    assert event["value"] == {"phase": "running"}
    assert event["revision"] == 1

    lease = LeaseManager(store, interval_seconds=0.05)
    lease.grant(watched_key, ttl_seconds=0.05)
    time.sleep(0.2)
    assert store.get(watched_key) is None
