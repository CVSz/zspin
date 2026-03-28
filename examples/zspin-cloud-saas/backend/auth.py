"""Authentication helpers for the zspin cloud SaaS example."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import jwt

SECRET = os.getenv("ZSPIN_JWT_SECRET", "change-me-in-production")
ALGORITHM = "HS256"
EXPIRY_SECONDS = int(os.getenv("ZSPIN_JWT_TTL_SECONDS", "86400"))


def create_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=EXPIRY_SECONDS)).timestamp()),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
