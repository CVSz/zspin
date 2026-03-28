from __future__ import annotations

from fastapi import FastAPI

from zspin.distributed_db.mvcc import MVCCStore
from zspin.kv import api, watch
from zspin.kv.lease import LeaseManager
from zspin.kv.revision import Revision
from zspin.kv.store import KVStore

app = FastAPI()


def init_app(raft: object, mvcc: MVCCStore | None = None) -> FastAPI:
    store = MVCCStore() if mvcc is None else mvcc
    revision = Revision()
    kv_store = KVStore(raft, store, revision)
    lease_manager = LeaseManager(kv_store)

    api.init(kv_store, lease_manager)
    watch.init(kv_store)

    app.include_router(api.router)
    app.include_router(watch.router)
    return app
