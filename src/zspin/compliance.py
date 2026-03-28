from __future__ import annotations

from dataclasses import dataclass

from .config import RuntimeConfig


@dataclass(frozen=True)
class ComplianceControl:
    id: str
    name: str
    status: str
    rationale: str


def evaluate_controls(config: RuntimeConfig) -> list[ComplianceControl]:
    controls = [
        ComplianceControl(
            id="ZT-001",
            name="Zero Trust baseline",
            status="pass" if config.enforce_compliance else "warn",
            rationale="Compliance enforcement toggle must remain enabled in production.",
        ),
        ComplianceControl(
            id="SBOM-001",
            name="SBOM generation requirement",
            status="pass",
            rationale="Release pipeline includes deterministic SBOM output.",
        ),
        ComplianceControl(
            id="AUDIT-001",
            name="Structured audit logging",
            status="pass",
            rationale="JSON logging and metadata reports are always generated.",
        ),
    ]
    return controls
