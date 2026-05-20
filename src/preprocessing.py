"""
M2 — Preprocessing (spec only).

Owner: M2 · Implement in notebooks/02_feature_engineering.ipynb
Reference: README.md Section 11

Cluster on X_scaled only. X_pca is for visualization, not clustering.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.features import FEATURE_COLS

LABEL_COLS = ["id_student", "final_result", "code_module", "code_presentation"]
LOG_TRANSFORM_COLS = ["total_clicks", "max_daily_clicks", "active_days"]

EDU_MAP = {
    "No Formal quals": 0,
    "Lower Than A Level": 1,
    "A Level or Equivalent": 2,
    "HE Qualification": 3,
    "Post Graduate Qualification": 4,
}
AGE_MAP = {"0-35": 0, "35-55": 1, "55<=": 2}
IMD_MAP = {f"{i * 10}-{(i + 1) * 10}%": i + 1 for i in range(10)}

_OWNER = "M2 — implement in 02_feature_engineering.ipynb"


def separate_labels(master: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Step 1 — Split validation columns from X.

    Returns
    -------
    labels_df : id_student, final_result, code_module, code_presentation
    X_raw : FEATURE_COLS only (20 features)
    """
    raise NotImplementedError(_OWNER)


def apply_log_transform(X_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Step 2 — log1p on total_clicks, max_daily_clicks, active_days; drop originals.
    """
    raise NotImplementedError(_OWNER)


def encode_categoricals(X_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Step 3 — Ordinal-encode highest_education, age_band, imd_band (use maps above).
    """
    raise NotImplementedError(_OWNER)


def fit_scaler(X_raw: pd.DataFrame, save_path: Path | None = None):
    """
    Step 4 — StandardScaler fit_transform; joblib.dump to models/scaler.pkl;
    np.save data/processed/X_scaled.npy.

    Returns
    -------
    X_scaled : ndarray
    scaler : fitted StandardScaler
    """
    raise NotImplementedError(_OWNER)


def fit_pca(X_scaled: np.ndarray, variance_threshold: float = 0.85, save_path: Path | None = None):
    """
    Step 5 — PCA for visualization only (random_state=42).

    Returns
    -------
    X_pca, X_pca_2d, pca_model
    Saves models/pca_model.pkl and data/processed/X_pca.npy.
    Add PC1, PC2 columns to master for scatter plots.
    """
    raise NotImplementedError(_OWNER)
