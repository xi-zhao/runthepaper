# Derivation

This turns the paper's equations into the exact matrices the code integrates.
Conventions: $\hbar = 1$, rotating frame, time in $\mu s$, frequencies in
$2\pi\cdot\mathrm{MHz}$. Gate time $\tau = 0.25\,\mu s$, blockade
$B = 2\pi\cdot 50$ MHz, Förster penalty $\delta_q = 0$.

## 1. Register encoding and sectors

Three atoms in a line: control qubit, **buffer**, target qubit. The buffer is
prepared in $|1\rangle$ and always driven; the qubit register state $|0\rangle$
is dark (not coupled to any laser). So each two-qubit input evolves in an
independent sector:

$$
|00\rangle\to|010\rangle,\quad
|01\rangle,|10\rangle\to|011\rangle,|110\rangle,\quad
|11\rangle\to|111\rangle .
$$

## 2. Driving waveforms

Every Rabi frequency and detuning is a truncated Fourier series (main text p. 4):

$$
f(t) = \frac{2\pi}{2N+1}\Big(a_0 + 2\sum_{n=1}^{N} a_n\cos\frac{2\pi n t}{\tau}\Big)\ \mathrm{MHz}.
$$

The published coefficients $\{a_n\}$ for each protocol are in
`code/src/coefficients.py`. The buffer atom is driven with $(\Omega_1,\Delta_1)$,
each qubit atom with $(\Omega_2,\Delta_2)$; single-atom coupling
$H=\tfrac{\Omega}{2}(|1\rangle\langle r|+\mathrm{h.c.})+\Delta|r\rangle\langle r|$.

## 3. Interaction (Förster resonance)

An adjacent (buffer, qubit) pair, both in Rydberg, undergoes a Förster exchange to
a second Rydberg pair:

$$
H_{\rm int}=B\big(|r r'\rangle\langle q q'| + |q q'\rangle\langle r r'|\big)
+ \delta_q\,|q q'\rangle\langle q q'| .
$$

Only the two adjacent pairs (control–buffer, buffer–target) interact; the distant
control–target pair does not.

## 4. Sector Hamiltonians (single photon, eqs. a1/a3/a4)

**$|00\rangle$ (buffer only), basis $\{|1_b\rangle,|r_b\rangle\}$ — eq. (a1):**

$$
H_{00}=\begin{pmatrix} 0 & \Omega_1/2 \\ \Omega_1/2 & \Delta_1 \end{pmatrix}.
$$

**$|01\rangle$ (buffer + one qubit), basis
$\{|11\rangle,|r1\rangle,|1r'\rangle,|rr'\rangle,|qq'\rangle\}$ — eq. (a3):**

$$
H_{01}=
\begin{pmatrix}
0 & \tfrac{\Omega_1}{2} & \tfrac{\Omega_2}{2} & 0 & 0\\
\tfrac{\Omega_1}{2} & \Delta_1 & 0 & \tfrac{\Omega_2}{2} & 0\\
\tfrac{\Omega_2}{2} & 0 & \Delta_2 & \tfrac{\Omega_1}{2} & 0\\
0 & \tfrac{\Omega_2}{2} & \tfrac{\Omega_1}{2} & \Delta_1{+}\Delta_2 & B\\
0 & 0 & 0 & B & \Delta_1{+}\Delta_2{+}\delta_q
\end{pmatrix}.
$$

**$|11\rangle$ (three-body) — eq. (a4).** Built directly in the 9-state product
basis $\{|111\rangle,|r'11\rangle,|1r1\rangle,|11r'\rangle,|r'r1\rangle,|1rr'\rangle,|r'1r'\rangle,|q'q1\rangle,|1qq'\rangle\}$
with qubit excitations $\Omega_2/2$, buffer excitations $\Omega_1/2$, Rydberg-count
detunings, and the two Förster couplings $|r'r1\rangle\!\leftrightarrow\!|q'q1\rangle$,
$|1rr'\rangle\!\leftrightarrow\!|1qq'\rangle$ (see `code/src/hamiltonians.py`).

### Morris–Shore cross-check

The paper writes eq. (a4) in a reduced 6-state **bright** basis where the two
identically driven qubit atoms enter only through their symmetric combination,
e.g. $|B_1\rangle=\tfrac{1}{\sqrt2}(|r'11\rangle+|11r'\rangle)$. Starting from
$|111\rangle$, the product form reproduces the published $\sqrt2$ symmetric
couplings, e.g.

$$
\langle 111|H|B_1\rangle=\tfrac{\sqrt2}{2}\,\Omega_2,\qquad
\langle 111|H|1r1\rangle=\tfrac{1}{2}\,\Omega_1,
$$

while the antisymmetric combinations stay dark. We implement this verbatim
6-state form (`h_sector11_bright`) independently and confirm the two give
**identical $|111\rangle$ dynamics to $<10^{-8}$** — this is what upgrades the
formula gate to `verified`.

## 5. Gate metric

Integrating $i\dot\psi = H(t)\psi$ from each sector's initial state gives the four
return amplitudes $a_{00},a_{01},a_{10}=a_{01},a_{11}$ and phases
$\varphi_{ij}=\arg a_{ij}$. The CZ conditional (entangling) phase is

$$
\Phi=\varphi_{11}+\varphi_{00}-2\varphi_{01},
$$

and the gate error is the Pedersen average gate error $1-F_{\rm avg}$ against the
ideal CZ, maximised over the free single-qubit $Z$ phases $(\alpha,\beta)$:

$$
F_{\rm avg}=\frac{|M|^2+\sum_i|a_i|^2}{d(d+1)},\quad d=4,\quad
M=\max_{\alpha,\beta}\big|a_{00}+e^{-i\beta}a_{01}+e^{-i\alpha}a_{10}-e^{-i(\alpha+\beta)}a_{11}\big|.
$$

A perfect CZ has $\Phi=\pi$ and all populations returning to 1. Acceptance is the
paper's own claim, $1-F_{\rm avg}<10^{-4}$ — a falsifiable test a wrong Hamiltonian
cannot pass with the paper's own coefficients.

## 6. Two-photon transition (eqs. a5/a6)

For the two-photon protocols each ground–Rydberg step becomes a ladder through an
intermediate state $|e\rangle$ at a large one-photon detuning
$\Delta_0=2\pi\cdot 5$ GHz:

$$
H_{\rm local}=\frac{\Omega_p}{2}|1\rangle\langle e|+\frac{\Omega_S}{2}|e\rangle\langle r|+\mathrm{h.c.}
+\Delta_0|e\rangle\langle e|+\delta|r\rangle\langle r| .
$$

Per the paper, the many-body Hamiltonian is exactly the single-photon eq. (a4)
with every $|1\rangle\!\leftrightarrow\!|r\rangle$ coupling replaced by this
ladder; the interaction $H_{\rm int}$ is unchanged. We build it as a per-atom
$\{|1\rangle,|e\rangle,|r\rangle,|q\rangle\}$ product (`code/src/hamiltonians_2p.py`).

Adiabatically eliminating $|e\rangle$ would give an effective two-level model with
$\Omega_{\rm eff}=\Omega_p\Omega_S/(2\Delta_0)$ and light shifts $\sim
\Omega_p^2/(4\Delta_0)$. Here $\Omega_p/(2\Delta_0)\approx0.32$ is **not** small,
so we integrate the full ladder instead — see [NUMERICAL_METHODS](NUMERICAL_METHODS.md).

## 7. Doppler-insensitive dual pulse (Fig. 5)

Because each single pulse returns all populations and imparts a conditional phase
$\Phi=\pi/2$, applying it twice composes a full CZ ($\Phi=\pi$). With a residual
atomic velocity $v$ the laser adds a Doppler detuning $\pm k v$ to the driven
transitions; the second pulse comes from the opposite direction, flipping the
sign. Since populations return after each pulse, the accumulated phase is
$\varphi(+kv)+\varphi(-kv)=2\varphi(0)+\mathcal{O}(v^2)$: the first-order velocity
term cancels. The code quantifies this by comparing the end-of-gate phase
deviation of the sign-flipped dual pulse to the un-flipped one.

## 8. Robustness (Fig. 7)

Scaling the buffer and qubit Rabi amplitudes of the Fig. 3(a) waveforms by overall
ratios $r_1,r_2\in[0.99,1.01]$ and mapping the gate error gives the 2-D robustness
colormap, minimal on the $r_1=r_2$ diagonal.
