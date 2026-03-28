# zspin

`zspin` is a compliance-ready automation starter kit (2026-oriented) focused on deterministic operations, reproducible releases, and security-first diagnostics.

## Highlights

- Deterministic config loading + execution plans
- Structured JSON logging and metadata extraction
- Stepwise diagnostics for host/container/cloud preflight checks
- Compliance validation hooks (GDPR, ISO-style controls, Zero Trust posture)
- Reproducible release packaging and SBOM generation
- CI-ready validation scripts

## Architecture (high-level)

```text
CLI (src/zspin/cli.py)
  -> Installer Workflow (src/zspin/installer.py)
  -> Diagnostics Engine (src/zspin/diagnostics.py)
  -> Compliance Engine (src/zspin/compliance.py)
  -> Audit Reporter (src/zspin/audit.py)
  -> SBOM Generator (src/zspin/sbom.py)

Artifacts:
  reports/*.json
  dist/zspin-<version>.zip
```

See full notes in `docs/architecture.md` and `docs/workflow.md`.


## New example: full-stack betting MVP

A buildable monorepo example (NestJS + Next.js + React admin + WebSocket wiring) is available at `examples/betting-platform-mvp/`.


## Enterprise blueprint add-on

For the production-grade backend/design/infrastructure blueprint (Kafka, double-entry accounting, Terraform scaffold, and design tokens), see `docs/enterprise_platform_blueprint.md` and `examples/enterprise-blueprint/`.

For the next-layer operating model (data lake/ML, regulatory reporting, Customer 360, real-time ML controls, CQRS evolution), see `docs/platform_kernel_blueprint.md`.

For a dedicated reliability + intelligence runbook (observability, chaos engineering, and MLOps lifecycle), see `docs/reliability_intelligence_backbone.md` and the corresponding assets under `examples/enterprise-blueprint/{observability,chaos,mlops}`.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Run installer workflow (dry-run)

```bash
zspin run --config examples/config.json --dry-run
```

### Run full validation bundle

```bash
python scripts/validate.py
```

### Build reproducible release artifact

```bash
bash scripts/build_release.sh
```

### Generate scaling feature bundle (autoscaling + canary + multi-region)

```bash
zspin scaling-plan --input examples/scaling_input.json --output reports/scaling_plan.json
```

## Pseudo-code workflow

```text
LOAD config deterministically
VALIDATE required controls
FOR each stage in [diagnostics, hardening, compliance, reporting, packaging]:
  EXECUTE stage with strict error boundaries
  WRITE structured logs + metadata
  IF failure AND autoheal enabled:
    RUN bounded remediation
    RETRY stage once
  IF failure persists:
    GENERATE rollback plan
    EXIT non-zero
EMIT audit report + SBOM + checksums
```

## Security checklist

- Input validation for all external config and CLI arguments
- No shell interpolation from untrusted input
- Explicit timeout and failure semantics for commands
- Data minimization in reports (no secrets, no PII dumps)
- Immutable audit timestamps + host metadata
- Dependency manifest and SBOM output

## Deliverables mapping

1. **Code implementation**: `src/zspin/*`
2. **Documentation**: `README.md`, `docs/*`
3. **Release artifacts**: `CHANGELOG.md`, `VERSION`, `dist/*.zip`
4. **Validation scripts**: `scripts/validate.py`
5. **Diagram/workflow**: `docs/workflow.md`
6. **Audit report**: `reports/audit_report.json` (generated)
7. **Security checklist**: this README section + compliance module controls

## License

MIT (see `LICENSE`).

# 🚀 Scaling Features

## Autoscaling
- HPA based on CPU

## Canary Deployments
- Argo Rollouts

## Observability
- Prometheus + Grafana

## Multi-region
- Node labeling strategy

## Cloudflare Tunnel
- Secure public access without exposing ingress
