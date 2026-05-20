"""
M4 — Required figures (spec only).

Owner: M4 · Implement in notebooks/08_interpretation_at_risk.ipynb
Reference: README.md Section 17

Save all plots to figures/ with dpi=150, bbox_inches='tight', then plt.close().
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

FIGURE_SPECS = {
    "elbow_silhouette": "elbow_silhouette.png",
    "pca_clusters": "pca_clusters.png",
    "cluster_heatmap": "cluster_heatmap.png",
    "cluster_outcome_bar": "cluster_outcome_bar.png",
    "dendrogram": "dendrogram.png",
    "radar_chart": "radar_chart.png",
}

_OWNER = "M4 — implement in 08_interpretation_at_risk.ipynb"


def plot_elbow_silhouette(
    k_values: list,
    inertias: list,
    silhouettes: list,
    chosen_k: int,
    fig_dir: Path | None = None,
) -> Path:
    """Plot 1 — 2-panel Elbow + Silhouette; vertical line at chosen_k."""
    raise NotImplementedError(_OWNER)


def plot_pca_clusters(
    master: pd.DataFrame,
    cluster_col: str = "cluster_kmeans",
    fig_dir: Path | None = None,
) -> Path:
    """Plot 2 — PC1 vs PC2 scatter, colored by cluster, alpha=0.6."""
    raise NotImplementedError(_OWNER)


def plot_cluster_heatmap(centroids: pd.DataFrame, fig_dir: Path | None = None) -> Path:
    """Plot 3 — seaborn heatmap, features normalized 0–1, clusters as rows."""
    raise NotImplementedError(_OWNER)


def plot_cluster_outcome_bar(
    master: pd.DataFrame,
    cluster_col: str = "cluster_kmeans",
    fig_dir: Path | None = None,
) -> Path:
    """Plot 4 — Stacked bar: crosstab(cluster, final_result), normalize='index'."""
    raise NotImplementedError(_OWNER)


def plot_dendrogram(
    X_sample,
    sample_size: int = 250,
    fig_dir: Path | None = None,
) -> Path:
    """Plot 5 — Dendrogram on 200–300 student sample, Ward, truncate_mode='lastp'."""
    raise NotImplementedError(_OWNER)


def plot_radar_chart(
    centroids: pd.DataFrame,
    features: list[str],
    fig_dir: Path | None = None,
) -> Path:
    """Plot 6 — Radar chart, 5–6 features, one polygon per cluster."""
    raise NotImplementedError(_OWNER)
