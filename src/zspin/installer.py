from __future__ import annotations

from dataclasses import asdict

from .audit import write_audit_report
from .compliance import evaluate_controls
from .config import RuntimeConfig
from .diagnostics import run_diagnostics
from .logging_utils import build_logger
from .sbom import generate_sbom


def run_workflow(config: RuntimeConfig, dry_run: bool = False) -> dict[str, object]:
    logger = build_logger()
    logger.info("starting zspin workflow", extra={"extra": asdict(config)})

    diagnostics = run_diagnostics()
    controls = evaluate_controls(config)

    if not dry_run:
        audit_file = write_audit_report(config, diagnostics, controls)
        sbom_file = generate_sbom()
    else:
        audit_file = None
        sbom_file = None

    summary = {
        "config": asdict(config),
        "diagnostics": [asdict(d) for d in diagnostics],
        "controls": [asdict(c) for c in controls],
        "artifacts": {
            "audit": str(audit_file) if audit_file else "skipped(dry-run)",
            "sbom": str(sbom_file) if sbom_file else "skipped(dry-run)",
        },
    }
    logger.info("workflow completed", extra={"extra": summary["artifacts"]})
    return summary
