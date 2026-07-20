# Numerical methods

Remote runtime: NVIDIA A100-SXM4-80GB, CuPy 14.1.1, Python 3.12.7.

```bash
PY=remote-system/projects/rra-2604-torch/bin/python
$PY scripts/run_z3_derivatives_a100.py
$PY scripts/run_odd_z2_vbs_a100.py
$PY scripts/run_z2_matter_bulk_a100.py
$PY scripts/run_z2_vison_a100.py
```

Ground states use matrix-free `cupyx.scipy.sparse.linalg.eigsh`. Vison dynamics
uses a degree-606 double-precision Chebyshev expansion with a conservative
Gershgorin interval [-50,74] and tail bound 8.1e-31.
