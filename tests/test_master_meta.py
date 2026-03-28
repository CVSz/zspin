from __future__ import annotations

import json
from pathlib import Path

from zspin.cli import build_parser
from zspin.config import DEFAULT_CONFIG
from zspin.master_meta import run_master_meta_bundle


def test_cli_has_master_meta_command() -> None:
    parser = build_parser()
    args = parser.parse_args(["master-meta", "--dry-run"])
    assert args.command == "master-meta"
    assert args.dry_run is True


def test_master_meta_bundle_generates_expected_artifacts(tmp_path: Path) -> None:
    result = run_master_meta_bundle(config=DEFAULT_CONFIG, output_dir=tmp_path.as_posix(), dry_run=True)

    assert result["status"] in {"production-ready", "needs-hardening"}
    assert Path(result["bundle_report"]).exists()
    assert Path(result["audit_report"]).exists()
    assert Path(result["sbom"]).exists()

    bundle = json.loads(Path(result["bundle_report"]).read_text(encoding="utf-8"))
    assert "pseudo_code_workflow" in bundle
    assert bundle["release"]["command"] == "skipped(dry-run)"
    assert bundle["ai_analytics"]["model_mode"] == "deterministic-heuristic-v1"
