"""
M3 — Clustering models (spec only).

· Implement in notebooks/03–06 (one algorithm per notebook)
Reference: README.md Section 13

All stochastic steps: random_state=42. Save each model to models/*.pkl.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

_OWNER = "M3 — implement in 03–06 notebooks, then move here"


def fit_kmeans(X_scaled: np.ndarray, n_clusters: int, save_path: Path | None = None):
    """
    Notebook 03 — Primary model.

    Fit KMeans(n_clusters, random_state=42, n_init=10).
    Save models/kmeans.pkl. Return fitted model and labels.
    """
    raise NotImplementedError(_OWNER)


def fit_hierarchical(
    X_scaled: np.ndarray,
    n_clusters: int,
    linkage: str = "ward",
    save_path: Path | None = None,
):
    """
    Notebook 04 — AgglomerativeClustering, Ward linkage.

    Save models/hierarchical.pkl. Return model and label array.
    """
    raise NotImplementedError(_OWNER)


def fit_dbscan(
    X_scaled: np.ndarray,
    eps: float,
    min_samples: int = 5,
    save_path: Path | None = None,
):
    """
    Notebook 05 — DBSCAN. Noise points labeled -1.

    Tune eps using k-distance plot in notebook. Save models/dbscan.pkl.
    """
    raise NotImplementedError(_OWNER)


def fit_gmm(X_scaled: np.ndarray, n_components: int, save_path: Path | None = None):
    """
    Notebook 06 — GaussianMixture (random_state=42).

    Save models/gmm.pkl. Return model; add gmm_max_prob to master in notebook 07.
    """
    raise NotImplementedError(_OWNER)


def find_optimal_k(X_scaled: np.ndarray, k_range: range = range(2, 11)) -> dict[str, list]:
    """
    Notebook 03 — Elbow + Silhouette over k_range.

    Returns
    -------
    dict with keys: k, inertia, silhouette
    Used for figures/elbow_silhouette.png. Do not hardcode K.
    """
    raise NotImplementedError(_OWNER)
