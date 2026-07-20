#!/usr/bin/env python3
"""Exact A100 audit of frozen idx47 Task 1 (5x5 pure Z3 derivatives)."""

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

from zn_dual import DualZNOBC


CUDA_SOURCE = r"""
extern "C" __global__
void build_vdiag_z3(
    double* vdiag,
    const unsigned long long dim,
    const unsigned long long* powers,
    const int* term_a,
    const int* term_b,
    const int n_terms
) {
    const unsigned long long state =
        (unsigned long long)blockDim.x * blockIdx.x + threadIdx.x;
    if (state >= dim) return;
    int nonzero = 0;
    for (int k = 0; k < n_terms; ++k) {
        const int a = term_a[k];
        const int da = (int)((state / powers[a]) % 3ULL);
        int electric = da;
        const int b = term_b[k];
        if (b >= 0) {
            const int db = (int)((state / powers[b]) % 3ULL);
            electric = da - db;
            if (electric < 0) electric += 3;
        }
        nonzero += (electric != 0);
    }
    vdiag[state] = 3.0 * (double)nonzero;
}

extern "C" __global__
void matvec_z3(
    const double* vector,
    const double* vdiag,
    double* output,
    const unsigned long long dim,
    const unsigned long long* powers,
    const int n_bits,
    const double h,
    const double g
) {
    const unsigned long long state =
        (unsigned long long)blockDim.x * blockIdx.x + threadIdx.x;
    if (state >= dim) return;
    double value = g * vdiag[state] * vector[state];
    for (int bit = 0; bit < n_bits; ++bit) {
        const unsigned long long power = powers[bit];
        const int digit = (int)((state / power) % 3ULL);
        const unsigned long long plus = digit == 2 ? state - 2ULL * power : state + power;
        const unsigned long long minus = digit == 0 ? state + 2ULL * power : state - power;
        value -= h * (vector[plus] + vector[minus]);
    }
    output[state] = value;
}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lattice-size", type=int, default=5)
    parser.add_argument("--g0", type=float, default=0.375)
    parser.add_argument("--step", type=float, default=0.001)
    parser.add_argument("--eig-tol", type=float, default=1e-11)
    parser.add_argument("--eig-maxiter", type=int, default=500)
    parser.add_argument(
        "--output",
        type=Path,
        default=CASE_ROOT / "outputs" / "data" / "idx47_z3_derivatives_a100.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    import cupy as cp
    from cupyx.scipy.sparse.linalg import LinearOperator, eigsh

    started = time.perf_counter()
    model = DualZNOBC(args.lattice_size, 3, h=1.0, g=args.g0)
    props = cp.cuda.runtime.getDeviceProperties(cp.cuda.Device().id)
    gpu_name = props["name"].decode() if isinstance(props["name"], bytes) else str(props["name"])
    if "A100" not in gpu_name:
        raise RuntimeError(f"paper-scale run requires A100; found {gpu_name}")

    module = cp.RawModule(code=CUDA_SOURCE, options=("--std=c++11",))
    diag_kernel = module.get_function("build_vdiag_z3")
    matvec_kernel = module.get_function("matvec_z3")
    threads = 256
    blocks = (model.hilbert_dim + threads - 1) // threads
    terms = model.electric_terms()
    powers = cp.asarray(model.powers, dtype=cp.uint64)
    term_a = cp.asarray([a for a, _ in terms], dtype=cp.int32)
    term_b = cp.asarray([-1 if b is None else b for _, b in terms], dtype=cp.int32)
    vdiag = cp.empty(model.hilbert_dim, dtype=cp.float64)
    diag_kernel(
        (blocks,),
        (threads,),
        (
            vdiag,
            np.uint64(model.hilbert_dim),
            powers,
            term_a,
            term_b,
            np.int32(len(terms)),
        ),
    )

    solve_records: dict[str, object] = {}
    matvec_calls = 0

    def solve(g_value: float, v0: cp.ndarray | None) -> tuple[float, float, float, cp.ndarray]:
        nonlocal matvec_calls

        def apply(vector: cp.ndarray) -> cp.ndarray:
            nonlocal matvec_calls
            flat = vector.reshape(-1)
            output = cp.empty_like(flat)
            matvec_kernel(
                (blocks,),
                (threads,),
                (
                    flat,
                    vdiag,
                    output,
                    np.uint64(model.hilbert_dim),
                    powers,
                    np.int32(model.n_plaquettes),
                    np.float64(model.h),
                    np.float64(g_value),
                ),
            )
            matvec_calls += 1
            return output

        if v0 is None:
            v0 = cp.full(model.hilbert_dim, 1.0 / math.sqrt(model.hilbert_dim), dtype=cp.float64)
        operator = LinearOperator((model.hilbert_dim, model.hilbert_dim), matvec=apply, dtype=cp.float64)
        t0 = time.perf_counter()
        values, vectors = eigsh(
            operator,
            k=1,
            which="SA",
            v0=v0,
            tol=args.eig_tol,
            maxiter=args.eig_maxiter,
        )
        state = vectors[:, 0]
        state /= cp.linalg.norm(state)
        energy = float(cp.asnumpy(values)[0])
        residual = float(cp.linalg.norm(apply(state) - energy * state).get())
        derivative = float(cp.real(cp.vdot(state, vdiag * state)).get())
        solve_records[f"{g_value:.9f}"] = {
            "energy": energy,
            "hellmann_feynman_dE_dg": derivative,
            "residual_norm": residual,
            "seconds": time.perf_counter() - t0,
        }
        return energy, derivative, residual, state

    offsets = [0, -1, 1, -2, 2]
    states: dict[int, cp.ndarray] = {}
    derivatives: dict[int, float] = {}
    residuals: list[float] = []
    previous: cp.ndarray | None = None
    for offset in offsets:
        _, derivative, residual, previous = solve(args.g0 + offset * args.step, previous)
        states[offset] = previous
        derivatives[offset] = derivative
        residuals.append(residual)

    second_derivative = (
        derivatives[-2]
        - 8.0 * derivatives[-1]
        + 8.0 * derivatives[1]
        - derivatives[2]
    ) / (12.0 * args.step)
    first_derivative = derivatives[0]
    frozen = {"first_derivative": 29.2609913710, "second_derivative": -179.0345184105}
    absolute_errors = {
        "first_derivative": abs(first_derivative - frozen["first_derivative"]),
        "second_derivative": abs(second_derivative - frozen["second_derivative"]),
    }
    checks = {
        "gpu_is_a100": "A100" in gpu_name,
        "dimension_is_3^16_for_L5": model.lattice_size != 5 or model.hilbert_dim == 3**16,
        "max_residual_below_1e-8": max(residuals) < 1e-8,
        "stencil_is_centered_five_point": set(derivatives) == {-2, -1, 0, 1, 2},
    }
    payload = {
        "schema_version": 1,
        "record": "prlb-f37350e-047",
        "target": "frozen Task 1 exact-dual audit",
        "machine": {"gpu": gpu_name, "cupy": cp.__version__, "python": platform.python_version()},
        "parameters": {
            "lattice_size_vertices": model.lattice_size,
            "plaquette_side": model.plaquette_side,
            "n_plaquettes": model.n_plaquettes,
            "hilbert_dim": model.hilbert_dim,
            "n_links": model.n_links,
            "group_order": 3,
            "h": 1.0,
            "g0": args.g0,
            "stencil_step": args.step,
        },
        "method": {
            "representation": "exact open-boundary dual Z3 plaquette variables",
            "first_derivative": "Hellmann-Feynman expectation of dH/dg",
            "second_derivative": "five-point centered derivative of Hellmann-Feynman values",
        },
        "solves": solve_records,
        "result": {"first_derivative": first_derivative, "second_derivative": second_derivative},
        "frozen": frozen,
        "absolute_errors": absolute_errors,
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
