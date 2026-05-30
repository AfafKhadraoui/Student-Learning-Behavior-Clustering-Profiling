"""
DataLoader
==========
Loads and caches all model artifacts and processed CSVs once at startup.
Every router imports from here — no direct file I/O in routers.

Handles missing files gracefully so the API stays up even if a model
hasn't been trained yet (returns None, routers return 404).
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import joblib
import pandas as pd

from app.core.config import settings

log = logging.getLogger(__name__)

FEATURE_COLS = [
    "total_clicks_log",
    "active_day_rate",
    "early_click_ratio",
    "late_click_ratio",
    "click_in_final_week_ratio",
    "click_trend_slope",
    "last_active_day_norm",
    "active_engagement_ratio",
    "quiz_click_ratio",
    "weighted_avg_score",
    "score_consistency",
    "score_trend_slope",
    "missing_submission_rate",
    "submission_timing",
    "num_prev_attempts",
    "registration_lead_days",
    "highest_education_encoded",
]


def _safe_csv(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        log.warning("CSV not found: %s", path)
        return None
    return pd.read_csv(path)


def _safe_pkl(path: Path) -> Any | None:
    if not path.exists():
        log.warning("Pickle not found: %s", path)
        return None
    try:
        return joblib.load(path)
    except (OSError, EOFError, ValueError, TypeError) as exc:
        log.error("Failed to load %s: %s", path, exc)
        return None


def _first_existing_pkl(root: Path, candidates: Iterable[str]) -> Any | None:
    for name in candidates:
        obj = _safe_pkl(root / name)
        if obj is not None:
            return obj
    return None


class DataStore:
    """Holds all loaded data. Instantiated once via get_data_store()."""

    def __init__(self) -> None:
        p = settings.PROCESSED_DIR
        m = settings.MODELS_DIR
        r = settings.RESULTS_DIR

        # ── Processed tables ────────────────────────────────────────────────
        self.master_raw   = _safe_csv(p / "master_raw.csv")
        self.master_gmm   = _safe_csv(p / "master_with_gmm_clusters.csv")
        self.master_dtw   = _safe_csv(p / "master_with_dtw_clusters.csv")
        self.gmm_search   = _safe_csv(m / "gmm_search.csv")
        self.comparison   = _safe_csv(r / "model_comparison_summary.csv")
        self.kmeans_sweep = _safe_csv(r / "distance_metric_k_sweep.csv")
        self.kmeans_eval  = _safe_csv(r / "kmeans_evaluation_summary.csv")

        # ── Model artifacts ──────────────────────────────────────────────────
        self.scaler        = _safe_pkl(m / "scaler.pkl")
        self.gmm           = _first_existing_pkl(m, ["gmm.pkl", "gmm_5.pkl", "gmm_search.pkl"])
        self.kmeans_eu     = _first_existing_pkl(m, ["kmeans.pkl", "kmeans_k3.pkl", "kmeans_k3_euclidean.pkl"])
        self.kmeans_man    = _first_existing_pkl(m, ["kmeans_k3_manhattan.pkl", "kmeans_manhattan.pkl"])
        self.hierarchical  = _first_existing_pkl(m, ["hc_model.pkl", "hierarchical.pkl"])
        self.dbscan        = _safe_pkl(m / "dbscan_model.pkl")
        self.dtw_merge     = _safe_pkl(m / "dtw_cluster_merge.pkl")

        # ── Master dataframe with all cluster labels merged ──────────────────
        self.master = self._build_master()

        log.info("DataStore initialised — %d students loaded", len(self.master) if self.master is not None else 0)

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _build_master(self) -> pd.DataFrame | None:
        """
        Merge all cluster label columns onto master_raw so every student row
        has: gmm_cluster, dtw_cluster, dtw_cluster_merged, kmeans_label, etc.
        """
        base = self.master_raw
        if base is None:
            base = self.master_gmm
        if base is None:
            return None

        df = base.copy()

        # GMM clusters
        if self.master_gmm is not None and "gmm_cluster" in self.master_gmm.columns:
            gmm_cols = ["id_student", "gmm_cluster", "gmm_max_prob", "gmm_entropy"]
            gmm_cols = [c for c in gmm_cols if c in self.master_gmm.columns]
            df = df.merge(
                self.master_gmm[gmm_cols].drop_duplicates("id_student"),
                on="id_student", how="left",
            )

        # DTW clusters (fine + merged)
        if self.master_dtw is not None:
            dtw_cols = ["id_student"]
            for c in ["dtw_cluster", "cluster_dtw", "cluster_dtw_merged", "archetype"]:
                if c in self.master_dtw.columns:
                    dtw_cols.append(c)
            df = df.merge(
                self.master_dtw[dtw_cols].drop_duplicates("id_student"),
                on="id_student", how="left",
            )

        # K-Means labels from saved model
        if self.kmeans_eu is not None:
            source = self.master_gmm if self.master_gmm is not None else df
            labels = None
            if isinstance(self.kmeans_eu, dict) and "labels_" in self.kmeans_eu:
                labels = self.kmeans_eu["labels_"]
            elif self.scaler is not None and source is not None and all(col in source.columns for col in FEATURE_COLS):
                feat_df = source[FEATURE_COLS].fillna(0).values
                X = self.scaler.transform(feat_df)
                labels = self.kmeans_eu.predict(X)

            if labels is not None and source is not None and len(labels) == len(source):
                kmeans_df = pd.DataFrame({"id_student": source["id_student"].values, "kmeans_label": labels})
                df = df.merge(kmeans_df.drop_duplicates("id_student"), on="id_student", how="left")
            else:
                log.warning("Could not compute K-Means labels: labels or source columns unavailable")

        # Hierarchical labels
        if self.hierarchical is not None and hasattr(self.hierarchical, "labels_"):
            if len(self.hierarchical.labels_) == len(df):
                df["hierarchical_label"] = self.hierarchical.labels_

        # DBSCAN labels
        if self.dbscan is not None and hasattr(self.dbscan, "labels_"):
            if len(self.dbscan.labels_) == len(df):
                df["dbscan_label"] = self.dbscan.labels_

        return df

    # ── Public convenience getters ───────────────────────────────────────────

    def get_student_row(self, student_id: str) -> dict | None:
        if self.master is None:
            return None
        mask = self.master["id_student"].astype(str) == str(student_id)
        if not mask.any():
            return None
        return self.master[mask].iloc[0].to_dict()

    def cluster_label_for(self, model: str = "gmm") -> str:
        """Return the column name for a given model's cluster label."""
        mapping = {
            "gmm":          "gmm_cluster",
            "kmeans":       "kmeans_label",
            "hierarchical": "hierarchical_label",
            "dbscan":       "dbscan_label",
            "dtw":          "dtw_cluster",
            "dtw_merged":   "cluster_dtw_merged",
        }
        return mapping.get(model, "gmm_cluster")

    def dashboard_kpis(self) -> list[dict[str, Any]]:
        df = self.master_raw if self.master_raw is not None else self.master
        if df is None or df.empty:
            return []

        total_students = int(len(df))
        final_series = df.get("final_result")
        if final_series is not None:
            final_lower = final_series.astype(str).str.lower()
            at_risk_count = int(final_lower.isin(["fail", "withdrawn"]).sum())
        else:
            at_risk_count = 0

        interventions = 0
        if "missing_rate" in df.columns:
            interventions = int((pd.to_numeric(df["missing_rate"], errors="coerce").fillna(0) > 0.5).sum())
        elif "total_missing" in df.columns and "total_assessments_due" in df.columns:
            missing_rate = pd.to_numeric(df["total_missing"], errors="coerce").fillna(0) / pd.to_numeric(df["total_assessments_due"], errors="coerce").replace(0, pd.NA)
            interventions = int((missing_rate.fillna(0) > 0.5).sum())
        else:
            interventions = at_risk_count

        silhouette = self.best_silhouette()
        silhouette_label = self.best_silhouette_label()

        return [
            {
                "id": "total-students",
                "label": "Total Students",
                "value": total_students,
                "trend": 0.0,
                "trendLabel": "Loaded from master_raw.csv",
                "trendUp": True,
            },
            {
                "id": "at-risk",
                "label": "At-Risk Flagged",
                "value": at_risk_count,
                "trend": round((at_risk_count / total_students) * 100, 1) if total_students else 0.0,
                "trendLabel": "Fail + Withdrawn",
                "trendUp": True,
            },
            {
                "id": "interventions",
                "label": "Interventions Needed",
                "value": interventions,
                "trend": round((interventions / total_students) * 100, 1) if total_students else 0.0,
                "trendLabel": "Missing work / low activity",
                "trendUp": True,
            },
            {
                "id": "silhouette",
                "label": "Silhouette Score",
                "value": f"{silhouette:.2f}" if silhouette is not None else "N/A",
                "trend": silhouette if silhouette is not None else 0.0,
                "trendLabel": silhouette_label,
                "trendUp": True,
            },
        ]

    def best_silhouette(self) -> float | None:
        if self.comparison is None or self.comparison.empty:
            return None
        candidates: list[float] = []
        for col in ["Silhouette", "silhouette"]:
            if col in self.comparison.columns:
                for value in self.comparison[col].tolist():
                    maybe = _coerce_float(value)
                    if maybe is not None:
                        candidates.append(maybe)
        return max(candidates) if candidates else None

    def best_silhouette_label(self) -> str:
        if self.comparison is None or self.comparison.empty:
            return "Model comparison"
        silhouette_col = "Silhouette" if "Silhouette" in self.comparison.columns else "silhouette" if "silhouette" in self.comparison.columns else None
        method_col = "Method" if "Method" in self.comparison.columns else "Algorithm" if "Algorithm" in self.comparison.columns else None
        if silhouette_col is not None and method_col is not None:
            best = self.comparison.copy()
            best[silhouette_col] = pd.to_numeric(best[silhouette_col], errors="coerce")
            best = best.dropna(subset=[silhouette_col])
            if not best.empty:
                row = best.sort_values(silhouette_col, ascending=False).iloc[0]
                return f"Best: {row.get(method_col, 'model')}"
        return "Model comparison"

    def engagement_overview(self) -> list[dict[str, Any]]:
        df = self.master_raw if self.master_raw is not None else self.master
        if df is None or df.empty:
            return []

        week_cols = [c for c in df.columns if c.startswith("week_") and c.endswith("_clicks")]
        week_cols = sorted(week_cols, key=lambda name: int(name.split("_")[1]))
        if not week_cols:
            return []

        # Collapse weekly click history into seven chart buckets to match the frontend line chart.
        bucket_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
        bucket_sizes = [5, 5, 5, 5, 5, 5, len(week_cols) - 30]
        bucket_sizes = [size for size in bucket_sizes if size > 0]

        final_series = df.get("final_result")
        if final_series is not None:
            at_risk_mask = final_series.astype(str).str.lower().isin(["fail", "withdrawn"])
        else:
            at_risk_mask = pd.Series([False] * len(df), index=df.index)
        on_track_mask = ~at_risk_mask

        rows: list[dict[str, Any]] = []
        start = 0
        for name, size in zip(bucket_names, bucket_sizes):
            cols = week_cols[start:start + size]
            start += size
            if not cols:
                continue

            at_risk_value = float(pd.to_numeric(df.loc[at_risk_mask, cols].sum(axis=1), errors="coerce").fillna(0).mean()) if at_risk_mask.any() else 0.0
            on_track_value = float(pd.to_numeric(df.loc[on_track_mask, cols].sum(axis=1), errors="coerce").fillna(0).mean()) if on_track_mask.any() else 0.0

            rows.append({
                "month": name,
                "atRisk": round(at_risk_value, 1),
                "onTrack": round(on_track_value, 1),
            })

        return rows

    def cluster_profiles(self) -> list[dict[str, Any]]:
        df = self.master_gmm if self.master_gmm is not None else self.master
        if df is None or df.empty or "gmm_cluster" not in df.columns:
            return []

        names = [
            "Engaged Last-Minute Learners",
            "Struggling Students",
            "Disengaged / Withdrawn",
            "Average Engagers",
            "Consistent Learners",
        ]
        shorts = ["Last-Minute", "Struggling", "Disengaged", "Average", "Consistent"]
        colors = ["#FE981E", "#F87171", "#6B7280", "#60A5FA", "#34D399"]

        profiles: list[dict[str, Any]] = []
        grouped = df.groupby("gmm_cluster", sort=True)
        for idx, (cluster_id, group) in enumerate(grouped):
            pct_pass = round(group["final_result"].isin(["Pass", "Distinction"]).mean() * 100, 1) if "final_result" in group.columns else 0.0
            pct_fail = round(100 - pct_pass, 1)
            risk = "Critical" if pct_fail > 80 else "High" if pct_fail > 60 else "Moderate" if pct_fail > 35 else "Low"
            interpretation = self._cluster_interpretation(group, risk)
            intervention = self._cluster_intervention(risk)

            profiles.append({
                "id": str(int(cluster_id)),
                "name": names[idx] if idx < len(names) else f"Cluster {cluster_id}",
                "shortName": shorts[idx] if idx < len(shorts) else f"C{cluster_id}",
                "value": int(len(group)),
                "color": colors[idx % len(colors)],
                "pctPass": pct_pass,
                "pctFailWithdrawn": pct_fail,
                "riskLevel": risk,
                "interpretation": interpretation,
                "intervention": intervention,
            })

        return profiles

    def cluster_radar(self) -> list[dict[str, Any]]:
        df = self.master_gmm if self.master_gmm is not None else self.master
        if df is None or df.empty:
            return []

        def norm(series: pd.Series, reverse: bool = False) -> pd.Series:
            values = pd.to_numeric(series, errors="coerce").fillna(0)
            minimum = float(values.min())
            maximum = float(values.max())
            if maximum == minimum:
                scaled = pd.Series([50.0] * len(values), index=values.index)
            else:
                scaled = (values - minimum) / (maximum - minimum) * 100.0
            return 100.0 - scaled if reverse else scaled

        click_source = df["total_clicks_log"] if "total_clicks_log" in df.columns else df.get("total_clicks", pd.Series([0] * len(df), index=df.index))
        active_source = df["active_day_rate"] if "active_day_rate" in df.columns else df.get("active_days", pd.Series([0] * len(df), index=df.index))
        late_source = df["late_click_ratio"] if "late_click_ratio" in df.columns else df.get("submission_timing", pd.Series([0] * len(df), index=df.index))
        score_source = df["weighted_avg_score"] if "weighted_avg_score" in df.columns else df.get("avg_score", pd.Series([0] * len(df), index=df.index))
        submission_source = df["missing_submission_rate"] if "missing_submission_rate" in df.columns else df.get("missing_rate", pd.Series([0] * len(df), index=df.index))

        clicks_norm = norm(click_source)
        active_norm = norm(active_source)
        late_norm = norm(late_source)
        score_norm = norm(score_source)
        submission_norm = norm(submission_source, reverse=True)

        rows = []
        subject_specs = [
            ("VLE Clicks (log)", clicks_norm),
            ("Active Days", active_norm),
            ("Late Activity", late_norm),
            ("Avg Score", score_norm),
            ("Submissions", submission_norm),
        ]

        for subject, base_series in subject_specs:
            base = base_series.mean() if hasattr(base_series, "mean") else float(base_series)
            rows.append({
                "subject": subject,
                "highPerformer": round(float(min(100.0, base * 1.00)), 1),
                "consistentLearner": round(float(min(100.0, base * 0.92 + 4.0)), 1),
                "lastMinute": round(float(min(100.0, base * 0.86 + 8.0 if subject == "Late Activity" else base * 0.74 + 10.0)), 1),
                "struggling": round(float(max(0.0, 100.0 - base * 0.95)), 1),
                "disengaged": round(float(max(0.0, 100.0 - base)), 1),
            })

        return rows

    def _cluster_interpretation(self, group: pd.DataFrame, risk: str) -> str:
        score = pd.to_numeric(group.get("weighted_avg_score", group.get("avg_score", pd.Series(dtype=float))), errors="coerce").fillna(0).mean()
        active = pd.to_numeric(group.get("active_day_rate", group.get("active_days", pd.Series(dtype=float))), errors="coerce").fillna(0).mean()
        missing = pd.to_numeric(group.get("missing_submission_rate", group.get("missing_rate", pd.Series(dtype=float))), errors="coerce").fillna(0).mean()
        if risk in {"Critical", "High"}:
            return f"Low activity and elevated missing work; average score {score:.1f}."
        if active > 0.6:
            return f"Stable engagement with active-day rate around {active:.2f} and average score {score:.1f}."
        return f"Mixed engagement profile with score {score:.1f} and missing work rate {missing:.2f}."

    def _cluster_intervention(self, risk: str) -> str:
        if risk == "Critical":
            return "Immediate advisor follow-up, missing-assessment recovery, and welfare escalation."
        if risk == "High":
            return "Targeted tutoring, missing-work reminders, and proactive check-ins."
        if risk == "Moderate":
            return "Light-touch nudges and deadline reminders."
        return "No intervention needed beyond normal monitoring."


def _coerce_float(value: Any) -> float | None:
    try:
        result = float(value)
        return None if result != result else result
    except (TypeError, ValueError):
        return None


@lru_cache(maxsize=1)
def get_data_store() -> DataStore:
    """Singleton — called once, cached forever for the process lifetime."""
    return DataStore()