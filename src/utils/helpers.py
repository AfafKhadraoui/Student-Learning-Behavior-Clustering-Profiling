"""
Path helpers and processed-data loading for the clustering pipeline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd

from src import MOD_DIR, PROC_DIR, RANDOM_STATE, ROOT
from src.features import FEATURE_COLS, META_COLS

REPORT_FIG_DIR = ROOT / "reports" / "figures"
RESULTS_DIR = ROOT / "reports" / "results"


def get_figure_dirs() -> tuple[Path, Path]:
    """Return (reports/figures, figures/) — save to both for repo compatibility."""
    from src import FIG_DIR

    return REPORT_FIG_DIR, FIG_DIR


def ensure_output_dirs() -> None:
    """Create models/, reports/figures/, reports/results/, figures/ if missing."""
    from src import FIG_DIR

    for d in (MOD_DIR, REPORT_FIG_DIR, RESULTS_DIR, FIG_DIR, PROC_DIR):
        d.mkdir(parents=True, exist_ok=True)


def load_processed_clustering_data(
    proc_dir: Path | None = None,
) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """
    Load artifacts produced by notebook 02.

    Returns
    -------
    X_scaled : (n_samples, 17) — clustering input only
    X_pca_2d : (n_samples, 2) — visualization only
    master_features : DataFrame with META_COLS + FEATURE_COLS
    """
    proc_dir = Path(proc_dir or PROC_DIR)
    X_scaled = np.load(proc_dir / "X_scaled.npy")
    X_pca_2d = np.load(proc_dir / "X_pca_2d.npy")
    master = pd.read_csv(proc_dir / "master_features.csv")

    expected_cols = META_COLS + FEATURE_COLS
    missing = [c for c in expected_cols if c not in master.columns]
    if missing:
        raise ValueError(f"master_features.csv missing columns: {missing}")

    if X_scaled.shape[1] != len(FEATURE_COLS):
        raise ValueError(
            f"X_scaled has {X_scaled.shape[1]} features; expected {len(FEATURE_COLS)}"
        )
    if len(master) != len(X_scaled):
        raise ValueError(
            f"Row mismatch: master_features {len(master)} vs X_scaled {len(X_scaled)}"
        )

    return X_scaled, X_pca_2d, master


def load_scaler(models_dir: Path | None = None):
    """Load fitted StandardScaler for inverse-transforming centroids."""
    models_dir = Path(models_dir or MOD_DIR)
    path = models_dir / "scaler.pkl"
    if not path.is_file():
        raise FileNotFoundError(f"Missing scaler at {path}")
    return joblib.load(path)


def explore_processed_data(
    X_scaled: np.ndarray,
    master: pd.DataFrame,
) -> pd.DataFrame:
    """
    Summarize shapes, missing values, and zero rates on raw (unscaled) features.

    Zeros are meaningful (e.g. no VLE activity) — never mean-impute for clustering.
    """
    raw = master[FEATURE_COLS]
    rows = []
    for col in FEATURE_COLS:
        n_zero = int((raw[col] == 0).sum())
        rows.append(
            {
                "feature": col,
                "n_zeros": n_zero,
                "pct_zeros": round(100 * n_zero / len(raw), 2),
                "mean_scaled": float(X_scaled[:, FEATURE_COLS.index(col)].mean()),
            }
        )
    summary = pd.DataFrame(rows)
    return summary


def save_figure(fig, name: str, dpi: int = 150) -> Path:
    """Save matplotlib figure to reports/figures/ and figures/."""
    import matplotlib.pyplot as plt

    report_dir, fig_dir = get_figure_dirs()
    ensure_output_dirs()
    primary = report_dir / name
    fig.savefig(primary, dpi=dpi, bbox_inches="tight")
    fig.savefig(fig_dir / name, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return primary


def print_data_overview(
    X_scaled: np.ndarray,
    X_pca_2d: np.ndarray,
    master: pd.DataFrame,
) -> None:
    """Print shapes and verification checks for notebook / CLI."""
    print(f"X_scaled shape:      {X_scaled.shape}  (expected (32593, 17))")
    print(f"X_pca_2d shape:      {X_pca_2d.shape}")
    print(f"master_features:     {master.shape}")
    print(f"Samples:             {len(X_scaled):,}")
    print(f"Features:            {X_scaled.shape[1]}")
    print(f"NaN in X_scaled:     {np.isnan(X_scaled).sum()}")
    print(f"Feature columns:     {FEATURE_COLS}")
    print(f"Metadata (not in X): {META_COLS}")
