# Source audit

## Identity

- *Spontaneous Emission Decay and Excitation in Photonic Time Crystals*;
- arXiv:2404.13287;
- Physical Review Letters 135, 133801 (2025);
- DOI: 10.1103/5v2w-yg7v.

## Convention finding

The source Floquet resolvent uses `(omega I-H)^{-1}`, but the projected electric Green tensor includes an external minus at lines 450-459. The source `I_alpha` at lines 648-650 is a separately normalized field intensity. Together these yield the positive Lorentzian term printed in the paper.

The benchmark instead declares `G_0=sum I_alpha/(omega-omega_alpha)` directly. Under that definition the same positive Lorentzian is wrong by a global sign. This distinction localizes the failure to benchmark transcription.

## Method scope

The paper omits singular contributions and takes a lossless remnant limit. It does not define the benchmark's residue-subtraction prescription or its universal toy constants.

## Data finding

The archive ships TeX and rendered PNGs only; no numerical arrays or simulation code are present.
