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

# Repo root = three levels up from this file (web/backend/app/)
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import MOD_DIR, PROC_DIR  # noqa: E402

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
    return PROC_DIR / "master_with_clusters.csv"


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
