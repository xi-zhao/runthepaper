from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from lyapunov_band import write_json


FIGURE_SPECS = {
    "fig3": {"size_points": (264.747, 204.967), "pixels_180dpi": (662, 513)},
    "fig4": {"size_points": (273.922, 98.9666), "pixels_180dpi": (685, 248)},
    "fig5": {"size_points": (224.398, 98.4269), "pixels_180dpi": (561, 247)},
}


def plot_paper_exact(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    data_dir = workspace / "outputs" / "data"
    figure_dir = workspace / "outputs" / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    required = [
        data_dir / "paper_ed_histograms.npz",
        data_dir / "paper_fig34_theory.npz",
        data_dir / "paper_fig5_contours.npz",
        data_dir / "paper_alpha.csv",
        data_dir / "paper_profiles.npz",
        data_dir / "paper_scaling.csv",
    ]
    missing = [str(path.relative_to(workspace)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"paper-matched plotting inputs are missing: {missing}")

    _configure_matplotlib()
    outputs = {
        "fig3": _plot_fig3(data_dir, figure_dir),
        "fig4": _plot_fig4(data_dir, figure_dir),
        "fig5": _plot_fig5(data_dir, figure_dir),
    }
    qa = _run_geometry_qa(workspace, outputs)
    result = {
        "status": "passed" if qa["geometry_all_exact"] else "failed",
        "artifact_stage": "paper_matched_reproduction",
        "parameter_match": "paper_reported_plus_documented_inference",
        "figures": outputs,
        "geometry_qa": qa,
    }
    write_json(workspace / "outputs" / "checks" / "paper_plot_artifacts.json", result)
    return result


def _plot_fig3(data_dir: Path, figure_dir: Path) -> dict[str, str]:
    ed = _load_npz(data_dir / "paper_ed_histograms.npz")
    theory = _load_npz(data_dir / "paper_fig34_theory.npz")
    profiles = _load_npz(data_dir / "paper_profiles.npz")
    scaling = _read_csv(data_dir / "paper_scaling.csv")
    spec = FIGURE_SPECS["fig3"]
    width_px, height_px = spec["pixels_180dpi"]
    fig = _new_figure(spec["size_points"])
    cmap = _paper_density_colormap()

    axis_a = _add_axis_px(fig, (width_px, height_px), (64, 13, 292, 202))
    cax_a = _add_axis_px(fig, (width_px, height_px), (309, 13, 324, 202))
    axis_c = _add_axis_px(fig, (width_px, height_px), (65, 268, 293, 457))
    cax_c = _add_axis_px(fig, (width_px, height_px), (310, 268, 325, 457))
    axis_d = _add_axis_px(fig, (width_px, height_px), (413, 270, 641, 459))
    profile_axes = [
        _add_axis_px(fig, (width_px, height_px), box)
        for box in ((413, 12, 641, 75), (413, 75, 641, 138), (413, 138, 641, 201))
    ]

    extent = [-2.5, 4.5, -0.9, 0.9]
    image_a = axis_a.imshow(
        ed["obc_density"],
        origin="lower",
        extent=extent,
        aspect="auto",
        interpolation="bilinear",
        cmap=cmap,
        vmin=0.0,
        vmax=8.0,
        rasterized=True,
    )
    axis_a.plot(-1.05, 0.32, marker="s", ms=3.4, mfc="none", mec="#ff0000", mew=0.7, linestyle="none")
    axis_a.plot(-0.82, 0.24, marker="^", ms=3.8, mfc="none", mec="#ff9900", mew=0.7, linestyle="none")
    axis_a.plot(-0.60, 0.00, marker="*", ms=4.2, mfc="none", mec="#0000ff", mew=0.7, linestyle="none")
    _style_spectrum_axis(axis_a, ylim=(-0.9, 0.9))
    _style_density_colorbar(fig, image_a, cax_a)

    image_c = axis_c.imshow(
        np.clip(theory["obc_density"], 0.0, None),
        origin="lower",
        extent=extent,
        aspect="auto",
        interpolation="bilinear",
        cmap=cmap,
        vmin=0.0,
        vmax=8.0,
        rasterized=True,
    )
    _plot_zero_contours(
        axis_c,
        theory["real_axis"],
        theory["imag_axis"],
        theory["exponents"],
        color="#ff00ff",
        linewidth=0.65,
    )
    axis_c.annotate(
        "mobility edge",
        xy=(0.25, -0.02),
        xytext=(-0.25, -0.47),
        color="white",
        fontsize=8,
        ha="center",
        arrowprops={"arrowstyle": "-", "color": "white", "lw": 0.55},
    )
    _style_spectrum_axis(axis_c, ylim=(-0.9, 0.9))
    _style_density_colorbar(fig, image_c, cax_c)

    site = profiles["site"]
    for profile in profiles["alm_profiles"]:
        profile_axes[0].plot(site, profile, color="#ff0000", lw=0.42)
    profile_axes[1].plot(site, profiles["critical_profile"], color="#ff9900", lw=0.52)
    profile_axes[2].plot(site, profiles["skin_profile"], color="#0000ff", lw=0.52)
    profile_limits = [(0.0, 0.11), (0.0, 0.52), (0.0, 0.52)]
    profile_ticks = [[0.05, 0.10], [0.0, 0.4], [0.0]]
    for index, (axis, ylim, ticks) in enumerate(zip(profile_axes, profile_limits, profile_ticks)):
        axis.set_xlim(0, 1000)
        axis.set_ylim(*ylim)
        axis.set_yticks(ticks)
        axis.set_xticks([0, 500, 1000])
        axis.tick_params(direction="in", top=True, right=True, width=0.45, length=2.0, labelsize=8, pad=1.5)
        for spine in axis.spines.values():
            spine.set_linewidth(0.45)
        if index < 2:
            axis.set_xticklabels([])
        else:
            axis.set_xlabel("site", fontsize=10, labelpad=0.5)
    fig.text(0.574, 0.806, r"$|\psi|^2$", fontsize=10, rotation=90, ha="center", va="center")

    for label, color, marker, fill in (
        ("skin", "#0000ff", "*", "none"),
        ("alm", "#ff0000", "s", "none"),
    ):
        subset = scaling[scaling["label"] == label]
        lengths = subset["L"].astype(float)
        deviations = subset["delta_phi"].astype(float)
        x_values = np.log(1.0 / lengths)
        y_values = np.log(deviations)
        fit_min_length = float(subset["fit_min_length"][0])
        fit_mask = lengths >= fit_min_length
        slope, intercept = np.polyfit(x_values[fit_mask], y_values[fit_mask], 1)
        axis_d.plot(
            x_values,
            y_values,
            linestyle="none",
            marker=marker,
            ms=4.4 if marker == "*" else 3.0,
            mfc=fill,
            mec=color,
            mew=0.6,
            color=color,
        )
        dense_x = np.linspace(x_values.min(), x_values.max(), 200)
        axis_d.plot(dense_x, slope * dense_x + intercept, color=color, lw=0.72)
    axis_d.set_xlim(-7.0, -4.45)
    axis_d.set_ylim(-8.0, -4.0)
    axis_d.set_xticks([-7, -6, -5])
    axis_d.set_yticks([-8, -7, -6, -5, -4])
    axis_d.set_xlabel(r"$\ln(1/L)$", fontsize=10, labelpad=1.0)
    axis_d.set_ylabel(r"$\ln(\Delta\phi)$", fontsize=10, labelpad=1.0)
    _style_axis(axis_d)

    _panel_label(fig, "(a)", 0, -2, width_px, height_px)
    _panel_label(fig, "(b)", 350, -3, width_px, height_px)
    _panel_label(fig, "(c)", 1, 253, width_px, height_px)
    _panel_label(fig, "(d)", 350, 255, width_px, height_px)
    outputs = _save_figure_bundle(fig, figure_dir / "fig3_paper_exact", spec)
    plt.close(fig)
    return outputs


def _plot_fig4(data_dir: Path, figure_dir: Path) -> dict[str, str]:
    ed = _load_npz(data_dir / "paper_ed_histograms.npz")
    theory = _load_npz(data_dir / "paper_fig34_theory.npz")
    spec = FIGURE_SPECS["fig4"]
    width_px, height_px = spec["pixels_180dpi"]
    fig = _new_figure(spec["size_points"])
    cmap = _paper_density_colormap()
    axis_a = _add_axis_px(fig, (width_px, height_px), (59, 13, 288, 202))
    cax_a = _add_axis_px(fig, (width_px, height_px), (305, 13, 321, 202))
    axis_b = _add_axis_px(fig, (width_px, height_px), (405, 13, 633, 202))
    cax_b = _add_axis_px(fig, (width_px, height_px), (651, 13, 666, 202))
    extent = [-2.5, 4.5, -0.9, 0.9]
    image_a = axis_a.imshow(
        ed["pbc_density"],
        origin="lower",
        extent=extent,
        aspect="auto",
        interpolation="bilinear",
        cmap=cmap,
        vmin=0.0,
        vmax=8.0,
        rasterized=True,
    )
    image_b = axis_b.imshow(
        np.clip(theory["pbc_density"], 0.0, None),
        origin="lower",
        extent=extent,
        aspect="auto",
        interpolation="bilinear",
        cmap=cmap,
        vmin=0.0,
        vmax=8.0,
        rasterized=True,
    )
    for axis in (axis_a, axis_b):
        _style_spectrum_axis(axis, ylim=(-0.9, 0.9))
    _style_density_colorbar(fig, image_a, cax_a)
    _style_density_colorbar(fig, image_b, cax_b)
    for x_value, label in ((-2.10, "-1"), (-0.45, "+1"), (2.50, "-1")):
        axis_b.text(x_value, 0.0, label, color="white", fontsize=7.5, ha="center", va="center")
    _panel_label(fig, "(a)", 0, -2, width_px, height_px)
    _panel_label(fig, "(b)", 346, -2, width_px, height_px)
    outputs = _save_figure_bundle(fig, figure_dir / "fig4_paper_exact", spec)
    plt.close(fig)
    return outputs


def _plot_fig5(data_dir: Path, figure_dir: Path) -> dict[str, str]:
    contours = _load_npz(data_dir / "paper_fig5_contours.npz")
    alpha = _read_csv(data_dir / "paper_alpha.csv")
    spec = FIGURE_SPECS["fig5"]
    width_px, height_px = spec["pixels_180dpi"]
    fig = _new_figure(spec["size_points"])
    axis_a = _add_axis_px(fig, (width_px, height_px), (44, 11, 272, 200))
    axis_b = _add_axis_px(fig, (width_px, height_px), (329, 11, 557, 200))
    colors = ["#ffb6ff", "#ff87ff", "#ff58ff", "#ff29f1", "#e600d7"]
    for index, color in enumerate(colors):
        _plot_zero_contours(
            axis_a,
            contours["real_axis"],
            contours["imag_axis"],
            contours["exponents"][index],
            color=color,
            linewidth=0.65,
        )
    axis_a.set_xlim(-2.5, 4.5)
    axis_a.set_ylim(-1.0, 1.0)
    axis_a.set_xticks([-2, 0, 2, 4])
    axis_a.set_yticks([-1, 0, 1])
    axis_a.set_xlabel(r"Re$E$", fontsize=10, labelpad=1.0)
    axis_a.set_ylabel(r"Im$E$", fontsize=10, labelpad=1.0)
    _style_axis(axis_a)

    axis_b.plot(alpha["W"], alpha["alpha"], color="black", lw=0.65, marker="o", ms=1.8, mfc="black", mec="black")
    axis_b.axvline(2.1, color="#8a8a8a", linestyle=(0, (1.3, 1.3)), lw=0.65)
    axis_b.set_xlim(0.0, 3.0)
    axis_b.set_ylim(0.0, 1.0)
    axis_b.set_xticks([0, 1, 2, 3])
    axis_b.set_yticks([0, 1])
    axis_b.set_xlabel(r"$W$", fontsize=10, labelpad=1.0)
    axis_b.set_ylabel(r"$\alpha$", fontsize=10, labelpad=1.0, rotation=0)
    axis_b.yaxis.set_label_coords(-0.10, 0.50)
    axis_b.text(0.95, 0.84, "Mixed", fontsize=9, fontweight="bold", ha="center")
    axis_b.text(2.55, 0.84, "AI", fontsize=9, fontweight="bold", ha="center")
    axis_b.text(2.13, 0.03, r"$W_c$", fontsize=8, ha="left", va="bottom")
    _style_axis(axis_b)
    _panel_label(fig, "(a)", 0, -2, width_px, height_px)
    _panel_label(fig, "(b)", 282, -2, width_px, height_px)
    outputs = _save_figure_bundle(fig, figure_dir / "fig5_paper_exact", spec)
    plt.close(fig)
    return outputs


def _run_geometry_qa(workspace: Path, outputs: dict[str, dict[str, str]]) -> dict[str, Any]:
    """Check only public, independently generated canvases.

    Export-time source-image metrics are published as a static audit check, but
    the public plotting command never requires or reconstructs publisher assets.
    """

    results: dict[str, Any] = {}
    geometry_all_exact = True
    for name, output in outputs.items():
        generated_path = workspace / output["png"]
        with Image.open(generated_path) as generated:
            actual_size = generated.size
        expected_size = tuple(FIGURE_SPECS[name]["pixels_180dpi"])
        dimensions_exact = actual_size == expected_size
        geometry_all_exact &= dimensions_exact
        results[name] = {
            "dimensions_exact": dimensions_exact,
            "expected_pixels": list(expected_size),
            "generated_pixels": list(actual_size),
        }
    return {"geometry_all_exact": geometry_all_exact, "figures": results}


def _configure_matplotlib() -> None:
    matplotlib.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "font.size": 8,
            "axes.linewidth": 0.45,
            "xtick.major.width": 0.45,
            "ytick.major.width": 0.45,
            "xtick.major.size": 2.2,
            "ytick.major.size": 2.2,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "runthepaper-2507.09447",
            "savefig.facecolor": "white",
        }
    )


def _new_figure(size_points: tuple[float, float]) -> plt.Figure:
    return plt.figure(figsize=(size_points[0] / 72.0, size_points[1] / 72.0), facecolor="white")


def _add_axis_px(
    fig: plt.Figure,
    canvas_pixels: tuple[int, int],
    box: tuple[int, int, int, int],
) -> plt.Axes:
    width, height = canvas_pixels
    left, top, right, bottom = box
    return fig.add_axes([left / width, (height - bottom) / height, (right - left) / width, (bottom - top) / height])


def _style_spectrum_axis(axis: plt.Axes, *, ylim: tuple[float, float]) -> None:
    axis.set_xlim(-2.5, 4.5)
    axis.set_ylim(*ylim)
    axis.set_xticks([-2, 0, 2, 4])
    axis.set_yticks([-0.5, 0.0, 0.5])
    axis.set_xlabel(r"Re$E$", fontsize=10, labelpad=1.0)
    axis.set_ylabel(r"Im$E$", fontsize=10, labelpad=1.0)
    _style_axis(axis)


def _style_axis(axis: plt.Axes) -> None:
    axis.tick_params(direction="in", top=True, right=True, labelsize=8, width=0.45, length=2.2, pad=1.5)
    for spine in axis.spines.values():
        spine.set_linewidth(0.45)


def _style_density_colorbar(fig: plt.Figure, image: Any, cax: plt.Axes) -> None:
    colorbar = fig.colorbar(image, cax=cax, ticks=[0, 2, 4, 6, 8])
    colorbar.ax.tick_params(direction="in", labelsize=7, width=0.4, length=1.8, pad=1.2)
    colorbar.outline.set_linewidth(0.4)
    colorbar.ax.set_title("DOS", fontsize=10, pad=-1.0)


def _plot_zero_contours(
    axis: plt.Axes,
    real_axis: np.ndarray,
    imag_axis: np.ndarray,
    exponents: np.ndarray,
    *,
    color: str,
    linewidth: float,
) -> None:
    for index in (1, 2):
        values = exponents[..., index]
        if float(values.min()) <= 0.0 <= float(values.max()):
            axis.contour(real_axis, imag_axis, values, levels=[0.0], colors=[color], linewidths=linewidth)


def _paper_density_colormap() -> mcolors.LinearSegmentedColormap:
    return mcolors.LinearSegmentedColormap.from_list(
        "paper_dos",
        [
            (0.00, "#2a004c"),
            (0.035, "#45047f"),
            (0.080, "#4547bd"),
            (0.135, "#448fe9"),
            (0.205, "#c4ebff"),
            (1.00, "#c4ebff"),
        ],
        N=256,
    )


def _panel_label(
    fig: plt.Figure,
    label: str,
    x: int,
    y: int,
    width: int,
    height: int,
) -> None:
    fig.text(x / width, 1.0 - y / height, label, fontsize=12, ha="left", va="top")


def _save_figure_bundle(fig: plt.Figure, stem: Path, spec: dict[str, Any]) -> dict[str, str]:
    paths = {
        "png": stem.with_suffix(".png"),
        "svg": stem.with_suffix(".svg"),
    }
    vector_size = fig.get_size_inches().copy()
    png_width, png_height = spec["pixels_180dpi"]
    fig.set_size_inches(png_width / 180.0, png_height / 180.0, forward=True)
    fig.savefig(paths["png"], dpi=180, facecolor="white")
    fig.set_size_inches(vector_size, forward=True)
    fig.savefig(
        paths["svg"],
        dpi=600,
        facecolor="white",
        metadata={"Date": "2026-07-14", "Creator": "RunThePaper"},
    )
    _normalize_svg_whitespace(paths["svg"])
    workspace = stem.parents[2]
    return {key: str(path.relative_to(workspace)) for key, path in paths.items()}


def _normalize_svg_whitespace(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def _load_npz(path: Path) -> dict[str, np.ndarray]:
    with np.load(path, allow_pickle=False) as data:
        return {name: data[name].copy() for name in data.files}


def _read_csv(path: Path) -> np.ndarray:
    data = np.genfromtxt(path, delimiter=",", names=True, dtype=None, encoding="utf-8")
    return np.atleast_1d(data)
