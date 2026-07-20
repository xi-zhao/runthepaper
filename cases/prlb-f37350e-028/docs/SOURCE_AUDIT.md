# Source audit

The direct source is Shui-Sen Zhang *et al.*, “Deterministic Switching of the Néel Vector by Asymmetric Spin Torque,” *Physical Review Letters* **136**, 096702 (2026), DOI `10.1103/fkyr-z5b8`, arXiv:2506.10786. It was published on 2026-03-02 in Volume 136 Issue 9, inside PRL-Bench's declared Volume 135 Issue 7 through Volume 136 Issue 10 window.

The accepted paper's Eqs. (7)-(8) reproduce the benchmark Lagrangian and Rayleigh function term by term. The benchmark's static potential is their zero-velocity conservative sector. This is therefore a direct, high-confidence source match.

The source also provides a decisive Task 4 check. For `beta=pi`, it lists three stationary solution classes; the third has `0<Theta<pi` and constant azimuthal motion, i.e. the rigid-precession branch that the frozen answer says cannot exist.

The arXiv e-print endpoint serves the accepted Microsoft-Word PDF rather than TeX source. The record exposes neither author simulation code nor numerical arrays. This does not block the four benchmark tasks, which close analytically, but it blocks pixel-level reproduction of the paper's numerical phase diagrams.
