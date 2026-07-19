# Lessons learned

- A printed rational approximant is not always the convention that produced a
  source curve.  The exact golden ratio removes the Fig. 2 IPR mismatch.
- Boundary conditions and lattice origins must be treated as target-local
  numerical conventions.  Periodic Fig. 2 and open-boundary Fig. S1 are both
  supported by their visible finite-chain structure.
- Pixel similarity is meaningful only after matching canvas and axes geometry.
  It must never replace a parameter or formula gate.
- PDF vector paths are strong audit references when author tables are absent,
  but they are not generation inputs and do not reveal omitted solver metadata.
- Missing pump samples, continuation rules, or normalization constants should
  cap the evidence tier even when the rendered figure looks close.

The reusable practice is therefore: derive first, generate independent data,
register the paper geometry, compare against reference vectors, and report the
remaining convention uncertainty separately from visual quality.
