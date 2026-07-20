# Source audit

## Verdict

`source_contract_mismatch`.

No PRL source identity was recoverable from the frozen JSON. Two primary sources explain the record:

1. **Huang, Wang & Zhou, arXiv:2501.01155v3 / Phys. Rev. B 111, 174525 (2025).** This is the closest topical candidate already associated with idx16. Its TeX gives the clean eigenbasis Green function, single-impurity T-matrix, LDOS, and the exact C4 cancellation of the gap-odd momentum sum. It is PRB, not PRL, and it does not print the frozen nodal (G_0) or strong-scattering closed form.
2. **Balatsky, Vekhter & Zhu, arXiv:cond-mat/0411318 / Rev. Mod. Phys. 78, 373 (2006).** This is the direct equation source. Its TeX prints (T_{11}=1/[c-g_{11}]), (c=g_{11}(\Omega)), the normalized low-energy local propagator with cutoff (4\Delta_0), and the logarithmic complex pole with \(\log[8/(\pi c)]\).

## Multi-evidence mapping

| Frozen object | 2025 PRB | 2006 RMP | Contract result |
| --- | --- | --- | --- |
| Clean Nambu Green function | General eigenbasis form | Standard formalism | Generic, not source-identifying |
| C4 cancellation of gap-odd term | Explicitly derived | Assumed in particle-hole symmetric reduction | Supported |
| (T_{11}=1/(c-g_{11})) and pole | General determinant T-matrix | Printed directly | RMP direct match |
| Low-energy logarithmic `g0` | Absent | Eq. `impdwave3` | RMP lineage; frozen cutoff and printed imaginary sign differ |
| Closed logarithmic pole | Absent | Eq. `impdwave1` | RMP lineage, frozen expression altered |

## Truth boundary

The 2006 RMP is a valid formula source but cannot repair the benchmark's missing PRL identity. The 2025 PRB cannot be promoted to a direct formula source merely because its topic is close. Therefore this case remains a benchmark audit rather than a paper-level reproduction.
