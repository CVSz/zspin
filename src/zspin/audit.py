from __future__ import annotations

import json
import socket
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .compliance import ComplianceControl
from .config import RuntimeConfig
from .diagnostics import DiagnosticResult


def write_audit_report(
    config: RuntimeConfig,
    diagnostics: list[DiagnosticResult],
    controls: list[ComplianceControl],
    output_path: str = "reports/audit_report.json",
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "host": socket.gethostname(),
        "config": asdict(config),
        "diagnostics": [asdict(item) for item in diagnostics],
        "compliance_controls": [asdict(item) for item in controls],
    }
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return path
