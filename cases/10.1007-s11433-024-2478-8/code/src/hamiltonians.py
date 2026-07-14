"""Sector Hamiltonians for the buffer-atom-mediated (BAM) CZ gate, single photon.

Order of the three physical atoms is (control qubit, buffer, target qubit).  The
buffer atom is always prepared in |1>; qubit register state |0> is dark.  Each
two-qubit register input therefore maps to an independent three-body sector:

    |00> -> |010>  : only the buffer couples          -> H_sector00  (2 states)  [eq. a1]
    |01> -> |011>  } one buffer + one qubit atom       -> H_sector01  (5 states)  [eq. a3]
    |10> -> |110>  }   (symmetric; same spectrum)
    |11> -> |111>  : full three-body dynamics          -> H_sector11  (9 states)  [eq. a4]

Local driving:  buffer atom 1<->r with (Omega1, Delta1);  each qubit atom
1<->r' with (Omega2, Delta2).  The Rydberg dipole-dipole interaction is modelled
(as in the appendix) as a Foerster resonance: an adjacent (buffer, qubit) pair in
|r r'> couples with strength B to the pair state |q q'> at extra energy delta_q.
Only the two adjacent pairs (control-buffer, buffer-target) interact; the distant
control-target pair is neglected.  Convention (appendix): H = (Omega/2)(|g><e|+h.c.)
+ Delta |e><e|, with hbar = 1.

The |11> sector is built directly in the 9-state product basis.  This is provably
equivalent to the paper's Morris-Shore-reduced eq. (a4): the symmetric qubit
combinations reproduce the published sqrt(2) couplings, while the antisymmetric
combinations stay dark when starting from |111> (verified as a sanity check).
"""
from __future__ import annotations

import numpy as np

# --- sector |00>: buffer atom alone -----------------------------------------
# basis: 0=|1_b>, 1=|r_b>
SECTOR00_BASIS = ("1_b", "r_b")
SECTOR00_INIT = 0

# --- sector |01|/|10>: buffer + one qubit atom ------------------------------
# basis: 0=|1 1>, 1=|r 1>, 2=|1 r'>, 3=|r r'>, 4=|q q'>   (first slot buffer)
SECTOR01_BASIS = ("1b1u", "rb1u", "1br'u", "rbr'u", "qbq'u")
SECTOR01_INIT = 0

# --- sector |11>: control + buffer + target ---------------------------------
# basis (control, buffer, target):
SECTOR11_BASIS = (
    "111",     # 0  all ground-|1>
    "r'11",    # 1  control Rydberg
    "1r1",     # 2  buffer Rydberg
    "11r'",    # 3  target Rydberg
    "r'r1",    # 4  control+buffer Rydberg  (adjacent pair)
    "1rr'",    # 5  buffer+target Rydberg   (adjacent pair)
    "r'1r'",   # 6  control+target Rydberg  (buffer ground; non-adjacent, no Foerster)
    "q'q1",    # 7  Foerster partner of state 4
    "1qq'",    # 8  Foerster partner of state 5
)
SECTOR11_INIT = 0


def h_sector00(omega1, delta1):
    """2x2 buffer-only Hamiltonian (eq. a1)."""
    h = np.zeros((2, 2), dtype=complex)
    h[0, 1] = omega1 / 2.0
    h[1, 0] = omega1 / 2.0
    h[1, 1] = delta1
    return h


def h_sector01(omega1, omega2, delta1, delta2, B, delta_q):
    """5x5 buffer+qubit Hamiltonian (eq. a3)."""
    h = np.zeros((5, 5), dtype=complex)
    # buffer excitation Omega1: |11>-|r1|, |1r'>-|rr'|
    h[0, 1] = h[1, 0] = omega1 / 2.0
    h[2, 3] = h[3, 2] = omega1 / 2.0
    # qubit excitation Omega2: |11>-|1r'|, |r1>-|rr'|
    h[0, 2] = h[2, 0] = omega2 / 2.0
    h[1, 3] = h[3, 1] = omega2 / 2.0
    # detunings
    h[1, 1] = delta1
    h[2, 2] = delta2
    h[3, 3] = delta1 + delta2
    h[4, 4] = delta1 + delta2 + delta_q
    # Foerster dipole-dipole coupling |rr'> <-> |qq'>
    h[3, 4] = h[4, 3] = B
    return h


def h_sector11(omega1, omega2, delta1, delta2, B, delta_q):
    """9x9 three-body Hamiltonian in the product basis (equivalent to eq. a4)."""
    h = np.zeros((9, 9), dtype=complex)
    o1 = omega1 / 2.0  # buffer 1<->r
    o2 = omega2 / 2.0  # qubit  1<->r'

    # control-qubit excitation (Omega2)
    for i, j in [(0, 1), (2, 4), (3, 6)]:  # |111>-|r'11>, |1r1>-|r'r1>, |11r'>-|r'1r'>
        h[i, j] = h[j, i] = o2
    # target-qubit excitation (Omega2)
    for i, j in [(0, 3), (1, 6), (2, 5)]:  # |111>-|11r'>, |r'11>-|r'1r'>, |1r1>-|1rr'>
        h[i, j] = h[j, i] = o2
    # buffer excitation (Omega1)
    for i, j in [(0, 2), (1, 4), (3, 5)]:  # |111>-|1r1>, |r'11>-|r'r1>, |11r'>-|1rr'>
        h[i, j] = h[j, i] = o1
    # (buffer excitation out of |r'1r'| would give a triply-excited state -> blockaded)

    # detunings (count Rydberg quanta: control r'->Delta2, target r'->Delta2, buffer r->Delta1)
    diag = {
        0: 0.0,
        1: delta2,
        2: delta1,
        3: delta2,
        4: delta1 + delta2,
        5: delta1 + delta2,
        6: 2.0 * delta2,
        7: delta1 + delta2 + delta_q,
        8: delta1 + delta2 + delta_q,
    }
    for k, v in diag.items():
        h[k, k] = v

    # Foerster dipole-dipole couplings on the two adjacent pairs
    h[4, 7] = h[7, 4] = B  # |r'r1> <-> |q'q1>
    h[5, 8] = h[8, 5] = B  # |1rr'> <-> |1qq'>
    return h


# Antisymmetric (dark) combinations in the |11> sector, used as an internal check:
# starting from |111> they must stay unpopulated for all time.
SECTOR11_DARK_PAIRS = ((1, 3), (4, 5), (7, 8))


# --- sector |11>, Morris-Shore bright form transcribed verbatim from eq. (a4) ---
# 6-state bright basis (the two identically-driven qubit atoms enter only through
# their symmetric combination):
#   0=|111>, 1=|B1>=(|r'11>+|11r'>)/sqrt2, 2=|1r1>,
#   3=|B2>=(|r'r1>+|1rr'>)/sqrt2, 4=|r'1r'>, 5=|Bq>=(|q'q1>+|1qq'>)/sqrt2
# Couplings exactly as written in eq. (a4):
#   <111|H|B1> = (sqrt2/2) Omega2      <111|H|1r1> = (1/2) Omega1
#   <B1|H|B2>  = (1/2) Omega1          <B1|H|r'1r'> = (sqrt2/2) Omega2
#   <1r1|H|B2> = (sqrt2/2) Omega2      <B2|H|Bq>   = B
# Diagonals: B1->Delta2, 1r1->Delta1, B2->Delta1+Delta2, r'1r'->2*Delta2,
#            Bq->Delta1+Delta2+delta_q.
SECTOR11_BRIGHT_BASIS = ("111", "B1", "1r1", "B2", "r'1r'", "Bq")


def h_sector11_bright(omega1, omega2, delta1, delta2, B, delta_q):
    """6x6 three-body Hamiltonian, Morris-Shore reduced form (eq. a4 verbatim)."""
    import numpy as _np

    h = _np.zeros((6, 6), dtype=complex)
    r2 = _np.sqrt(2.0) / 2.0  # sqrt(2)/2
    h[0, 1] = h[1, 0] = r2 * omega2
    h[0, 2] = h[2, 0] = 0.5 * omega1
    h[1, 3] = h[3, 1] = 0.5 * omega1
    h[1, 4] = h[4, 1] = r2 * omega2
    h[2, 3] = h[3, 2] = r2 * omega2
    h[3, 5] = h[5, 3] = B
    h[1, 1] = delta2
    h[2, 2] = delta1
    h[3, 3] = delta1 + delta2
    h[4, 4] = 2.0 * delta2
    h[5, 5] = delta1 + delta2 + delta_q
    return h


SECTOR11_BRIGHT_INIT = 0
