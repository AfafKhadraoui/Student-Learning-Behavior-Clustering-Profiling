"""Smoke tests — verify package structure and constants."""

from pathlib import Path

import pytest


def test_repo_paths_exist():
    root = Path(__file__).resolve().parent.parent
    for sub in [
        "data/raw",
        "data/processed",
        "notebooks",
        "src",
        "models",
        "figures",
        "reports/slides",
        "reports/results",
        "docs",
        "web/backend",
        "web/frontend",
    ]:
        assert (root / sub).is_dir(), f"Missing directory: {sub}"


def test_algorithm_notebooks_exist():
    root = Path(__file__).resolve().parent.parent
    expected = [
        "03_kmeans_clustering.ipynb",
        "04_hierarchical_clustering.ipynb",
        "05_dbscan_clustering.ipynb",
        "06_gmm_clustering.ipynb",
        "07_model_comparison.ipynb",
        "08_interpretation_at_risk.ipynb",
    ]
    for name in expected:
        assert (root / "notebooks" / name).is_file(), f"Missing notebook: {name}"


def test_research_paper_template():
    root = Path(__file__).resolve().parent.parent
    assert (root / "reports" / "research_paper.md").is_file()


def test_final_notebooks():
    root = Path(__file__).resolve().parent.parent
    assert (root / "notebooks" / "07_model_comparison.ipynb").is_file()
    assert (root / "notebooks" / "03_kmeans_clustering.ipynb").is_file()


def test_src_imports():
    from src import MODULE, PRES, RANDOM_STATE, ROOT
    from src.features import FEATURE_COLS

    assert MODULE == "BBB"
    assert PRES == "2013J"
    assert RANDOM_STATE == 42
    assert len(FEATURE_COLS) == 17


def test_visualization_specs():
    from src.visualization import FIGURE_SPECS

    assert len(FIGURE_SPECS) == 6


def test_eda_plot_functions():
    from src.eda_plots import plot_result_distribution, plot_temporal_heatmap

    assert callable(plot_result_distribution)
    assert callable(plot_temporal_heatmap)


def test_m1_helpers_exist():
    """M1 module exposes load/save helpers (implementation in notebook)."""
    from src import data_loader

    assert hasattr(data_loader, "load_csv")
    assert hasattr(data_loader, "build_master_raw")
    assert hasattr(data_loader, "save_master_raw")


def test_m2_features_implemented():
    from src.features import build_feature_matrix, compute_group_a

    assert callable(build_feature_matrix)
    assert callable(compute_group_a)


def test_m3_clustering_implemented():
    """M3 clustering module exposes train/evaluate API."""
    import numpy as np
    from src.clustering import fit_kmeans, sweep_kmeans_k

    rng = np.random.default_rng(42)
    X = rng.normal(size=(200, 17))
    model = fit_kmeans(X, n_clusters=3)
    assert model.n_clusters == 3
    assert len(model.labels_) == 200


def test_m3_evaluation_metrics():
    import numpy as np
    from src import evaluation

    rng = np.random.default_rng(42)
    X = rng.normal(size=(100, 17))
    labels = rng.integers(0, 3, size=100)
    score = evaluation.silhouette_on_scaled(X, labels)
    assert -1.0 <= score <= 1.0


def test_m4_visualization_stubs_raise():
    """M4 clustering plot stubs until 08_interpretation notebook."""
    import pytest
    from src import visualization

    with pytest.raises(NotImplementedError):
        visualization.plot_pca_clusters(None)
