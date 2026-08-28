"""Validate the container, GPU, pinned imports, and external mounts."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import os
import platform
from pathlib import Path


IMPORTS = {
    "carla": "carla",
    "cv2": "opencv-python",
    "matplotlib": "matplotlib",
    "numpy": "numpy",
    "omegaconf": "omegaconf",
    "pandas": "pandas",
    "pyarrow": "pyarrow",
    "torch": "torch",
    "torchvision": "torchvision",
    "yaml": "PyYAML",
}

REQUIRED_PATHS = (
    "CARLA_ROOT",
    "CARLA_GARAGE_ROOT",
    "TRANSFUSERPP_CHECKPOINT",
    "EXPERIMENT_OUTPUT_ROOT",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="return non-zero on any failure")
    args = parser.parse_args()

    failures: list[str] = []
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")

    for module_name, distribution_name in IMPORTS.items():
        try:
            importlib.import_module(module_name)
            version = importlib.metadata.version(distribution_name)
            print(f"[OK] {module_name}: {version}")
        except Exception as error:  # import failures can include missing shared libraries
            message = f"[FAIL] {module_name}: {error}"
            print(message)
            failures.append(message)

    try:
        import torch

        if torch.cuda.is_available():
            print(f"[OK] CUDA device: {torch.cuda.get_device_name(0)}")
            print(f"[OK] torch CUDA runtime: {torch.version.cuda}")
        else:
            message = "[FAIL] torch.cuda.is_available() is False"
            print(message)
            failures.append(message)
    except Exception as error:
        failures.append(f"[FAIL] CUDA check: {error}")

    for key in REQUIRED_PATHS:
        value = os.environ.get(key)
        if not value:
            message = f"[FAIL] {key}: not set"
        elif not Path(value).exists():
            message = f"[FAIL] {key}: path does not exist: {value}"
        else:
            print(f"[OK] {key}: {value}")
            continue
        print(message)
        failures.append(message)

    print(f"Failures: {len(failures)}")
    return 1 if args.strict and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

