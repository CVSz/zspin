from __future__ import annotations

import json

try:
    from kafka import KafkaProducer
except ImportError:  # pragma: no cover - optional dependency
    KafkaProducer = None  # type: ignore[assignment]


class _NoopProducer:
    def send(self, topic: str, data: dict[str, object]) -> None:
        _ = (topic, data)


def _build_producer() -> KafkaProducer | _NoopProducer:
    if KafkaProducer is None:
        return _NoopProducer()

    return KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


producer = _build_producer()


def publish_event(topic: str, data: dict[str, object]) -> None:
    producer.send(topic, data)
