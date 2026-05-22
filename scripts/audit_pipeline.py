"""Audit notebooks 00-02 handoff and clustering readiness."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.features import (
    FEATURE_COLS,
    build_feature_matrix,
    compute_group_a,
    compute_group_b,
    compute_group_c,
    compute_group_d,
    compute_group_e,
    compute_score_trend,
)

PROCESSED = ROOT / "data/processed"
RAW = ROOT / "data/raw"
issues: list[str] = []
ok: list[str] = []


def check(cond: bool, good: str, bad: str) -> None:
    (ok if cond else issues).append(good if cond else bad)


# --- Files exist ---
for f in ["master_raw.csv", "master_features.csv", "X_scaled.npy", "X_pca_2d.npy"]:
    p = PROCESSED / f
    check(p.exists(), f"{f} exists", f"MISSING {f}")

scaler = ROOT / "models" / "scaler.pkl"
check(scaler.exists(), "scaler.pkl exists", "MISSING models/scaler.pkl")

raw = pd.read_csv(PROCESSED / "master_raw.csv")
feat = pd.read_csv(PROCESSED / "master_features.csv")
X = np.load(PROCESSED / "X_scaled.npy")

check(raw.shape[0] == 32_593, "master_raw: 32,593 rows", f"master_raw rows {raw.shape[0]}")
check(raw.shape[1] == 68, "master_raw: 68 columns", f"master_raw cols {raw.shape[1]} (expected 68)")
check("missing_rate" in raw.columns, "master_raw has missing_rate", "missing_rate column missing")
check(feat.shape[0] == 32_593, "master_features: 32,593 rows", f"master_features rows {feat.shape[0]}")
check(X.shape == (32_593, len(FEATURE_COLS)), f"X_scaled: {X.shape}", f"X_scaled shape {X.shape}")

# Keys unique
keys = ["id_student", "code_module", "code_presentation"]
check(raw.duplicated(keys).sum() == 0, "master_raw keys unique", "duplicate keys in master_raw")
check(feat.duplicated(keys).sum() == 0, "master_features keys unique", "duplicate keys in master_features")

# final_result not in features
check("final_result" not in FEATURE_COLS, "final_result not in FEATURE_COLS", "LEAK: final_result in FEATURE_COLS")
check("is_withdrawn" not in FEATURE_COLS, "is_withdrawn not in FEATURE_COLS", "LEAK: is_withdrawn in FEATURE_COLS")
check("gender" not in FEATURE_COLS, "gender not in FEATURE_COLS", "gender in FEATURE_COLS")

# Feature column alignment
saved_cols = [c for c in feat.columns if c not in keys + ["final_result"]]
check(saved_cols == FEATURE_COLS, "master_features columns match FEATURE_COLS", f"column mismatch: {saved_cols}")

# NaN / inf in X
check(not np.isnan(X).any(), "X_scaled has no NaN", "NaN in X_scaled")
check(not np.isinf(X).any(), "X_scaled has no inf", "inf in X_scaled")
check(feat[FEATURE_COLS].isna().sum().sum() == 0, "master_features no NaN", "NaN in feature columns")

# Rebuild pipeline consistency
built = build_feature_matrix(
    PROCESSED / "master_raw.csv",
    RAW / "studentAssessment.csv",
    RAW / "assessments.csv",
)
diff = np.abs(built[FEATURE_COLS].fillna(0).values - feat[FEATURE_COLS].values).max()
check(diff < 1e-6, "saved features match rebuild", f"rebuild max diff {diff}")

# EDA numbers
df = raw.copy()
df = compute_group_a(df)
df = compute_group_b(df)
df = compute_group_c(df)
st = compute_score_trend(RAW / "studentAssessment.csv", RAW / "assessments.csv")
df = compute_group_d(df, st)
miss_pct = (df.groupby("final_result")["missing_submission_rate"].mean() * 100).round(1)
expected_miss = {"Distinction": 3.4, "Pass": 4.7, "Fail": 36.4, "Withdrawn": 30.1}
for k, v in expected_miss.items():
    check(abs(miss_pct[k] - v) < 0.05, f"missing % {k}={miss_pct[k]}", f"missing % {k}: got {miss_pct[k]} expected {v}")

zero_pct = (df["total_clicks_log"] == 0).mean() * 100
check(abs(zero_pct - 10.3) < 0.1, f"zero-click rate {zero_pct:.1f}%", f"zero-click {zero_pct}% not 10.3%")

# Outcomes
outcomes = set(raw["final_result"].dropna().unique())
check(outcomes == {"Distinction", "Fail", "Pass", "Withdrawn"}, f"outcomes {outcomes}", f"unexpected outcomes {outcomes}")

# master_raw intentional NaN / zeros
vle_zero = (raw["total_clicks"] == 0).sum()
check(vle_zero == 3365, f"zero VLE {vle_zero}", f"zero VLE count {vle_zero} not 3365")
delay_nan = raw["avg_submission_delay"].isna().sum()
check(7000 < delay_nan < 7500, f"avg_submission_delay NaN {delay_nan} (documented)", f"unexpected delay NaN {delay_nan}")

# Scaler sanity
import joblib

sc = joblib.load(scaler)
check(len(sc.mean_) == len(FEATURE_COLS), "scaler n_features", "scaler feature count wrong")
check(np.allclose(X.mean(axis=0), 0, atol=0.02), "X_scaled mean~0", "X_scaled means not ~0")
check(np.allclose(X.std(axis=0), 1, atol=0.06), "X_scaled std~1", "X_scaled stds not ~1")

# High correlation count
corr = feat[FEATURE_COLS].corr()
n_high = sum(
    1
    for i, a in enumerate(FEATURE_COLS)
    for j, b in enumerate(FEATURE_COLS)
    if j > i and abs(corr.loc[a, b]) > 0.7
)
check(n_high == 6, f"6 high-corr pairs (documented)", f"{n_high} pairs |r|>0.7 (expected 6)")

# studentInfo anchor
si = pd.read_csv(RAW / "studentInfo.csv")
check(len(si) == 32_593, "studentInfo rows = 32,593", f"studentInfo {len(si)} rows")

print("=== OK ===")
for line in ok:
    print("  ✓", line)
if issues:
    print("\n=== ISSUES ===")
    for line in issues:
        print("  ✗", line)
    sys.exit(1)
print(f"\nAll {len(ok)} checks passed. Ready for clustering on X_scaled.npy.")
