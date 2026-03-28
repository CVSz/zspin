from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from zspin.kv.store import KVStore

router = APIRouter()


class KVItem(BaseModel):
    key: str
    value: str | None = None


kv_store: KVStore | None = None


def init(store: KVStore) -> None:
    global kv_store
    kv_store = store


def _store() -> KVStore:
    if kv_store is None:
        raise HTTPException(status_code=503, detail="KV store is not initialized")
    return kv_store


@router.post("/v1/kv")
def put(item: KVItem) -> dict[str, bool]:
    ok = _store().put(item.key, item.value)
    return {"ok": ok}


@router.get("/v1/kv")
def get(key: str) -> dict[str, object | None]:
    val = _store().get(key)
    return {"value": val}


@router.delete("/v1/kv")
def delete(key: str) -> dict[str, bool]:
    ok = _store().delete(key)
    return {"ok": ok}


@router.get("/v1/watch")
def watch(key: str) -> dict[str, object | None]:
    return {"value": _store().get(key)}
