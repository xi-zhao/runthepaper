#!/usr/bin/env python3
"""Exact A100 audit of frozen idx47 Task 2 (odd-Z2 VBS order)."""

from __future__ import annotations

import argparse
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from odd_z2 import OddZ2OBC


CUDA_SOURCE = r"""
extern "C" __global__
void build_odd_observables(
    double* diag,
    double* dx,
    double* dy,
    const unsigned long long dim,
    const int* term_a,
    const int* term_b,
    const int* eta,
    const double* wx,
    const double* wy,
    const int n_terms,
    const double g
) {
    const unsigned long long state =
        (unsigned long long)blockDim.x * blockIdx.x + threadIdx.x;
    if (state >= dim) return;
    double electric = 0.0;
    double value_x = 0.0;
    double value_y = 0.0;
    for (int k = 0; k < n_terms; ++k) {
        int z = eta[k] * (1 - 2 * ((state >> term_a[k]) & 1ULL));
        if (term_b[k] >= 0) z *= 1 - 2 * ((state >> term_b[k]) & 1ULL);
        const double bar_e = 2.0 - 2.0 * (double)z;
        electric += g * bar_e;
        value_x += wx[k] * bar_e;
        value_y += wy[k] * bar_e;
    }
    diag[state] = electric;
    dx[state] = value_x;
    dy[state] = value_y;
}

extern "C" __global__
void matvec_odd(
    const double* vector,
    const double* diag,
    double* output,
    const unsigned long long dim,
    const int n_bits,
    const double h
) {
    const unsigned long long state =
        (unsigned long long)blockDim.x * blockIdx.x + threadIdx.x;
    if (state >= dim) return;
    double value = diag[state] * vector[state];
    for (int bit = 0; bit < n_bits; ++bit) value -= 2.0 * h * vector[state ^ (1ULL << bit)];
    output[state] = value;
}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lattice-size", type=int, default=6)
    parser.add_argument("--g", type=float, default=0.4)
    parser.add_argument("--eig-tol", type=float, default=1e-11)
    parser.add_argument("--eig-maxiter", type=int, default=500)
    parser.add_argument(
        "--output",
        type=Path,
        default=CASE_ROOT / "outputs" / "data" / "idx47_odd_z2_vbs_a100.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    import cupy as cp
    from cupyx.scipy.sparse.linalg import LinearOperator, eigsh

    started = time.perf_counter()
    model = OddZ2OBC(args.lattice_size, h=1.0, g=args.g)
    props = cp.cuda.runtime.getDeviceProperties(cp.cuda.Device().id)
    gpu_name = props["name"].decode() if isinstance(props["name"], bytes) else str(props["name"])
    if "A100" not in gpu_name:
        raise RuntimeError(f"paper-scale run requires A100; found {gpu_name}")

    module = cp.RawModule(code=CUDA_SOURCE, options=("--std=c++11",))
    build_kernel = module.get_function("build_odd_observables")
    matvec_kernel = module.get_function("matvec_odd")
    threads = 256
    blocks = (model.hilbert_dim + threads - 1) // threads
    links = model.links()
    norm = model.lattice_size * (model.lattice_size - 1)
    term_a = cp.asarray([link.a for link in links], dtype=cp.int32)
    term_b = cp.asarray([-1 if link.b is None else link.b for link in links], dtype=cp.int32)
    eta = cp.asarray([link.eta for link in links], dtype=cp.int32)
    wx = cp.asarray(
        [((-1.0) ** link.x) / norm if link.direction == "x" else 0.0 for link in links],
        dtype=cp.float64,
    )
    wy = cp.asarray(
        [((-1.0) ** link.y) / norm if link.direction == "y" else 0.0 for link in links],
        dtype=cp.float64,
    )
    diag = cp.empty(model.hilbert_dim, dtype=cp.float64)
    dx = cp.empty_like(diag)
    dy = cp.empty_like(diag)
    build_kernel(
        (blocks,),
        (threads,),
        (
            diag,
            dx,
            dy,
            np.uint64(model.hilbert_dim),
            term_a,
            term_b,
            eta,
            wx,
            wy,
            np.int32(len(links)),
            np.float64(model.g),
        ),
    )

    matvec_calls = 0

    def apply(vector: cp.ndarray) -> cp.ndarray:
        nonlocal matvec_calls
        flat = vector.reshape(-1)
        output = cp.empty_like(flat)
        matvec_kernel(
            (blocks,),
            (threads,),
            (
                flat,
                diag,
                output,
                np.uint64(model.hilbert_dim),
                np.int32(model.n_plaquettes),
                np.float64(model.h),
            ),
        )
        matvec_calls += 1
        return output

    operator = LinearOperator((model.hilbert_dim, model.hilbert_dim), matvec=apply, dtype=cp.float64)
    v0 = cp.full(model.hilbert_dim, 1.0 / math.sqrt(model.hilbert_dim), dtype=cp.float64)
    values, vectors = eigsh(operator, k=1, which="SA", v0=v0, tol=args.eig_tol, maxiter=args.eig_maxiter)
    state = vectors[:, 0]
    state /= cp.linalg.norm(state)
    energy = float(cp.asnumpy(values)[0])
    residual = float(cp.linalg.norm(apply(state) - energy * state).get())
    probability = state * state

    mean_dx = float(cp.dot(probability, dx).get())
    mean_dy = float(cp.dot(probability, dy).get())
    mean_dx2 = float(cp.dot(probability, dx * dx).get())
    mean_dy2 = float(cp.dot(probability, dy * dy).get())
    frozen = 0.2421075221119777
    candidates = {
        "square_of_mean_Dx": mean_dx**2,
        "square_of_mean_Dy": mean_dy**2,
        "mean_of_Dx_squared": mean_dx2,
        "mean_of_Dy_squared": mean_dy2,
    }
    errors = {name: abs(value - frozen) for name, value in candidates.items()}
    checks = {
        "gpu_is_a100": "A100" in gpu_name,
        "reference_satisfies_Q1": bool(np.all(model.reference_vertex_parities() == 1)),
        "dimension_is_2^25_for_L6": model.lattice_size != 6 or model.hilbert_dim == 2**25,
        "residual_below_1e-8": residual < 1e-8,
        "C4_mean_square_match_below_1e-8": abs(mean_dx2 - mean_dy2) < 1e-8,
    }
    payload = {
        "schema_version": 1,
        "record": "prlb-f37350e-047",
        "target": "frozen Task 2 exact fully-frustrated dual audit",
        "machine": {"gpu": gpu_name, "cupy": cp.__version__, "python": platform.python_version()},
        "parameters": {
            "lattice_size_vertices": model.lattice_size,
            "plaquette_side": model.plaquette_side,
            "n_plaquettes": model.n_plaquettes,
            "hilbert_dim": model.hilbert_dim,
            "n_links": model.n_links,
            "h": model.h,
            "g": model.g,
            "charge_sector": "Q_x=1 for every vertex",
        },
        "method": {
            "representation": "exact fully-frustrated transverse-field Ising dual",
            "reference_field": "horizontal E=1 dimers at even x; plaquette orbit spans the sector",
        },
        "ground_state": {"energy": energy, "residual_norm": residual},
        "raw_moments": {"mean_Dx": mean_dx, "mean_Dy": mean_dy, "mean_Dx2": mean_dx2, "mean_Dy2": mean_dy2},
        "candidate_interpretations": candidates,
        "frozen_value_each_direction": frozen,
        "absolute_errors": errors,
        "closest_interpretation": min(errors, key=errors.get),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "matvec_calls": matvec_calls,
        "wall_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
