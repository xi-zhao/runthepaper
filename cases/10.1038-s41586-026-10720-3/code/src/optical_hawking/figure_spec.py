"""Pixel-registration geometry for the main numerical paper figures.

The rectangles use PDF points in the paper page coordinate system.  Keeping
one canonical geometry object lets the independent renderer and the reference
crop use exactly the same canvas and panel bounds.
"""

from __future__ import annotations

from dataclasses import dataclass


PdfRect = tuple[float, float, float, float]


@dataclass(frozen=True)
class PaperFigureGeometry:
    figure_id: str
    page_index: int
    crop: PdfRect
    panels: tuple[tuple[str, PdfRect], ...]

    @property
    def width_points(self) -> float:
        return self.crop[2] - self.crop[0]

    @property
    def height_points(self) -> float:
        return self.crop[3] - self.crop[1]

    @property
    def figsize_inches(self) -> tuple[float, float]:
        return self.width_points / 72.0, self.height_points / 72.0

    def pixel_size(self, dpi: int) -> tuple[int, int]:
        """Return the exact registered raster size for an integer DPI."""

        return (
            round(self.width_points * dpi / 72.0),
            round(self.height_points * dpi / 72.0),
        )

    def axes_position(self, panel_id: str) -> tuple[float, float, float, float]:
        page_rect = dict(self.panels)[panel_id]
        x0, y0, x1, y1 = page_rect
        crop_x0, crop_y0, crop_x1, crop_y1 = self.crop
        return (
            (x0 - crop_x0) / self.width_points,
            (crop_y1 - y1) / self.height_points,
            (x1 - x0) / self.width_points,
            (y1 - y0) / self.height_points,
        )

    def figure_position(self, page_x: float, page_y: float) -> tuple[float, float]:
        crop_x0, _, _, crop_y1 = self.crop
        return (
            (page_x - crop_x0) / self.width_points,
            (crop_y1 - page_y) / self.height_points,
        )


FIG2_GEOMETRY = PaperFigureGeometry(
    figure_id="fig2",
    page_index=2,
    crop=(118.0, 54.0, 506.0, 260.0),
    panels=(
        ("a", (164.500, 66.355, 305.233, 235.234)),
        ("b", (360.113, 65.652, 501.315, 136.253)),
        ("c", (364.912, 167.298, 500.963, 235.322)),
    ),
)

FIG4_GEOMETRY = PaperFigureGeometry(
    figure_id="fig4",
    page_index=6,
    crop=(101.0, 54.0, 522.0, 257.0),
    panels=(
        ("a", (128.728, 69.805, 240.547, 138.912)),
        ("b", (270.652, 69.970, 382.471, 139.077)),
        ("c", (408.078, 69.777, 519.897, 138.884)),
        ("d", (128.728, 167.016, 240.547, 236.123)),
        ("e", (270.652, 167.016, 382.471, 236.123)),
        ("f", (408.078, 167.016, 519.897, 236.123)),
    ),
)

FIG5_GEOMETRY = PaperFigureGeometry(
    figure_id="fig5",
    page_index=7,
    crop=(184.0, 246.0, 437.0, 422.0),
    panels=(("main", (214.073, 252.268, 432.099, 387.016)),),
)

MAIN_NUMERIC_FIGURES = (FIG2_GEOMETRY, FIG4_GEOMETRY, FIG5_GEOMETRY)
