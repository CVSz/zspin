from __future__ import annotations

from prometheus_client import Counter, start_http_server

REQUEST_COUNT = Counter("zspin_requests_total", "Total requests")


def start_metrics_server(port: int = 8000) -> None:
    start_http_server(port)


def track_request() -> None:
    REQUEST_COUNT.inc()
