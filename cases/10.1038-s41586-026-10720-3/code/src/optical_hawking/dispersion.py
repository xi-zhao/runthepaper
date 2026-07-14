"""Paper-derived co-moving dispersion without author data or code.

Nature Fig. 2 is a vector figure.  Its black curve was read directly from the
PDF path and calibrated from the printed axes.  The IR and UV zoom panels
replace the lower-resolution main-panel trace in their domains.  Compact
piecewise Chebyshev fits keep the A100 run independent of PyMuPDF and the
source PDF.  The maximum fit residual inside the plotted domain is 2e-5
rad/fs; the unreported region above 8.107 rad/fs uses tangent extrapolation.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class _ChebyshevSegment:
    lower: float
    upper: float
    coefficients: tuple[float, ...]


_SEGMENTS = (
    _ChebyshevSegment(
        0.0,
        0.9546518994345407,
        (
            0.05325848084649358,
            0.05275318444250595,
            -0.003273497309543422,
            -0.0033245299908951295,
            -0.00027888765560022544,
            0.00034420513770897057,
            6.253825484325216e-05,
            -3.216788128311529e-05,
            -2.8405735191732705e-05,
            2.9856339995393012e-05,
            5.452988789692512e-06,
            -2.4295216693489175e-05,
            7.135806348072761e-06,
            1.416456880424613e-05,
            -1.0184124134495441e-05,
        ),
    ),
    _ChebyshevSegment(
        0.9546518994345407,
        2.3958921200854277,
        (
            0.10117746014912719,
            -7.110331432111343e-05,
            -0.0002241914924356737,
            0.000867962701743055,
            -0.0004532096608294407,
            0.00015153034553027766,
            -4.1550225621623266e-05,
            9.38630264593296e-06,
            -1.475745320930621e-06,
        ),
    ),
    _ChebyshevSegment(
        2.3958921200854277,
        4.5,
        (
            0.10267190283936641,
            -0.00023254968639009786,
            -0.0019407447432401262,
            -0.00043266243809393146,
            1.6371994822119054e-05,
            -2.5934678620709406e-06,
            -7.798117991973072e-07,
        ),
    ),
    _ChebyshevSegment(
        4.5,
        6.5,
        (
            0.07427160380277036,
            -0.031271447244481436,
            -0.005789980281588623,
            -0.0003398404988037893,
            -7.889824963940092e-06,
            -9.018166935768618e-07,
            3.402079784593009e-08,
            5.674836420156586e-07,
            7.539678369246025e-07,
            3.827555369444653e-07,
            -6.304385020326475e-07,
        ),
    ),
    _ChebyshevSegment(
        6.5,
        7.6,
        (
            -0.0028472389204762952,
            -0.04251479015486362,
            -0.0028893762752180397,
            -8.379290502643362e-05,
            -3.0250882202363185e-06,
        ),
    ),
    _ChebyshevSegment(
        7.6,
        7.9,
        (
            -0.06408422222883334,
            -0.01601880725771187,
            -0.0002705094428683344,
            -3.54589840566869e-07,
            -1.592804724670292e-06,
            -5.503960573084142e-07,
            7.878812120775408e-07,
            1.308543284815512e-07,
            6.833259071314188e-09,
        ),
    ),
    _ChebyshevSegment(
        8.062013851176069,
        8.107000506725724,
        (
            -0.10227718886751473,
            -0.00278023677337426,
            -6.728009078639335e-06,
            -1.0482653137449334e-08,
            5.918003522193608e-09,
        ),
    ),
)

_BRIDGE_LOWER = 7.9
_BRIDGE_UPPER = 8.062013851176069
_BRIDGE_Y0 = -0.0803754991192126
_BRIDGE_DY0 = -0.11415111354611868
_BRIDGE_Y1 = -0.09950369555260621
_BRIDGE_DY1 = -0.12675142196392972
_UV_END = 8.107000506725724
_UV_END_VALUE = -0.10506420501354279
_UV_END_SLOPE = -0.12141311833680454


def _evaluate_segment(omega: torch.Tensor, segment: _ChebyshevSegment) -> torch.Tensor:
    x = (2.0 * omega - segment.lower - segment.upper) / (segment.upper - segment.lower)
    coefficients = segment.coefficients
    b_k_plus_1 = torch.zeros_like(x)
    b_k_plus_2 = torch.zeros_like(x)
    for coefficient in reversed(coefficients[1:]):
        b_k = 2.0 * x * b_k_plus_1 - b_k_plus_2 + coefficient
        b_k_plus_2 = b_k_plus_1
        b_k_plus_1 = b_k
    return x * b_k_plus_1 - b_k_plus_2 + coefficients[0]


def _hermite_bridge(omega: torch.Tensor) -> torch.Tensor:
    width = _BRIDGE_UPPER - _BRIDGE_LOWER
    s = (omega - _BRIDGE_LOWER) / width
    h00 = 2.0 * s**3 - 3.0 * s**2 + 1.0
    h10 = s**3 - 2.0 * s**2 + s
    h01 = -2.0 * s**3 + 3.0 * s**2
    h11 = s**3 - s**2
    return (
        h00 * _BRIDGE_Y0
        + h10 * width * _BRIDGE_DY0
        + h01 * _BRIDGE_Y1
        + h11 * width * _BRIDGE_DY1
    )


class PaperTracedDispersion:
    """Co-moving frequency omega'(omega) reconstructed from Nature Fig. 2."""

    source = "Nature Fig. 2 vector path; no author data or code"
    plotted_upper_rad_fs = _UV_END
    fit_residual_rad_fs = 2.0e-5

    def omega_prime(self, omega_rad_fs: torch.Tensor) -> torch.Tensor:
        omega = torch.clamp_min(omega_rad_fs, 0.0)
        result = torch.zeros_like(omega)
        for segment in _SEGMENTS[:-1]:
            value = _evaluate_segment(omega, segment)
            result = torch.where(
                (omega >= segment.lower) & (omega < segment.upper), value, result
            )
        bridge = _hermite_bridge(omega)
        result = torch.where(
            (omega >= _BRIDGE_LOWER) & (omega < _BRIDGE_UPPER), bridge, result
        )
        uv_segment = _SEGMENTS[-1]
        uv_value = _evaluate_segment(omega, uv_segment)
        result = torch.where(
            (omega >= uv_segment.lower) & (omega <= uv_segment.upper), uv_value, result
        )
        extrapolated = _UV_END_VALUE + _UV_END_SLOPE * (omega - _UV_END)
        result = torch.where(omega > _UV_END, extrapolated, result)
        return torch.where(omega_rad_fs > 0, result, torch.zeros_like(result))
