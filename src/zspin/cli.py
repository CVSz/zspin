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

    scale_cmd = sub.add_parser("scaling-plan", help="Generate deterministic scaling plan bundle")
    scale_cmd.add_argument("--input", required=True, help="Path to scaling input JSON")
    scale_cmd.add_argument("--output", default="reports/scaling_plan.json", help="Output report path")

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
    sub.add_parser("start-control-plane", help="Start lightweight custom control plane API")
    sub.add_parser("run-operator", help="Run custom control plane operator reconcile loop")
    sub.add_parser("run-distributed", help="Run distributed control plane loop")

    grpc_raft_cmd = sub.add_parser("run-raft-grpc", help="Run Raft node with gRPC service")
    grpc_raft_cmd.add_argument("node_id", type=str)
    grpc_raft_cmd.add_argument("port", type=int)

    deploy_multi_cmd = sub.add_parser("deploy-multi", help="Deploy service in multi-tenant mode")
    deploy_multi_cmd.add_argument("name", type=str)
    deploy_multi_cmd.add_argument("tenant", type=str)

    token_cmd = sub.add_parser("gen-token", help="Generate JWT token")
    token_cmd.add_argument("user", type=str)
    token_cmd.add_argument("tenant", type=str)

    api_key_cmd = sub.add_parser("gen-apikey", help="Generate tenant API key")
    api_key_cmd.add_argument("tenant", type=str)

    raft_cmd = sub.add_parser("run-raft", help="Run a local Raft node")
    raft_cmd.add_argument("node_id", type=str)
    raft_cmd.add_argument("--peers", nargs="*", default=[], help="Peer IDs in local cluster")

    db_cmd = sub.add_parser("run-db", help="Run distributed DB shell on top of Raft")
    db_cmd.add_argument("node_id", type=str)

    master_meta_cmd = sub.add_parser(
        "master-meta", help="Generate full implementation bundle (audit + release + validation)"
    )
    master_meta_cmd.add_argument("--config", default=None, help="Path to workflow config JSON")
    master_meta_cmd.add_argument(
        "--output-dir",
        default="reports/master_meta",
        help="Directory to store generated reports and reproducibility metadata",
    )
    master_meta_cmd.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip release artifact generation and perform analysis/reporting only",
    )
    go_live_cmd = sub.add_parser(
        "go-live-installer",
        help="Generate full source-code go-live installer bundle",
    )
    go_live_cmd.add_argument("--config", default=None, help="Path to workflow config JSON")
    go_live_cmd.add_argument(
        "--output-dir",
        default="dist/go_live_installer",
        help="Directory to store installer scripts, source snapshot, and reports",
    )
    go_live_cmd.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip heavy release packaging in nested master-meta bundle",
    )

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

    if args.command == "scaling-plan":
        from .scaling import generate_scaling_bundle

        report = generate_scaling_bundle(args.input, args.output)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

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

    if args.command == "start-control-plane":
        import uvicorn

        from .apiserver import app as cp_custom_app

        uvicorn.run(cp_custom_app, host="0.0.0.0", port=8081)
        return 0

    if args.command == "run-operator":
        from .apiserver import store
        from .control_loop import run_operator_loop
        from .operator import Operator
        from .platform.runtime import Runtime

        op = Operator(store, Runtime())
        run_operator_loop(op)
        return 0

    if args.command == "run-distributed":
        from .controller import Controller
        from .distributed_loop import DistributedLoop
        from .etcd import KVStore
        from .leader import LeaderElection

        store = KVStore()
        store.put("service-a", {"replicas": 1})

        def reconcile(key: str, val: object) -> None:
            print(f"[reconcile] {key} -> {val}")

        controller = Controller(store, reconcile)
        leader = LeaderElection()

        loop = DistributedLoop(leader, controller)
        loop.run()
        return 0

    if args.command == "run-raft-grpc":
        import threading

        from .raft.node import RaftNode
        from .raft.server import serve

        peers: list[str] = []
        node = RaftNode(args.node_id, peers)

        threading.Thread(target=node.run, daemon=True).start()
        serve(node, args.port)
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

    if args.command == "gen-apikey":
        from .apikeys import generate_key

        key = generate_key(args.tenant)
        print("API KEY:", key)
        return 0

    if args.command == "run-raft":
        from .raft.cluster import LocalCluster
        from .raft.node import RaftNode

        cluster = LocalCluster()
        node = RaftNode(args.node_id, args.peers)
        cluster.register(args.node_id, node)
        node.attach_clients(cluster.clients_for(args.peers))
        print(f"Raft node ready: id={args.node_id} peers={args.peers}")
        return 0

    if args.command == "run-db":
        from .distributed_db.engine import Database
        from .raft.node import RaftNode

        node = RaftNode(args.node_id, [])
        node.become_leader()
        db = Database(node)
        print("Distributed DB ready. Use commands: INSERT <k> <v>, SELECT <k>, DELETE <k>")

        while True:
            try:
                q = input("sql> ").strip()
            except EOFError:
                print()
                break

            if q.lower() in {"quit", "exit"}:
                break
            if not q:
                continue

            try:
                print(db.query(q))
            except Exception as exc:
                print("error:", exc)
        return 0

    if args.command == "master-meta":
        from .master_meta import run_master_meta_bundle

        config = load_config(args.config)
        bundle = run_master_meta_bundle(config=config, output_dir=args.output_dir, dry_run=args.dry_run)
        print(json.dumps(bundle, indent=2, sort_keys=True))
        return 0

    if args.command == "go-live-installer":
        from .go_live import run_go_live_installer_bundle

        config = load_config(args.config)
        bundle = run_go_live_installer_bundle(config=config, output_dir=args.output_dir, dry_run=args.dry_run)
        print(json.dumps(bundle, indent=2, sort_keys=True))
        return 0

    parser.error(f"Unhandled command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
