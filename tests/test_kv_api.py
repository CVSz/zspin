from zspin.apiserver import init_app
from zspin.distributed_db.mvcc import MVCCStore
from zspin.kv import api as kv_api


class FakeRaft:
    def __init__(self, mvcc: MVCCStore) -> None:
        self.mvcc = mvcc
        self.commands: list[dict[str, object]] = []

    def propose(self, command: dict[str, object]) -> bool:
        self.commands.append(command)
        self.mvcc.write(
            key=str(command["key"]),
            value=command.get("value"),
            ts=float(command["ts"]),
        )
        return True


def test_kv_endpoints_support_put_get_delete_and_watch() -> None:
    mvcc = MVCCStore()
    raft = FakeRaft(mvcc)
    init_app(raft=raft, mvcc=mvcc)

    put_result = kv_api.put(kv_api.KVItem(key="/registry/pods/default/nginx", value='{"image":"nginx"}'))
    assert put_result == {"ok": True}

    get_result = kv_api.get("/registry/pods/default/nginx")
    assert get_result == {"value": '{"image":"nginx"}'}

    watch_result = kv_api.watch("/registry/pods/default/nginx")
    assert watch_result == {"value": '{"image":"nginx"}'}

    delete_result = kv_api.delete("/registry/pods/default/nginx")
    assert delete_result == {"ok": True}

    assert kv_api.get("/registry/pods/default/nginx") == {"value": None}
