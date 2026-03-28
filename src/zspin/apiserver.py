from __future__ import annotations

from fastapi import FastAPI

from zspin.crd import Resource, ResourceStore
from zspin.distributed_db.mvcc import MVCCStore
from zspin.kv.store import KVStore
from zspin.kv import api as kv_api


class _LocalRaftAdapter:
    """Fallback adapter that executes writes locally when no raft node is provided."""

    def __init__(self, mvcc: MVCCStore) -> None:
        self.mvcc = mvcc

    def propose(self, command: dict[str, object]) -> bool:
        if str(command.get("op", "")).lower() != "mvcc_write":
            return False
        self.mvcc.write(
            key=str(command.get("key", "")),
            value=command.get("value"),
            ts=float(command.get("ts", 0.0)),
        )
        return True


app = FastAPI()
store = ResourceStore()


def init_app(raft=None, mvcc: MVCCStore | None = None) -> FastAPI:
    mvcc_store = mvcc or MVCCStore()
    raft_node = raft or _LocalRaftAdapter(mvcc_store)

    if hasattr(raft_node, "sm") and hasattr(raft_node.sm, "register_handler"):
        raft_node.sm.register_handler(
            "mvcc_write",
            lambda command: mvcc_store.write(
                key=str(command.get("key", "")),
                value=command.get("value"),
                ts=float(command.get("ts", 0.0)),
            ),
        )

    kv_api.init(KVStore(raft_node, mvcc_store))
    if not getattr(app.state, "kv_router_initialized", False):
        app.include_router(kv_api.router)
        app.state.kv_router_initialized = True
    return app


init_app()


@app.post("/apply")
def apply(resource: dict[str, object]) -> dict[str, str]:
    name = str(resource["name"])
    spec = resource["spec"]
    if not isinstance(spec, dict):
        raise ValueError("spec must be a dictionary")

    r = Resource(name, spec)
    store.apply(r)
    return {"status": "applied", "name": r.name}


@app.get("/resources")
def list_resources() -> list[dict[str, object]]:
    return [
        {"name": r.name, "spec": r.spec, "status": r.status}
        for r in store.list()
    ]
