from __future__ import annotations

import secrets

API_KEYS: dict[str, str] = {}


def generate_key(tenant: str) -> str:
    key = secrets.token_hex(16)
    API_KEYS[key] = tenant
    return key


def get_tenant(key: str) -> str | None:
    return API_KEYS.get(key)
