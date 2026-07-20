"""Exact finite-Fock-space checks for PRL-Bench task idx60.

The implementation deliberately starts from the physical system/reference
fermions.  Referenced-fermion CARs and reference-boundary identities are
therefore outputs of the calculation rather than assumptions.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import comb

import numpy as np
from numpy.typing import NDArray


ComplexArray = NDArray[np.complex128]


def annihilation_operator(mode_count: int, mode: int) -> ComplexArray:
    """Jordan-Wigner annihilation matrix in the occupation-number basis."""

    dimension = 1 << mode_count
    operator = np.zeros((dimension, dimension), dtype=np.complex128)
    lower_mask = (1 << mode) - 1
    for state in range(dimension):
        if not state & (1 << mode):
            continue
        target = state ^ (1 << mode)
        sign = -1.0 if (state & lower_mask).bit_count() % 2 else 1.0
        operator[target, state] = sign
    return operator


@dataclass
class ReferenceModel:
    """Physical finite reference and its referenced-fermion subspace."""

    system_modes: int
    particles: int
    reference_modes: int

    def __post_init__(self) -> None:
        if not self.reference_modes >= self.particles >= self.system_modes:
            raise ValueError("requires M_r >= N >= M_s")

        self.mode_count = self.system_modes + self.reference_modes
        self.dimension = 1 << self.mode_count
        self.identity = np.eye(self.dimension, dtype=np.complex128)

        all_annihilators = [
            annihilation_operator(self.mode_count, mode)
            for mode in range(self.mode_count)
        ]
        self.system = all_annihilators[: self.system_modes]
        self.reference = all_annihilators[self.system_modes :]
        reference_numbers = [operator.conj().T @ operator for operator in self.reference]

        self.reference_ladder = np.zeros_like(self.identity)
        for index, operator in enumerate(self.reference):
            previous_number = self.identity if index == 0 else reference_numbers[index - 1]
            next_hole = (
                self.identity
                if index == self.reference_modes - 1
                else self.identity - reference_numbers[index + 1]
            )
            self.reference_ladder += next_hole @ operator @ previous_number

        self.c_daggers = [operator.conj().T @ self.reference_ladder for operator in self.system]
        self.c = [operator.conj().T for operator in self.c_daggers]
        self.omega = self._omega()
        self.sector_vectors = self._sector_vectors()
        self.basis = np.column_stack(list(self.sector_vectors.values()))
        gram = self.basis.conj().T @ self.basis
        if not np.allclose(gram, np.eye(1 << self.system_modes), atol=1e-12):
            raise AssertionError("referenced Fock vectors are not orthonormal")

        self.sector_index = {
            subset: index for index, subset in enumerate(self.sector_vectors)
        }
        self.pi_bottom = self._sector_projector(())
        self.pi_top = self._sector_projector(tuple(range(self.system_modes)))

    def _omega(self) -> ComplexArray:
        state = np.zeros(self.dimension, dtype=np.complex128)
        state[0] = 1.0
        for reference_index in range(self.particles):
            creation = self.reference[reference_index].conj().T
            state = creation @ state
        return state / np.linalg.norm(state)

    def _sector_vectors(self) -> dict[tuple[int, ...], ComplexArray]:
        vectors: dict[tuple[int, ...], ComplexArray] = {}
        for size in range(self.system_modes + 1):
            for subset in combinations(range(self.system_modes), size):
                state = self.omega.copy()
                for mode in subset:
                    state = self.c_daggers[mode] @ state
                norm = np.linalg.norm(state)
                if norm < 1e-14:
                    raise AssertionError(f"zero referenced state for subset {subset}")
                vectors[subset] = state / norm
        return vectors

    def _sector_projector(self, subset: tuple[int, ...]) -> ComplexArray:
        result = np.zeros((1 << self.system_modes, 1 << self.system_modes), dtype=np.complex128)
        result[self.sector_index[subset], self.sector_index[subset]] = 1.0
        return result

    def compress(self, operator: ComplexArray) -> ComplexArray:
        """Represent a physical operator on the referenced Fock subspace."""

        return self.basis.conj().T @ operator @ self.basis


def reference_identity_audit(model: ReferenceModel) -> dict[str, float | bool]:
    """Compare the actual identities with source, frozen, and conditional forms."""

    dimension = 1 << model.system_modes
    identity = np.eye(dimension, dtype=np.complex128)
    ladder = model.reference_ladder
    r_dag_r = model.compress(ladder.conj().T @ ladder)
    r_r_dag = model.compress(ladder @ ladder.conj().T)

    top_defect = model.particles == model.system_modes
    bottom_defect = model.reference_modes == model.particles
    corrected_r_dag_r = identity - (model.pi_top if top_defect else 0.0)
    corrected_r_r_dag = identity - (model.pi_bottom if bottom_defect else 0.0)

    frozen_r_dag_r = identity - model.pi_top
    frozen_r_r_dag = identity - model.pi_bottom
    return {
        "paper_strict_regime": bool(
            model.reference_modes > model.particles > model.system_modes
        ),
        "top_defect_present": top_defect,
        "bottom_defect_present": bottom_defect,
        "r_dag_r_identity_residual": float(np.linalg.norm(r_dag_r - identity, ord=2)),
        "r_r_dag_identity_residual": float(np.linalg.norm(r_r_dag - identity, ord=2)),
        "conditional_r_dag_r_residual": float(
            np.linalg.norm(r_dag_r - corrected_r_dag_r, ord=2)
        ),
        "conditional_r_r_dag_residual": float(
            np.linalg.norm(r_r_dag - corrected_r_r_dag, ord=2)
        ),
        "frozen_r_dag_r_residual": float(
            np.linalg.norm(r_dag_r - frozen_r_dag_r, ord=2)
        ),
        "frozen_r_r_dag_residual": float(
            np.linalg.norm(r_r_dag - frozen_r_r_dag, ord=2)
        ),
        "commutator_norm": float(np.linalg.norm(r_r_dag - r_dag_r, ord=2)),
    }


def mixed_car_residual(model: ReferenceModel) -> float:
    """Largest projected residual of {c_i^dagger,c_j}=delta_ij."""

    identity = np.eye(1 << model.system_modes, dtype=np.complex128)
    largest = 0.0
    for i in range(model.system_modes):
        for j in range(model.system_modes):
            anticommutator = (
                model.c_daggers[i] @ model.c[j]
                + model.c[j] @ model.c_daggers[i]
            )
            target = identity if i == j else np.zeros_like(identity)
            largest = max(
                largest,
                float(np.linalg.norm(model.compress(anticommutator) - target, ord=2)),
            )
    return largest


def logical_code_audit() -> dict[str, float]:
    """Evaluate Task 3 and the stabilizer premise behind Task 4 exactly."""

    model = ReferenceModel(system_modes=3, particles=4, reference_modes=5)
    identity = model.identity
    c = model.c
    c_dag = model.c_daggers

    logical_zero = 0.5 * (
        identity
        + 1j * c_dag[0] @ c_dag[1]
        - 1j * c_dag[1] @ c_dag[2]
        + c_dag[0] @ c_dag[2]
    ) @ model.omega
    logical_zero /= np.linalg.norm(logical_zero)

    logical_c = 1j * (
        c[0] @ c[1] @ c[2]
        + c[0] @ c_dag[1] @ c_dag[2]
        + c_dag[0] @ c[1] @ c_dag[2]
        + c_dag[0] @ c_dag[1] @ c[2]
    )
    logical_one = logical_c.conj().T @ logical_zero
    logical_one /= np.linalg.norm(logical_one)

    s12 = 1j * (c[0] + c_dag[0]) @ (c[1] + c_dag[1])
    s23 = -1j * (c[1] - c_dag[1]) @ (c[2] - c_dag[2])
    xi = 0.5 * (identity - s12)
    q = 1j * c[0] @ c[1] @ c[2]
    q_expectation = np.vdot(logical_zero, q.conj().T @ q @ logical_zero)

    return {
        "logical_zero_norm": float(np.vdot(logical_zero, logical_zero).real),
        "logical_one_norm": float(np.vdot(logical_one, logical_one).real),
        "s12_zero_residual": float(np.linalg.norm(s12 @ logical_zero - logical_zero)),
        "s23_zero_residual": float(np.linalg.norm(s23 @ logical_zero - logical_zero)),
        "s12_one_residual": float(np.linalg.norm(s12 @ logical_one - logical_one)),
        "s23_one_residual": float(np.linalg.norm(s23 @ logical_one - logical_one)),
        "xi_one_norm": float(np.linalg.norm(xi @ logical_one)),
        "q_dag_q_expectation": float(np.real_if_close(q_expectation).real),
    }


def ancilla_y_signal(lambdas: NDArray[np.float64]) -> NDArray[np.float64]:
    """Task-4 signal from Xi|psi>=0 and U|psi>=i|psi>."""

    # The controlled-branch overlap is <psi|U exp(i lambda Xi)|psi> = i.
    overlap = np.full(lambdas.shape, 1j, dtype=np.complex128)
    return overlap.imag


def calibrated_theta(y_signal: NDArray[np.float64]) -> NDArray[np.float64]:
    """Principal calibration inverse for <Y>=-cos(theta)."""

    return np.arccos(np.clip(-y_signal, -1.0, 1.0))


def task5_counterexamples(lambdas: NDArray[np.float64]) -> dict[str, ComplexArray]:
    """Two allowed extensions of U with different Task-5 amplitudes.

    The frozen statement specifies U|psi>=i|psi> but not U on
    |phi>=p|psi>.  Choosing U|phi>=+/- i|phi> yields the two amplitudes
    below, so A(lambda) is not fixed by the stated data.
    """

    phase = np.exp(-1j * lambdas)
    return {"u_phi_plus_i": phase, "u_phi_minus_i": -phase}


def task_summary() -> dict[str, object]:
    """Return the exact audit payload used by the case runner."""

    strict = ReferenceModel(system_modes=3, particles=4, reference_modes=5)
    minimal = ReferenceModel(system_modes=3, particles=3, reference_modes=3)
    top_only = ReferenceModel(system_modes=3, particles=3, reference_modes=4)
    bottom_only = ReferenceModel(system_modes=3, particles=4, reference_modes=4)
    lambdas = np.linspace(0.0, 2.0 * np.pi, 9)
    counterexamples = task5_counterexamples(lambdas)
    logical = logical_code_audit()
    signals = ancilla_y_signal(lambdas)
    return {
        "models": {
            "paper_strict_Ms3_N4_Mr5": reference_identity_audit(strict),
            "minimal_Ms3_N3_Mr3": reference_identity_audit(minimal),
            "top_only_Ms3_N3_Mr4": reference_identity_audit(top_only),
            "bottom_only_Ms3_N4_Mr4": reference_identity_audit(bottom_only),
        },
        "mixed_car_max_residual": {
            "paper_strict": mixed_car_residual(strict),
            "minimal": mixed_car_residual(minimal),
        },
        "logical_code": logical,
        "fringe": {
            "lambda": lambdas.tolist(),
            "y_signal": signals.tolist(),
            "theta_principal": calibrated_theta(signals).tolist(),
        },
        "task5_nonuniqueness": {
            "lambda": lambdas.tolist(),
            **{key: value.tolist() for key, value in counterexamples.items()},
        },
        "frozen_verdicts": {
            "task_1": "invalid_unless_N_equals_Ms_and_Mr_equals_N",
            "task_2": "valid",
            "task_3": "invalid_exact_value_is_zero",
            "task_4": "invalid_signal_is_constant_plus_one",
            "task_5": "underdetermined_without_U_on_error_sector",
        },
        "combinatorial_dimension": comb(3, 0) + comb(3, 1) + comb(3, 2) + comb(3, 3),
    }
