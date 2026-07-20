# Frozen-gold audit

Verdict: `benchmark_source_invalid_gold_valid`.

- Tasks 1–3 match the 2024 PRL: rotating Hamiltonian sign, `B`, `C`, `K=4`, and `gamma proportional to a_in^(-9/2)` are correct.
- Task 4: independent SI-unit evaluation gives `gamma0=0.6475310621649106`, hence `0.648` and `gamma0<1`.
- Task 5: `a_in,res=0.42 gamma0^(2/9)=0.38133546981629685 AU`, hence `0.381 AU`.
- Task 6: at resonance, `D=2.88`, `C=0.236801326711099`, and `C/D=0.08222268288579825`; the rounded peak `0.082` and the judgment `0.08<peak` are correct.
- Task 7 matches the source Poincaré action and captured-orbit trend: eccentricity increases as the PRL-convention gamma increases.
- All frozen answers are valid. The failure is the source contract: the direct PRL is from 2024, while the 2025 ApJL is not PRL and reverses the gamma ratio.

Separate paper finding: Supplemental Fig. C's displayed quadratic solution uses a radicand parameter equal to `-H/D`, although its prose calls it `H/D`; consequently the blue/red energy-sign labels are reversed. The zero-energy separatrix and the frozen peak result are unaffected.
