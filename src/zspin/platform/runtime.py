from __future__ import annotations

import subprocess


class Runtime:
    """Runtime adapter that executes deployment actions against Kubernetes."""

    def deploy(self, service: object) -> str:
        service_name = getattr(service, "name", "")
        manifest_path = f"k8s/{service_name}.yaml"
        cmd = ["kubectl", "apply", "-f", manifest_path]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            return result.stdout or result.stderr
        except OSError as exc:
            return str(exc)

    def scale(self, service: object, replicas: int) -> str:
        service_name = getattr(service, "name", "")
        cmd = [
            "kubectl",
            "scale",
            "deployment",
            service_name,
            f"--replicas={replicas}",
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            return result.stdout or result.stderr
        except OSError as exc:
            return str(exc)
