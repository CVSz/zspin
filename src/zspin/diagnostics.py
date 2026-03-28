from __future__ import annotations

import platform
import shutil
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class DiagnosticResult:
    stage: str
    check: str
    status: str
    detail: str


PASS = "pass"
WARN = "warn"


def run_diagnostics(required_bins: Iterable[str]) -> list[DiagnosticResult]:
    results: list[DiagnosticResult] = []

    results.append(
        DiagnosticResult(
            stage="host",
            check="platform",
            status=PASS,
            detail=f"{platform.system()} {platform.release()}",
        )
    )
    results.append(
        DiagnosticResult(
            stage="host",
            check="python",
            status=PASS,
            detail=platform.python_version(),
        )
    )

    for tool in required_bins:
        path = shutil.which(tool)
        results.append(
            DiagnosticResult(
                stage="tooling",
                check=f"binary:{tool}",
                status=PASS if path else WARN,
                detail=path or "not found in PATH",
            )
        )

    container_runtime = shutil.which("docker") or shutil.which("podman")
    results.append(
        DiagnosticResult(
            stage="orchestration",
            check="container-runtime",
            status=PASS if container_runtime else WARN,
            detail=container_runtime or "docker/podman unavailable",
        )
    )

    k8s_cli = shutil.which("kubectl")
    results.append(
        DiagnosticResult(
            stage="orchestration",
            check="kubernetes-cli",
            status=PASS if k8s_cli else WARN,
            detail=k8s_cli or "kubectl unavailable",
        )
    )

    return results
