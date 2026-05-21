"""
M1 — Load and merge OULAD CSV files into master_raw.csv.

Owner: M1 (Afaf) · Notebook: 00_data_engineering.ipynb
Uses all students across all modules; engagement normalized by module length.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src import PROC_DIR, RAW_DIR

OULAD_FILES = [
    "assessments.csv",
    "courses.csv",
    "studentAssessment.csv",
    "studentInfo.csv",
    "studentRegistration.csv",
    "studentVle.csv",
    "vle.csv",
]

LABEL_COLS = ["id_student", "final_result", "code_module", "code_presentation"]

STUDENT_KEYS = ["id_student", "code_module", "code_presentation"]

MAX_WEEK = 33  # covers longest module (~269 days)

VLE_AGG_COLS = [
    "total_clicks",
    "active_days",
    "first_access_day",
    "last_access_day",
    "quiz_clicks",
    "forum_clicks",
    "resource_clicks",
] + [f"week_{w}_clicks" for w in range(MAX_WEEK + 1)]

ASSESS_AGG_COLS = [
    "total_assessments_due",
    "total_submitted",
    "total_missing",
    "avg_score",
    "score_std",
    "avg_submission_delay",
    "late_submission_count",
    "early_submission_count",
]


def load_csv(name: str, raw_dir: Path | None = None, **read_kwargs) -> pd.DataFrame:
    """Load a single OULAD CSV from data/raw/."""
    raw_dir = raw_dir or RAW_DIR
    path = raw_dir / name
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Download OULAD CSVs into data/raw/ — see README Section 5."
        )
    return pd.read_csv(path, **read_kwargs)


def load_oulad(raw_path: Path | None = None) -> dict[str, pd.DataFrame]:
    """
    Load all 7 OULAD CSV files.

    Returns
    -------
    dict
        Keys: courses, assessments, vle, student_info, student_reg,
        student_assess, student_vle
    """
    raw_path = raw_path or RAW_DIR
    vle_dtypes = {
        "code_module": "category",
        "code_presentation": "category",
        "id_student": "int32",
        "id_site": "int32",
        "date": "int32",
        "sum_click": "int32",
    }
    return {
        "courses": load_csv("courses.csv", raw_path),
        "assessments": load_csv("assessments.csv", raw_path),
        "vle": load_csv("vle.csv", raw_path),
        "student_info": load_csv("studentInfo.csv", raw_path),
        "student_reg": load_csv("studentRegistration.csv", raw_path),
        "student_assess": load_csv("studentAssessment.csv", raw_path),
        "student_vle": load_csv(
            "studentVle.csv",
            raw_path,
            dtype=vle_dtypes,
            low_memory=False,
        ),
    }


def add_module_length(
    student_info: pd.DataFrame,
    courses: pd.DataFrame,
) -> pd.DataFrame:
    """
    Left-join module length from courses onto student_info.

    OULAD column: module_presentation_length (days).
    """
    length_col = "module_presentation_length"
    if length_col not in courses.columns and "length" in courses.columns:
        length_col = "length"

    course_len = courses[["code_module", "code_presentation", length_col]].drop_duplicates()
    course_len = course_len.rename(columns={length_col: "module_length"})

    out = student_info.merge(
        course_len,
        on=["code_module", "code_presentation"],
        how="left",
    )
    missing = out["module_length"].isna().sum()
    if missing:
        raise ValueError(f"{missing} students missing module_length after courses join.")
    return out


def build_vle_aggregations(
    student_vle: pd.DataFrame,
    vle: pd.DataFrame,
) -> pd.DataFrame:
    """
    Per-student VLE features for each (id_student, code_module, code_presentation).

    Includes weekly columns week_0_clicks … week_{MAX_WEEK}_clicks.
    """
    vle_sites = vle[["id_site", "code_module", "code_presentation", "activity_type"]]
    sv = student_vle.merge(
        vle_sites,
        on=["id_site", "code_module", "code_presentation"],
        how="left",
    )

    keys = STUDENT_KEYS
    overall = (
        sv.groupby(keys, observed=True)
        .agg(
            total_clicks=("sum_click", "sum"),
            active_days=("date", "nunique"),
            first_access_day=("date", "min"),
            last_access_day=("date", "max"),
        )
        .reset_index()
    )

    sv["week"] = sv["date"] // 7
    weekly = (
        sv.groupby(keys + ["week"], observed=True)["sum_click"]
        .sum()
        .reset_index()
    )
    weekly_wide = weekly.pivot_table(
        index=keys,
        columns="week",
        values="sum_click",
        fill_value=0,
    )
    week_cols = {}
    for w in range(MAX_WEEK + 1):
        col_name = f"week_{w}_clicks"
        week_cols[col_name] = weekly_wide[w] if w in weekly_wide.columns else 0
    weekly_df = pd.DataFrame(week_cols, index=weekly_wide.index).reset_index()

    activity = (
        sv.groupby(keys + ["activity_type"], observed=True)["sum_click"]
        .sum()
        .reset_index()
    )
    activity_wide = activity.pivot_table(
        index=keys,
        columns="activity_type",
        values="sum_click",
        fill_value=0,
    ).reset_index()

    for src, dst in [
        ("quiz", "quiz_clicks"),
        ("forumng", "forum_clicks"),
        ("resource", "resource_clicks"),
    ]:
        activity_wide[dst] = activity_wide[src] if src in activity_wide.columns else 0

    out = overall.merge(weekly_df, on=keys, how="left")
    out = out.merge(
        activity_wide[keys + ["quiz_clicks", "forum_clicks", "resource_clicks"]],
        on=keys,
        how="left",
    )
    return out


def build_assessment_aggregations(
    student_assess: pd.DataFrame,
    assessments: pd.DataFrame,
    *,
    exclude_exam: bool = True,
) -> pd.DataFrame:
    """
    Per-student assessment features per module registration.

    Missing studentAssessment row = did not submit that assessment.
    Excludes is_banked == 1 from score/delay aggregates.
    """
    assess = assessments.copy()
    if exclude_exam:
        assess = assess[assess["assessment_type"] != "Exam"]

    due = (
        assess.groupby(["code_module", "code_presentation"], observed=True)
        .size()
        .reset_index(name="total_assessments_due")
    )

    sa = student_assess.merge(
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
    sa = sa[sa["is_banked"] != 1].copy()
    sa["submission_delay"] = sa["date_submitted"] - sa["date"]

    agg = (
        sa.groupby(STUDENT_KEYS, observed=True)
        .agg(
            total_submitted=("id_assessment", "count"),
            score_std=("score", lambda s: s.std(ddof=1) if len(s) > 1 else 0.0),
            avg_submission_delay=("submission_delay", "mean"),
            late_submission_count=("submission_delay", lambda d: (d > 0).sum()),
            early_submission_count=("submission_delay", lambda d: (d < -3).sum()),
        )
        .reset_index()
    )

    weighted = (
        sa.assign(wscore=sa["score"] * sa["weight"])
        .groupby(STUDENT_KEYS, observed=True)
        .agg(wsum=("wscore", "sum"), wden=("weight", "sum"))
        .reset_index()
    )
    weighted["avg_score"] = np.where(
        weighted["wden"] > 0,
        weighted["wsum"] / weighted["wden"],
        0.0,
    )
    agg = agg.merge(weighted[STUDENT_KEYS + ["avg_score"]], on=STUDENT_KEYS, how="left")

    agg = agg.merge(due, on=["code_module", "code_presentation"], how="left")
    agg["total_missing"] = agg["total_assessments_due"] - agg["total_submitted"]
    agg["total_missing"] = agg["total_missing"].clip(lower=0).fillna(0).astype(int)

    return agg


def build_master_raw(
    student_info: pd.DataFrame,
    courses: pd.DataFrame,
    student_reg: pd.DataFrame,
    student_vle: pd.DataFrame,
    vle: pd.DataFrame,
    student_assess: pd.DataFrame,
    assessments: pd.DataFrame,
) -> pd.DataFrame:
    """
    Full pipeline: module length, registration, VLE, assessments, normalize, zero-fill.

    Returns one row per studentInfo row (all modules).
    """
    master = add_module_length(student_info, courses)

    reg = student_reg[STUDENT_KEYS + ["date_registration", "date_unregistration"]]
    master = master.merge(reg, on=STUDENT_KEYS, how="left")
    master["is_withdrawn"] = master["date_unregistration"].notna().astype(int)

    vle_agg = build_vle_aggregations(student_vle, vle)
    master = master.merge(vle_agg, on=STUDENT_KEYS, how="left")

    week_cols = [c for c in master.columns if c.startswith("week_") and c.endswith("_clicks")]
    fill_cols = VLE_AGG_COLS + week_cols
    fill_cols = [c for c in fill_cols if c in master.columns]
    master[fill_cols] = master[fill_cols].fillna(0)

    assess_agg = build_assessment_aggregations(student_assess, assessments)
    master = master.merge(assess_agg, on=STUDENT_KEYS, how="left")

    for col in ASSESS_AGG_COLS:
        if col not in master.columns:
            continue
        if col in ("avg_submission_delay", "score_std", "avg_score"):
            continue
        master[col] = master[col].fillna(0)
    master["total_submitted"] = master["total_submitted"].fillna(0).astype(int)
    master["total_missing"] = master["total_missing"].fillna(
        master["total_assessments_due"]
    ).fillna(0).astype(int)
    master["avg_score"] = master["avg_score"].fillna(0)
    master["score_std"] = master["score_std"].fillna(0)
    master["late_submission_count"] = master["late_submission_count"].fillna(0).astype(int)
    master["early_submission_count"] = master["early_submission_count"].fillna(0).astype(int)

    master["clicks_per_day"] = master["total_clicks"] / master["module_length"]
    master["active_day_rate"] = master["active_days"] / master["module_length"]

    assert master.shape[0] == student_info.shape[0], (
        f"Row count changed after merges: {student_info.shape[0]} -> {master.shape[0]}"
    )
    return master


def build_master_raw_from_disk(raw_dir: Path | None = None) -> pd.DataFrame:
    """Load all CSVs from disk and run build_master_raw."""
    data = load_oulad(raw_dir)
    return build_master_raw(
        data["student_info"],
        data["courses"],
        data["student_reg"],
        data["student_vle"],
        data["vle"],
        data["student_assess"],
        data["assessments"],
    )


def save_master_raw(
    master: pd.DataFrame,
    path: Path | None = None,
) -> Path:
    """Write master_raw.csv to data/processed/."""
    path = path or PROC_DIR / "master_raw.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    master.to_csv(path, index=False)
    return path
