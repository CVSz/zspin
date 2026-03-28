import json

from zspin.scaling import ScalingPlanner, ServiceMetrics, generate_scaling_bundle


def test_scaling_planner_generates_bounded_target_replicas() -> None:
    planner = ScalingPlanner()
    decision = planner.plan(
        ServiceMetrics(
            service="api",
            current_replicas=3,
            cpu_per_replica=0.3,
            memory_per_replica_gb=0.4,
            historical_rps=[100, 120, 140, 180],
            p95_latency_ms=100,
        )
    )

    assert decision.target_replicas >= 2
    assert decision.target_replicas <= 50
    assert decision.hpa["kind"] == "HorizontalPodAutoscaler"
    assert decision.canary["steps"][-1]["setWeight"] == 100


def test_generate_scaling_bundle_writes_report(tmp_path) -> None:
    input_file = tmp_path / "scaling-input.json"
    output_file = tmp_path / "scaling-plan.json"
    input_file.write_text(
        json.dumps(
            {
                "services": [
                    {
                        "service": "billing",
                        "current_replicas": 2,
                        "cpu_per_replica": 0.2,
                        "memory_per_replica_gb": 0.3,
                        "historical_rps": [20, 30, 40],
                        "p95_latency_ms": 150,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    report = generate_scaling_bundle(input_file, output_file)

    assert report["metadata"]["deterministic"] is True
    assert len(report["decisions"]) == 1
    assert output_file.exists()
