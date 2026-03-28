#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    severity: str
    category: str
    message: str
    file: str
    line: int
    recommendation: str


def iter_python_files(repo_root: Path) -> Iterable[Path]:
    for path in sorted((repo_root / "src").rglob("*.py")):
        yield path
    for path in sorted((repo_root / "scripts").glob("*.py")):
        yield path
    for path in sorted((repo_root / "tests").rglob("*.py")):
        yield path


def find_dangerous_patterns(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []

    for path in iter_python_files(repo_root):
        rel = path.relative_to(repo_root).as_posix()
        source = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            findings.append(
                Finding(
                    severity="high",
                    category="quality",
                    message=f"Syntax error prevents static audit parsing: {exc.msg}",
                    file=rel,
                    line=exc.lineno or 1,
                    recommendation="Fix syntax issues before release validation.",
                )
            )
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name in {"eval", "exec"}:
                    findings.append(
                        Finding(
                            severity="critical",
                            category="security",
                            message=f"Potentially unsafe dynamic execution via {func_name}().",
                            file=rel,
                            line=node.lineno,
                            recommendation="Replace with explicit parsing/dispatch tables.",
                        )
                    )

                if func_name == "run":
                    for kw in node.keywords:
                        if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                            findings.append(
                                Finding(
                                    severity="high",
                                    category="security",
                                    message="subprocess.run(..., shell=True) detected.",
                                    file=rel,
                                    line=node.lineno,
                                    recommendation="Use list-style arguments and shell=False.",
                                )
                            )

    return sorted(findings, key=lambda f: (f.severity, f.file, f.line))


def gather_inventory(repo_root: Path) -> dict[str, object]:
    tests = sorted((repo_root / "tests").rglob("test_*.py")) if (repo_root / "tests").exists() else []
    docs = sorted((repo_root / "docs").glob("*.md")) if (repo_root / "docs").exists() else []

    return {
        "python_modules": len(list((repo_root / "src").rglob("*.py"))),
        "test_files": len(tests),
        "documentation_files": len(docs),
        "kubernetes_manifests": len(list((repo_root / "k8s").glob("*.yaml"))),
        "helm_templates": len(list((repo_root / "helm").rglob("*.yaml"))),
        "examples": len(list((repo_root / "examples").rglob("*"))),
    }


def compliance_matrix(repo_root: Path) -> dict[str, dict[str, object]]:
    checks = {
        "structured_logging": repo_root / "src/zspin/logging_utils.py",
        "sbom_generation": repo_root / "src/zspin/sbom.py",
        "compliance_controls": repo_root / "src/zspin/compliance.py",
        "audit_reporting": repo_root / "src/zspin/audit.py",
        "reproducible_release": repo_root / "scripts/build_release.sh",
        "validation_bundle": repo_root / "scripts/validate.py",
        "workflow_documentation": repo_root / "docs/workflow.md",
        "architecture_documentation": repo_root / "docs/architecture.md",
    }

    matrix: dict[str, dict[str, object]] = {}
    for control, path in checks.items():
        matrix[control] = {
            "status": "pass" if path.exists() else "fail",
            "evidence": path.relative_to(repo_root).as_posix(),
        }
    return matrix


def compute_score(findings: list[Finding], matrix: dict[str, dict[str, object]]) -> int:
    score = 100
    penalty = {"critical": 20, "high": 10, "medium": 5, "low": 2}
    for finding in findings:
        score -= penalty.get(finding.severity, 1)

    missing_controls = sum(1 for item in matrix.values() if item["status"] == "fail")
    score -= missing_controls * 8
    return max(score, 0)


def build_report(repo_root: Path, generated_at: str | None = None) -> dict[str, object]:
    findings = find_dangerous_patterns(repo_root)
    matrix = compliance_matrix(repo_root)
    inventory = gather_inventory(repo_root)
    score = compute_score(findings, matrix)

    return {
        "metadata": {
            "project": repo_root.name,
            "generated_at": generated_at
            or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "audit_type": "master-meta-deep-audit",
            "standard_profile": [
                "ISO/IEC-2026-ready",
                "GDPR-update-ready",
                "Zero-Trust-aligned",
                "SBOM-required",
            ],
        },
        "pseudo_workflow": [
            "DISCOVER repository inventory and execution surfaces",
            "VALIDATE compliance control evidence",
            "ANALYZE code patterns for deterministic and security risks",
            "SCORE maturity and enumerate remediation backlog",
            "EMIT machine-readable and human-readable reports",
        ],
        "inventory": inventory,
        "compliance_matrix": matrix,
        "findings": [asdict(item) for item in findings],
        "summary": {
            "score": score,
            "status": "pass" if score >= 80 else "needs-attention",
            "finding_count": len(findings),
            "critical_findings": sum(1 for f in findings if f.severity == "critical"),
            "high_findings": sum(1 for f in findings if f.severity == "high"),
        },
    }


def render_markdown(report: dict[str, object]) -> str:
    summary = report["summary"]
    metadata = report["metadata"]
    lines: list[str] = [
        "# Master Meta Deep Audit Report",
        "",
        f"- **Project**: `{metadata['project']}`",
        f"- **Generated at**: `{metadata['generated_at']}`",
        f"- **Score**: `{summary['score']}/100`",
        f"- **Status**: `{summary['status']}`",
        "",
        "## Compliance Matrix",
        "",
        "| Control | Status | Evidence |",
        "|---|---|---|",
    ]

    matrix = report["compliance_matrix"]
    for control, values in matrix.items():
        lines.append(f"| `{control}` | `{values['status']}` | `{values['evidence']}` |")

    lines.extend(["", "## Findings", ""])
    findings: list[dict[str, object]] = report["findings"]
    if not findings:
        lines.append("No static red flags detected in the scanned code paths.")
    else:
        for item in findings:
            lines.extend(
                [
                    f"- **{item['severity'].upper()}** `{item['category']}` {item['message']}",
                    f"  - Evidence: `{item['file']}:{item['line']}`",
                    f"  - Recommendation: {item['recommendation']}",
                ]
            )

    lines.extend(
        [
            "",
            "## Next Actions",
            "",
            "1. Address all high/critical findings with deterministic fixes and tests.",
            "2. Integrate this audit in CI/CD before release packaging.",
            "3. Keep SBOM and compliance reports as release artifacts for traceability.",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Master Meta deep audit for zspin repository")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--json-output", default="reports/master_meta_audit.json", help="JSON output path")
    parser.add_argument("--md-output", default="reports/master_meta_audit.md", help="Markdown output path")
    parser.add_argument(
        "--generated-at",
        default=None,
        help="Override RFC3339 timestamp for deterministic report generation",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root, generated_at=args.generated_at)

    json_path = Path(args.json_output)
    md_path = Path(args.md_output)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)

    json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")

    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
