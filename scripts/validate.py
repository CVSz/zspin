#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> tuple[int, str]:
    env = os.environ.copy()
    src_path = str(Path("src").resolve())
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = src_path if not existing else f"{src_path}:{existing}"
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True, env=env)
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    checks: list[tuple[str, list[str]]] = [
        ("unit_tests", [sys.executable, "-m", "pytest"]),
        ("dry_run", [sys.executable, "-m", "zspin.cli", "run", "--dry-run"]),
        (
            "full_run",
            [sys.executable, "-m", "zspin.cli", "run", "--config", "examples/config.json"],
        ),
    ]

    summary = {}
    failed = False

    for name, cmd in checks:
        code, output = run(cmd)
        summary[name] = {"code": code, "output": output[-4000:]}
        if code != 0:
            failed = True

    Path("reports").mkdir(exist_ok=True)
    Path("reports/validation_report.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
    )

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
