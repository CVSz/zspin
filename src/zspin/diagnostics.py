from __future__ import annotations

import platform
import shutil
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class DiagnosticResult:
    check: str
    status: str
    detail: str


def run_diagnostics(required_bins: Iterable[str] = ("git", "python3")) -> list[DiagnosticResult]:
    results: list[DiagnosticResult] = []

    results.append(
        DiagnosticResult(
            check="platform",
            status="pass",
            detail=f"{platform.system()} {platform.release()}",
        )
    )

    for tool in required_bins:
        path = shutil.which(tool)
        results.append(
            DiagnosticResult(
                check=f"binary:{tool}",
                status="pass" if path else "warn",
                detail=path or "not found in PATH",
            )
        )

    return results
