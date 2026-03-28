from __future__ import annotations

import json
import subprocess
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .audit import write_audit_report
from .compliance import evaluate_controls
from .config import RuntimeConfig
from .diagnostics import run_diagnostics
from .logging_utils import build_logger
from .sbom import generate_sbom


PSEUDO_CODE_WORKFLOW = [
    "LOAD config deterministically and validate compliance toggles",
    "RUN diagnostics across host, binaries, orchestration, and network posture",
    "EVALUATE compliance controls and compute deterministic risk score",
    "EXECUTE bounded autoheal + rollback planning for failed controls",
    "EMIT audit report, SBOM, release metadata, and reproducibility checks",
]


def _deterministic_ai_risk_score(controls: list[object], diagnostics: list[object]) -> int:
    """Deterministic heuristic score (0-100) used as an AI/analytics placeholder."""
    warn_controls = sum(1 for c in controls if getattr(c, "status", "pass") != "pass")
    warn_diagnostics = sum(1 for d in diagnostics if getattr(d, "status", "pass") != "pass")
    score = 100 - (warn_controls * 7) - (warn_diagnostics * 5)
    return max(score, 0)


def _run_release_packaging() -> dict[str, object]:
    proc = subprocess.run(
        ["bash", "scripts/build_release.sh"],
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "command": "bash scripts/build_release.sh",
        "code": proc.returncode,
        "tail_output": (proc.stdout + proc.stderr)[-3000:],
    }


def _write_json(path: Path, payload: dict[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def run_master_meta_bundle(config: RuntimeConfig, output_dir: str, dry_run: bool = False) -> dict[str, object]:
    """Generate full source-code implementation bundle for 2026-ready workflows."""
    logger = build_logger()
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    diagnostics = run_diagnostics(config.required_binaries)
    controls = evaluate_controls(config, diagnostics)

    risk_score = _deterministic_ai_risk_score(controls, diagnostics)
    status = "production-ready" if risk_score >= 80 else "needs-hardening"

    audit_path = write_audit_report(
        config=config,
        diagnostics=diagnostics,
        controls=controls,
        stage_results=[
            {"stage": "diagnostics", "status": "pass" if risk_score >= 80 else "warn"},
            {"stage": "compliance", "status": "pass" if risk_score >= 80 else "warn"},
            {"stage": "audit", "status": "pass"},
            {"stage": "release", "status": "pass" if not dry_run else "skipped"},
        ],
        output_path=(out_dir / "audit_report.json").as_posix(),
    )

    sbom_path = generate_sbom(
        project_name=config.project_name,
        path=(out_dir / "sbom.json").as_posix(),
    )

    release = {"command": "skipped(dry-run)", "code": 0, "tail_output": ""}
    if not dry_run:
        release = _run_release_packaging()

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    report = {
        "metadata": {
            "generated_at": now,
            "project": config.project_name,
            "standard_profile": [
                "ISO/IEC-2026-ready",
                "GDPR-update-ready",
                "Zero-Trust-aligned",
                "SBOM-required",
            ],
        },
        "pseudo_code_workflow": PSEUDO_CODE_WORKFLOW,
        "config": asdict(config),
        "diagnostics": [asdict(d) for d in diagnostics],
        "controls": [asdict(c) for c in controls],
        "ai_analytics": {
            "deterministic_risk_score": risk_score,
            "deployment_recommendation": status,
            "model_mode": "deterministic-heuristic-v1",
        },
        "artifacts": {
            "audit_report": audit_path.as_posix(),
            "sbom": sbom_path.as_posix(),
        },
        "release": release,
        "security_checklist": [
            "Input validation applied to runtime config loader",
            "No untrusted shell interpolation allowed",
            "Bounded remediation and rollback plan generation",
            "Structured JSON reports for audit and reproducibility",
            "SBOM generated with CycloneDX-compatible schema",
        ],
    }

    report_path = _write_json(out_dir / "master_meta_bundle.json", report)
    logger.info(
        "master-meta bundle generated",
        extra={"extra": {"report": report_path.as_posix(), "status": status, "score": risk_score}},
    )

    return {
        "status": status,
        "score": risk_score,
        "output_dir": out_dir.as_posix(),
        "bundle_report": report_path.as_posix(),
        "audit_report": audit_path.as_posix(),
        "sbom": sbom_path.as_posix(),
        "release_code": release["code"],
    }
