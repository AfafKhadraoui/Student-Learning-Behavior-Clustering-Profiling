"""/api/clusters.

Serves the live cluster summaries and radar data used by the dashboard.
"""

from fastapi import APIRouter

from app.core.data_loader import get_data_store
from app.schemas.dashboard import ClusterAnalysis, ClusterSummary, RadarPoint

router = APIRouter()


@router.get("/analysis", response_model=ClusterAnalysis)
def get_cluster_analysis():
    ds = get_data_store()
    profiles = [ClusterSummary(**profile) for profile in ds.cluster_profiles()]
    radar = [RadarPoint(**row) for row in ds.cluster_radar()]

    return ClusterAnalysis(clusters=profiles, radar=radar)