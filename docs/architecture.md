# zspin Architecture Notes

## Goals

- Deterministic workflow execution
- Reproducible artifact generation
- Security and compliance by default
- Modular services for extension

## Modules

1. `config.py`: deterministic config loading
2. `diagnostics.py`: host/tooling readiness checks
3. `compliance.py`: policy controls and statuses
4. `audit.py`: structured JSON compliance report generation
5. `sbom.py`: CycloneDX-style SBOM output
6. `installer.py`: orchestration and autoheal boundary point
7. `cli.py`: user/operator interface

## Data Flow

```text
config.json -> load_config -> run_diagnostics + evaluate_controls
           -> write_audit_report + generate_sbom
           -> print deterministic summary
```
