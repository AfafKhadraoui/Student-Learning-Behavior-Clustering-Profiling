"""
M2 — Feature engineering (17 clustering features, EDA-informed).

Built in notebooks/02_feature_engineering.ipynb; reusable for tests and pipeline.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import linregress
from sklearn.preprocessing import StandardScaler

import joblib

# Final clustering feature matrix (17 columns; weekly_click_std_log dropped — |r|≈0.96 with total_clicks_log)
FEATURE_COLS = [
    "total_clicks_log",
    "active_day_rate",
    "early_click_ratio",
    "late_click_ratio",
    "click_in_final_week_ratio",
    "click_trend_slope",
    "last_active_day_norm",
    "active_engagement_ratio",
    "quiz_click_ratio",
    "weighted_avg_score",
    "score_consistency",
    "score_trend_slope",
    "missing_submission_rate",
    "submission_timing",
    "num_prev_attempts",
    "registration_lead_days",
    "highest_education_encoded",
]

META_COLS = ["id_student", "code_module", "code_presentation", "final_result"]

WEEK_COLS = [f"week_{i}_clicks" for i in range(34)]

EDU_MAP = {
    "No Formal quals": 0,
    "Lower Than A Level": 1,
    "A Level or Equivalent": 2,
    "HE Qualification": 3,
    "Post Graduate Qualification": 4,
}

STUDENT_KEYS = ["code_module", "code_presentation", "id_student"]


def _safe_div(num: np.ndarray, den: np.ndarray) -> np.ndarray:
    out = np.zeros_like(num, dtype=float)
    mask = den > 0
    out[mask] = num[mask] / den[mask]
    return out


def _clip_percentile(arr: np.ndarray, low: float = 1.0, high: float = 99.0) -> np.ndarray:
    if len(arr) == 0:
        return arr
    p1, p99 = np.percentile(arr, [low, high])
    return np.clip(arr, p1, p99)


def compute_group_a(df: pd.DataFrame) -> pd.DataFrame:
    """total_clicks_log and active_day_rate (already normalized in master_raw)."""
    out = df.copy()
    out["total_clicks_log"] = np.log1p(out["total_clicks"].fillna(0))
    if "active_day_rate" not in out.columns:
        out["active_day_rate"] = _safe_div(
            out["active_days"].fillna(0).values,
            out["module_length"].replace(0, np.nan).fillna(1).values,
        )
    return out


def compute_group_b(df: pd.DataFrame) -> pd.DataFrame:
    """Six temporal features from weekly click columns."""
    out = df.copy()
    weekly = out[WEEK_COLS].fillna(0).values
    module_weeks = (out["module_length"] // 7).clip(lower=1).astype(int).values
    total = out["total_clicks"].fillna(0).values.astype(float)
    last_access = out["last_access_day"].fillna(0).values.astype(float)
    module_len = out["module_length"].replace(0, np.nan).fillna(1).values.astype(float)

    n = len(out)
    early_sum = np.zeros(n)
    late_sum = np.zeros(n)
    final_week = np.zeros(n)
    weekly_std = np.zeros(n)
    slopes = np.zeros(n)

    max_weeks = weekly.shape[1]

    for i in range(n):
        mw = min(int(module_weeks[i]), max_weeks)
        w = weekly[i, :mw]
        tc = total[i]
        third = max(mw // 3, 1)
        early_end = third
        late_start = (2 * mw) // 3

        early_sum[i] = w[:early_end].sum()
        late_sum[i] = w[late_start:mw].sum() if late_start < mw else 0.0
        final_week[i] = w[mw - 1] if mw > 0 else 0.0
        weekly_std[i] = float(np.std(w)) if len(w) > 1 else 0.0

        nonzero = np.where(w > 0)[0]
        if len(nonzero) >= 3:
            try:
                slopes[i] = linregress(nonzero, w[nonzero]).slope
            except Exception:
                slopes[i] = 0.0

    out["early_click_ratio"] = _safe_div(early_sum, total)
    out["late_click_ratio"] = _safe_div(late_sum, total)
    out["click_in_final_week_ratio"] = _safe_div(final_week, total)
    # weekly_click_std_log omitted: nearly collinear with total_clicks_log (EDA warned |r|>0.83)
    out["click_trend_slope"] = _clip_percentile(slopes)

    lan = last_access / module_len
    lan = np.where(total > 0, np.clip(lan, 0, 1), 0.0)
    out["last_active_day_norm"] = lan

    return out


def compute_score_trend(
    student_assess_path: Path,
    assessments_path: Path,
) -> pd.DataFrame:
    """
    Per-registration score_trend_slope from chronological non-banked scores.
    """
    sa = pd.read_csv(student_assess_path)
    assess = pd.read_csv(assessments_path)
    assess = assess[assess["assessment_type"] != "Exam"]

    merged = sa.merge(
        assess[
            [
                "id_assessment",
                "code_module",
                "code_presentation",
                "date",
                "weight",
                "assessment_type",
            ]
        ],
        on="id_assessment",
        how="inner",
    )
    merged = merged[merged["is_banked"] != 1].copy()
    merged = merged.sort_values(STUDENT_KEYS + ["date_submitted"])

    slopes = []
    keys = []
    for key, grp in merged.groupby(STUDENT_KEYS, observed=True):
        scores = grp["score"].dropna().values
        if len(scores) < 2:
            slope = 0.0
        else:
            try:
                slope = linregress(np.arange(len(scores)), scores).slope
            except Exception:
                slope = 0.0
        keys.append(key)
        slopes.append(slope)

    trend = pd.DataFrame(keys, columns=STUDENT_KEYS)
    trend["score_trend_slope"] = _clip_percentile(np.array(slopes, dtype=float))
    return trend


def compute_group_c(df: pd.DataFrame) -> pd.DataFrame:
    """active_engagement_ratio and quiz_click_ratio."""
    out = df.copy()
    total = out["total_clicks"].fillna(0).values.astype(float)
    active = (out["quiz_clicks"].fillna(0) + out["forum_clicks"].fillna(0)).values
    quiz = out["quiz_clicks"].fillna(0).values
    out["active_engagement_ratio"] = _safe_div(active, total)
    out["quiz_click_ratio"] = _safe_div(quiz, total)
    return out


def compute_group_d(
    df: pd.DataFrame,
    score_trend: pd.DataFrame,
) -> pd.DataFrame:
    """Five assessment features; merges score_trend on STUDENT_KEYS."""
    out = df.merge(score_trend, on=STUDENT_KEYS, how="left")
    out["score_trend_slope"] = out["score_trend_slope"].fillna(0.0)

    out["weighted_avg_score"] = out["avg_score"].fillna(0.0)
    std = out["score_std"]
    out["score_consistency"] = np.where(
        std.notna() & (std > 0),
        1.0 / (1.0 + std),
        0.5,
    )

    due = out["total_assessments_due"].replace(0, np.nan)
    out["missing_submission_rate"] = (
        out["total_missing"].fillna(0) / due
    ).fillna(0.0).clip(0, 1)

    timing = out["avg_submission_delay"].copy()
    # NaN = no submissions; fill with mean delay among submitters (not 0 — EDA means use dropna-style aggregates)
    fill_delay = timing.dropna().mean()
    timing = timing.fillna(fill_delay)
    out["submission_timing"] = _clip_percentile(timing.values)

    return out


def compute_group_e(df: pd.DataFrame) -> pd.DataFrame:
    """Background context features (no gender / final_result)."""
    out = df.copy()
    out["num_prev_attempts"] = out["num_of_prev_attempts"].fillna(0).astype(int)

    reg = out["date_registration"]
    out["registration_lead_days"] = np.where(
        reg < 0,
        np.abs(reg),
        0,
    )
    out["registration_lead_days"] = out["registration_lead_days"].fillna(0)

    out["highest_education_encoded"] = (
        out["highest_education"].map(EDU_MAP).fillna(-1).astype(int)
    )
    unknown = out["highest_education_encoded"] == -1
    if unknown.any():
        out.loc[unknown, "highest_education_encoded"] = (
            out.loc[~unknown, "highest_education_encoded"].median()
        )
    return out


def build_feature_matrix(
    master_raw_path: Path,
    student_assess_path: Path,
    assessments_path: Path,
) -> pd.DataFrame:
    """Full pipeline: load master_raw, compute all groups, return features_df."""
    df = pd.read_csv(master_raw_path)
    df = compute_group_a(df)
    df = compute_group_b(df)
    df = compute_group_c(df)
    score_trend = compute_score_trend(student_assess_path, assessments_path)
    df = compute_group_d(df, score_trend)
    df = compute_group_e(df)

    features_df = df[META_COLS + FEATURE_COLS].copy()
    missing = features_df[FEATURE_COLS].isna().sum()
    if missing.any():
        for col in missing[missing > 0].index:
            features_df[col] = features_df[col].fillna(0)
    return features_df


def scale_features(
    X: np.ndarray,
    models_dir: Path,
    *,
    save_name: str = "scaler.pkl",
) -> tuple[np.ndarray, StandardScaler]:
    """Fit StandardScaler, save to models_dir, return scaled X."""
    models_dir = Path(models_dir)
    models_dir.mkdir(parents=True, exist_ok=True)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, models_dir / save_name)
    return X_scaled, scaler
