from __future__ import annotations

import subprocess


def apply_gitops() -> str:
    cmd = ["kubectl", "apply", "-f", "gitops/argocd-app.yaml"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.stdout.strip() or result.stderr.strip()
