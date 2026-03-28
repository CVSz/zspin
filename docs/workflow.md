# zspin Workflow Diagram

```mermaid
flowchart TD
    A[Load Config] --> B[Diagnostics]
    B --> C[Compliance Evaluation]
    C --> D{Dry Run?}
    D -- Yes --> E[Print Summary]
    D -- No --> F[Generate Audit Report]
    F --> G[Generate SBOM]
    G --> E
```

## Stepwise diagnostics

1. Platform identity check.
2. Required toolchain availability check (`git`, `python3`).
3. Compliance control state evaluation.
4. Audit + SBOM artifact output.
