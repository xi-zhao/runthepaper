# Similarity scorecard

Public audit score: **89.00/100**.

All nine scientific gates pass:

- the `L=1000`, 3200-realization ED ensemble is complete;
- OBC and PBC finite/thermodynamic density overlaps are `0.8069` and `0.8498`;
- the two finite-size exponent gaps are below `0.05`;
- ALM, near-critical, and skin profiles satisfy their Lyapunov sign rules;
- mobility-contour area decreases monotonically;
- the transition estimate is `W_c=2.1`.

The export-time full-image SSIM values are `0.7721`, `0.7735`, and `0.8521`
for Figs. 3, 4, and 5. They document the visual gap but are not the scientific
acceptance rule. The public package does not redistribute publisher figure
assets, so it publishes these metrics as provenance-labelled audit evidence
rather than attempting to recompute them from copied source images.

See the machine-readable
[`similarity_scorecard.json`](../outputs/checks/similarity_scorecard.json),
[`paper_scientific_similarity.json`](../outputs/checks/paper_scientific_similarity.json),
and [`paper_pixel_similarity.json`](../outputs/checks/paper_pixel_similarity.json).
