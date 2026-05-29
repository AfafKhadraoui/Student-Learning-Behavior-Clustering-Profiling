"""
Pydantic schemas — one file keeps all response shapes in sync
with the TypeScript types in the frontend.
"""

from __future__ import annotations
from typing import Literal
from pydantic import BaseModel


# ── Shared ────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str


# ── Dashboard ─────────────────────────────────────────────────────────────────

class KpiMetric(BaseModel):
    id: str
    label: str
    value: str | int | float
    trend: float
    trendLabel: str
    trendUp: bool


class EngagementPoint(BaseModel):
    month: str
    atRisk: float
    onTrack: float


class ClusterSummary(BaseModel):
    name: str
    value: int
    color: str
    shortName: str | None = None
    pctPass: float | None = None
    pctFailWithdrawn: float | None = None
    riskLevel: Literal["Low", "Moderate", "High", "Critical", "Low-moderate", "Very high"] | None = None


class StudentBrief(BaseModel):
    id: str
    name: str
    cluster: str
    risk: Literal["Low", "Moderate", "High", "Critical"]
    score: float | None = None
    activeDays: int | None = None
    submissions: int | None = None
    avgGrade: float | None = None
    clicks: int | None = None
    lastActive: str | None = None


class DashboardOverview(BaseModel):
    kpis: list[KpiMetric]
    engagement: list[EngagementPoint]
    clusters: list[ClusterSummary]
    recentStudents: list[StudentBrief]


# ── Students ──────────────────────────────────────────────────────────────────

class StudentDetail(BaseModel):
    id: str
    name: str
    cluster: str
    clusterGmm: str | None = None
    clusterDtw: str | None = None
    clusterKmeans: str | None = None
    risk: Literal["Low", "Moderate", "High", "Critical"]
    score: float | None = None
    clicks: int | None = None
    activeDays: int | None = None
    submissionRate: float | None = None
    lateRate: float | None = None
    gmmMaxProb: float | None = None
    gmmEntropy: float | None = None
    finalResult: str | None = None
    lastActive: str | None = None


# ── Clusters ──────────────────────────────────────────────────────────────────

class RadarPoint(BaseModel):
    subject: str
    highPerformer: float
    consistentLearner: float
    lastMinute: float
    struggling: float
    disengaged: float


class ClusterAnalysis(BaseModel):
    clusters: list[ClusterSummary]
    radar: list[RadarPoint]


# ── ML Lab ────────────────────────────────────────────────────────────────────

class KSelectionMetric(BaseModel):
    k: int
    inertia: float | None = None
    silhouette: float
    daviesBouldin: float
    calinskiHarabasz: float


class DistanceMetric(BaseModel):
    metric: str
    silhouette: float
    selected: bool


class KSelectionResult(BaseModel):
    recommendedK: int
    reason: str
    metrics: list[KSelectionMetric]
    distanceMetrics: list[DistanceMetric]


class ClusteringAlgorithm(BaseModel):
    id: str
    name: str
    description: str
    notebook: str
    artifact: str
    status: Literal["active", "coming-soon", "planned"]
    features: int | None = None
    selectedK: int | None = None
    k: int | None = None


class ModelComparisonRow(BaseModel):
    algorithm: str
    status: Literal["active", "coming-soon", "planned"]
    k: int | None = None
    silhouette: float | None = None
    daviesBouldin: float | None = None
    ariVsKmeans: float | None = None
    noisePct: float | None = None
    notes: str | None = None


class PipelineStep(BaseModel):
    id: str
    name: str
    notebook: str | None = None
    output: str
    status: Literal["complete", "pending", "planned", "in_progress"]


class ClusterProfile(BaseModel):
    id: str
    name: str
    shortName: str
    value: int
    color: str
    pctPass: float
    pctFailWithdrawn: float
    riskLevel: Literal["Low", "Moderate", "High", "Critical"]
    interpretation: str | None = None
    intervention: str | None = None


class MlLabBundle(BaseModel):
    kSelection: KSelectionResult
    algorithms: list[ClusteringAlgorithm]
    comparison: list[ModelComparisonRow]
    pipeline: list[PipelineStep]
    clusterProfiles: list[ClusterProfile]


# ── Upload ────────────────────────────────────────────────────────────────────

class CsvFile(BaseModel):
    name: str
    size: str
    status: Literal["ready", "missing", "processing"]


class ProcessJobResponse(BaseModel):
    jobId: str
    message: str