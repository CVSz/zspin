"""Demo FastAPI app for zspin cloud SaaS skeleton."""

from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException

from analytics import get_stats
from auth import create_token, verify_token
from billing import create_checkout
from usage import meter

app = FastAPI(title="zspin-cloud-demo")


def get_user(authorization: str) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ", 1)[1]
    try:
        payload = verify_token(token)
    except Exception as exc:  # pragma: no cover - demo code
        raise HTTPException(status_code=401, detail="Invalid token") from exc
    return str(payload["sub"])


@app.post("/login")
def login() -> dict[str, str]:
    token = create_token("user-1")
    return {"token": token}


@app.post("/query")
def query(sql: str, authorization: str = Header(...)) -> dict[str, object]:
    user_id = get_user(authorization)
    meter(user_id, "query")
    return {"ok": True, "user": user_id, "sql": sql}


@app.get("/analytics")
def analytics(authorization: str = Header(...)) -> dict[str, int]:
    user_id = get_user(authorization)
    return get_stats(user_id)


@app.post("/billing/checkout")
def billing_checkout() -> dict[str, str]:
    return {"url": create_checkout()}
