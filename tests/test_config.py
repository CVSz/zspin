import json

import pytest

from zspin.config import DEFAULT_CONFIG, load_config


def test_load_default_config() -> None:
    cfg = load_config(None)
    assert cfg == DEFAULT_CONFIG


def test_load_config_normalizes_booleans_and_lists(tmp_path) -> None:
    path = tmp_path / "cfg.json"
    path.write_text(
        json.dumps(
            {
                "environment": "prod",
                "autoheal": "true",
                "enforce_compliance": "1",
                "deployment_target": "kubernetes",
                "project_name": "acme-platform",
                "required_binaries": ["git", "python3", "kubectl"],
                "network_hardening": "yes",
                "sbom_required": "on",
            }
        ),
        encoding="utf-8",
    )

    cfg = load_config(str(path))
    assert cfg.environment == "prod"
    assert cfg.deployment_target == "kubernetes"
    assert cfg.autoheal is True
    assert cfg.required_binaries[-1] == "kubectl"


def test_load_config_rejects_invalid_environment(tmp_path) -> None:
    path = tmp_path / "cfg.json"
    path.write_text(json.dumps({"environment": "qa"}), encoding="utf-8")

    with pytest.raises(ValueError):
        load_config(str(path))
