"""
M3 — K-Means clustering (minimal API for scripts and later notebooks).

Full pipeline, plots, and interpretation live in notebooks/03_kmeans_clustering.ipynb.
"""

from src.clustering.evaluate import (
    K_RANGE_DEFAULT,
    build_final_evaluation_summary,
    cluster_size_table,
    compute_clustering_metrics,
    recommend_k,
)
from src.clustering.train_kmeans import (
    find_optimal_k,
    fit_kmeans,
    fit_manhattan_kmeans,
    sweep_kmeans_k,
    train_final_model,
)

__all__ = [
    "K_RANGE_DEFAULT",
    "build_final_evaluation_summary",
    "cluster_size_table",
    "compute_clustering_metrics",
    "find_optimal_k",
    "fit_kmeans",
    "fit_manhattan_kmeans",
    "recommend_k",
    "sweep_kmeans_k",
    "train_final_model",
]
