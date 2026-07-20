#!/usr/bin/env python3
"""Exact A100 audit of frozen idx47 Task 3 (4x4 Z2 matter bulk energy)."""

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

from z2_matter import Z2MatterOBC


CUDA_SOURCE = r"""
extern "C" __global__
void build_matter_diag(
    double* diag,
    double* central_diag,
    const unsigned long long dim,
    const int n_plaquettes,
    const unsigned int* matter_configs,
    const unsigned int* reference_edges,
    const unsigned int* edge_plaquette_masks,
    const int* central_edge,
    const int n_edges,
    const double mass,
    const double g
) {
    const unsigned long long state =
        (unsigned long long)blockDim.x * blockIdx.x + threadIdx.x;
    if (state >= dim) return;
    const unsigned int plaquette_mask = (unsigned int)(state & ((1ULL << n_plaquettes) - 1ULL));
    const unsigned int matter_index = (unsigned int)(state >> n_plaquettes);
    const unsigned int matter = matter_configs[matter_index];
    const unsigned int reference = reference_edges[matter_index];
    double total = mass * (double)__popc(matter);
    double central = 0.0;
    for (int edge = 0; edge < n_edges; ++edge) {
        const int electric = ((reference >> edge) & 1U)
            ^ (__popc(plaquette_mask & edge_plaquette_masks[edge]) & 1);
        const double electric_energy = electric ? 4.0 * g : 0.0;
        total += electric_energy;
        if (central_edge[edge]) central += electric_energy;
    }
    diag[state] = total;
    central_diag[state] = central;
}

extern "C" __global__
void matvec_matter(
    const double* vector,
    const double* diag,
    double* output,
    const unsigned long long dim,
    const int n_plaquettes,
    const unsigned int* matter_configs,
    const int* config_to_index,
    const int* edge_u,
    const int* edge_v,
    const unsigned int* hop_masks,
    const int n_edges,
    const double h,
    const double hopping
) {
    const unsigned long long state =
        (unsigned long long)blockDim.x * blockIdx.x + threadIdx.x;
    if (state >= dim) return;
    const unsigned int plaquette_mask = (unsigned int)(state & ((1ULL << n_plaquettes) - 1ULL));
    const unsigned int matter_index = (unsigned int)(state >> n_plaquettes);
    const unsigned int matter = matter_configs[matter_index];
    double value = diag[state] * vector[state];
    for (int plaquette = 0; plaquette < n_plaquettes; ++plaquette) {
        value -= 2.0 * h * vector[state ^ (1ULL << plaquette)];
    }
    for (int edge = 0; edge < n_edges; ++edge) {
        const unsigned int u = (matter >> edge_u[edge]) & 1U;
        const unsigned int v = (matter >> edge_v[edge]) & 1U;
        if (u != v) {
            const unsigned int moved = matter ^ (1U << edge_u[edge]) ^ (1U << edge_v[edge]);
            const unsigned long long target =
                ((unsigned long long)config_to_index[moved] << n_plaquettes)
                | (unsigned long long)(plaquette_mask ^ hop_masks[edge]);
            value += hopping * vector[target];
        }
    }
    output[state] = value;
}

extern "C" __global__
void matvec_central(
    const double* vector,
    const double* central_diag,
    double* output,
    const unsigned long long dim,
    const int n_plaquettes,
    const unsigned int* matter_configs,
    const int* config_to_index,
    const int* edge_u,
    const int* edge_v,
    const unsigned int* hop_masks,
    const int* central_edges,
    const int n_central_edges,
    const int* central_plaquettes,
    const int n_central_plaquettes,
    const double h,
    const double hopping
) {
    const unsigned long long state =
        (unsigned long long)blockDim.x * blockIdx.x + threadIdx.x;
    if (state >= dim) return;
    const unsigned int plaquette_mask = (unsigned int)(state & ((1ULL << n_plaquettes) - 1ULL));
    const unsigned int matter_index = (unsigned int)(state >> n_plaquettes);
    const unsigned int matter = matter_configs[matter_index];
    double value = central_diag[state] * vector[state];
    for (int k = 0; k < n_central_plaquettes; ++k) {
        value -= 2.0 * h * vector[state ^ (1ULL << central_plaquettes[k])];
    }
    for (int k = 0; k < n_central_edges; ++k) {
        const int edge = central_edges[k];
        const unsigned int u = (matter >> edge_u[edge]) & 1U;
        const unsigned int v = (matter >> edge_v[edge]) & 1U;
        if (u != v) {
            const unsigned int moved = matter ^ (1U << edge_u[edge]) ^ (1U << edge_v[edge]);
            const unsigned long long target =
                ((unsigned long long)config_to_index[moved] << n_plaquettes)
                | (unsigned long long)(plaquette_mask ^ hop_masks[edge]);
            value += hopping * vector[target];
        }
    }
    output[state] = value;
}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eig-tol", type=float, default=1e-11)
    parser.add_argument("--eig-maxiter", type=int, default=500)
    parser.add_argument(
        "--output",
        type=Path,
        default=CASE_ROOT / "outputs" / "data" / "idx47_z2_matter_bulk_a100.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    import cupy as cp
    from cupyx.scipy.sparse.linalg import LinearOperator, eigsh

    started = time.perf_counter()
    model = Z2MatterOBC(4, 8, mass=0.0, h=1.0, g=0.33, hopping=0.5)
    props = cp.cuda.runtime.getDeviceProperties(cp.cuda.Device().id)
    gpu_name = props["name"].decode() if isinstance(props["name"], bytes) else str(props["name"])
    if "A100" not in gpu_name:
        raise RuntimeError(f"paper-scale run requires A100; found {gpu_name}")

    configs_np = np.asarray(model.matter_configurations(), dtype=np.uint32)
    config_to_index_np = np.full(1 << model.n_vertices, -1, dtype=np.int32)
    config_to_index_np[configs_np] = np.arange(len(configs_np), dtype=np.int32)
    reference_np = np.asarray([model.reference_edge_mask(int(mask)) for mask in configs_np], dtype=np.uint32)
    edges = model.edges()
    _, central_edges_tuple, central_plaquettes_tuple = model.central_region()
    central_edge_flag = np.zeros(model.n_links, dtype=np.int32)
    central_edge_flag[list(central_edges_tuple)] = 1

    configs = cp.asarray(configs_np)
    config_to_index = cp.asarray(config_to_index_np)
    reference = cp.asarray(reference_np)
    edge_plaquette_masks = cp.asarray(model.edge_plaquette_masks(), dtype=cp.uint32)
    hop_masks = cp.asarray(model.hopping_plaquette_masks(), dtype=cp.uint32)
    edge_u = cp.asarray([edge.u for edge in edges], dtype=cp.int32)
    edge_v = cp.asarray([edge.v for edge in edges], dtype=cp.int32)
    central_edge = cp.asarray(central_edge_flag)
    central_edges = cp.asarray(central_edges_tuple, dtype=cp.int32)
    central_plaquettes = cp.asarray(central_plaquettes_tuple, dtype=cp.int32)

    module = cp.RawModule(code=CUDA_SOURCE, options=("--std=c++11",))
    build_kernel = module.get_function("build_matter_diag")
    matvec_kernel = module.get_function("matvec_matter")
    central_kernel = module.get_function("matvec_central")
    threads = 256
    blocks = (model.hilbert_dim + threads - 1) // threads
    diag = cp.empty(model.hilbert_dim, dtype=cp.float64)
    central_diag = cp.empty_like(diag)
    build_kernel(
        (blocks,),
        (threads,),
        (
            diag,
            central_diag,
            np.uint64(model.hilbert_dim),
            np.int32(model.n_plaquettes),
            configs,
            reference,
            edge_plaquette_masks,
            central_edge,
            np.int32(model.n_links),
            np.float64(model.mass),
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
                configs,
                config_to_index,
                edge_u,
                edge_v,
                hop_masks,
                np.int32(model.n_links),
                np.float64(model.h),
                np.float64(model.hopping),
            ),
        )
        matvec_calls += 1
        return output

    def apply_central(vector: cp.ndarray) -> cp.ndarray:
        flat = vector.reshape(-1)
        output = cp.empty_like(flat)
        central_kernel(
            (blocks,),
            (threads,),
            (
                flat,
                central_diag,
                output,
                np.uint64(model.hilbert_dim),
                np.int32(model.n_plaquettes),
                configs,
                config_to_index,
                edge_u,
                edge_v,
                hop_masks,
                central_edges,
                np.int32(len(central_edges_tuple)),
                central_plaquettes,
                np.int32(len(central_plaquettes_tuple)),
                np.float64(model.h),
                np.float64(model.hopping),
            ),
        )
        return output

    # Positive J is bipartite-gauge equivalent to negative hopping.  This sign
    # pattern gives a high-overlap deterministic Lanczos start.
    sublattice_a = sum(
        1 << model.vertex(x, y)
        for y in range(model.lattice_size)
        for x in range(model.lattice_size)
        if (x + y) % 2 == 0
    )
    matter_phase_np = np.asarray(
        [-1.0 if (int(mask) & sublattice_a).bit_count() % 2 else 1.0 for mask in configs_np],
        dtype=np.float64,
    )
    v0 = cp.repeat(cp.asarray(matter_phase_np), 1 << model.n_plaquettes)
    v0 /= cp.linalg.norm(v0)
    operator = LinearOperator((model.hilbert_dim, model.hilbert_dim), matvec=apply, dtype=cp.float64)
    values, vectors = eigsh(operator, k=1, which="SA", v0=v0, tol=args.eig_tol, maxiter=args.eig_maxiter)
    state = vectors[:, 0]
    state /= cp.linalg.norm(state)
    energy = float(cp.asnumpy(values)[0])
    residual = float(cp.linalg.norm(apply(state) - energy * state).get())
    central_energy = float(cp.real(cp.vdot(state, apply_central(state))).get())

    frozen = -4.3252682631
    checks = {
        "gpu_is_a100": "A100" in gpu_name,
        "dimension_is_6589440": model.hilbert_dim == 6_589_440,
        "all_reference_fields_satisfy_gauss": all(
            not np.any(model.gauss_parity(int(mask), int(reference_mask)))
            for mask, reference_mask in zip(configs_np, reference_np)
        ),
        "residual_below_1e-8": residual < 1e-8,
    }
    payload = {
        "schema_version": 1,
        "record": "prlb-f37350e-047",
        "target": "frozen Task 3 exact gauge-invariant matter audit",
        "machine": {"gpu": gpu_name, "cupy": cp.__version__, "python": platform.python_version()},
        "parameters": {
            "lattice_size_vertices": 4,
            "particle_number": 8,
            "matter_configurations": len(configs_np),
            "gauge_states_per_matter_configuration": 1 << model.n_plaquettes,
            "hilbert_dim": model.hilbert_dim,
            "mass": model.mass,
            "h": model.h,
            "g": model.g,
            "J": model.hopping,
            "charge_sector": "Q_x=0",
        },
        "central_contract": {
            "vertices": 9,
            "links": len(central_edges_tuple),
            "plaquettes": len(central_plaquettes_tuple),
            "choice": "lower-left 3x3; all four reflected choices are symmetry equivalent",
        },
        "method": {
            "basis": "fixed half-filled matter masks x 2^9 plaquette-cycle gauge orbit",
            "reference_field": "spanning-tree Gauss-law solve per matter mask",
            "hopping": "exact gauge-dressed hard-core-boson transition in physical basis",
        },
        "ground_state": {"energy": energy, "residual_norm": residual},
        "result": {"central_bulk_energy": central_energy},
        "frozen": {"central_bulk_energy": frozen},
        "absolute_error": abs(central_energy - frozen),
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
