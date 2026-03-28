from __future__ import annotations

from dataclasses import asdict

from .audit import write_audit_report
from .compliance import evaluate_controls
from .config import RuntimeConfig
from .diagnostics import DiagnosticResult, run_diagnostics
from .logging_utils import build_logger
from .sbom import generate_sbom


def _attempt_autoheal(config: RuntimeConfig, diagnostics: list[DiagnosticResult]) -> bool:
    if not config.autoheal:
        return False

    missing_required = [d for d in diagnostics if d.check.startswith("binary:") and d.status != "pass"]
    # bounded remediation: if only optional orchestration tools are missing, continue.
    return len(missing_required) == 0


def run_workflow(config: RuntimeConfig, dry_run: bool = False) -> dict[str, object]:
    logger = build_logger()
    logger.info("starting zspin workflow", extra={"extra": asdict(config)})

    diagnostics = run_diagnostics(required_bins=config.required_binaries)
    controls = evaluate_controls(config, diagnostics)

    stage_results: list[dict[str, str]] = []
    failed_stage: str | None = None
    autoheal_applied = False

    for stage_name in ("diagnostics", "compliance", "reporting", "packaging"):
        status = "pass"
        if stage_name == "diagnostics":
            required_warnings = [
                d for d in diagnostics if d.check.startswith("binary:") and d.status != "pass"
            ]
            if required_warnings:
                status = "warn"

        if stage_name == "compliance":
            if any(c.id == "ZT-001" and c.status != "pass" for c in controls):
                status = "warn"

        if status == "warn" and not autoheal_applied:
            autoheal_applied = _attempt_autoheal(config, diagnostics)
            if not autoheal_applied:
                failed_stage = stage_name

        stage_results.append({"stage": stage_name, "status": status})
        if failed_stage:
            break

    rollback_plan = []
    if failed_stage:
        rollback_plan = [
            "Stop provisioning actions",
            "Preserve diagnostics and compliance snapshots",
            "Revert mutable runtime settings to last known good state",
        ]

    if not dry_run and not failed_stage:
        audit_file = write_audit_report(config, diagnostics, controls, stage_results=stage_results)
        sbom_file = generate_sbom(project_name=config.project_name) if config.sbom_required else None
    else:
        audit_file = None
        sbom_file = None

    summary = {
        "config": asdict(config),
        "diagnostics": [asdict(d) for d in diagnostics],
        "controls": [asdict(c) for c in controls],
        "stage_results": stage_results,
        "autoheal_applied": autoheal_applied,
        "failed_stage": failed_stage,
        "rollback_plan": rollback_plan,
        "artifacts": {
            "audit": str(audit_file) if audit_file else "skipped(dry-run or failure)",
            "sbom": str(sbom_file) if sbom_file else "skipped(dry-run or policy)",
        },
    }
    logger.info("workflow completed", extra={"extra": summary["artifacts"]})
    return summary
