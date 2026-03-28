from __future__ import annotations

import subprocess

from .services import Service


class Runtime:
    def _run(self, cmd: list[str]) -> str:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        except OSError as exc:
            return str(exc)

        return result.stdout.strip() or result.stderr.strip()

    def deploy(self, service: Service) -> str:
        cmd = ["kubectl", "apply", "-f", f"k8s/{service.name}-service.yaml"]
        return self._run(cmd)

    def scale(self, service: Service, replicas: int) -> str:
        cmd = [
            "kubectl",
            "scale",
            "deployment",
            service.name,
            f"--replicas={replicas}",
        ]
        return self._run(cmd)

    def restart(self, service: Service) -> str:
        cmd = ["kubectl", "rollout", "restart", f"deployment/{service.name}"]
        return self._run(cmd)
