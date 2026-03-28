from __future__ import annotations

from zspin.scheduler import Scheduler


class Operator:
    def __init__(self, store, runtime) -> None:
        self.store = store
        self.runtime = runtime
        self.scheduler = Scheduler()

    def reconcile(self) -> None:
        for res in self.store.list():
            desired = res.spec
            current = res.status.get("state")

            if current != "running":
                node = self.scheduler.schedule(res)

                result = self.runtime.deploy(
                    type("Obj", (), {"name": res.name})
                )

                res.status["state"] = "running"
                res.status["node"] = node
                res.status["runtime"] = result
                res.status["desired"] = desired
