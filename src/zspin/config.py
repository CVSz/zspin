from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RuntimeConfig:
    environment: str
    autoheal: bool
    enforce_compliance: bool
    deployment_target: str


DEFAULT_CONFIG = RuntimeConfig(
    environment="dev",
    autoheal=True,
    enforce_compliance=True,
    deployment_target="local",
)


def load_config(path: str | None) -> RuntimeConfig:
    if path is None:
        return DEFAULT_CONFIG

    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    normalized: dict[str, Any] = {
        "environment": str(raw.get("environment", DEFAULT_CONFIG.environment)),
        "autoheal": bool(raw.get("autoheal", DEFAULT_CONFIG.autoheal)),
        "enforce_compliance": bool(
            raw.get("enforce_compliance", DEFAULT_CONFIG.enforce_compliance)
        ),
        "deployment_target": str(
            raw.get("deployment_target", DEFAULT_CONFIG.deployment_target)
        ),
    }
    return RuntimeConfig(**normalized)
