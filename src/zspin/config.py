from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_ENVIRONMENTS = {"dev", "staging", "prod"}
ALLOWED_DEPLOYMENT_TARGETS = {"local", "docker", "kubernetes", "serverless"}


@dataclass(frozen=True)
class RuntimeConfig:
    environment: str
    autoheal: bool
    enforce_compliance: bool
    deployment_target: str
    project_name: str
    required_binaries: tuple[str, ...]
    network_hardening: bool
    sbom_required: bool


DEFAULT_CONFIG = RuntimeConfig(
    environment="dev",
    autoheal=True,
    enforce_compliance=True,
    deployment_target="local",
    project_name="zspin",
    required_binaries=("git", "python3"),
    network_hardening=True,
    sbom_required=True,
)


def _to_bool(value: Any, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    raise ValueError(f"Expected boolean-like value, got: {value!r}")


def _normalize_required_binaries(raw: Any) -> tuple[str, ...]:
    if raw is None:
        return DEFAULT_CONFIG.required_binaries
    if not isinstance(raw, list) or not raw:
        raise ValueError("required_binaries must be a non-empty list of strings")
    binaries = tuple(str(item).strip() for item in raw if str(item).strip())
    if not binaries:
        raise ValueError("required_binaries cannot be empty after normalization")
    return binaries


def load_config(path: str | None) -> RuntimeConfig:
    if path is None:
        return DEFAULT_CONFIG

    raw = json.loads(Path(path).read_text(encoding="utf-8"))

    environment = str(raw.get("environment", DEFAULT_CONFIG.environment)).strip().lower()
    if environment not in ALLOWED_ENVIRONMENTS:
        raise ValueError(f"environment must be one of {sorted(ALLOWED_ENVIRONMENTS)}")

    deployment_target = str(
        raw.get("deployment_target", DEFAULT_CONFIG.deployment_target)
    ).strip().lower()
    if deployment_target not in ALLOWED_DEPLOYMENT_TARGETS:
        raise ValueError(
            f"deployment_target must be one of {sorted(ALLOWED_DEPLOYMENT_TARGETS)}"
        )

    project_name = str(raw.get("project_name", DEFAULT_CONFIG.project_name)).strip()
    if not project_name:
        raise ValueError("project_name cannot be empty")

    normalized: dict[str, Any] = {
        "environment": environment,
        "autoheal": _to_bool(raw.get("autoheal"), DEFAULT_CONFIG.autoheal),
        "enforce_compliance": _to_bool(
            raw.get("enforce_compliance"), DEFAULT_CONFIG.enforce_compliance
        ),
        "deployment_target": deployment_target,
        "project_name": project_name,
        "required_binaries": _normalize_required_binaries(raw.get("required_binaries")),
        "network_hardening": _to_bool(
            raw.get("network_hardening"), DEFAULT_CONFIG.network_hardening
        ),
        "sbom_required": _to_bool(raw.get("sbom_required"), DEFAULT_CONFIG.sbom_required),
    }
    return RuntimeConfig(**normalized)
