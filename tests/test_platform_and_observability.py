from zspin.intelligence import IntelligentRemediation
from zspin.observability.alerts import AlertHandler
from zspin.slo import SLOEngine


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
