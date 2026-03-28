from pathlib import Path

from zspin.intelligence import IntelligentRemediation
from zspin.observability.alerts import AlertHandler
from zspin.platform.runtime import Runtime
from zspin.slo import SLOEngine


class DummyService:
    def __init__(self, name: str) -> None:
        self.name = name


def test_slo_engine_detects_violations() -> None:
    engine = SLOEngine()
    violations = engine.evaluate({"availability": 0.95, "latency_ms": 250})
    assert "availability" in violations
    assert "latency" in violations


def test_intelligent_remediation_prioritizes_availability() -> None:
    decision = IntelligentRemediation().decide({"type": "high_cpu"}, ["availability", "latency"])
    assert decision == {"type": "restart", "priority": "high"}


def test_alert_mapping_high_cpu() -> None:
    handler = AlertHandler()
    mapped = handler.map_alert({"alert": "HighCPU"})
    assert mapped["type"] == "high_cpu"
    assert mapped["service"] == "api"


def test_runtime_deploy_prefers_service_manifest(monkeypatch, tmp_path) -> None:
    called: list[list[str]] = []

    class Result:
        stdout = "ok"
        stderr = ""

    def fake_run(cmd, capture_output, text, check):
        called.append(cmd)
        return Result()

    monkeypatch.setattr("subprocess.run", fake_run)
    monkeypatch.chdir(tmp_path)

    Path("k8s").mkdir()
    Path("k8s/api-service.yaml").write_text("apiVersion: v1\nkind: Service\n", encoding="utf-8")

    runtime = Runtime()
    runtime.deploy(DummyService("api"))

    assert called[0] == ["kubectl", "apply", "-f", "k8s/api-service.yaml"]
