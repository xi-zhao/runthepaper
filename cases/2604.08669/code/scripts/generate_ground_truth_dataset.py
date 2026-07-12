#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code/src"))

from atom_path_planner import generate_ground_truth_dataset_shard  # noqa: E402


def dataset_profiles() -> dict[str, dict[str, Any]]:
    return {
        "canary": {
            "initial_side": 9,
            "target_side": 5,
            "k_neighbors": 16,
            "loading_probability": 0.75,
            "graph_backend": "kdtree",
            "workers": 1,
            "sample_count": 4,
            "seed_start": 260408690,
            "shard_id": "canary-000000",
            "output_dir": ROOT / "outputs" / "datasets" / "paper_gnn_canary" / "shard-000000",
        },
        "a100_calibration": {
            "initial_side": 33,
            "target_side": 25,
            "k_neighbors": 64,
            "loading_probability": 0.75,
            "graph_backend": "kdtree",
            "workers": 1,
            "sample_count": 1024,
            "seed_start": 260408690,
            "shard_id": "a100-calibration-000000",
            "output_dir": ROOT / "outputs" / "datasets" / "paper_gnn_a100_calibration" / "shard-000000",
        },
        "paper_target": {
            "initial_side": 127,
            "target_side": 101,
            "target_lattice_spacing": (127 - 1) / (101 - 1),
            "k_neighbors": 128,
            "loading_probability": 0.75,
            "graph_backend": "kdtree",
            "workers": 1,
            "sample_count": 1000,
            "seed_start": 260408690,
            "shard_id": "paper-target-000000",
            "output_dir": ROOT / "outputs" / "datasets" / "paper_gnn_target" / "shard-000000",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate 2604.08669 GNN ground-truth dataset shards.")
    parser.add_argument("--profile", choices=sorted(dataset_profiles()), default="canary")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--shard-id")
    parser.add_argument("--sample-count", type=int)
    parser.add_argument("--seed-start", type=int)
    parser.add_argument("--initial-side", type=int)
    parser.add_argument("--target-side", type=int)
    parser.add_argument("--target-lattice-spacing", type=float)
    parser.add_argument("--k-neighbors", type=int)
    parser.add_argument("--loading-probability", type=float)
    parser.add_argument("--graph-backend", choices=["auto", "dense", "kdtree"])
    parser.add_argument("--workers", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = dict(dataset_profiles()[args.profile])
    for key in [
        "output_dir",
        "shard_id",
        "sample_count",
        "seed_start",
        "initial_side",
        "target_side",
        "target_lattice_spacing",
        "k_neighbors",
        "loading_probability",
        "graph_backend",
        "workers",
    ]:
        value = getattr(args, key)
        if value is not None:
            config[key] = value
    config["profile"] = args.profile
    config["platform"] = platform_payload()

    if args.dry_run:
        print(json.dumps({"status": "dry_run", "config": json_ready(config)}, indent=2, sort_keys=True))
        return 0

    started = time.time()
    manifest = generate_ground_truth_dataset_shard(
        output_dir=Path(config["output_dir"]),
        shard_id=str(config["shard_id"]),
        sample_count=int(config["sample_count"]),
        initial_side=int(config["initial_side"]),
        target_side=int(config["target_side"]),
        loading_probability=float(config["loading_probability"]),
        k_neighbors=int(config["k_neighbors"]),
        seed_start=int(config["seed_start"]),
        graph_backend=str(config["graph_backend"]),
        workers=int(config["workers"]),
        target_lattice_spacing=config.get("target_lattice_spacing"),
    )
    manifest["generator_profile"] = args.profile
    manifest["platform"] = config["platform"]
    manifest["runtime"] = {"wall_time_seconds": time.time() - started}
    manifest_path = Path(manifest["manifest_path"])
    manifest_path.write_text(json.dumps(json_ready(manifest), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "completed", "manifest_path": str(manifest_path)}, indent=2, sort_keys=True))
    return 0


def platform_payload() -> dict[str, Any]:
    payload: dict[str, Any] = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "gpu": None,
    }
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return payload
    if result.returncode == 0:
        payload["gpu"] = result.stdout.strip()
    return payload


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    return value


if __name__ == "__main__":
    raise SystemExit(main())
