"""
M3 — Evaluation metrics (spec only).

Owner: M3 · Implement in notebooks/07_model_comparison.ipynb
Reference: README.md Section 14

All internal metrics computed on X_scaled, not X_pca.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

_OWNER = "M3 — implement in 07_model_comparison.ipynb"


def silhouette_on_scaled(X_scaled: np.ndarray, labels: np.ndarray) -> float:
    """
    Silhouette score on X_scaled.

    Exclude DBSCAN noise (label == -1). Return nan if fewer than 2 valid clusters.
    """
    raise NotImplementedError(_OWNER)


def davies_bouldin_on_scaled(X_scaled: np.ndarray, labels: np.ndarray) -> float:
    """Davies–Bouldin Index — lower is better. Exclude noise labels."""
    raise NotImplementedError(_OWNER)


def calinski_harabasz_on_scaled(X_scaled: np.ndarray, labels: np.ndarray) -> float:
    """Calinski–Harabasz Index — higher is better. Exclude noise labels."""
    raise NotImplementedError(_OWNER)


def adjusted_rand(labels_a: np.ndarray, labels_b: np.ndarray) -> float:
    """
    Adjusted Rand Index between two labelings (e.g. K-Means vs Hierarchical).
    """
    raise NotImplementedError(_OWNER)


def build_evaluation_table(
    X_scaled: np.ndarray,
    results: dict[str, np.ndarray],
) -> pd.DataFrame:
    """
    Build comparison table for all models.

    Parameters
    ----------
    results : dict
        Keys = model names ('kmeans', 'hierarchical', …);
        values = label arrays per student.

    Returns
    -------
    DataFrame
        Columns: model, silhouette, davies_bouldin, calinski_harabasz,
        n_clusters, noise_pct (for DBSCAN).

    Export to reports/results/evaluation_table.csv
    """
    raise NotImplementedError(_OWNER)
