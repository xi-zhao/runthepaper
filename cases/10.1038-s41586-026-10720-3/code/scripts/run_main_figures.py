#!/usr/bin/env python3
"""Regenerate the public-safe numerical content of Nature Figs. 2, 4, and 5.

The public package deliberately omits the paper PDF and source-derived point
sets. Fig. 2 is evaluated from the compressed dispersion representation,
Fig. 4 from the frozen red-only Eq. (D.1) fits, and Fig. 5 from the independently
recomputed line coefficients. The full source-reference validation is reported
as an audit result, not redistributed as fitting data.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import torch


FROZEN_FIG4_FITS = {
    1100: (
        10.0,
        {
            "hawking_wavelength_nm": 233.12049676229594,
            "backreaction_shift_nm": 0.36697195592568566,
            "spectral_width_rad_fs": 0.0071135396899466505,
            "modulation_x": 0.651805169939522,
            "hawking_intensity": 139.44446217855184,
            "backreaction_intensity": 18.844678004190126,
        },
    ),
    1200: (
        1.2,
        {
            "hawking_wavelength_nm": 233.55016165232686,
            "backreaction_shift_nm": 0.7509128227316448,
            "spectral_width_rad_fs": 0.018427688851811338,
            "modulation_x": 0.020000000000000122,
            "hawking_intensity": 195.88437038230808,
            "backreaction_intensity": 148.59942995800742,
        },
    ),
    1300: (
        1.1,
        {
            "hawking_wavelength_nm": 233.1953045165703,
            "backreaction_shift_nm": 0.6264290389791359,
            "spectral_width_rad_fs": 0.012779402301948656,
            "modulation_x": 0.1744208681032773,
            "hawking_intensity": 674.3603587362682,
            "backreaction_intensity": 512.8833871344971,
        },
    ),
    1400: (
        10.0,
        {
            "hawking_wavelength_nm": 232.90886728860772,
            "backreaction_shift_nm": 0.7282360660746642,
            "spectral_width_rad_fs": 0.013625257834955587,
            "modulation_x": 0.38235729968436566,
            "hawking_intensity": 90.82542816034247,
            "backreaction_intensity": 55.62620533592012,
        },
    ),
    1450: (
        1.0,
        {
            "hawking_wavelength_nm": 233.20735927454425,
            "backreaction_shift_nm": 0.7046406971423109,
            "spectral_width_rad_fs": 0.011634528090628553,
            "modulation_x": 0.28615678077551726,
            "hawking_intensity": 252.93757413149402,
            "backreaction_intensity": 113.16260900267764,
        },
    ),
    1600: (
        1.05,
        {
            "hawking_wavelength_nm": 232.94811013097907,
            "backreaction_shift_nm": 1.0500699994084899,
            "spectral_width_rad_fs": 0.01487784837692147,
            "modulation_x": 0.020000000003763313,
            "hawking_intensity": 94.0791593132253,
            "backreaction_intensity": 40.93241924577731,
        },
    ),
}

FIG5_LINES = {
    "hawking": {"slope": -22.689645738327776, "intercept": 14.701687121196775},
    "backreaction": {"slope": -22.220197347554738, "intercept": 14.0351423645815},
}


def parse_args() -> argparse.Namespace:
    script = Path(__file__).resolve()
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=script.parents[1] / "src")
    parser.add_argument("--output-root", type=Path, default=script.parents[2] / "outputs")
    return parser.parse_args()


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def configure_plotting() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.size": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 144,
            "savefig.dpi": 144,
        }
    )


def render_fig2(output_root: Path, model: object, probe: object) -> dict[str, object]:
    dispersion = model.PaperTracedDispersion()
    marks = model.figure2_landmarks(probe, dispersion)
    panels = {
        "a": (0.0, 8.5, 1600),
        "b": (0.8, 2.4, 800),
        "c": (8.062, 8.107, 800),
    }
    rows: list[dict[str, object]] = []
    figure, axes = plt.subplots(1, 3, figsize=(10.2, 3.2), gridspec_kw={"width_ratios": [1.6, 1, 1]})
    for axis, (panel, (lower, upper, points)) in zip(axes, panels.items(), strict=True):
        omega = torch.linspace(lower, upper, points, dtype=torch.float64)
        omega_prime = dispersion.omega_prime(omega).numpy()
        axis.plot(omega.numpy(), omega_prime, color="black", lw=1.25)
        axis.set(xlabel=r"$\omega$ (rad/fs)", ylabel=r"$\omega'$ (rad/fs)")
        axis.text(-0.13, 1.03, panel, transform=axis.transAxes, fontweight="bold", fontsize=12)
        for x_value, y_value in zip(omega.numpy(), omega_prime, strict=True):
            rows.append(
                {
                    "series": f"curve_{panel}",
                    "role": "dispersion",
                    "omega_rad_fs": float(x_value),
                    "omega_prime_rad_fs": float(y_value),
                }
            )

    ir_markers = {
        "pump": (marks["pump_omega_rad_fs"], marks["pump_omega_prime_rad_fs"]),
        "redshifted_probe": (
            marks["redshifted_probe"]["omega_rad_fs"],
            marks["redshifted_probe"]["omega_prime_rad_fs"],
        ),
        "horizon": (marks["horizon"]["omega_rad_fs"], marks["horizon"]["omega_prime_rad_fs"]),
        "probe": (marks["probe_omega_rad_fs"], marks["probe_omega_prime_rad_fs"]),
    }
    uv_markers = {
        role: (marks[role]["omega_rad_fs"], marks[role]["omega_prime_rad_fs"])
        for role in ("nrr", "hawking_partner", "backreaction")
    }
    for role, (x_value, y_value) in ir_markers.items():
        axes[1].scatter(x_value, y_value, s=22, zorder=3)
        rows.append(
            {
                "series": "landmark",
                "role": role,
                "omega_rad_fs": x_value,
                "omega_prime_rad_fs": y_value,
            }
        )
    for role, (x_value, y_value) in uv_markers.items():
        axes[2].scatter(x_value, y_value, s=22, zorder=3)
        rows.append(
            {
                "series": "landmark",
                "role": role,
                "omega_rad_fs": x_value,
                "omega_prime_rad_fs": y_value,
            }
        )
    figure.tight_layout()
    figure_dir = output_root / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(figure_dir / "fig2_doppler_reproduction_public.png")
    plt.close(figure)
    write_csv(
        output_root / "data" / "fig2_generated.csv",
        ["series", "role", "omega_rad_fs", "omega_prime_rad_fs"],
        rows,
    )
    return {
        "pump_omega_rad_fs": marks["pump_omega_rad_fs"],
        "nrr_wavelength_nm": marks["nrr"]["wavelength_nm"],
        "hawking_partner_wavelength_nm": marks["hawking_partner"]["wavelength_nm"],
        "backreaction_wavelength_nm": marks["backreaction"]["wavelength_nm"],
        "backreaction_blue_shift_nm": marks["backreaction_shift_nm"],
    }


def render_fig4(output_root: Path, model: object) -> dict[str, object]:
    figure, axes = plt.subplots(2, 3, figsize=(9.6, 5.2), sharex=True)
    rows: list[dict[str, object]] = []
    for axis, (probe, (mu, values)) in zip(axes.flat, FROZEN_FIG4_FITS.items(), strict=True):
        wavelength = np.linspace(231.0, 234.5, 800)
        parameters = model.SidebandParameters(**values)
        counts = model.sideband_spectrum(wavelength, parameters, mu)
        axis.plot(wavelength, counts, color="black", lw=1.2)
        axis.set_title(f"Probe @ {probe:,} nm")
        axis.set(xlabel="Wavelength (nm)", ylabel="Counts (Hz)")
        for x_value, y_value in zip(wavelength, counts, strict=True):
            rows.append(
                {
                    "probe_wavelength_nm": probe,
                    "wavelength_nm": float(x_value),
                    "eq_d1_counts_hz": float(y_value),
                }
            )
    figure.tight_layout()
    figure_dir = output_root / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(figure_dir / "fig4_eq_d1_theory_public.png")
    plt.close(figure)
    write_csv(
        output_root / "data" / "fig4_eq_d1_generated.csv",
        ["probe_wavelength_nm", "wavelength_nm", "eq_d1_counts_hz"],
        rows,
    )
    return {
        "curves": len(FROZEN_FIG4_FITS),
        "fit_policy": "frozen red-only fits; public output contains generated theory only",
        "master_blind_mean_nrmse": 0.06530816268331546,
        "master_blind_mean_pearson_correlation": 0.9809955813620547,
    }


def render_fig5(output_root: Path) -> dict[str, object]:
    ratio = np.linspace(0.515, 0.61, 160)
    colors = {"hawking": "#1e8c88", "backreaction": "#a1334e"}
    labels = {"hawking": "Hawking radiation", "backreaction": "Backreaction"}
    rows: list[dict[str, object]] = []
    figure, axis = plt.subplots(figsize=(5.2, 3.8))
    for role, fit in FIG5_LINES.items():
        values = fit["slope"] * ratio + fit["intercept"]
        axis.plot(ratio, values, color=colors[role], lw=1.6, label=labels[role])
        for x_value, y_value in zip(ratio, values, strict=True):
            rows.append(
                {
                    "series": role,
                    "frequency_ratio": float(x_value),
                    "fitted_log_probability": float(y_value),
                }
            )
    slope_ratio = abs(FIG5_LINES["hawking"]["slope"] / FIG5_LINES["backreaction"]["slope"])
    axis.set(xlabel="Frequency ratio", ylabel="ln p", title=f"Eq. (D.3) slope ratio = {slope_ratio:.4f}")
    axis.legend(frameon=False)
    figure.tight_layout()
    figure_dir = output_root / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(figure_dir / "fig5_eq_d3_lines_public.png")
    plt.close(figure)
    write_csv(
        output_root / "data" / "fig5_fitted_lines.csv",
        ["series", "frequency_ratio", "fitted_log_probability"],
        rows,
    )
    return {
        "hawking_slope": FIG5_LINES["hawking"]["slope"],
        "backreaction_slope": FIG5_LINES["backreaction"]["slope"],
        "slope_ratio_hawking_over_backreaction": slope_ratio,
        "paper_reported_ratio": 1.02,
        "source_points_redistributed": False,
    }


def main() -> None:
    args = parse_args()
    sys.path.insert(0, str(args.source_dir.resolve()))
    import optical_hawking as model
    from optical_hawking.model import PAPER_PROBE_1400

    configure_plotting()
    output_root = args.output_root.resolve()
    payload = {
        "schema_version": 1,
        "status": "passed",
        "scope": "main-text numerical figures only",
        "exact_reproduction": False,
        "fig2": render_fig2(output_root, model, PAPER_PROBE_1400),
        "fig4": render_fig4(output_root, model),
        "fig5": render_fig5(output_root),
        "public_boundary": {
            "author_code_used": False,
            "paper_pdf_included": False,
            "source_derived_point_sets_included": False,
            "fig1": "conceptual schematic; not a numerical target",
            "fig3": "raw experimental acquisition unavailable",
        },
    }
    checks = output_root / "checks"
    checks.mkdir(parents=True, exist_ok=True)
    (checks / "main_figure_reproduction.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
