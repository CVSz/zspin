from __future__ import annotations

import json
from pathlib import Path

from zspin.cli import build_parser
from zspin.config import DEFAULT_CONFIG
from zspin.go_live import run_go_live_installer_bundle


def test_cli_has_go_live_installer_command() -> None:
    parser = build_parser()
    args = parser.parse_args(["go-live-installer", "--dry-run"])
    assert args.command == "go-live-installer"
    assert args.dry_run is True


def test_go_live_bundle_generates_expected_artifacts(tmp_path: Path) -> None:
    result = run_go_live_installer_bundle(config=DEFAULT_CONFIG, output_dir=tmp_path.as_posix(), dry_run=True)

    assert Path(result["go_live_report"]).exists()
    assert Path(result["audit_report"]).exists()
    assert Path(result["sbom"]).exists()
    assert Path(result["linux_installer"]).exists()
    assert Path(result["windows_installer"]).exists()

    report = json.loads(Path(result["go_live_report"]).read_text(encoding="utf-8"))
    assert "pseudo_code_workflow" in report
    assert report["metadata"]["dry_run"] is True
    assert "source_snapshot" in report["artifacts"]
    assert "rollback_plan" in report
