"""
Shared helpers for building student response objects.
"""
from __future__ import annotations
from typing import Literal
import pandas as pd
from app.schemas.dashboard import StudentBrief, StudentDetail

ARCHETYPE_NAMES = {
    0: "Struggling / At-risk",
    1: "Last-minute Learner",
    2: "Average Engager",
    3: "High Performer",
    4: "Consistent Learner",
}

def infer_risk(row: pd.Series) -> Literal["Low", "Moderate", "High", "Critical"]:
    final = str(row.get("final_result", "")).lower()
    if final == "withdrawn":
        return "Critical"
    if final == "fail":
        return "High"
    score = row.get("weighted_avg_score") or row.get("avg_score")
    if score is not None:
        if float(score) < 40:
            return "High"
        if float(score) < 55:
            return "Moderate"
    miss = row.get("missing_submission_rate")
    if miss is not None and float(miss) > 0.5:
        return "Moderate"
    return "Low"


def cluster_name(row: pd.Series) -> str:
    # prefer archetype label if available
    arch = row.get("archetype")
    if arch and str(arch) not in ("nan", "None", ""):
        return str(arch)
    gmm = row.get("gmm_cluster")
    if gmm is not None and str(gmm) not in ("nan", ""):
        return ARCHETYPE_NAMES.get(int(float(gmm)), f"Cluster {int(float(gmm))}")
    return "Unassigned"


def build_student_brief(row: pd.Series) -> StudentBrief:
    sid = str(row.get("id_student", ""))
    return StudentBrief(
        id=sid,
        name=f"Student {sid}",
        cluster=cluster_name(row),
        risk=infer_risk(row),
        score=_safe_float(row.get("weighted_avg_score") or row.get("avg_score")),
        activeDays=_safe_int(row.get("active_days") or row.get("total_active_days")),
        submissions=_safe_int(row.get("total_submitted") or row.get("total_assessments_due")),
        avgGrade=_safe_float(row.get("avg_score") or row.get("weighted_avg_score")),
        clicks=_safe_int(row.get("total_clicks") or row.get("total_clicks_log")),
        lastActive=str(row.get("last_active_day", "")) or None,
    )


def build_student_detail(row: pd.Series) -> StudentDetail:
    sid = str(row.get("id_student", ""))
    gmm_c = row.get("gmm_cluster")
    dtw_c = row.get("dtw_cluster") or row.get("cluster_dtw")
    km_c  = row.get("kmeans_label")
    return StudentDetail(
        id=sid,
        name=f"Student {sid}",
        cluster=cluster_name(row),
        clusterGmm=ARCHETYPE_NAMES.get(int(float(gmm_c)), f"GMM-{gmm_c}") if gmm_c is not None and str(gmm_c) not in ("nan",) else None,
        clusterDtw=f"DTW-{int(float(dtw_c))}" if dtw_c is not None and str(dtw_c) not in ("nan",) else None,
        clusterKmeans=f"KM-{int(float(km_c))}" if km_c is not None and str(km_c) not in ("nan",) else None,
        risk=infer_risk(row),
        score=_safe_float(row.get("weighted_avg_score") or row.get("avg_score")),
        clicks=_safe_int(row.get("total_clicks")),
        activeDays=_safe_int(row.get("active_days") or row.get("total_active_days")),
        submissionRate=_safe_float(row.get("submission_rate")),
        lateRate=_safe_float(row.get("late_click_ratio") or row.get("late_submission_rate")),
        gmmMaxProb=_safe_float(row.get("gmm_max_prob")),
        gmmEntropy=_safe_float(row.get("gmm_entropy")),
        finalResult=str(row.get("final_result", "")) or None,
    )


def _safe_float(v) -> float | None:
    try:
        f = float(v)
        return None if f != f else round(f, 4)   # NaN check
    except (TypeError, ValueError):
        return None


def _safe_int(v) -> int | None:
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None