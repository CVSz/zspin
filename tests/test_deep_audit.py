from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "deep_audit.py"
spec = importlib.util.spec_from_file_location("deep_audit", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_build_report_has_expected_sections() -> None:
    report = module.build_report(Path(__file__).resolve().parents[1], generated_at="2026-01-01T00:00:00+00:00")

    assert report["metadata"]["audit_type"] == "master-meta-deep-audit"
    assert report["metadata"]["generated_at"] == "2026-01-01T00:00:00+00:00"
    assert "compliance_matrix" in report
    assert "summary" in report


def test_render_markdown_contains_score_and_controls() -> None:
    report = module.build_report(Path(__file__).resolve().parents[1], generated_at="2026-01-01T00:00:00+00:00")
    markdown = module.render_markdown(report)

    assert "Master Meta Deep Audit Report" in markdown
    assert "Compliance Matrix" in markdown
    assert "Score" in markdown
