from __future__ import annotations

import argparse
import json

from .config import load_config
from .finops import FinOpsEngine
from .installer import run_workflow
from .platform.services import Service


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="zspin", description="zspin automation CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run workflow")
    run_cmd.add_argument("--config", type=str, default=None, help="Path to JSON config")
    run_cmd.add_argument("--dry-run", action="store_true", help="Skip artifact generation")

    sub.add_parser("cost", help="Analyze resource costs and optimization opportunities")

    create_cmd = sub.add_parser("create-service", help="Create a service descriptor")
    create_cmd.add_argument("name", type=str)
    create_cmd.add_argument("service_type", type=str)

    deploy_cmd = sub.add_parser("deploy-service", help="Deploy a service descriptor")
    deploy_cmd.add_argument("name", type=str)

    sub.add_parser("gitops-apply", help="Apply GitOps Argo CD application")

    alert_cmd = sub.add_parser("simulate-alert", help="Simulate an alert to trigger remediation")
    alert_cmd.add_argument("alert_name", type=str)

    sub.add_parser("start-metrics", help="Start Prometheus metrics endpoint")

    sub.add_parser("start-api", help="Start control plane API")

    deploy_multi_cmd = sub.add_parser("deploy-multi", help="Deploy service in multi-tenant mode")
    deploy_multi_cmd.add_argument("name", type=str)
    deploy_multi_cmd.add_argument("tenant", type=str)

    token_cmd = sub.add_parser("gen-token", help="Generate JWT token")
    token_cmd.add_argument("user", type=str)
    token_cmd.add_argument("tenant", type=str)

    return parser


def _run_cost() -> int:
    engine = FinOpsEngine()
    resources = [{"name": "api", "cpu": 2, "uptime": 5000, "cost_per_hour": 0.2}]

    report = engine.analyze(resources)
    total = engine.estimate_cost(resources)

    print("Cost Report:", report)
    print("Total Cost:", total)
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        config = load_config(args.config)
        summary = run_workflow(config=config, dry_run=args.dry_run)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    if args.command == "cost":
        return _run_cost()

    if args.command == "create-service":
        service = Service(args.name, args.service_type)
        print("Created:", service.to_dict())
        return 0

    if args.command == "deploy-service":
        from .platform.runtime import Runtime

        service = Service(args.name, "api")
        runtime = Runtime()
        print("Deploy:", runtime.deploy(service))
        return 0

    if args.command == "gitops-apply":
        from .platform.gitops import apply_gitops

        print("GitOps applied:", apply_gitops())
        return 0

    if args.command == "simulate-alert":
        from .observability.alerts import AlertHandler

        handler = AlertHandler()
        alert = {"alert": args.alert_name}
        print("Auto-healing result:", handler.handle(alert))
        return 0

    if args.command == "start-metrics":
        from .observability.metrics import start_metrics_server

        start_metrics_server()
        print("Metrics server running on :8000")
        return 0

    if args.command == "start-api":
        import uvicorn

        from .control_plane.api import app as cp_app

        uvicorn.run(cp_app, host="0.0.0.0", port=8080)
        return 0

    if args.command == "deploy-multi":
        from .control_plane.manager import ControlPlane
        from .multicluster import MultiClusterScheduler

        cp = ControlPlane()
        scheduler = MultiClusterScheduler()
        cluster = scheduler.select_cluster({"name": args.name}, cp.clusters)
        result = cp.deploy({"name": args.name}, args.tenant, cluster)
        print(result)
        return 0

    if args.command == "gen-token":
        from .auth import create_token

        token = create_token(args.user, args.tenant)
        print("JWT:", token)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
