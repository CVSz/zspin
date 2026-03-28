from zspin.config import DEFAULT_CONFIG
from zspin.installer import run_workflow


def test_workflow_dry_run_has_expected_artifacts() -> None:
    result = run_workflow(DEFAULT_CONFIG, dry_run=True)
    assert result["artifacts"]["audit"] == "skipped(dry-run)"
    assert result["artifacts"]["sbom"] == "skipped(dry-run)"
