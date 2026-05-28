"""
OULAD Clustering API — serves trained models and processed results.

Run from repo root:
    uvicorn web.backend.app.main:app --reload --port 8000

Artifacts expected (after running notebooks):
    - models/scaler.pkl, models/kmeans.pkl
    - data/processed/master_with_clusters.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
from typing import Optional
import json
from pprint import pformat

# Repo root = three levels up from this file (web/backend/app/)
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import MOD_DIR, PROC_DIR  # noqa: E402
try:
    from src.features import FEATURE_COLS
except Exception:
    FEATURE_COLS = None

app = FastAPI(
    title="OULAD Student Clustering API",
    description="Loads .pkl models and processed CSVs produced by the ML pipeline.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _master_path() -> Path:
    # prefer a canonical master file; fall back to other common names
    candidates = [
        PROC_DIR / "master_with_clusters.csv",
        PROC_DIR / "master_with_gmm_clusters.csv",
        PROC_DIR / "master_with_dtw_clusters.csv",
        PROC_DIR / "master_features.csv",
        PROC_DIR / "master_raw.csv",
    ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]


def _mock_path(name: str) -> Path:
    # frontend mock data location (used as fallback)
    return ROOT / "web" / "frontend" / "src" / "data" / "mock" / f"{name}.json"


def _load_mock(name: str):
    p = _mock_path(name)
    if not p.exists():
        return None
    try:
        with open(p, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


@app.get("/health")
def health():
    return {
        "status": "ok",
        "master_exists": _master_path().exists(),
        "kmeans_exists": (MOD_DIR / "kmeans.pkl").exists(),
        "scaler_exists": (MOD_DIR / "scaler.pkl").exists(),
    }


@app.get("/clusters/summary")
def cluster_summary():
    """Cluster counts — implement after master_with_clusters.csv exists."""
    path = _master_path()
    if not path.exists():
        raise HTTPException(
            503,
            "Run notebooks through 07_model_comparison first.",
        )
    import pandas as pd

    df = pd.read_csv(path)
    if "cluster_kmeans" not in df.columns:
        raise HTTPException(503, "cluster_kmeans column missing.")
    counts = df["cluster_kmeans"].value_counts().sort_index().to_dict()
    return {"cluster_counts": counts, "n_students": len(df)}


@app.get("/dashboard/overview")
def dashboard_overview():
    """Return KPIs + engagement + cluster summaries + recent students.
    Falls back to frontend mock JSONs when processed outputs are not available.
    """
    import pandas as pd

    master = _master_path()
    if not master.exists():
        # fallback to mock
        kpis = _load_mock("kpis") or []
        engagement = _load_mock("engagement") or []
        clusters = _load_mock("clusters") or []
        students = (_load_mock("students") or [])[:5]
        return {"kpis": kpis, "engagement": engagement, "clusters": clusters, "recentStudents": students}

    df = pd.read_csv(master)

    total = len(df)
    at_risk = int(df.get("is_at_risk", df.get("at_risk", 0)).fillna(0).astype(int).sum()) if "is_at_risk" in df.columns or "at_risk" in df.columns else 0

    kpis = [
        {"id": "total-students", "label": "Total Students", "value": total, "trend": 0, "trendLabel": "", "trendUp": True},
        {"id": "at-risk", "label": "At-Risk Flagged", "value": at_risk, "trend": 0, "trendLabel": "", "trendUp": True},
        {"id": "interventions", "label": "Interventions Done", "value": 0, "trend": 0, "trendLabel": "", "trendUp": True},
        {"id": "silhouette", "label": "Silhouette Score", "value": "—", "trend": 0, "trendLabel": "", "trendUp": True},
    ]

    # cluster summary: prefer archetype/cluster columns
    cluster_col = None
    for c in ("archetype", "cluster_manhattan", "cluster", "cluster_kmeans"):
        if c in df.columns:
            cluster_col = c
            break

    if cluster_col is not None:
        counts = df[cluster_col].value_counts().to_dict()
        clusters = [{"name": k, "value": int(v), "color": "#6B7280"} for k, v in counts.items()]
    else:
        clusters = _load_mock("clusters") or []

    # recent students
    recent = []
    sample = df.head(6)
    for _, row in sample.iterrows():
        sid = str(row.get("id_student", ""))
        name = row.get("display_name") or row.get("name") or sid
        cluster = row.get(cluster_col) if cluster_col else None
        is_at = int(row.get("is_at_risk", row.get("at_risk", 0)) or 0)
        risk = "High" if is_at else "Low"
        score = None
        # try to compute a simple proxy score from numeric feature columns
        if FEATURE_COLS:
            available = [c for c in FEATURE_COLS if c in df.columns]
            if available:
                vals = row[available].astype(float).fillna(0).values
                if vals.size:
                    # normalize to 0-10
                    s = float(vals.mean())
                    score = round((s - vals.min()) / (vals.max() - vals.min() + 1e-9) * 10, 1)
        recent.append({"id": sid, "name": name, "cluster": cluster or "", "risk": risk, "score": score or 0, "activeDays": int(row.get("active_days", 0) or 0), "submissions": int(row.get("n_submissions", 0) or 0), "avgGrade": float(row.get("avg_grade", row.get("avgScore", 0) or 0))})

    engagement = _load_mock("engagement") or []

    return {"kpis": kpis, "engagement": engagement, "clusters": clusters, "recentStudents": recent}


@app.get("/clusters/analysis")
def clusters_analysis():
    """Return cluster summaries and radar profile (used by Cluster Analysis page)."""
    clusters = _load_mock("clusters") or []
    radar = _load_mock("radar") or []
    return {"clusters": clusters, "radar": radar}


@app.get("/ml-lab")
def ml_lab():
    """Return ML Lab bundle: kSelection, algorithms, comparison, pipeline, clusterProfiles."""
    kSelection = _load_mock("k-selection") or {}
    algorithms = _load_mock("algorithms") or []
    comparison = _load_mock("model-comparison") or []
    pipeline = _load_mock("pipeline") or []
    clusterProfiles = _load_mock("clusters") or []
    return {"kSelection": kSelection, "algorithms": algorithms, "comparison": comparison, "pipeline": pipeline, "clusterProfiles": clusterProfiles}


@app.get("/students")
def students(cluster: Optional[str] = Query(None), risk: Optional[str] = Query(None), q: Optional[str] = Query(None), limit: int = 200):
    """Return students list filtered by cluster, risk, or search query.
    Falls back to mock students if processed master is missing.
    """
    import pandas as pd

    master = _master_path()
    if not master.exists():
        return (_load_mock("students") or [])[:limit]

    df = pd.read_csv(master)

    # Normalize columns
    id_col = "id_student" if "id_student" in df.columns else df.columns[0]
    cluster_col = next((c for c in ("archetype", "cluster_manhattan", "cluster", "cluster_kmeans") if c in df.columns), None)
    is_at_col = "is_at_risk" if "is_at_risk" in df.columns else ("at_risk" if "at_risk" in df.columns else None)

    students = []
    for _, row in df.iterrows():
        sid = str(row.get(id_col, ""))
        name = row.get("display_name") or row.get("name") or sid
        cluster_val = row.get(cluster_col) if cluster_col else ""
        is_at = int(row.get(is_at_col, 0) or 0) if is_at_col else 0
        risk = "High" if is_at else "Low"
        score = float(row.get("avg_score", row.get("avg_grade", 0) or 0)) if ("avg_score" in df.columns or "avg_grade" in df.columns) else 0.0
        students.append({"id": sid, "name": name, "cluster": cluster_val, "risk": risk, "score": score, "activeDays": int(row.get("active_days", 0) or 0), "submissions": int(row.get("n_submissions", 0) or 0), "avgGrade": float(row.get("avg_grade", 0) or 0)})

    # apply filters
    def keep(s):
        if cluster and cluster != "all" and s.get("cluster") != cluster:
            return False
        if risk and risk != "all" and s.get("risk") != risk:
            return False
        if q:
            ql = q.strip().lower()
            if ql not in s.get("name", "").lower() and ql not in s.get("id", "").lower():
                return False
        return True

    filtered = [s for s in students if keep(s)]
    return filtered[:limit]


@app.get("/upload/status")
def upload_status():
    """Return statuses for expected raw CSV files (ready/processing/missing)."""
    raw_dir = ROOT / "data" / "raw"
    required = [
        'studentInfo.csv',
        'studentAssessment.csv',
        'assessments.csv',
        'courses.csv',
        'studentRegistration.csv',
        'studentVle.csv',
        'vle.csv',
    ]
    out = []
    for name in required:
        p = raw_dir / name
        status = 'ready' if p.exists() else 'missing'
        out.append({"name": name, "status": status, "size": f"{p.stat().st_size // 1024} KB" if p.exists() else "0 KB"})
    return out


@app.post("/upload/process")
def upload_process():
    """Trigger processing of uploaded files (stub). Returns a job id.
    In production this would enqueue a background job that runs the ETL notebooks.
    """
    # In this project we only return a job id and instruct the user to run the pipeline.
    return {"jobId": "local-manual-1", "message": "Use the notebooks or scripts to process files (see README)."}


@app.get("/at-risk")
def at_risk_list(limit: int = 100):
    path = _master_path()
    if not path.exists():
        raise HTTPException(503, "Processed data not found.")
    import pandas as pd

    df = pd.read_csv(path)
    if "at_risk" not in df.columns:
        raise HTTPException(503, "Run 08_interpretation_at_risk.ipynb first.")
    flagged = df[df["at_risk"] == 1].head(limit)
    cols = [c for c in ["id_student", "cluster_label", "risk_score", "final_result"] if c in flagged.columns]
    return flagged[cols].to_dict(orient="records")
