# Strongly correlated quantum walks on a 12-qubit processor

## Paper and question

Zhiguang Yan et al., *Strongly correlated quantum walks with a 12-qubit
superconducting processor*, Science **364**, 753–756 (2019), DOI
`10.1126/science.aaw1611`.

The experiment realizes continuous-time walks of one and two microwave photons
on a chain of twelve superconducting transmon qubits. This reproduction focuses
on three linked claims: light-cone-like one-photon information spreading,
fermionization-like antibunching of two photons under strong attractive
interactions, and suppression of double occupancy.

## Core model

The code works directly in fixed-particle-number sectors of the calibrated
Bose–Hubbard Hamiltonian. The one-photon sector has dimension 12, the bosonic
two-photon sector 78, and the hard-core sector 66. One Hamiltonian builder
creates the calibrated, `U=0`, and hard-core variants, while one observable
layer produces density, entropy, connected correlation, concurrence,
two-particle correlators, and double occupancy.

## Results

- Q6, Q1, and Q11 launches cover the full 0–250 ns interval with conserved norm
  and total density.
- The independent velocity scale is 156.33 sites/us, 1.52% from the reported
  153.99 sites/us.
- The mean correlator distance from the calibrated model to the hard-core limit
  is 0.0196, compared with 1.177 to free bosons.
- Peak double occupancy remains below 3%.

The released paper-layout theory figures are accompanied by a sanitized pixel
audit. Mean pattern similarities are 94.67% for one-particle density, 92.54%
for one-particle entropy, 96.34% for two-particle density, and 77.88% for the
S20 correlator grid. The weaker late-time free-boson correlators are reported
without per-panel fitting.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1126-science.aaw1611/code
python scripts/run_reproduction.py
```

The command writes CSV arrays, overview figures, and JSON checks to the sibling
`outputs` directory. See `../docs/DERIVATION.md`, `../docs/NUMERICAL_METHODS.md`,
and `../docs/PIXEL_AUDIT.md` for the scientific contract.

## Evidence boundary

The formal audit score is **80/100**, at numerical-feature level. Author theory
tables, experimental shots, and tomography arrays are unavailable. Publisher
rasters were used for internal validation but are not redistributed. Pixel
similarity therefore measures theoretical panel interiors, not identity with
author arrays or reproduction of experimental noise and calibration.
