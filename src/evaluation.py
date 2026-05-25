"""
M3 — Evaluation metrics (shared across clustering algorithms).

Implemented for K-Means; reused in notebook 07 model comparison.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)

from src.clustering.evaluate import compute_clustering_metrics


def _valid_mask(labels: np.ndarray) -> np.ndarray:
    """Exclude DBSCAN noise points."""
    return labels >= 0


def silhouette_on_scaled(X_scaled: np.ndarray, labels: np.ndarray) -> float:
    """Silhouette score on X_scaled. Exclude DBSCAN noise (label == -1)."""
    mask = _valid_mask(labels)
    if len(np.unique(labels[mask])) < 2:
        return float("nan")
    return float(silhouette_score(X_scaled[mask], labels[mask]))


def davies_bouldin_on_scaled(X_scaled: np.ndarray, labels: np.ndarray) -> float:
    """Davies–Bouldin Index — lower is better. Exclude noise labels."""
    mask = _valid_mask(labels)
    if len(np.unique(labels[mask])) < 2:
        return float("nan")
    return float(davies_bouldin_score(X_scaled[mask], labels[mask]))


def calinski_harabasz_on_scaled(X_scaled: np.ndarray, labels: np.ndarray) -> float:
    """Calinski–Harabasz Index — higher is better. Exclude noise labels."""
    mask = _valid_mask(labels)
    if len(np.unique(labels[mask])) < 2:
        return float("nan")
    return float(calinski_harabasz_score(X_scaled[mask], labels[mask]))


def adjusted_rand(labels_a: np.ndarray, labels_b: np.ndarray) -> float:
    """Adjusted Rand Index between two labelings."""
    return float(adjusted_rand_score(labels_a, labels_b))


def build_evaluation_table(
    X_scaled: np.ndarray,
    results: dict[str, np.ndarray],
) -> pd.DataFrame:
    """
    Build comparison table for all models.

    Parameters
    ----------
    results : dict
        Keys = model names; values = label arrays per student.

    Returns
    -------
    DataFrame with model, silhouette, davies_bouldin, calinski_harabasz,
    n_clusters, noise_pct (for DBSCAN).
    """
    rows = []
    for name, labels in results.items():
        labels = np.asarray(labels)
        noise_pct = float((labels < 0).mean() * 100) if (labels < 0).any() else 0.0
        valid_labels = labels[_valid_mask(labels)]
        n_clusters = len(np.unique(valid_labels)) if len(valid_labels) else 0
        if n_clusters >= 2:
            m = compute_clustering_metrics(X_scaled[_valid_mask(labels)], valid_labels)
        else:
            m = {"silhouette": np.nan, "davies_bouldin": np.nan, "calinski_harabasz": np.nan}
        rows.append(
            {
                "model": name,
                "silhouette": m["silhouette"],
                "davies_bouldin": m["davies_bouldin"],
                "calinski_harabasz": m["calinski_harabasz"],
                "n_clusters": n_clusters,
                "noise_pct": round(noise_pct, 2),
            }
        )
    return pd.DataFrame(rows)
