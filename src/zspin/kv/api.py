from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from zspin.kv.lease import LeaseManager
from zspin.kv.store import KVStore

router = APIRouter()
_store: KVStore | None = None
_lease_mgr: LeaseManager | None = None


class KVRequest(BaseModel):
    key: str
    value: object | None = None


class CASRequest(BaseModel):
    key: str
    expected: object | None = None
    value: object | None = None


class LeaseRequest(BaseModel):
    key: str
    ttl_seconds: float


def init(store: KVStore, lease_mgr: LeaseManager | None = None) -> None:
    global _store, _lease_mgr
    _store = store
    _lease_mgr = lease_mgr


def _require_store() -> KVStore:
    if _store is None:
        raise HTTPException(status_code=500, detail="kv store is not initialized")
    return _store


@router.post("/v1/kv")
def put(payload: KVRequest) -> dict[str, object]:
    return _require_store().put(payload.key, payload.value)


@router.get("/v1/kv")
def get(key: str) -> dict[str, object | None]:
    return {"value": _require_store().get(key)}


@router.delete("/v1/kv")
def delete(key: str) -> dict[str, object]:
    return _require_store().delete(key)


@router.get("/v1/kv/prefix")
def prefix(prefix: str) -> dict[str, object | None]:
    return _require_store().prefix(prefix)


@router.post("/v1/kv/cas")
def cas(payload: CASRequest) -> dict[str, object]:
    return _require_store().cas(payload.key, payload.expected, payload.value)


@router.post("/v1/lease")
def grant_lease(payload: LeaseRequest) -> dict[str, object]:
    if _lease_mgr is None:
        raise HTTPException(status_code=500, detail="lease manager is not initialized")
    expire_at = _lease_mgr.grant(payload.key, payload.ttl_seconds)
    return {"ok": True, "key": payload.key, "expire_at": expire_at}
