# Pixel-domain audit

## Purpose

The physical checks and the visual audit answer different questions. The
physical checks establish conservation laws, limiting behaviour, and agreement
with reported scalar benchmarks. The pixel audit asks how closely the
independently generated scalar fields match the theoretical interiors of the
published raster panels after using the panel geometry and colour scale.

No published pixels are included in the generated figures. Experimental panels
are excluded because the shot-level and tomography arrays are unavailable.

## Method

For each theoretical heatmap, the publisher raster was decoded through its own
colour bar. Labels, ticks, borders, and panel letters were masked. The generated
array was sampled in the same orientation and compared using a weighted pattern
metric built from literal RGB similarity, decoded scalar MAE, Pearson
correlation, global SSIM, and gradient correlation.

The source rasters and crop coordinates are validation-only assets and are not
redistributed in this public package. The released JSON contains aggregate
metrics without private or copyrighted source paths.

## Results

| Group | Panels | Mean pattern similarity | Pearson r | Decoded MAE |
| --- | ---: | ---: | ---: | ---: |
| One-particle density | 3 | 94.67% | 0.9266 | 0.0130 |
| One-particle entropy | 1 | 92.54% | 0.9366 | 0.0819 |
| Two-particle density | 2 | 96.34% | 0.9638 | 0.0182 |
| Two-particle correlator | 12 | 77.88% | 0.4614 | 0.1033 |

The density and entropy fields are close pixel-domain matches. The S20
correlator grid is weaker, especially for the late-time free-boson comparator;
that discrepancy is retained rather than fitted away. The formal case score
therefore remains 80/100 under the author-array evidence cap.
