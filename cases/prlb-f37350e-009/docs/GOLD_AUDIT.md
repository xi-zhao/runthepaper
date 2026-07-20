# Frozen-gold audit

Terminal verdict: `benchmark_gold_invalid`.

| Item | Verdict | Independent result |
| --- | --- | --- |
| 1 | valid | Eliminating `beta` between `n_t=2 beta+4` and `epsilon=(beta+2)/(beta+1)` gives `n_t=-2 epsilon/(1-epsilon)`. |
| 2.1 | valid | A finite jump in `a''/a` gives `beta_k = Delta(a''/a)e^(i phi)/(4k^2)+...`. |
| 2.2 | valid | Therefore `|beta_k|^2 proportional to k^-4`. |
| 2.3 | valid with wording caveat | For continuous nonzero `a`, a finite jump in `a''` is equivalently a jump in `a''/a`. |
| 3.1 | semantic error | The second displayed spectrum is pressure, but the frozen answer labels both formulas `rho_k`. |
| 3.2 WKB amplitude | valid | The amplitude equals `(2k)^-1[1-V/(2k^2)+(3V^2+V'')/(8k^4)]`, with `V=m^2a^2-a''/a`. |
| 3.2 counterterms | **invalid** | Direct substitution of that amplitude into the prompt's own `rho_k,p_k` definitions yields different mass powers and signs. |
| 3.3 | **incomplete** | The question requests separate leading `rho_k^re` and `p_k^re`; the frozen answer gives only a ratio. |
| 3.4 scalar | **invalid** | The derived massless scalar ratio is `(beta+7)/(3(beta+1))`, the reciprocal of the frozen result. |
| 3.4 RGW | formula valid, conclusion **invalid** | `w_RGW=(beta-2)/(3(beta+4))`; hence `w=1` at `beta=-7`. At frozen `beta=-2`, it equals `-2/3`, not `1`. |

## Counterterm contradiction

Write `t=-tau>0`, `a=t^(1+beta)`, and normalize each fourth-order
counterterm by `k^4/(8 pi^2 a^4)`. Independent WKB substitution gives

```text
Rho4 = 2 + [(beta+1)^2 + m^2 t^(4+2 beta)]/(t^2 k^2)
       + [3 beta^4+12 beta^3+15 beta^2+6 beta
          +2(beta+1)^2 m^2 t^(4+2 beta)-m^4 t^(8+4 beta)]/(4 t^4 k^4)

P4   = 2/3 + [beta^2+4 beta+3-m^2 t^(4+2 beta)]/(3 t^2 k^2)
       + [3 beta^4+24 beta^3+51 beta^2+30 beta
          +(2-2 beta^2)m^2 t^(4+2 beta)+3m^4t^(8+4 beta)]/(12 t^4 k^4)
```

At `(beta,m,t,k)=(-2.2,0.3,0.8,7)`, the machine-readable audit records the
correct and frozen brackets and their nonzero differences. This is an internal
consistency check, not reliance on another gold answer.

## Equation-of-state check

For the massless minimally coupled scalar, the high-frequency residual pieces
from the same mode expansion give

```text
rho_re proportional to 2 F (beta+1)
p_re   proportional to 2 F (beta+7)/3
```

so `w_scalar=(beta+7)/(3(beta+1))`. The scalar fixed points remain `beta=2`
for stiff matter and `beta=-2.5` for dark energy, although `beta=2` is outside
the usual power-law inflation regime `beta<-2`. For RGW, the correct stiff
point is `beta=-7`; both sectors share the dark-energy point `beta=-2.5`.

Evidence: `outputs/data/idx9_gold_audit.json`,
`src/power_law_audit.py`, and `tests/test_power_law_audit.py`.
