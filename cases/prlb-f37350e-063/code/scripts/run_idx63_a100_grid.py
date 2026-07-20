#!/usr/bin/env python3
"""Run the full PRL-Bench idx63 finite-time protocol on a CUDA device.

The benchmark prose is ambiguous about which NumPy MT19937 normal sampler is
intended.  By default this runner executes both modern
``Generator(MT19937(1))`` and legacy ``RandomState(1)`` initial states, for
both RK4 and Heun.  Each kappa value is still an independent trajectory from
the same prescribed initial state; batching only changes execution layout.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from typing import Callable

import numpy as np
import torch
import torch.nn.functional as torch_functional


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from nonreciprocal_cep_audit import seeded_initial_state  # noqa: E402


TensorStep = Callable[
    [torch.Tensor, torch.Tensor, torch.Tensor], tuple[torch.Tensor, torch.Tensor]
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def append_event(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"timestamp": utc_now(), **payload}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def rhs(
    real: torch.Tensor,
    imag: torch.Tensor,
    kappa: torch.Tensor,
    *,
    gamma: float,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Real/imaginary OBC vector field with the site index last."""

    pump_shape = (kappa.shape[0],) + (1,) * (real.ndim - 1)
    onsite = kappa.reshape(pump_shape) - 2.0 * gamma - real.square() - imag.square()
    next_real = torch_functional.pad(real[..., 1:], (0, 1))
    previous_real = torch_functional.pad(real[..., :-1], (1, 0))
    next_imag = torch_functional.pad(imag[..., 1:], (0, 1))
    previous_imag = torch_functional.pad(imag[..., :-1], (1, 0))
    derivative_real = (
        onsite * real
        - (1.0 - gamma) * next_imag
        - (1.0 + gamma) * previous_imag
    )
    derivative_imag = (
        onsite * imag
        + (1.0 - gamma) * next_real
        + (1.0 + gamma) * previous_real
    )
    return derivative_real, derivative_imag


def make_step(method: str, *, gamma: float, dt: float) -> TensorStep:
    if method == "rk4":

        def step(
            real: torch.Tensor, imag: torch.Tensor, kappa: torch.Tensor
        ) -> tuple[torch.Tensor, torch.Tensor]:
            k1r, k1i = rhs(real, imag, kappa, gamma=gamma)
            k2r, k2i = rhs(
                real + 0.5 * dt * k1r,
                imag + 0.5 * dt * k1i,
                kappa,
                gamma=gamma,
            )
            k3r, k3i = rhs(
                real + 0.5 * dt * k2r,
                imag + 0.5 * dt * k2i,
                kappa,
                gamma=gamma,
            )
            k4r, k4i = rhs(real + dt * k3r, imag + dt * k3i, kappa, gamma=gamma)
            return (
                real + (dt / 6.0) * (k1r + 2.0 * k2r + 2.0 * k3r + k4r),
                imag + (dt / 6.0) * (k1i + 2.0 * k2i + 2.0 * k3i + k4i),
            )

        return step

    if method == "heun":

        def step(
            real: torch.Tensor, imag: torch.Tensor, kappa: torch.Tensor
        ) -> tuple[torch.Tensor, torch.Tensor]:
            k1r, k1i = rhs(real, imag, kappa, gamma=gamma)
            k2r, k2i = rhs(real + dt * k1r, imag + dt * k1i, kappa, gamma=gamma)
            return real + 0.5 * dt * (k1r + k2r), imag + 0.5 * dt * (k1i + k2i)

        return step

    raise ValueError(f"unknown integration method: {method}")


def residual_norms(
    real: torch.Tensor,
    imag: torch.Tensor,
    kappa: torch.Tensor,
    *,
    gamma: float,
) -> torch.Tensor:
    derivative_real, derivative_imag = rhs(real, imag, kappa, gamma=gamma)
    return torch.sqrt(
        torch.sum(derivative_real.square() + derivative_imag.square(), dim=-1)
    )


def finite_difference_jacobian(
    state: torch.Tensor,
    kappa: torch.Tensor,
    *,
    gamma: float,
    epsilon: float,
) -> torch.Tensor:
    """Return batched forward-difference Jacobians for real 2N states."""

    coordinates = state.shape[-1]
    n = coordinates // 2
    eye = torch.eye(coordinates, dtype=state.dtype, device=state.device)
    perturbed = state[:, None, :] + epsilon * eye[None, :, :]
    base_real, base_imag = rhs(state[:, :n], state[:, n:], kappa, gamma=gamma)
    perturbed_real, perturbed_imag = rhs(
        perturbed[..., :n], perturbed[..., n:], kappa, gamma=gamma
    )
    base = torch.cat((base_real, base_imag), dim=-1)
    values = torch.cat((perturbed_real, perturbed_imag), dim=-1)
    return ((values - base[:, None, :]) / epsilon).transpose(-1, -2)


def diagnose_states(
    real: torch.Tensor,
    imag: torch.Tensor,
    kappa: torch.Tensor,
    accepted: torch.Tensor,
    *,
    gamma: float,
    epsilon: float,
    tolerance: float,
    batch_size: int,
) -> dict[str, np.ndarray]:
    """Compute all diagnostics for accepted states and NaNs elsewhere."""

    count = real.shape[0]
    lambda_1 = np.full(count, np.nan + 1j * np.nan, dtype=np.complex128)
    lambda_2 = np.full(count, np.nan + 1j * np.nan, dtype=np.complex128)
    nullity_1 = np.full(count, -1, dtype=np.int16)
    nullity_2 = np.full(count, -1, dtype=np.int16)
    accepted_indices = torch.nonzero(accepted, as_tuple=False).flatten()

    for offset in range(0, accepted_indices.numel(), batch_size):
        selection = accepted_indices[offset : offset + batch_size]
        state = torch.cat((real[selection], imag[selection]), dim=-1)
        selected_kappa = kappa[selection]
        jacobian = finite_difference_jacobian(
            state,
            selected_kappa,
            gamma=gamma,
            epsilon=epsilon,
        )
        singular = torch.linalg.svdvals(jacobian)
        squared_singular = torch.linalg.svdvals(jacobian @ jacobian)
        eigenvalues = torch.linalg.eigvals(jacobian).cpu().numpy()
        selected_numpy = selection.cpu().numpy()
        nullity_1[selected_numpy] = (
            torch.count_nonzero(singular < tolerance, dim=-1).cpu().numpy()
        )
        nullity_2[selected_numpy] = (
            torch.count_nonzero(squared_singular < tolerance, dim=-1).cpu().numpy()
        )
        for row, grid_index in enumerate(selected_numpy):
            values = eigenvalues[row]
            order = np.lexsort((-values.imag, -values.real))
            lambda_1[grid_index] = values[order[0]]
            lambda_2[grid_index] = values[order[1]]

    return {
        "lambda_1": lambda_1,
        "lambda_2": lambda_2,
        "nullity_1": nullity_1,
        "nullity_2": nullity_2,
    }


def grid_values(start: float, stop: float, spacing: float) -> np.ndarray:
    count = int(round((stop - start) / spacing)) + 1
    values = start + spacing * np.arange(count, dtype=np.float64)
    if not np.isclose(values[-1], stop, rtol=0.0, atol=1.0e-12):
        raise ValueError("grid endpoints are not commensurate with spacing")
    return values


def run_one(
    *,
    style: str,
    method: str,
    kappas_numpy: np.ndarray,
    args: argparse.Namespace,
    device: torch.device,
    progress_path: Path,
) -> dict[str, object]:
    run_name = f"{style}_{method}"
    append_event(progress_path, {"event": "run_started", "run": run_name})
    initial = seeded_initial_state(args.n, seed=args.seed, style=style)
    initial_hash = hashlib.sha256(initial.tobytes()).hexdigest()
    real = torch.as_tensor(initial.real, dtype=torch.float64, device=device)[None, :]
    imag = torch.as_tensor(initial.imag, dtype=torch.float64, device=device)[None, :]
    real = real.expand(len(kappas_numpy), -1).clone()
    imag = imag.expand(len(kappas_numpy), -1).clone()
    kappas = torch.as_tensor(kappas_numpy, dtype=torch.float64, device=device)

    step: TensorStep = make_step(method, gamma=args.gamma, dt=args.dt)
    if not args.eager:
        step = torch.compile(step, fullgraph=True, dynamic=False)

    started = time.perf_counter()
    with torch.no_grad():
        for completed in range(1, args.steps + 1):
            real, imag = step(real, imag, kappas)
            if completed % args.checkpoint_every == 0 or completed == args.steps:
                residual = residual_norms(real, imag, kappas, gamma=args.gamma)
                append_event(
                    progress_path,
                    {
                        "event": "integration_checkpoint",
                        "run": run_name,
                        "step": completed,
                        "elapsed_seconds": time.perf_counter() - started,
                        "residual_min": float(residual.min().item()),
                        "residual_max": float(residual.max().item()),
                        "static_count": int(
                            torch.count_nonzero(residual < args.static_tolerance).item()
                        ),
                    },
                )

        torch.cuda.synchronize(device) if device.type == "cuda" else None
        integration_seconds = time.perf_counter() - started
        residual = residual_norms(real, imag, kappas, gamma=args.gamma)
        accepted = residual < args.static_tolerance

        diagnostics = diagnose_states(
            real,
            imag,
            kappas,
            accepted,
            gamma=args.gamma,
            epsilon=args.epsilon,
            tolerance=args.svd_tolerance,
            batch_size=args.diagnostic_batch_size,
        )
        half_diagnostics = diagnose_states(
            real,
            imag,
            kappas,
            accepted,
            gamma=args.gamma,
            epsilon=0.5 * args.epsilon,
            tolerance=args.svd_tolerance,
            batch_size=args.diagnostic_batch_size,
        )

    residual_numpy = residual.cpu().numpy()
    accepted_numpy = accepted.cpu().numpy()
    criterion = (
        accepted_numpy
        & (np.abs(diagnostics["lambda_2"].real) < args.cep_real_tolerance)
        & (diagnostics["nullity_1"] == 1)
        & (diagnostics["nullity_2"] == 2)
    )
    half_criterion = (
        accepted_numpy
        & (np.abs(half_diagnostics["lambda_2"].real) < args.cep_real_tolerance)
        & (half_diagnostics["nullity_1"] == 1)
        & (half_diagnostics["nullity_2"] == 2)
    )
    state_real = real.cpu().numpy()
    state_imag = imag.cpu().numpy()

    output_path = args.output_dir / f"idx63_{run_name}.npz"
    np.savez_compressed(
        output_path,
        kappa=kappas_numpy,
        residual=residual_numpy,
        accepted=accepted_numpy,
        state_real=state_real,
        state_imag=state_imag,
        criterion=criterion,
        half_criterion=half_criterion,
        **diagnostics,
        half_lambda_1=half_diagnostics["lambda_1"],
        half_lambda_2=half_diagnostics["lambda_2"],
        half_nullity_1=half_diagnostics["nullity_1"],
        half_nullity_2=half_diagnostics["nullity_2"],
    )

    static_indices = np.flatnonzero(accepted_numpy)
    criterion_indices = np.flatnonzero(criterion)
    half_indices = np.flatnonzero(half_criterion)
    frozen_index = int(round((2.38930 - kappas_numpy[0]) / args.grid_spacing))
    frozen_on_grid = 0 <= frozen_index < len(kappas_numpy) and np.isclose(
        kappas_numpy[frozen_index], 2.38930, rtol=0.0, atol=1.0e-12
    )
    summary: dict[str, object] = {
        "run": run_name,
        "style": style,
        "method": method,
        "initial_state_sha256": initial_hash,
        "integration_seconds": integration_seconds,
        "static_count": int(len(static_indices)),
        "first_static_kappa": (
            float(kappas_numpy[static_indices[0]]) if len(static_indices) else None
        ),
        "last_static_kappa": (
            float(kappas_numpy[static_indices[-1]]) if len(static_indices) else None
        ),
        "criterion_kappas": kappas_numpy[criterion_indices].tolist(),
        "half_epsilon_criterion_kappas": kappas_numpy[half_indices].tolist(),
        "kappa_cep": (
            float(kappas_numpy[criterion_indices[0]]) if len(criterion_indices) else None
        ),
        "half_epsilon_kappa_cep": (
            float(kappas_numpy[half_indices[0]]) if len(half_indices) else None
        ),
        "frozen_point": None,
        "output": str(output_path),
    }
    if frozen_on_grid:
        summary["frozen_point"] = {
            "kappa": float(kappas_numpy[frozen_index]),
            "residual": float(residual_numpy[frozen_index]),
            "accepted": bool(accepted_numpy[frozen_index]),
            "lambda_2": (
                [
                    float(diagnostics["lambda_2"][frozen_index].real),
                    float(diagnostics["lambda_2"][frozen_index].imag),
                ]
                if accepted_numpy[frozen_index]
                else None
            ),
            "nullities": (
                [
                    int(diagnostics["nullity_1"][frozen_index]),
                    int(diagnostics["nullity_2"][frozen_index]),
                ]
                if accepted_numpy[frozen_index]
                else None
            ),
        }
    append_event(
        progress_path,
        {
            "event": "run_completed",
            "run": run_name,
            "integration_seconds": integration_seconds,
            "static_count": int(len(static_indices)),
            "criterion_count": int(len(criterion_indices)),
            "kappa_cep": summary["kappa_cep"],
        },
    )
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--styles", nargs="+", default=["generator", "legacy"])
    parser.add_argument("--methods", nargs="+", default=["rk4", "heun"])
    parser.add_argument("--n", type=int, default=40)
    parser.add_argument("--gamma", type=float, default=0.3)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--dt", type=float, default=0.02)
    parser.add_argument("--steps", type=int, default=200_000)
    parser.add_argument("--grid-start", type=float, default=2.36)
    parser.add_argument("--grid-stop", type=float, default=2.41)
    parser.add_argument("--grid-spacing", type=float, default=1.0e-5)
    parser.add_argument("--epsilon", type=float, default=1.0e-7)
    parser.add_argument("--static-tolerance", type=float, default=1.0e-8)
    parser.add_argument("--svd-tolerance", type=float, default=5.0e-7)
    parser.add_argument("--cep-real-tolerance", type=float, default=1.0e-5)
    parser.add_argument("--checkpoint-every", type=int, default=10_000)
    parser.add_argument("--diagnostic-batch-size", type=int, default=256)
    parser.add_argument("--eager", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir = args.output_dir.resolve()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    progress_path = args.output_dir / "idx63_a100_progress.jsonl"
    progress_path.write_text("", encoding="utf-8")
    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    kappas = grid_values(args.grid_start, args.grid_stop, args.grid_spacing)
    append_event(
        progress_path,
        {
            "event": "campaign_started",
            "device": str(device),
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "grid_count": len(kappas),
            "steps": args.steps,
            "styles": args.styles,
            "methods": args.methods,
            "eager": args.eager,
        },
    )
    summaries = []
    for method in args.methods:
        for style in args.styles:
            summaries.append(
                run_one(
                    style=style,
                    method=method,
                    kappas_numpy=kappas,
                    args=args,
                    device=device,
                    progress_path=progress_path,
                )
            )
    result = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "source_contract": "benchmark_extension_not_source_protocol",
        "parameters": {
            "n": args.n,
            "gamma": args.gamma,
            "seed": args.seed,
            "dt": args.dt,
            "steps": args.steps,
            "total_time": args.dt * args.steps,
            "grid_start": args.grid_start,
            "grid_stop": args.grid_stop,
            "grid_spacing": args.grid_spacing,
            "grid_count": len(kappas),
            "epsilon": args.epsilon,
            "static_tolerance": args.static_tolerance,
            "svd_tolerance": args.svd_tolerance,
            "cep_real_tolerance": args.cep_real_tolerance,
            "device": str(device),
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
        },
        "runs": summaries,
        "frozen_answer": {
            "kappa_cep": 2.38930,
            "lambda_2_real": -9.6e-6,
            "nullities": [1, 2],
            "epsilon_half_changes": False,
            "heun_changes": False,
        },
    }
    result_path = args.output_dir / "idx63_a100_result.json"
    write_json(result_path, result)
    append_event(progress_path, {"event": "campaign_completed", "result": str(result_path)})
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
