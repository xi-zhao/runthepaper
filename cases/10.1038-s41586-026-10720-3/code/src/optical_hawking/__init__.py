"""Public numerical core for the optical Hawking reproduction."""

from .analysis import figure2_landmarks, phase_matching_from_angular_frequencies
from .dispersion import PaperTracedDispersion
from .model import PAPER_PROBE_1400
from .theory import SidebandParameters, sideband_spectrum

__all__ = [
    "PAPER_PROBE_1400",
    "PaperTracedDispersion",
    "SidebandParameters",
    "figure2_landmarks",
    "phase_matching_from_angular_frequencies",
    "sideband_spectrum",
]
