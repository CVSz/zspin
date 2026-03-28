from __future__ import annotations

import json
import subprocess


class PolicyEngine:
    def evaluate(self, action: dict[str, object]) -> bool:
        try:
            result = subprocess.run(
                ["opa", "eval", "-i", "-", "-d", "policy/", "data.zspin.policy.allow"],
                input=json.dumps(action),
                capture_output=True,
                text=True,
                check=False,
            )
            return "true" in result.stdout.lower()
        except OSError:
            return True
