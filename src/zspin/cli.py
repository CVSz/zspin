from __future__ import annotations

import argparse
import json

from .config import load_config
from .finops import FinOpsEngine
from .installer import run_workflow
from .platform.deploy import deploy
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
        service = Service(args.name, "api")
        print("Deploy:", deploy(service))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
