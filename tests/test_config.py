from zspin.config import DEFAULT_CONFIG, load_config


def test_load_default_config() -> None:
    cfg = load_config(None)
    assert cfg == DEFAULT_CONFIG
