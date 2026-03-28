# Enterprise Blueprint Assets

This folder contains implementation starter assets for a production-grade platform:

- `kafka/docker-compose.kafka.yml`: local Kafka + Zookeeper stack.
- `sql/double_entry.sql`: double-entry schema with balancing constraints.
- `terraform/main.tf`: AWS infrastructure baseline scaffold.
- `figma/design_tokens.json`: design tokens suitable for code + design sync.
- `observability/*`: OpenTelemetry + Prometheus + Loki + Tempo + Grafana local stack templates.
- `chaos/*`: Chaos Mesh experiments for pod kill, latency injection, and Kafka connectivity failure.
- `mlops/*`: Airflow retraining DAG and MLflow tracking examples.

## Suggested rollout order

1. Bring up local Kafka and verify producer/consumer loops.
2. Apply SQL schema and build accounting posting service with idempotency.
3. Wire tokens into frontend theme config and Figma token plugin.
4. Expand Terraform module scaffold for environment-specific deployments.

5. Stand up observability stack and verify logs/metrics/traces landing in Grafana.
6. Run chaos experiments with blast-radius limits and SLO monitoring.
7. Wire retraining DAG + MLflow registry before enabling canary model deploys.
