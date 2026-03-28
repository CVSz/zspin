from __future__ import annotations

import json
import platform
from datetime import datetime, timezone
from pathlib import Path

from . import __version__


def generate_sbom(project_name: str, path: str = "reports/sbom.json") -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{project_name}-{__version__}",
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "component": {
                "name": project_name,
                "version": __version__,
                "type": "application",
            },
            "tools": [{"name": "zspin-sbom", "version": __version__}],
            "properties": [
                {"name": "security.supply_chain", "value": "sbom-enabled"},
                {"name": "compliance.profile", "value": "2026-ready-baseline"},
            ],
        },
        "components": [
            {
                "name": "python",
                "version": platform.python_version(),
                "type": "framework",
            }
        ],
    }

    output.write_text(json.dumps(sbom, indent=2, sort_keys=True), encoding="utf-8")
    return output
