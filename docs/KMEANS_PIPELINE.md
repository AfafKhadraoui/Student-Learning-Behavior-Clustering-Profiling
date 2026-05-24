# K-Means Clustering Pipeline — Implementation Guide

**Project:** ENSIA · Student Learning Behavior Clustering (OULAD)  
**Notebook:** `notebooks/03_kmeans_clustering.ipynb`  
**Last updated:** May 2026  

This document describes everything implemented for Module 3 (K-Means): design choices, notebook sections step by step, techniques used, file inventory (created / modified / removed), what is shared vs notebook-only, tests, and how to re-run the pipeline.

---

## 1. Design overview

### 1.1 Self-contained notebook + minimal `src/`


| Layer                                      | Role                                                                                                                                                                          |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `**notebooks/03_kmeans_clustering.ipynb`** | **Single source of truth** for the full K-Means story: preprocessing, metrics, training, plots, ENSIA labels, validation. All helpers are defined **inline** in the notebook. |
| `**src/clustering/`**                      | **Thin API** for tests and later notebooks/backend: `fit_kmeans`, `sweep_kmeans_k`, `find_optimal_k`, `train_final_model`, metrics.                                           |
| `**src/utils/helpers.py`**                 | Load processed artifacts (`X_scaled`, `X_pca_2d`, `master_features`) and `load_scaler` for centroid plots.                                                                    |
| `**src/evaluation.py**`                    | Reuses `compute_clustering_metrics` from `src/clustering/evaluate.py` for notebook 07 model comparison.                                                                       |


**Rule:** Run and read notebook 03 for analysis. Import `src.clustering` only when you need programmatic training without opening Jupyter.

### 1.2 Primary model choice

- **k = 3** (chosen from Euclidean k-sweep on full cohort, k = 2…10).
- **Primary cluster column:** `cluster_manhattan` (Manhattan / L1 K-Means via Lloyd + `scipy.spatial.distance.cdist`).
- **Rationale:** Manhattan is more robust to outliers after ±4σ clipping and is common for mixed behavioral rates in ~17 dimensions.

### 1.3 What is *not* used in training

- `final_result` (Pass / Fail / Withdrawn / Distinction) is **never** in `X_scaled` or `X_clipped`.
- It appears only in **Section 10** for post-hoc validation and interpretation tables.

---

## 2. Notebook sections (step by step)

Each section has **markdown** (what & why), **code** (run), and often a follow-up markdown cell **interpreting the output**. Figures are **saved and shown** with `plt.show()`.

### Section 1 — Imports & configuration

- Sets `ROOT = Path("..").resolve()` when run from `notebooks/`.
- Paths: `reports/figures/clustering/`, `reports/results/`, `models/`.
- Imports: NumPy, Pandas, Matplotlib, Seaborn, SciPy, scikit-learn.
- Project imports: `FEATURE_COLS`, `load_processed_clustering_data` from `src.utils.helpers`.
- Defines inline helper blocks (Sections A–E in code): preprocessing, distances, K-Means, evaluation, interpretation.

### Section 2 — Load preprocessed artifacts

**Technique:** Load-only; no re-feature-engineering.


| File                                 | Shape / role                                                  |
| ------------------------------------ | ------------------------------------------------------------- |
| `data/processed/X_scaled.npy`        | (32,593 × 17) standardized features for clustering            |
| `data/processed/X_pca_2d.npy`        | 2D PCA for visualization only (fit in notebook 02)            |
| `data/processed/master_features.csv` | Features + metadata (`id_student`, module, `final_result`, …) |


**Output:** Printed shapes and optional `final_result` balance table (reference only).

### Section 3 — Clustering preprocessing (±4σ clip)

**Technique:** `clip_features(X, low=-4, high=4)` on already standardized `X_scaled`.

**Why:** A few students sit at extreme σ; K-Means (especially Euclidean) is sensitive to squared distance. Clipping caps influence without dropping rows.

**Plots:**

- `preprocessing_outlier_clip.png` — outlier rate per feature (pre-clip) + boxplots after clip.

**Variable used downstream:** `X_clipped` for all clustering and metrics.

### Section 4 — Distance metric analysis

**Techniques:**

1. **Pairwise distance sample** (n = 2,000) for Euclidean, Manhattan, Mahalanobis.
2. **Coefficient of variation (CV)** = std / mean of pairwise distances — higher ⇒ better spread / discrimination.
3. **Multi-metric k-sweep** (k = 2…10) on **7,000-student subsample** — compares silhouette per metric (Euclidean silhouette on assignments; Lloyd for L1/Mahalanobis).

**Plots:**

- `distance_distributions.png` — KDE + CV bar chart.

**Tables:**

- `reports/results/distance_metric_k_sweep.csv`

**Decision (documented in notebook):** Manhattan as **primary** training metric; Euclidean used for k-selection reference.

### Section 5 — Optimal K selection

**Techniques (full 32,593 rows, Euclidean sklearn K-Means, k = 2…10):**


| Metric                 | Meaning                       | Direction |
| ---------------------- | ----------------------------- | --------- |
| Inertia                | Within-cluster sum of squares | Elbow     |
| Silhouette             | Cohesion vs separation        | Higher    |
| Davies–Bouldin (DBI)   | Cluster overlap               | Lower     |
| Calinski–Harabasz (CH) | Between / within variance     | Higher    |


**Selection rule (`recommend_k`):** Among k with `min_cluster_pct ≥ 2%`, pick high silhouette (within 0.05 of max), tie-break with lower DBI.

**Typical result:** **k = 3**.

**Plots:**

- `k_selection_combined.png` — 2×2 elbow / silhouette / DBI / CH.
- `metric_comparison_sweep.png` — metric comparison on subsample.

**Tables:**

- `reports/results/kmeans_k_sweep.csv`

### Section 6 — Train final models

**Techniques:**

- **Euclidean:** `sklearn.cluster.KMeans` — k-means++, `n_init=20`, `max_iter=500`.
- **Manhattan:** Custom **Lloyd** loop with `cdist(..., metric='cityblock')`, k-means++ init.

**Saved models:**

- `models/kmeans_k3_euclidean.pkl`
- `models/kmeans_k3_manhattan.pkl`
- `models/kmeans_k3.pkl`, `models/kmeans.pkl` (primary = Manhattan dict)

**Columns added to master:**

- `cluster_euclidean`, `cluster_manhattan`, `cluster` (alias of Manhattan)

**Tables:**

- `reports/results/kmeans_evaluation_summary.csv`

### Section 7 — Cluster stability (ARI)

**Technique:** **Adjusted Rand Index (ARI)** between label vectors from 15 Manhattan fits (seeds 0, 10, …, 140).

- ARI ≈ 1 ⇒ stable partitions across random initializations.

**Plot:** `cluster_stability_ari.png` — heatmap of pairwise ARI.

### Section 8 — Cluster visualization


| Subsection                   | Technique                                                                                        | Output file                  |
| ---------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------- |
| 8.1 PCA 2D                   | Precomputed `X_pca_2d`; color by cluster                                                         | `pca_clusters.png`           |
| 8.2 UMAP 2D                  | `umap-learn`, n_neighbors=30, min_dist=0.1 (optional if installed)                               | `umap_clusters.png`          |
| 8.3 Centroid heatmap & sizes | Row-normalized centroid heatmap (Euclidean centers → inverse scaler); bar chart of cluster sizes | `centroid_heatmap_sizes.png` |


**Note:** Overlap in 2D PCA is expected; separation lives in 17D.

### Section 9 — Cluster interpretation & profiling

**Techniques:**

1. **Z-score profiles** — per-cluster mean of each feature vs global mean/std.
2. `**classify_profile(z)`** — rule-based ENSIA mapping (order matters):
  - `disengaged` — very low clicks + active days
  - `struggling` — high `missing_submission_rate` (and secondary rules with trend + score)
  - `high_performer` — high clicks, stable trend, low late ratio, high score (visible at k ≥ 4; at k=3 often only three profiles appear)
  - `last_minute_ok` — deadline-concentrated engagement
3. **9.2 Top defining features** — rank z per cluster; bar charts per cluster.
4. **9.3 Cluster heatmap** — full z-score heatmap + pairwise Euclidean distance between cluster z-vectors.
5. **Radar chart** — key behavioral features per cluster.
6. **Interpretation table** — labels, risk, outcomes %, interventions.
7. **Silhouette per sample** — width plot per cluster.

**Plots:**

- `top_defining_features_per_cluster.png`
- `cluster_heatmap_zscores.png`
- `radar_profiles.png`
- `silhouette_per_sample.png`

**Tables:**

- `reports/results/cluster_interpretation_ensia.csv`

**Saved data:**

- `data/processed/master_features_with_clusters.csv`


| Cluster | Typical profile       | Why it can look “the same” as another                     |
| ------- | --------------------- | --------------------------------------------------------- |
| 0       | Last-minute / engaged | High Pass %                                               |
| 1       | Struggling            | ~98% Fail+Withdrawn — **high missing work**, some VLE use |
| 2       | Disengaged            | ~99% Fail+Withdrawn — **near-zero VLE**, high Withdrawn % |


Clusters **1 and 2** share bad **outcomes** but differ on **behavior** (see Section 9.2–9.3). 

### Section 10 — External validation (`final_result`)

**Techniques:**

- Row-normalized **crosstab** cluster × `final_result`
- **Chi-squared** test + **Cramér’s V** effect size
- Stacked bar chart (% within cluster)
- **At-risk precision** — % Fail+Withdrawn among students in struggling + disengaged clusters

**Plot:** `cluster_outcome_stacked.png`

### Section 11 — Summary & conclusions

- Final metrics table, list of saved figures, limitations, future work.
- Writes `master_features_with_clusters.csv` if not already saved.

---

## 3. File inventory

### 3.1 Created or replaced


| Path                                   | Purpose                                                 |
| -------------------------------------- | ------------------------------------------------------- |
| `notebooks/03_kmeans_clustering.ipynb` | Full self-contained pipeline (66 cells, executed)       |
| `scripts/execute_notebook03.py`        | Headless runner: `python scripts/execute_notebook03.py` |
| `reports/figures/clustering/*.png`     | 13 figures (see list below)                             |
| `reports/results/*.csv`                | Sweeps, evaluation, interpretation tables               |
| `docs/KMEANS_PIPELINE.md`              | This document                                           |


**Figures in `reports/figures/clustering/`:**

1. `preprocessing_outlier_clip.png`
2. `distance_distributions.png`
3. `k_selection_combined.png`
4. `metric_comparison_sweep.png`
5. `cluster_stability_ari.png`
6. `pca_clusters.png`
7. `umap_clusters.png`
8. `centroid_heatmap_sizes.png`
9. `top_defining_features_per_cluster.png`
10. `cluster_heatmap_zscores.png`
11. `radar_profiles.png`
12. `silhouette_per_sample.png`
13. `cluster_outcome_stacked.png`

### 3.2 Modified (still in repo)


| Path                             | Change                                                                        |
| -------------------------------- | ----------------------------------------------------------------------------- |
| `src/clustering/__init__.py`     | Minimal re-exports only                                                       |
| `src/clustering/train_kmeans.py` | Training API; no interpret dependency                                         |
| `src/clustering/evaluate.py`     | Metrics + `recommend_k`; no interpret / distance_analysis                     |
| `src/utils/helpers.py`           | Unchanged role; used by notebook 03                                           |
| `requirements.txt`               | Added `nbclient>=0.10`                                                        |
| `docs/ARCHITECTURE.md`           | Notebook 03 noted as self-contained                                           |
| `tests/test_imports.py`          | `test_final_notebooks` checks `03` + `07` (not missing `MAIN_NOTEBOOK.ipynb`) |


---

## 4. What is used vs not used

### 4.1 Used by notebook 03


| Module / file       | Functions used                                      |
| ------------------- | --------------------------------------------------- |
| `src.utils.helpers` | `load_processed_clustering_data`, `load_scaler`     |
| `src.features`      | `FEATURE_COLS` (via helpers / imports)              |
| `src` constants     | `MOD_DIR`, `PROC_DIR`, `RANDOM_STATE`, `REPORT_DIR` |


### 4.2 Used elsewhere (shared library)


| Module                           | Used by                                                                                |
| -------------------------------- | -------------------------------------------------------------------------------------- |
| `src/clustering/train_kmeans.py` | `src/clustering/__init__.py`, `tests/test_imports.py` (`fit_kmeans`, `sweep_kmeans_k`) |
| `src/clustering/evaluate.py`     | `train_kmeans.py`, `src/evaluation.py`, tests                                          |
| `scripts/execute_notebook03.py`  | Manual / CI — executes notebook 03                                                     |


### 4.3 Not used by notebook 03 (by design)

Notebook 03 **does not** `import src.clustering`. It duplicates the logic inline so the narrative and code stay in one file.

Later notebooks (04–07) or a backend **can** call:

```python
from src.clustering import find_optimal_k, fit_kmeans, train_final_model
from src.evaluation import silhouette_on_scaled
```

### 4.4 Helpers not called anywhere (kept for future API)

In `src/utils/helpers.py`, these are exported but **not** used by notebook 03 today:

- `explore_processed_data`
- `print_data_overview`
- `save_figure` / `ensure_output_dirs` / `get_figure_dirs` (notebook saves figures directly to `FIG_DIR`)

They remain small utilities for other notebooks or the web backend; safe to use or trim later.

---

## 5. Tests


| Test                             | File                    | What it checks                                |
| -------------------------------- | ----------------------- | --------------------------------------------- |
| `test_m3_clustering_implemented` | `tests/test_imports.py` | `fit_kmeans`, `sweep_kmeans_k` on random data |
| `test_m3_evaluation_metrics`     | `tests/test_imports.py` | `src.evaluation.silhouette_on_scaled`         |
| `test_algorithm_notebooks_exist` | `tests/test_imports.py` | `notebooks/03_kmeans_clustering.ipynb` exists |
| `test_final_notebooks`           | `tests/test_imports.py` | `03` + `07` present                           |


**Run:**

```bash
python -m pytest tests/test_imports.py -q
```

---

## 6. How to run

### Interactive

```bash
jupyter notebook notebooks/03_kmeans_clustering.ipynb
```

Run all cells from the `notebooks/` directory (or ensure `ROOT` resolves to repo root).

### Headless (saves outputs into the notebook file)

```bash
python scripts/execute_notebook03.py
```

Requires: `pip install -r requirements.txt` (includes `nbclient`).

**Runtime:** ~10–15 minutes on full OULAD (metric subsample + stability + optional UMAP). Set `OMP_NUM_THREADS=1` on Windows to avoid sklearn K-Means MKL warnings (the execute script sets this by default).

### Prerequisites

Run notebooks **00 → 02** first so these exist:

- `data/processed/X_scaled.npy`
- `data/processed/X_pca_2d.npy`
- `data/processed/master_features.csv`
- `models/scaler.pkl`

---

## 7. Typical cluster summary (k = 3, Manhattan)

Results depend on exact run/seed; executed notebook output is authoritative.


| Cluster | Label (typical)        | ~% cohort | Behavioral gist                                |
| ------- | ---------------------- | --------- | ---------------------------------------------- |
| 0       | Engaged last-minute    | ~55%      | High VLE, late clicks, many Pass               |
| 1       | Struggling             | ~22%      | High missing submissions, declining engagement |
| 2       | Disengaged / withdrawn | ~23%      | Near-zero VLE, high Withdrawn                  |


**Validation:** Strong association with `final_result` (χ² significant, Cramér’s V often ≥ 0.3 on full cohort).

---

## 8. Related documentation

- `docs/ARCHITECTURE.md` — repo layout, `data/processed` vs `models/`, notebook vs `src` ownership.
- `notebooks/02_feature_engineering.ipynb` — builds the 17 features and `X_scaled.npy`.

---

## 9. Which `.pkl` to submit?


| File                             | Submit?           | Role                                         |
| -------------------------------- | ----------------- | -------------------------------------------- |
| `**models/kmeans.pkl`**          | **Yes — primary** | Manhattan k=3; official deployment artifact  |
| `**models/scaler.pkl`**          | **Yes**           | Scale new students before cluster assignment |
| `models/kmeans_k3_manhattan.pkl` | Optional          | Same content as `kmeans.pkl`                 |
| `models/kmeans_k3_euclidean.pkl` | Optional          | Comparison only; not used for final labels   |


**Final distance metric:** **Manhattan (L1)**. Euclidean is used only to **choose k** in Section 5.

---

## 10. Exploratory k = 4 (notebook Section 11)

Section 11 tests whether k=3 **Cluster 0** (~55% of cohort) should be split to recover **Consistent** vs **Last-minute** learners.

**Tests run:** within-Cluster-0 Mann–Whitney on `late_click_ratio` halves; k=2 silhouette inside Cluster 0; full Manhattan k=4 model.

**Executed findings:**

| Step | Result |
|------|--------|
| 11.1 Cluster 0 size | **17,830 (54.7%)** — Engaged Last-Minute label |
| 11.1 Mann–Whitney (late-ratio halves) | **p ≈ 0** on all timing/score features |
| 11.1 Silhouette k=2 inside C0 only | **0.342** (above full-cohort k=3 **0.261**) |
| 11.2 k=4 vs k=3 silhouette | **0.191** vs **0.261**; DBI **2.05** vs **1.72** |
| 11.3 k=4 profiles | **0** `high_performer`; **2** `last_minute_ok`; 1 struggling; 1 disengaged |
| 11.4 k=3 C0 → k=4 | **79.7%** → C1, **20.2%** → C3 (both last-minute) |
| 11.4 k=3 C1 → k=4 | **97.1%** → C0 struggling |

**Decision:** keep official **k = 3** (`kmeans.pkl`, `cluster_manhattan`).

---

## 11. Changelog (K-Means refactor)

1. Consolidated pipeline into **one notebook** with inline code and interpretation markdown under each output.
2. Moved all clustering figures under `**reports/figures/clustering/`**.
3. Slimmed `**src/clustering**` to `train_kmeans.py` + `evaluate.py` only.
4. Added **Top defining features** and **z-score cluster heatmap** (Sections 9.2–9.3).
5. Fixed profile rules to separate last-minute vs consistent / struggling vs disengaged using trend and late-click features.
6. Removed unused `**feature_docs.py`** and obsolete generator/runner scripts.
7. Added `**execute_notebook03.py**` and `**nbclient**` for reproducible headless runs.

