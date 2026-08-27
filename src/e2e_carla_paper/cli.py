"""Small command-line entry points that do not require vendored CARLA code."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


REQUIRED_PATHS = (
    "CARLA_ROOT",
    "CARLA_GARAGE_ROOT",
    "TRANSFUSERPP_CHECKPOINT",
    "EXPERIMENT_OUTPUT_ROOT",
)


def check_environment() -> int:
    failures: list[str] = []
    for key in REQUIRED_PATHS:
        raw_value = os.environ.get(key)
        if not raw_value:
            failures.append(f"{key}: not set")
            continue
        path = Path(raw_value).expanduser()
        if key == "EXPERIMENT_OUTPUT_ROOT":
            if not path.parent.exists():
                failures.append(f"{key}: parent directory does not exist: {path.parent}")
        elif not path.exists():
            failures.append(f"{key}: path does not exist: {path}")

    if failures:
        print("Environment check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Environment paths are configured.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="e2e-carla-paper")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check-env", help="validate required external paths")
    args = parser.parse_args()

    if args.command == "check-env":
        return check_environment()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

