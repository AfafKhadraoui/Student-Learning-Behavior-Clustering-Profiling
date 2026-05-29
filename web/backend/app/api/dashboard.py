"""/api/dashboard.

The frontend renders directly from these model-backed dashboard payloads.
"""
from __future__ import annotations

from fastapi import APIRouter

from app.core.data_loader import get_data_store
from app.schemas.dashboard import (
    ClusterSummary,
    DashboardOverview,
    EngagementPoint,
    KpiMetric,
    StudentBrief,
)
from app.services.student_service import build_student_brief

router = APIRouter()


@router.get("/overview", response_model=DashboardOverview)
def get_overview():
    ds = get_data_store()
    kpis = [KpiMetric(**row) for row in ds.dashboard_kpis()]
    engagement = [EngagementPoint(**row) for row in ds.engagement_overview()]
    clusters = [ClusterSummary(**row) for row in ds.cluster_profiles()]

    # Recent students: build brief rows from master
    recent: list[StudentBrief] = []
    if ds.master is not None:
        recent_df = ds.master.head(5)
        recent = [build_student_brief(row) for _, row in recent_df.iterrows()]

    return DashboardOverview(kpis=kpis, engagement=engagement, clusters=clusters, recentStudents=recent)
