from __future__ import annotations

import json
import platform
from datetime import datetime, timezone
from pathlib import Path

from . import __version__


def generate_sbom(path: str = "reports/sbom.json") -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:zspin-{__version__}",
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "component": {
                "name": "zspin",
                "version": __version__,
                "type": "application",
            },
            "tools": [{"name": "zspin-sbom", "version": __version__}],
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
