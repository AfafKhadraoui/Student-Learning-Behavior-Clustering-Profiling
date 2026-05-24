"""
K-Means training and k-sweep (Euclidean sklearn + Manhattan Lloyd).
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

from src import MOD_DIR, PROC_DIR, RANDOM_STATE
from src.clustering.evaluate import (
    K_RANGE_DEFAULT,
    cluster_size_table,
    compute_clustering_metrics,
    recommend_k,
)


def _kmeans_params(random_state: int = RANDOM_STATE) -> dict:
    return {
        "init": "k-means++",
        "n_init": 20,
        "max_iter": 500,
        "random_state": random_state,
    }


def fit_kmeans(
    X_scaled: np.ndarray,
    n_clusters: int,
    *,
    random_state: int = RANDOM_STATE,
    save_path: Path | None = None,
) -> KMeans:
    """Fit sklearn K-Means (Euclidean) on standardized features."""
    model = KMeans(n_clusters=n_clusters, **_kmeans_params(random_state))
    model.fit(X_scaled)
    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, save_path)
    return model


def fit_kmeans_metric(
    X: np.ndarray,
    n_clusters: int,
    metric: str = "cityblock",
    *,
    max_iter: int = 300,
    random_state: int = RANDOM_STATE,
    VI: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Lloyd k-means with scipy cdist (Manhattan or Mahalanobis)."""
    rng = np.random.default_rng(random_state)
    n = len(X)
    k = n_clusters
    cdist_kwargs: dict = {}
    if metric == "mahalanobis":
        if VI is None:
            cov = np.cov(X, rowvar=False)
            VI = np.linalg.pinv(cov + 1e-6 * np.eye(X.shape[1]))
        cdist_kwargs["VI"] = VI

    centers = np.empty((k, X.shape[1]))
    centers[0] = X[rng.integers(n)]
    for i in range(1, k):
        D = cdist(X, centers[:i], metric=metric, **cdist_kwargs)
        d_min = D.min(axis=1)
        probs = d_min / d_min.sum() if d_min.sum() > 0 else np.ones(n) / n
        centers[i] = X[rng.choice(n, p=probs)]

    labels = np.zeros(n, dtype=int)
    for _ in range(max_iter):
        D = cdist(X, centers, metric=metric, **cdist_kwargs)
        new_labels = D.argmin(axis=1)
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
        for j in range(k):
            mask = labels == j
            centers[j] = X[mask].mean(axis=0) if mask.any() else X[rng.integers(n)]

    return labels, centers


def fit_manhattan_kmeans(
    X: np.ndarray,
    n_clusters: int,
    *,
    random_state: int = RANDOM_STATE,
    save_path: Path | None = None,
) -> dict:
    """Fit Manhattan K-Means; returns dict with labels and centers."""
    labels, centers = fit_kmeans_metric(
        X, n_clusters, metric="cityblock", random_state=random_state, max_iter=500
    )
    result = {
        "n_clusters": n_clusters,
        "metric": "manhattan",
        "labels_": labels,
        "cluster_centers_": centers,
        "random_state": random_state,
    }
    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(result, save_path)
    return result


def sweep_kmeans_k(
    X_scaled: np.ndarray,
    k_range: range | list[int] | None = None,
    *,
    random_state: int = RANDOM_STATE,
) -> pd.DataFrame:
    """Elbow + internal metrics for k in k_range (default 2..10)."""
    k_range = list(k_range or K_RANGE_DEFAULT)
    rows = []
    for k in k_range:
        model = fit_kmeans(X_scaled, n_clusters=k, random_state=random_state)
        labels = model.labels_
        m = compute_clustering_metrics(X_scaled, labels)
        sizes = cluster_size_table(labels)
        rows.append(
            {
                "k": k,
                "inertia": model.inertia_,
                "silhouette": m["silhouette"],
                "davies_bouldin": m["davies_bouldin"],
                "calinski_harabasz": m["calinski_harabasz"],
                "min_cluster_pct": sizes["pct"].min(),
                "max_cluster_pct": sizes["pct"].max(),
            }
        )
    return pd.DataFrame(rows)


def find_optimal_k(
    X_scaled: np.ndarray,
    k_range: range | list[int] | None = None,
    *,
    random_state: int = RANDOM_STATE,
) -> tuple[int, pd.DataFrame, str]:
    """Run k-sweep and return recommended k, sweep table, and explanation."""
    sweep = sweep_kmeans_k(X_scaled, k_range=k_range, random_state=random_state)
    k, reason = recommend_k(sweep)
    return k, sweep, reason


def train_final_model(
    X: np.ndarray,
    n_clusters: int,
    master_features: pd.DataFrame,
    *,
    models_dir: Path | None = None,
    proc_dir: Path | None = None,
    random_state: int = RANDOM_STATE,
    primary_metric: str = "manhattan",
) -> tuple[dict | KMeans, np.ndarray, pd.DataFrame]:
    """
    Train Euclidean and Manhattan models; primary labels from Manhattan by default.

    Saves models under models/ and master_features_with_clusters.csv.
    Interpretation and ENSIA labels are assigned in notebook 03.
    """
    models_dir = Path(models_dir or MOD_DIR)
    proc_dir = Path(proc_dir or PROC_DIR)

    eucl_model = fit_kmeans(
        X,
        n_clusters=n_clusters,
        random_state=random_state,
        save_path=models_dir / f"kmeans_k{n_clusters}_euclidean.pkl",
    )

    manhattan_model = fit_manhattan_kmeans(
        X,
        n_clusters=n_clusters,
        random_state=random_state,
        save_path=models_dir / f"kmeans_k{n_clusters}_manhattan.pkl",
    )

    if primary_metric == "manhattan":
        labels = manhattan_model["labels_"]
        primary = manhattan_model
    else:
        labels = eucl_model.labels_
        primary = eucl_model

    joblib.dump(primary, models_dir / f"kmeans_k{n_clusters}.pkl")
    joblib.dump(primary, models_dir / "kmeans.pkl")

    master_out = master_features.copy()
    master_out["cluster_euclidean"] = eucl_model.labels_
    master_out["cluster_manhattan"] = manhattan_model["labels_"]
    master_out["cluster"] = master_out["cluster_manhattan"]
    master_out.to_csv(proc_dir / "master_features_with_clusters.csv", index=False)

    return primary, labels, master_out
