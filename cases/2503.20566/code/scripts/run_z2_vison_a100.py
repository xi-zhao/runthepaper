#!/usr/bin/env python3
"""Independent A100 exact dynamics for the PRL-Bench idx47 vison target.

The full 6x6 charge-free gauge problem is represented by 25 dual plaquette
spins (dimension 2^25).  CuPy RawKernels apply the matrix-free Hamiltonian;
CuPy Lanczos obtains the ground state and a Chebyshev expansion performs the
real-time propagation.  No PEPS data or frozen answer is used by the solver.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import sys
import time
from pathlib import Path
from typing import Callable

import numpy as np
from scipy.special import jv


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from z2_dual import DualZ2OBC, evolve_exact, exact_ground_state


CUDA_SOURCE = r"""
extern "C" __global__
void build_diag(
    double* diag,
    const unsigned long long dim,
    const int* term_a,
    const int* term_b,
    const int n_terms,
    const int n_links,
    const double g
) {
    const unsigned long long state =
        (unsigned long long)blockDim.x * blockIdx.x + threadIdx.x;
    if (state >= dim) return;
    int electric_sum = 0;
    for (int k = 0; k < n_terms; ++k) {
        const int a = term_a[k];
        const int za = 1 - 2 * ((state >> a) & 1ULL);
        int product = za;
        const int b = term_b[k];
        if (b >= 0) {
            const int zb = 1 - 2 * ((state >> b) & 1ULL);
            product *= zb;
        }
        electric_sum += product;
    }
    diag[state] = 2.0 * g * ((double)n_links - (double)electric_sum);
}

extern "C" __global__
void matvec_real(
    const double* vector,
    const double* diag,
    double* output,
    const unsigned long long dim,
    const int n_bits,
    const double h,
    const double shift,
    const double scale
) {
    const unsigned long long state =
        (unsigned long long)blockDim.x * blockIdx.x + threadIdx.x;
    if (state >= dim) return;
    double value = (diag[state] - shift) * vector[state];
    for (int bit = 0; bit < n_bits; ++bit) {
        value -= 2.0 * h * vector[state ^ (1ULL << bit)];
    }
    output[state] = value / scale;
}

extern "C" __global__
void matvec_complex(
    const double2* vector,
    const double* diag,
    double2* output,
    const unsigned long long dim,
    const int n_bits,
    const double h,
    const double shift,
    const double scale
) {
    const unsigned long long state =
        (unsigned long long)blockDim.x * blockIdx.x + threadIdx.x;
    if (state >= dim) return;
    const double diagonal = diag[state] - shift;
    double2 value;
    value.x = diagonal * vector[state].x;
    value.y = diagonal * vector[state].y;
    for (int bit = 0; bit < n_bits; ++bit) {
        const double2 flipped = vector[state ^ (1ULL << bit)];
        value.x -= 2.0 * h * flipped.x;
        value.y -= 2.0 * h * flipped.y;
    }
    output[state].x = value.x / scale;
    output[state].y = value.y / scale;
}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lattice-size", type=int, default=6)
    parser.add_argument("--h", type=float, default=1.0)
    parser.add_argument("--g", type=float, default=0.1)
    parser.add_argument("--times", default="4.5,6.0,7.5")
    parser.add_argument("--eig-tol", type=float, default=1e-11)
    parser.add_argument("--eig-maxiter", type=int, default=500)
    parser.add_argument("--cheb-degree", type=int)
    parser.add_argument(
        "--output",
        type=Path,
        default=CASE_ROOT / "outputs" / "data" / "idx47_z2_vison_a100.json",
    )
    return parser.parse_args()


def json_float(value: object) -> float:
    return float(np.asarray(value).item())


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    import cupy as cp
    from cupyx.scipy.sparse.linalg import LinearOperator, eigsh

    started = time.perf_counter()
    model = DualZ2OBC(args.lattice_size, h=args.h, g=args.g)
    times = tuple(sorted({float(item) for item in args.times.split(",") if item.strip()}))
    if not times or min(times) < 0:
        raise ValueError("times must contain non-negative values")

    device = cp.cuda.Device()
    props = cp.cuda.runtime.getDeviceProperties(device.id)
    gpu_name = props["name"].decode() if isinstance(props["name"], bytes) else str(props["name"])
    if "A100" not in gpu_name:
        raise RuntimeError(f"paper-scale run requires A100; found {gpu_name}")

    kernels = cp.RawModule(code=CUDA_SOURCE, options=("--std=c++11",))
    build_diag_kernel = kernels.get_function("build_diag")
    real_kernel = kernels.get_function("matvec_real")
    complex_kernel = kernels.get_function("matvec_complex")
    threads = 256
    blocks = (model.hilbert_dim + threads - 1) // threads

    terms = model.electric_terms()
    term_a = cp.asarray([a for a, _ in terms], dtype=cp.int32)
    term_b = cp.asarray([-1 if b is None else b for _, b in terms], dtype=cp.int32)
    diagonal = cp.empty(model.hilbert_dim, dtype=cp.float64)
    build_diag_kernel(
        (blocks,),
        (threads,),
        (
            diagonal,
            np.uint64(model.hilbert_dim),
            term_a,
            term_b,
            np.int32(len(terms)),
            np.int32(model.n_links),
            np.float64(model.g),
        ),
    )
    cp.cuda.Stream.null.synchronize()

    matvec_count = {"real": 0, "complex": 0}

    def apply_real(vector: cp.ndarray, shift: float = 0.0, scale: float = 1.0) -> cp.ndarray:
        flat = vector.reshape(-1)
        output = cp.empty_like(flat)
        real_kernel(
            (blocks,),
            (threads,),
            (
                flat,
                diagonal,
                output,
                np.uint64(model.hilbert_dim),
                np.int32(model.n_plaquettes),
                np.float64(model.h),
                np.float64(shift),
                np.float64(scale),
            ),
        )
        matvec_count["real"] += 1
        return output

    def apply_complex(vector: cp.ndarray, shift: float = 0.0, scale: float = 1.0) -> cp.ndarray:
        flat = vector.reshape(-1)
        output = cp.empty_like(flat)
        complex_kernel(
            (blocks,),
            (threads,),
            (
                flat,
                diagonal,
                output,
                np.uint64(model.hilbert_dim),
                np.int32(model.n_plaquettes),
                np.float64(model.h),
                np.float64(shift),
                np.float64(scale),
            ),
        )
        matvec_count["complex"] += 1
        return output

    eig_started = time.perf_counter()
    operator = LinearOperator(
        shape=(model.hilbert_dim, model.hilbert_dim),
        matvec=apply_real,
        dtype=cp.float64,
    )
    initial = cp.full(
        model.hilbert_dim,
        1.0 / math.sqrt(model.hilbert_dim),
        dtype=cp.float64,
    )
    eigenvalues, eigenvectors = eigsh(
        operator,
        k=1,
        which="SA",
        v0=initial,
        tol=args.eig_tol,
        maxiter=args.eig_maxiter,
    )
    ground_energy = json_float(cp.asnumpy(eigenvalues)[0])
    ground = eigenvectors[:, 0]
    ground /= cp.linalg.norm(ground)
    h_ground = apply_real(ground)
    ground_residual = json_float(cp.linalg.norm(h_ground - ground_energy * ground).get())
    eig_seconds = time.perf_counter() - eig_started

    indices = cp.arange(model.hilbert_dim, dtype=cp.uint64)
    source_bit = model.plaquette_index(0, 0)
    source_sign = 1.0 - 2.0 * ((indices >> source_bit) & 1).astype(cp.float64)
    vison = (ground * source_sign).astype(cp.complex128)
    del source_sign, h_ground, eigenvectors, initial
    cp.get_default_memory_pool().free_all_blocks()

    h_vison = apply_complex(vison)
    initial_energy = json_float(cp.real(cp.vdot(vison, h_vison)).get())
    initial_norm = json_float(cp.real(cp.vdot(vison, vison)).get())
    del h_vison

    # Gershgorin bounds: H_E lies in [0, 4g*N_links], while every row has
    # magnetic off-diagonal radius 2h*N_plaquettes.
    lower_bound = -2.0 * model.h * model.n_plaquettes
    upper_bound = 4.0 * model.g * model.n_links + 2.0 * model.h * model.n_plaquettes
    center = 0.5 * (lower_bound + upper_bound)
    half_width = 0.5 * (upper_bound - lower_bound) + 1.0
    z_max = half_width * max(times)
    degree = args.cheb_degree
    if degree is None:
        degree = int(math.ceil(z_max + 12.0 * z_max ** (1.0 / 3.0) + 40.0))
    tail_probe = np.arange(degree + 1, degree + 129)
    tail_bound = float(2.0 * np.sum(np.abs(jv(tail_probe, z_max))))

    coeffs = {
        time_value: np.asarray(
            [
                jv(0, half_width * time_value),
                *[
                    2.0 * ((-1j) ** n) * jv(n, half_width * time_value)
                    for n in range(1, degree + 1)
                ],
            ],
            dtype=np.complex128,
        )
        for time_value in times
    }

    evolution_started = time.perf_counter()
    t_prev = vison.copy()
    evolved = {time_value: coeffs[time_value][0] * t_prev for time_value in times}
    if degree >= 1:
        t_curr = apply_complex(vison, shift=center, scale=half_width)
        for time_value in times:
            evolved[time_value] += coeffs[time_value][1] * t_curr
    else:
        t_curr = None

    for n in range(2, degree + 1):
        t_next = 2.0 * apply_complex(t_curr, shift=center, scale=half_width) - t_prev
        for time_value in times:
            evolved[time_value] += coeffs[time_value][n] * t_next
        t_prev, t_curr = t_curr, t_next

    for time_value in times:
        evolved[time_value] *= np.exp(-1j * center * time_value)
    evolution_seconds = time.perf_counter() - evolution_started

    requested_coordinates = [(0, 0), (0, 1), (1, 1), (2, 2)]
    valid_coordinates = [
        coordinate
        for coordinate in requested_coordinates
        if max(coordinate) < model.plaquette_side
    ]

    def plaquette_value(state: cp.ndarray, coordinate: tuple[int, int]) -> float:
        bit = model.plaquette_index(*coordinate)
        return json_float(cp.real(cp.vdot(state, state[indices ^ np.uint64(1 << bit)])).get())

    observations: dict[str, object] = {}
    norm_drifts: list[float] = []
    energy_drifts: list[float] = []
    for time_value in times:
        state = evolved[time_value]
        norm = json_float(cp.real(cp.vdot(state, state)).get())
        energy = json_float(cp.real(cp.vdot(state, apply_complex(state))).get())
        norm_drifts.append(abs(norm - initial_norm))
        energy_drifts.append(abs(energy - initial_energy))
        observations[f"{time_value:g}"] = {
            "norm": norm,
            "energy": energy,
            "plaquettes": {
                f"P_{x}_{y}": plaquette_value(state, (x, y))
                for x, y in valid_coordinates
            },
        }

    cpu_reference: dict[str, object] | None = None
    if model.hilbert_dim <= 4096:
        cpu_e0, cpu_ground = exact_ground_state(model)
        cpu_vison = model.apply_boundary_vison(cpu_ground).astype(np.complex128)
        cpu_states = evolve_exact(model, cpu_vison, times)
        cpu_reference = {
            "ground_energy": cpu_e0,
            "initial_energy": float(np.real(np.vdot(cpu_vison, model.matvec(cpu_vison)))),
            "max_state_error_up_to_global_phase": max(
                float(
                    np.linalg.norm(
                        cp.asnumpy(evolved[time_value])
                        - cpu_states[time_value]
                        * np.vdot(cpu_states[time_value], cp.asnumpy(evolved[time_value]))
                        / abs(np.vdot(cpu_states[time_value], cp.asnumpy(evolved[time_value])))
                    )
                )
                for time_value in times
            ),
        }

    frozen = {
        "P_0_0_at_4.5": 0.56388,
        "P_0_1_at_6": 0.80091,
        "P_1_1_at_7.5": 0.65918,
        "energy": -34.64316,
    }
    source_curve = {"third_coordinate": "P_2_2", "source_asset": "figs/vison_6x6.pdf"}
    comparison: dict[str, object] = {"frozen": frozen, "source_curve": source_curve}
    if {"4.5", "6", "7.5"}.issubset(observations):
        comparison["absolute_errors"] = {
            "P_0_0_at_4.5": abs(observations["4.5"]["plaquettes"]["P_0_0"] - frozen["P_0_0_at_4.5"]),
            "P_0_1_at_6": abs(observations["6"]["plaquettes"]["P_0_1"] - frozen["P_0_1_at_6"]),
            "P_1_1_at_7.5": abs(observations["7.5"]["plaquettes"]["P_1_1"] - frozen["P_1_1_at_7.5"]),
            "P_2_2_at_7.5_vs_frozen_third": abs(observations["7.5"]["plaquettes"]["P_2_2"] - frozen["P_1_1_at_7.5"]),
            "max_energy": max(
                abs(observations[key]["energy"] - frozen["energy"])
                for key in ("4.5", "6", "7.5")
            ),
        }

    checks = {
        "gpu_is_a100": "A100" in gpu_name,
        "dual_dimension_is_2^25_for_L6": model.lattice_size != 6 or model.hilbert_dim == 2**25,
        "dual_link_count_is_60_for_L6": model.lattice_size != 6 or model.n_links == 60,
        "ground_residual_below_1e-8": ground_residual < 1e-8,
        "chebyshev_tail_below_1e-11": tail_bound < 1e-11,
        "norm_drift_below_1e-9": max(norm_drifts) < 1e-9,
        "energy_drift_below_1e-8": max(energy_drifts) < 1e-8,
        "cpu_smoke_matches": cpu_reference is None
        or cpu_reference["max_state_error_up_to_global_phase"] < 1e-9,
    }

    payload = {
        "schema_version": 1,
        "record": "prlb-f37350e-047",
        "paper": "arXiv:2503.20566 / PRL 135, 130401 (2025)",
        "method": {
            "representation": "exact open-boundary dual Z2 plaquette spins",
            "ground_state": "cupyx.scipy.sparse.linalg.eigsh matrix-free Lanczos",
            "time_evolution": "double-precision Chebyshev expansion",
            "observable": "<tau_x> = Z2 plaquette value plotted by the source",
        },
        "parameters": {
            "lattice_size_vertices": model.lattice_size,
            "plaquette_side": model.plaquette_side,
            "n_plaquettes": model.n_plaquettes,
            "hilbert_dim": model.hilbert_dim,
            "n_links": model.n_links,
            "h": model.h,
            "g": model.g,
            "times": times,
        },
        "machine": {
            "gpu": gpu_name,
            "cupy": cp.__version__,
            "python": platform.python_version(),
        },
        "ground_state": {
            "energy": ground_energy,
            "residual_norm": ground_residual,
            "eig_seconds": eig_seconds,
        },
        "initial_vison": {"norm": initial_norm, "energy": initial_energy},
        "chebyshev": {
            "gershgorin_bounds": [lower_bound, upper_bound],
            "center": center,
            "half_width_with_margin": half_width,
            "degree": degree,
            "tail_bound_128_terms": tail_bound,
            "evolution_seconds": evolution_seconds,
        },
        "observations": observations,
        "comparison": comparison,
        "cpu_reference": cpu_reference,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "matvec_count": matvec_count,
        "wall_seconds": time.perf_counter() - started,
    }
    write_json(args.output, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
