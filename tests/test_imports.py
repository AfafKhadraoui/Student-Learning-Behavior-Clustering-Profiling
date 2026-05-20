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
    assert (root / "notebooks" / "MAIN_NOTEBOOK.ipynb").is_file()
    assert (root / "notebooks" / "07_model_comparison.ipynb").is_file()


def test_src_imports():
    from src import MODULE, PRES, RANDOM_STATE, ROOT
    from src.features import FEATURE_COLS

    assert MODULE == "BBB"
    assert PRES == "2013J"
    assert RANDOM_STATE == 42
    assert len(FEATURE_COLS) == 20


def test_visualization_specs():
    from src.visualization import FIGURE_SPECS

    assert len(FIGURE_SPECS) == 6


def test_m1_helpers_exist():
    """M1 module exposes load/save helpers (implementation in notebook)."""
    from src import data_loader

    assert hasattr(data_loader, "load_csv")
    assert hasattr(data_loader, "build_master_raw")
    assert hasattr(data_loader, "save_master_raw")


def test_m2_m4_stubs_raise():
    """Non-M1 modules are spec stubs until owners implement them."""
    import numpy as np
    import pytest
    from src import clustering, evaluation, features, preprocessing, visualization

    with pytest.raises(NotImplementedError):
        features.engineer_features(None)
    with pytest.raises(NotImplementedError):
        clustering.fit_kmeans(np.zeros((10, 20)), n_clusters=3)
    with pytest.raises(NotImplementedError):
        evaluation.silhouette_on_scaled(np.zeros((10, 20)), np.zeros(10, dtype=int))
    with pytest.raises(NotImplementedError):
        visualization.plot_pca_clusters(None)
