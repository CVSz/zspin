from __future__ import annotations

from fastapi import FastAPI

from zspin.crd import Resource, ResourceStore

app = FastAPI()
store = ResourceStore()


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
