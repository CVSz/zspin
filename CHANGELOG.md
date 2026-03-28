
## Unreleased

- Added `docs/platform_kernel_blueprint.md` with an integrated 2026 operating blueprint covering data lake + ML, regulatory reporting, Customer 360, internal tools governance, real-time inference guardrails, and CQRS/event-sourcing migration phases.
- Added a buildable `examples/betting-platform-mvp` full-stack scaffold with NestJS backend, Socket.IO real-time events, Next.js frontend dashboard, React admin panel, and Docker Compose wiring.
- Added deterministic scaling-planner source code (`src/zspin/scaling.py`) with autoscaling, canary rollout, and multi-region planning outputs plus CLI/report generation support.

# Changelog

## 0.1.0 - 2026-03-28

- Initial zspin baseline with deterministic CLI workflow.
- Added diagnostics, compliance checks, audit report generation, and SBOM output.
- Added validation and release packaging scripts.
