"""
Clustering evaluation metrics and k-selection helpers.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_samples,
    silhouette_score,
)

from src import RANDOM_STATE

K_RANGE_DEFAULT = range(2, 11)


def compute_clustering_metrics(
    X: np.ndarray,
    labels: np.ndarray,
    *,
    metric: str = "euclidean",
) -> dict[str, float]:
    """Silhouette, Davies–Bouldin, and Calinski–Harabasz on scaled features."""
    labels = np.asarray(labels)
    valid = labels >= 0
    Xv, lv = X[valid], labels[valid]
    if len(np.unique(lv)) < 2:
        return {
            "silhouette": float("nan"),
            "davies_bouldin": float("nan"),
            "calinski_harabasz": float("nan"),
        }
    return {
        "silhouette": float(silhouette_score(Xv, lv, metric=metric)),
        "davies_bouldin": float(davies_bouldin_score(Xv, lv)),
        "calinski_harabasz": float(calinski_harabasz_score(Xv, lv)),
    }


def cluster_size_table(labels: np.ndarray) -> pd.DataFrame:
    """Per-cluster counts and percentages."""
    labels = np.asarray(labels)
    vc = pd.Series(labels).value_counts().sort_index()
    total = len(labels)
    return pd.DataFrame(
        {
            "cluster": vc.index,
            "count": vc.values,
            "pct": (vc.values / total * 100).round(2),
        }
    )


def build_final_evaluation_summary(
    X_scaled: np.ndarray,
    labels: np.ndarray,
    inertia: float,
    n_clusters: int,
) -> pd.DataFrame:
    """Single-row summary for the chosen K-Means model."""
    m = compute_clustering_metrics(X_scaled, labels)
    sizes = cluster_size_table(labels)
    return pd.DataFrame(
        [
            {
                "algorithm": "K-Means",
                "n_clusters": n_clusters,
                "n_samples": len(labels),
                "inertia": round(inertia, 2),
                "silhouette": round(m["silhouette"], 4),
                "davies_bouldin": round(m["davies_bouldin"], 4),
                "calinski_harabasz": round(m["calinski_harabasz"], 2),
                "min_cluster_pct": sizes["pct"].min(),
                "max_cluster_pct": sizes["pct"].max(),
            }
        ]
    )


def recommend_k(sweep_df: pd.DataFrame) -> tuple[int, str]:
    """
    Recommend k: maximize silhouette, break ties with lower DBI,
    penalize clusters smaller than 2% of the cohort.
    """
    df = sweep_df.copy()
    if "min_cluster_pct" in df.columns:
        ok = df[df["min_cluster_pct"] >= 2.0]
        df = ok if not ok.empty else df

    max_sil = df["silhouette"].max()
    candidates = df[df["silhouette"] >= max_sil - 0.05]
    chosen = candidates.loc[candidates["davies_bouldin"].idxmin()]
    k = int(chosen["k"])
    reason = (
        f"k={k}: silhouette={chosen['silhouette']:.3f} (near peak {max_sil:.3f}), "
        f"Davies–Bouldin={chosen['davies_bouldin']:.3f}."
    )
    return k, reason


def per_sample_silhouette_stats(X: np.ndarray, labels: np.ndarray) -> dict[str, Any]:
    """Distribution of per-sample silhouette widths."""
    s = silhouette_samples(X, labels)
    return {
        "mean": float(s.mean()),
        "std": float(s.std()),
        "min": float(s.min()),
        "pct_negative": float((s < 0).mean() * 100),
    }
