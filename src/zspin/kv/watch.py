from __future__ import annotations

import asyncio
import json
import queue
from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from zspin.kv.store import KVStore

router = APIRouter()
_store: KVStore | None = None


def init(store: KVStore) -> None:
    global _store
    _store = store


def _require_store() -> KVStore:
    if _store is None:
        raise HTTPException(status_code=500, detail="kv store is not initialized")
    return _store


@router.get("/v1/watch/stream")
async def watch_stream(key: str) -> StreamingResponse:
    event_queue: queue.Queue[dict[str, object]] = queue.Queue()
    _require_store().watch(key, event_queue)

    async def event_stream() -> AsyncGenerator[str, None]:
        while True:
            while not event_queue.empty():
                event = event_queue.get()
                yield f"data: {json.dumps(event)}\n\n"
            await asyncio.sleep(0.5)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
