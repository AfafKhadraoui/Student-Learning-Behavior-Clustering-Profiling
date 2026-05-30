"""
/api/students
=============
  GET /          → filtered list of students
  GET /{id}      → full student detail with all cluster labels
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.core.data_loader import get_data_store
from app.schemas.dashboard import StudentBrief, StudentDetail
from app.services.student_service import build_student_brief, build_student_detail

router = APIRouter()


@router.get("", response_model=list[StudentBrief])
def list_students(
    cluster: str = Query(default="all", description="Filter by cluster name or 'all'"),
    risk:    str = Query(default="all", description="Low | Moderate | High | Critical | all"),
    q:       str = Query(default="",   description="Search by student ID"),
    limit:   int = Query(default=200,  le=2000),
    offset:  int = Query(default=0,    ge=0),
):
    ds = get_data_store()
    if ds.master is None:
        raise HTTPException(status_code=503, detail="Data not loaded")

    df = ds.master.copy()

    # 1. Filter by student ID search query (fast vectorized string match)
    if q:
        df = df[df["id_student"].astype(str).str.contains(str(q), case=False, na=False)]

    # 2. Filter by GMM cluster name
    if cluster != "all":
        df = df[df.apply(lambda r: cluster.lower() in cluster_name(r).lower(), axis=1)]

    # 3. Filter by risk level
    if risk != "all":
        df = df[df.apply(lambda r: infer_risk(r) == risk, axis=1)]

    # 4. Slice the filtered DataFrame (reduce rows to limit/offset)
    sliced_df = df.iloc[offset : offset + limit]

    # 5. Build briefs only for the sliced subset
    briefs = sliced_df.apply(build_student_brief, axis=1).tolist()
    return briefs


@router.get("/{student_id}", response_model=StudentDetail)
def get_student(student_id: str):
    ds = get_data_store()
    row = ds.get_student_row(student_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")

    import pandas as pd
    return build_student_detail(pd.Series(row))