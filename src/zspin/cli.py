from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass

from .config import load_config
from .installer import run_workflow


@dataclass(frozen=True)
class DeployService:
    name: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="zspin", description="zspin automation CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run workflow")
    run_cmd.add_argument("--config", type=str, default=None, help="Path to JSON config")
    run_cmd.add_argument("--dry-run", action="store_true", help="Skip artifact generation")

    deploy_cmd = sub.add_parser("deploy-service", help="Deploy a service using Kubernetes runtime")
    deploy_cmd.add_argument("name", type=str, help="Service name (manifest expected at k8s/<name>.yaml)")

    scale_cmd = sub.add_parser("scale-service", help="Scale a Kubernetes deployment")
    scale_cmd.add_argument("name", type=str, help="Deployment/service name")
    scale_cmd.add_argument("replicas", type=int, help="Replica count")

    sub.add_parser("gitops-apply", help="Apply ArgoCD application manifest")

    alert_cmd = sub.add_parser("simulate-alert", help="Simulate an alert and trigger auto-healing")
    alert_cmd.add_argument("alert_name", type=str, help="Alert name (e.g. HighCPU, ServiceDown)")

    metrics_cmd = sub.add_parser("start-metrics", help="Start Prometheus metrics endpoint")
    metrics_cmd.add_argument("--port", type=int, default=8000, help="Metrics bind port")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        config = load_config(args.config)
        summary = run_workflow(config=config, dry_run=args.dry_run)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    if args.command == "deploy-service":
        from .platform.runtime import Runtime

        runtime = Runtime()
        result = runtime.deploy(DeployService(args.name))
        print("Deploy:", result)
        return 0

    if args.command == "scale-service":
        from .platform.runtime import Runtime

        runtime = Runtime()
        result = runtime.scale(DeployService(args.name), args.replicas)
        print("Scale:", result)
        return 0

    if args.command == "gitops-apply":
        from .platform.gitops import apply_gitops

        result = apply_gitops()
        print("GitOps applied:", result)
        return 0

    if args.command == "simulate-alert":
        from .observability.alerts import AlertHandler

        handler = AlertHandler()
        alert = {"alert": args.alert_name}
        result = handler.handle(alert)
        print("Auto-healing result:", json.dumps(result, sort_keys=True))
        return 0

    if args.command == "start-metrics":
        from .observability.metrics import start_metrics_server

        start_metrics_server(port=args.port)
        print(f"Metrics server running on :{args.port}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
