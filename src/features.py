"""
M2 — Feature engineering (spec only).

Owner: M2 · Implement in notebooks/02_feature_engineering.ipynb
Reference: README.md Section 10

Do not implement here until M2 copies finished code from the notebook.
"""

from __future__ import annotations

import pandas as pd

# ─── Contract: 20 clustering features (Groups A–D) ───────────────────────────
FEATURE_COLS = [
    "total_clicks",
    "active_days",
    "avg_daily_clicks",
    "first_activity_day",
    "late_click_ratio",
    "early_click_ratio",
    "click_in_final_week_ratio",
    "weekly_click_std",
    "click_trend_slope",
    "max_daily_clicks",
    "quiz_click_ratio",
    "forum_click_ratio",
    "resource_click_ratio",
    "active_vs_passive_ratio",
    "weighted_avg_score",
    "score_variance",
    "score_trend_slope",
    "avg_submission_delay",
    "missing_submission_rate",
    "early_submission_rate",
]

BACKGROUND_COLS = [
    "num_prev_attempts",
    "registration_lead_days",
    "is_withdrawn",
]

_OWNER = "M2 — implement in 02_feature_engineering.ipynb"


def compute_click_trend_slope(weekly: pd.DataFrame) -> pd.Series:
    """
    Linear slope of weekly clicks per student.

    Parameters
    ----------
    weekly : DataFrame
        Columns: id_student, week, sum_click

    Returns
    -------
    Series
        Index id_student, values = slope from scipy.stats.linregress.
        If fewer than 2 weeks for a student, return 0.0.

    Notes
    -----
    README Section 10 Group B. Use scipy.stats.linregress, not numpy.polyfit.
    """
    raise NotImplementedError(_OWNER)


def compute_score_trend_slope(scores: pd.DataFrame) -> pd.Series:
    """
    Slope of time-ordered assessment scores per student.

    Parameters
    ----------
    scores : DataFrame
        Per-student scores in chronological order (define columns in notebook).

    Returns
    -------
    Series
        Index id_student. Same linregress rules as click_trend_slope.
    """
    raise NotImplementedError(_OWNER)


def engineer_features(master_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Build master table with all FEATURE_COLS (+ BACKGROUND_COLS if needed).

    Parameters
    ----------
    master_raw : DataFrame
        Output of M1 build_master_raw().

    Returns
    -------
    DataFrame
        One row per student; includes FEATURE_COLS.
        Save to data/processed/master_features.csv.

    Rules
    -----
    - final_result must NOT be in feature columns used for clustering
    - Zero-VLE students: VLE features = 0, not column mean
    - Ratios clipped to [0, 1]
    """
    raise NotImplementedError(_OWNER)
