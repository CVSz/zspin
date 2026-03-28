from __future__ import annotations

import subprocess
from pathlib import Path


class Runtime:
    """Runtime adapter that executes deployment actions against Kubernetes."""

    def _run(self, cmd: list[str]) -> str:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            return result.stdout or result.stderr
        except OSError as exc:
            return str(exc)

    def deploy(self, service: object) -> str:
        service_name = getattr(service, "name", "")
        preferred = Path(f"k8s/{service_name}-service.yaml")
        fallback = Path(f"k8s/{service_name}.yaml")
        manifest_path = preferred if preferred.exists() else fallback
        cmd = ["kubectl", "apply", "-f", str(manifest_path)]
        return self._run(cmd)

    def scale(self, service: object, replicas: int) -> str:
        service_name = getattr(service, "name", "")
        cmd = [
            "kubectl",
            "scale",
            "deployment",
            service_name,
            f"--replicas={replicas}",
        ]
        return self._run(cmd)

    def restart(self, service: object) -> str:
        service_name = getattr(service, "name", "")
        cmd = ["kubectl", "rollout", "restart", f"deployment/{service_name}"]
        return self._run(cmd)
