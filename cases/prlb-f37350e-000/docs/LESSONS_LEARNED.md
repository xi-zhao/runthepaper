# Lessons learned

## New Failure Modes

- A missing exponent can hide because downstream numerical answers silently use the correct source formula.
- Defining a Stokes convention does not define an incident polarization state.
- A verbatim old PRL formula block can masquerade as a new-paper benchmark unless title, date, and DOI are audited.
- Source vector artwork is a reference artifact, not independent reproduction evidence.

## Reusable Checks Or Tools

- Cross-evaluate every displayed equation against every numerical example that depends on it.
- For discrete polarization answers, enumerate all unspecified initial modes before accepting a sign.
- Use exact curve invariants, here `K_+K_-=-1`, in addition to visual comparison.
