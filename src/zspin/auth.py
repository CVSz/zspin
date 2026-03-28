from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time

SECRET = os.getenv("ZSPIN_JWT_SECRET", "zspin-secret")


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(f"{data}{padding}".encode("ascii"))


def create_token(user: str, tenant: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": user,
        "tenant": tenant,
        "iat": int(time.time()),
    }

    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = hmac.new(SECRET.encode("utf-8"), signing_input, hashlib.sha256).digest()
    signature_b64 = _b64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def verify_token(token: str) -> dict[str, str | int]:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError as exc:
        raise ValueError("malformed token") from exc

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    expected_signature = hmac.new(SECRET.encode("utf-8"), signing_input, hashlib.sha256).digest()
    provided_signature = _b64url_decode(signature_b64)
    if not hmac.compare_digest(expected_signature, provided_signature):
        raise ValueError("invalid token signature")

    payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))
    if "tenant" not in payload or "sub" not in payload:
        raise ValueError("token missing required claims")
    return payload
