from __future__ import annotations

import argparse
import json

from .config import load_config
from .installer import run_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="zspin", description="zspin automation CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run workflow")
    run_cmd.add_argument("--config", type=str, default=None, help="Path to JSON config")
    run_cmd.add_argument("--dry-run", action="store_true", help="Skip artifact generation")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        config = load_config(args.config)
        summary = run_workflow(config=config, dry_run=args.dry_run)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
