# Enterprise Platform Blueprint (2026)

This guide turns the architecture plan into a practical, buildable baseline for a regulated betting/fintech-style SaaS stack.

## 1) Event Streaming Backbone (Kafka)

### Target topology

```text
API Gateway -> Producer Services -> Kafka Topics -> Consumer Services
```

Topics:

- `bet.events`
- `wallet.events`
- `payment.events`
- `risk.events`
- `notification.events`
- `*.dlq` (dead-letter queue per domain)

### Non-negotiable controls

1. Idempotency key per command/event (`x-idempotency-key` at API edge).
2. At-least-once handling + idempotent consumers.
3. DLQ with retry budget and alerting.
4. Trace context propagation (`trace_id`, `span_id`, `tenant_id`).
5. Schema contracts (Avro/JSON schema + compatibility gate in CI).

### Reference assets

- Local dev compose: `examples/enterprise-blueprint/kafka/docker-compose.kafka.yml`

## 2) Financial Core (Double-entry accounting)

### Core invariant

> For every transaction: total debits == total credits.

### Recommended tables

- `accounts`
- `transactions`
- `entries`
- `idempotency_keys`

Schema reference: `examples/enterprise-blueprint/sql/double_entry.sql`.

### Runtime safeguards

1. All postings happen inside a single DB transaction.
2. Reject unbalanced postings at service and database layer.
3. Unique business reference (`reference`) per external event.
4. Immutable entries (reverse with compensating transaction, never mutate).

## 3) Design Tokens + Design Ops

Token source-of-truth should live in version control and sync into Figma + frontend build configs.

- Token seed file: `examples/enterprise-blueprint/figma/design_tokens.json`
- Includes colors, spacing, typography, radius, and button variants.

## 4) Global reliability and deployments

### Multi-region model

- Region-local stateless services.
- Strong consistency zone for wallet/payments.
- Regional Kafka + optional inter-region mirroring.
- Route53 latency routing + health checks.

### Release strategy

- Blue/green with instant rollback.
- Backward-compatible migrations only.
- Progressive canary percentages for risky changes.

### IaC reference

- Terraform baseline scaffold: `examples/enterprise-blueprint/terraform/main.tf`

## 5) Compliance and observability

Required for production readiness:

1. KYC/AML workflow states + immutable audit trail.
2. Structured logs with sensitive-field redaction.
3. SIEM-friendly event feed.
4. SBOM generation and vulnerability scan in CI.
5. Automated policy checks before deployment.

## Delivery checklist

- [ ] Kafka cluster up locally and topic bootstrap scripted.
- [ ] Double-entry posting service passing invariants tests.
- [ ] Design tokens synced to UI + Figma workflow.
- [ ] Terraform validated with `terraform fmt/validate`.
- [ ] CI gates: tests + SBOM + vuln scans + policy checks.
