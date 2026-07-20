# Lessons learned

## New Failure Modes

- Always classify a constrained stationary point with the tangent Hessian; branch existence alone does not determine its Morse index.
- A minimax path barrier and `max(U)-min(U)` are separate operations. Both arcs and every endpoint must be included.
- Check that a requested saddle exists before differentiating it. Implicit differentiation can correctly track the wrong physical branch.
- For nonconservative stationary motion, solve all generalized-coordinate equations. Static-potential intuition cannot exclude a damping-supported orbit.

## Reusable Checks Or Tools

- Add a tangent-Hessian classifier for constrained extrema.
- Add an extremum-existence gate before implicit response calculations.
- Require direct residual substitution for every claimed nonexistence result in a driven-dissipative system.

These checks were copied_to_backlog for reuse across later cases.
