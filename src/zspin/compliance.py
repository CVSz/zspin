from __future__ import annotations

from dataclasses import dataclass

from .config import RuntimeConfig
from .diagnostics import DiagnosticResult


@dataclass(frozen=True)
class ComplianceControl:
    id: str
    name: str
    status: str
    rationale: str


def _has_warn(results: list[DiagnosticResult], check_prefix: str) -> bool:
    return any(item.check.startswith(check_prefix) and item.status != "pass" for item in results)


def evaluate_controls(
    config: RuntimeConfig, diagnostics: list[DiagnosticResult]
) -> list[ComplianceControl]:
    tooling_gap = _has_warn(diagnostics, "binary:")
    container_gap = _has_warn(diagnostics, "container-runtime")

    controls = [
        ComplianceControl(
            id="ZT-001",
            name="Zero Trust baseline",
            status="pass" if config.enforce_compliance else "warn",
            rationale="Compliance enforcement toggle must remain enabled in production.",
        ),
        ComplianceControl(
            id="CFG-001",
            name="Deterministic configuration profile",
            status="pass",
            rationale=(
                f"Environment={config.environment}, target={config.deployment_target}, "
                f"project={config.project_name}."
            ),
        ),
        ComplianceControl(
            id="SBOM-001",
            name="SBOM generation requirement",
            status="pass" if config.sbom_required else "warn",
            rationale="Release pipeline must include deterministic SBOM output.",
        ),
        ComplianceControl(
            id="NET-001",
            name="Network hardening policy",
            status="pass" if config.network_hardening else "warn",
            rationale="Firewall/VPN/DNS/NTP baseline should be enabled in non-local environments.",
        ),
        ComplianceControl(
            id="TOOL-001",
            name="Required toolchain availability",
            status="warn" if tooling_gap else "pass",
            rationale="All required binaries should be present for reproducible automation.",
        ),
        ComplianceControl(
            id="ORCH-001",
            name="Container orchestration readiness",
            status="warn" if container_gap else "pass",
            rationale="Container runtime availability is required for cloud-native orchestration.",
        ),
        ComplianceControl(
            id="AUDIT-001",
            name="Structured audit logging",
            status="pass",
            rationale="JSON logging and metadata reports are generated for every workflow.",
        ),
    ]
    return controls
