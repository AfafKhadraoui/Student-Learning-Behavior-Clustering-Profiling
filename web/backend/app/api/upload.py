"""Upload endpoints used by the frontend upload page.

Provides a small status endpoint and a processing trigger. These are
lightweight and safe — they inspect presence of processed CSVs and return
structured metadata expected by the frontend types.
"""
from __future__ import annotations

from fastapi import APIRouter
import uuid

from app.schemas.dashboard import CsvFile, ProcessJobResponse
from app.core.config import settings

router = APIRouter()


@router.get("/status", response_model=list[CsvFile])
def get_status():
    files = [
        ("master_raw.csv", settings.PROCESSED_DIR / "master_raw.csv"),
        ("master_with_gmm_clusters.csv", settings.PROCESSED_DIR / "master_with_gmm_clusters.csv"),
        ("master_with_dtw_clusters.csv", settings.PROCESSED_DIR / "master_with_dtw_clusters.csv"),
    ]
    out: list[CsvFile] = []
    for name, path in files:
        if path.exists():
            size = f"{path.stat().st_size}"
            status = "ready"
        else:
            size = "0"
            status = "missing"
        out.append(CsvFile(name=name, size=size, status=status))
    return out


@router.post("/process", response_model=ProcessJobResponse)
def trigger_processing():
    # In this lightweight implementation we don't actually run a background
    # job; return a jobId that the frontend can poll if desired.
    job_id = str(uuid.uuid4())
    return ProcessJobResponse(jobId=job_id, message="Processing started (simulated)")
