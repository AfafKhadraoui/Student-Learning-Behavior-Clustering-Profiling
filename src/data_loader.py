"""
M1 — Data loading and merge (Afaf / Data Engineer).

Owner: M1 · Implement in notebooks/00_data_engineering.ipynb
Reference: README.md Sections 5, 6, 9

Output: data/processed/master_raw.csv (~7,000 rows, BBB-2013J)
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src import MODULE, PRES, PROC_DIR, RAW_DIR

OULAD_FILES = [
    "assessments.csv",
    "courses.csv",
    "studentAssessment.csv",
    "studentInfo.csv",
    "studentRegistration.csv",
    "studentVle.csv",
    "vle.csv",
]

# Kept for post-hoc validation — never use as clustering features
LABEL_COLS = ["id_student", "final_result", "code_module", "code_presentation"]


def load_csv(name: str, raw_dir: Path | None = None, **read_kwargs) -> pd.DataFrame:
    """
    Load one OULAD file from data/raw/.

    Parameters
    ----------
    name : str
        Filename, e.g. 'studentInfo.csv'
    raw_dir : Path, optional
        Defaults to RAW_DIR from src/__init__.py

    Raises
    ------
    FileNotFoundError
        If CSV missing — download OULAD into data/raw/ (README Section 5).
    """
    raw_dir = raw_dir or RAW_DIR
    path = raw_dir / name
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Download OULAD CSVs into data/raw/ — see README Section 5."
        )
    return pd.read_csv(path, **read_kwargs)


def filter_cohort(
    df: pd.DataFrame,
    module: str = MODULE,
    presentation: str = PRES,
) -> pd.DataFrame:
    """
    Keep primary cohort only (default BBB-2013J).

    Parameters
    ----------
    df : DataFrame
        Must contain code_module and code_presentation columns.
    """
    return df[
        (df["code_module"] == module) & (df["code_presentation"] == presentation)
    ].copy()


def build_master_raw(
    module: str = MODULE,
    presentation: str = PRES,
    raw_dir: Path | None = None,
) -> pd.DataFrame:
    """
    Full M1 pipeline — merge steps 1–7 (README Section 9).

    Implement this in 00_data_engineering.ipynb, then copy here when stable.

    Steps (summary)
    ---------------
    1. Load studentInfo → filter module/presentation → master list
    2. Load studentVle + vle → join activity_type → filter cohort
    3. Aggregate VLE per student: total_clicks, active_days, weekly columns, type splits
    4. Load assessments + studentAssessment → delays, scores
    5. Aggregate assessment per student
    6. Load studentRegistration → dates
    7. LEFT JOIN all on id_student; NaN VLE → 0 (not mean); keep final_result

    Returns
    -------
    DataFrame
        One row per student. Columns per README “Master Table Schema”.
        Call save_master_raw() to write data/processed/master_raw.csv.

    Handoff to M2
    -------------
    - Row count ~7,000 for BBB-2013J
    - No NaN in VLE aggregation columns (use 0)
    - final_result present; not used in clustering
    """
    raise NotImplementedError(
        "M1: implement in notebooks/00_data_engineering.ipynb, then move code here."
    )


def save_master_raw(
    master: pd.DataFrame,
    path: Path | None = None,
) -> Path:
    """
    Write master_raw.csv for M2.

    Parameters
    ----------
    master : DataFrame
        Output of build_master_raw()

    Returns
    -------
    Path
        File written under data/processed/
    """
    path = path or PROC_DIR / "master_raw.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    master.to_csv(path, index=False)
    return path
