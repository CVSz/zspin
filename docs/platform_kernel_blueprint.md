# Platform Kernel Blueprint (2026)

This blueprint extends the existing enterprise foundation (`docs/enterprise_platform_blueprint.md`) into an integrated operating model for a data company, regulated operator, and customer-centric SaaS business.

## 1) Strategic target state

```text
Data Platform + Regulated Reporting + Customer Operations
  -> unified intelligence + controlled automation
```

Outcomes:

- One event backbone for product, finance, risk, support, and AI workloads.
- Audit-ready exports and regulator-facing reporting.
- Customer 360 views with real-time and batch intelligence.
- Human-in-the-loop controls for high-impact AI decisions.

## 2) Data lake and ML platform

### 2.1 End-to-end flow

```text
App Services -> Kafka Topics -> Ingestion -> S3 Data Lake
  -> Batch/Stream Processing -> Warehouse/Feature Store
  -> Model Training/Inference -> Product + Ops APIs
```

Recommended Kafka topics:

- `bet.events`
- `user.events`
- `payment.events`
- `support.events`
- `risk.events`

### 2.2 Lake zones and object layout

```text
s3://data-lake/
  raw/{domain}/yyyy/mm/dd/
  processed/{dataset}/run_date=
  features/{feature_set}/version=
  models/{model_name}/version=
```

Rules:

1. Never overwrite raw events.
2. Partition by domain and event date.
3. Track schema versions and producer version in metadata.
4. Encrypt at rest and enforce least-privilege IAM.

### 2.3 Processing and feature engineering

Use Glue/Spark for batch transforms and Flink/Kafka Streams for low-latency transformations.

Core feature groups:

- Behavioral: session length, recency/frequency metrics, stake volatility.
- Financial: deposits, withdrawals, net position, payment cadence.
- Risk: unusual velocity, anomaly counts, sanctions/KYC flags.
- Support: ticket frequency, dispute rate, SLA breach markers.

### 2.4 Model lifecycle controls

```text
Dataset versioning -> Training -> Evaluation -> Registry -> Deployment -> Monitoring
```

Guardrails:

- Approval gate for models affecting wallet, account access, or compliance decisions.
- Drift + performance monitors with rollback capability.
- Immutable inference logs (`features`, `model_version`, `score`, `decision`).

## 3) Regulatory reporting system

### 3.1 Reporting architecture

```text
Ledger + Event Store + KYC/AML Signals
  -> Reporting Engine
  -> CSV/PDF/API Exports
  -> Signed + timestamped archive
```

Core report families:

- Financial: deposits/withdrawals/revenue/house P&L.
- User: KYC state transitions, account activity, risk annotations.
- Compliance: suspicious activity, AML triggers, threshold breaches.

### 3.2 Data model and run management

Minimum metadata table:

```sql
reports(
  id,
  report_type,
  period_start,
  period_end,
  generated_at,
  generated_by,
  checksum,
  file_url,
  signature,
  status
)
```

Operational requirements:

1. Deterministic report generation with pinned query versions.
2. Hash and sign all generated files.
3. Maintain retention + legal-hold policy by jurisdiction.
4. Store export request + access log for every download.

## 4) Customer support and dispute operations

### 4.1 Core entities

- `tickets(id, user_id, status, priority, category, created_at, updated_at)`
- `messages(id, ticket_id, sender_type, body, created_at)`
- `sla_events(id, ticket_id, state, due_at, breached_at)`

### 4.2 Operating model

```text
User ticket -> triage -> agent handling -> resolution -> CSAT feedback
```

Automation targets:

- Auto-tagging and queue routing.
- Priority escalation for payment/risk/KYC categories.
- SLA timers with breach alerts.

## 5) Customer 360 system

### 5.1 Unified profile contract

The read model should aggregate:

- Identity + compliance profile.
- Financial summaries (LTV, inflow/outflow, balance history).
- Behavioral telemetry.
- Risk scores and active flags.
- Support timeline and unresolved issues.
- ML predictions (churn, fraud propensity, recommendation action).

### 5.2 Serving path

```text
Services + projections + feature store
  -> Customer 360 API
  -> Admin/UI + internal tooling
```

Implementation guidance:

- Build as a read-optimized view, not a write source of truth.
- Use asynchronous projection updates with freshness indicators.
- Return `as_of` timestamps for every section.

## 6) Real-time ML inference and autonomous actions

### 6.1 Streaming path

```text
Live event -> feature lookup -> model scoring -> decision policy -> action topic
```

Decision examples:

- `BLOCK_OR_REVIEW`
- `LIMIT_ACCOUNT`
- `TRIGGER_RETENTION_OFFER`
- `ESCALATE_TO_AGENT`

### 6.2 Safety policy

1. High-impact actions require confidence + policy threshold checks.
2. Ambiguous/high-risk decisions route to human review.
3. Every action must be reversible with an incident workflow.
4. Maintain per-decision explainability fields for audit.

## 7) Internal tools platform

### 7.1 Core modules

- User management console.
- Transaction and ledger explorer.
- Risk operations console.
- Support workspace.
- Controlled query studio (read-only by default).

### 7.2 Security and governance

- RBAC/ABAC with least privilege.
- Mandatory action auditing (`who`, `what`, `when`, `why`).
- Break-glass access workflow with expiry and approval.
- PII redaction by role and purpose.

## 8) Event sourcing + CQRS evolution plan

```text
Command API -> Command handler -> Event store -> Kafka
                                     -> Projection services -> Query/read models
```

Phased adoption:

1. Start with wallet/payments/risk domains where auditability is critical.
2. Keep dual-write transition window with strict reconciliation.
3. Add snapshots and replay tooling for performance and recovery.

## 9) Delivery roadmap (phased)

### Phase A: Foundation hardening (2–4 weeks)

- Topic taxonomy, schema governance, DLQ policy.
- Data lake zones and ingestion contracts.
- Baseline compliance report engine.

### Phase B: Customer intelligence (4–8 weeks)

- Customer 360 read model + admin view.
- Batch fraud/churn pipelines + model registry.
- Support triage automation and SLA management.

### Phase C: Real-time intelligence (6–10 weeks)

- Streaming inference service and risk action policies.
- Human-in-the-loop AI control panel.
- Drift monitoring and automated rollback playbooks.

### Phase D: Core architecture shift (ongoing)

- CQRS/event sourcing for critical bounded contexts.
- Cross-domain lineage, data catalog, and governance expansion.

## 10) Non-negotiable controls checklist

- [ ] Immutable event and audit logs.
- [ ] Double-entry invariants enforced for monetary flows.
- [ ] Signed compliance exports with retention policy.
- [ ] RBAC/ABAC + detailed internal tool auditing.
- [ ] AI decision guardrails + override workflows.
- [ ] Model/version lineage and reproducible training metadata.
- [ ] End-to-end observability (logs, metrics, traces, SLOs).
