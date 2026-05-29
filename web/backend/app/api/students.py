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

    # Build brief for every row first (fast — just column access)
    briefs = df.apply(build_student_brief, axis=1).tolist()

    # Filter
    if cluster != "all":
        briefs = [b for b in briefs if cluster.lower() in b.cluster.lower()]
    if risk != "all":
        briefs = [b for b in briefs if b.risk == risk]
    if q:
        briefs = [b for b in briefs if q.lower() in b.id.lower()]

    return briefs[offset : offset + limit]


@router.get("/{student_id}", response_model=StudentDetail)
def get_student(student_id: str):
    ds = get_data_store()
    row = ds.get_student_row(student_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")

    import pandas as pd
    return build_student_detail(pd.Series(row))