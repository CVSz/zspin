from __future__ import annotations

ROLES: dict[str, list[str]] = {
    "admin": ["deploy", "billing"],
    "developer": ["deploy"],
    "viewer": [],
}


def check_permission(role: str, action: str) -> bool:
    return action in ROLES.get(role, [])
