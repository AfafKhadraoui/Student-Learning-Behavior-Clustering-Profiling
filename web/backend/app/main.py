"""
OULAD Student Clustering — FastAPI Backend
==========================================
Serves all data needed by the React frontend:
  /dashboard   → overview KPIs, engagement, clusters
  /students    → filterable student table
  /clusters    → cluster analysis + radar
  /ml-lab      → k-selection, algorithms, model comparison
  /upload      → CSV file status + processing trigger
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import clusters, dashboard, ml_lab, students, upload
from app.core.config import settings
from app.core.data_loader import get_data_store

app = FastAPI(
    title="OULAD Clustering API",
    description="Backend for the OULAD Student Behaviour Clustering dashboard",
    version="1.0.0",
)

# Allow the React dev server (Vite default: 5173) and production build
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(students.router,  prefix="/api/students",  tags=["Students"])
app.include_router(clusters.router,  prefix="/api/clusters",  tags=["Clusters"])
app.include_router(ml_lab.router,    prefix="/api/ml-lab",    tags=["ML Lab"])
app.include_router(upload.router,    prefix="/api/upload",    tags=["Upload"])


@app.on_event("startup")
def warm_data_store() -> None:
    get_data_store()


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0"}