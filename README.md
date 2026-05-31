# OULAD Student Clustering — Complete Project Reference

> **ENSIA · Machine Learning Project · Spring 2025–2026**
> **Team:** 4 Members · **Dataset:** Open University Learning Analytics Dataset (OULAD) · **Task:** Unsupervised Clustering

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Research Question](#2-research-question)
3. [Scientific Foundation](#3-scientific-foundation)
4. [Repository Structure](#4-repository-structure)
5. [Dataset Description](#5-dataset-description)
6. [Module Selection](#6-module-selection)
7. [Attribute Selection](#7-attribute-selection)
8. [The Core Engineering Problem](#8-the-core-engineering-problem)
9. [Data Merge Strategy](#9-data-merge-strategy)
10. [Feature Engineering — All 20 Features](#10-feature-engineering--all-20-features)
11. [Preprocessing Pipeline](#11-preprocessing-pipeline)
12. [Exploratory Data Analysis](#12-exploratory-data-analysis)
13. [Clustering Models](#13-clustering-models)
14. [Evaluation Protocol](#14-evaluation-protocol)
15. [Team Structure and Timeline](#15-team-structure-and-timeline)
16. [References](#16-references)

---

## 1. Project Overview

This project builds an end-to-end machine learning system that applies **unsupervised clustering** to student behavioral data from the Open University Learning Analytics Dataset (OULAD). The implemented notebooks derive student-level features from interaction logs, assessment submissions, and academic records, then group students into behavioral clusters that are interpreted post hoc from the outputs.

The system is designed to support academic decision-making by identifying at-risk students **before** they fail or withdraw, enabling targeted early intervention.

### Key Facts

| Property             | Value                                    |
| -------------------- | ---------------------------------------- |
| Dataset              | OULAD (Kuzilek et al., 2017)             |
| License              | CC-BY 4.0 (no ethics approval needed)    |
| Total students       | 32,593                                   |
| Working cohort       | BBB-2013J (~7,000 students)              |
| VLE interaction logs | 10,655,280 rows                          |
| Engineered features  | 20 behavioral constructs                 |
| ML task              | Unsupervised clustering                  |
| Primary algorithm    | K-Means                                  |
| Validation benchmark | Peach et al. (2019) — 86% at-risk recall |

---

## 2. Research Question

> **Can unsupervised clustering of students' behavioral signals in OULAD recover educationally meaningful learning profiles — and can those profiles be used to identify at-risk students before they fail or withdraw?**

The answer is **yes** — Peach et al. (2019, _npj Science of Learning_) demonstrated exactly this on the same dataset using unsupervised temporal clustering on VLE click data, recovering a robust 3-cluster partition where 6/7 low-performing students concentrated in a single "massed learning" cluster. This project replicates, extends, and explains that finding with a richer 20-feature behavioral model.

---

## 3. Scientific Foundation

### Primary Citation

```
Peach R.L., Yaliraki S.N., Lefevre D., Barahona M. (2019).
"Data-driven unsupervised clustering of online learner behaviour."
npj Science of Learning, 4, Article 14.
https://doi.org/10.1038/s41539-019-0054-0
```

**Key findings from Peach et al.:**

- Applied unsupervised temporal clustering to OULAD `studentVle` data — identical to our planned approach
- Found a robust **3-cluster partition**: (1) Distributed/regular learners, (2) Massed/cramming learners, (3) Outliers with sporadic behavior
- **6 out of 7 low-performing students** concentrated in the cramming cluster (86% at-risk precision)
- Validated results across **two independent cohorts** — results are reproducible, not artifacts
- Their unsupervised approach **outperformed supervised classifiers** (SVM, Decision Tree) trained on statistical features

### Dataset Citation

```
Kuzilek J., Hlosta M., Zdrahal Z. (2017).
"Open University Learning Analytics dataset."
Scientific Data, 4:170171.
https://doi.org/10.1038/sdata.2017.171
```

### Supplementary Reference

```
Jin L., Wang Y., Song H., So H-J. (2024).
"Predictive Modelling with the Open University Learning Analytics Dataset (OULAD):
A Systematic Literature Review."
AIED 2024, CCIS vol. 2150.
```

---

## 4. Repository Structure

```
oulad-student-clustering/
│
├── data/
│   ├── raw/                        # OULAD CSVs — NEVER MODIFIED, git-ignored
│   │   ├── assessments.csv
│   │   ├── courses.csv
│   │   ├── studentAssessment.csv
│   │   ├── studentInfo.csv
│   │   ├── studentRegistration.csv
│   │   ├── studentVle.csv          # 10.6M rows — load carefully
│   │   └── vle.csv
│   └── processed/                  # Pipeline outputs — git-ignored
│       ├── master_raw.csv          # M1 output: one row/student, raw aggregations
│       ├── master_features.csv     # M2 output: 20 engineered features
│       └── master_with_clusters.csv # M3 output: cluster labels added
│
├── notebooks/
│   ├── 00_data_engineering.ipynb   # M1: load, merge, aggregate
│   ├── 01_eda.ipynb                # M2: exploratory data analysis (7 plots)
│   ├── 02_feature_engineering.ipynb # M2: all 20 features + scaling + PCA
│   ├── 03_clustering.ipynb         # M3: K-Means, Hierarchical, DBSCAN, GMM
│   ├── 04_evaluation.ipynb         # M3: metrics, ARI, evaluation table
│   ├── 05_interpretation.ipynb     # M4: labeling, at-risk, visualizations
│   └── MAIN_NOTEBOOK.ipynb         # Final merged demo notebook
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py              # M1: load + merge functions
│   ├── features.py                 # M2: all 20 feature engineering functions
│   ├── preprocessing.py            # M2: scaling, encoding, PCA
│   ├── clustering.py               # M3: model training functions
│   ├── evaluation.py               # M3: Silhouette, DBI, CHI, ARI wrappers
│   └── visualization.py            # M4: all 6 required plot functions
│
├── models/                         # Saved .pkl files — git-ignored
├── figures/                        # Output plots — git-ignored
├── reports/slides/                 # Presentation files
│
├── README.md                       # This file
├── CONTRIBUTING.md                 # Git workflow conventions
├── requirements.txt                # Python dependencies
└── .gitignore                      # Ignores data/, models/, .venv/, etc.
```

---

## 5. Dataset Description

OULAD is a **relational database** split across 7 CSV files, all linkable via `id_student`, `code_module`, and `code_presentation`.

| File                      | Rows       | Git Status | Role in Project                                                      |
| ------------------------- | ---------- | ---------- | -------------------------------------------------------------------- |
| `studentInfo.csv`         | 32,593     | ignored    | Primary table. Demographics + `final_result` for post-hoc validation |
| `studentVle.csv`          | 10,655,280 | ignored    | Core behavioral data. Every click, every day, every material         |
| `studentAssessment.csv`   | 173,912    | ignored    | Submission dates and scores                                          |
| `assessments.csv`         | 206        | ignored    | Assessment deadlines and weights — join key                          |
| `vle.csv`                 | 6,364      | ignored    | Activity type per material — join key                                |
| `studentRegistration.csv` | 32,593     | ignored    | Registration + withdrawal dates                                      |
| `courses.csv`             | 22         | ignored    | Module lengths only — not used                                       |

### Critical Rule: `final_result`

The column `final_result` (Pass / Fail / Distinction / Withdrawn) exists in `studentInfo.csv`. It **must never enter the feature matrix X**. It stays in the master DataFrame for post-hoc external validation only. Including it would make the task supervised and give trivially perfect "validation."

---

## 6. Module Selection

**Primary cohort: `code_module='BBB'`, `code_presentation='2013J'`**

Three reasons:

1. **Largest single cohort** — more students than any other single presentation, providing statistically robust cluster sizes
2. **Balanced assessment mix** — BBB uses both CMA (Computer Marked) and TMA (Tutor Marked) types, giving richer submission behavior signals
3. **Published benchmark** — Peach et al. (2019) used comparable cohort characteristics, enabling direct comparison

After primary analysis is validated, the pipeline can be re-run on all cohorts combined, with `code_module` added as a stratification variable — **never** as a clustering feature.

---

## 7. Attribute Selection

### Usage Type Legend

- `CORE` — goes into feature matrix X
- `VALIDATION` — kept in DataFrame, never in X, used post-hoc only
- `JOIN_KEY` — used only to merge tables, dropped afterward
- `COVARIATE` — used for fairness audit only, not in X

### Category A — Academic Records (`studentInfo.csv`)

| Attribute              | Usage          | Reason                                                |
| ---------------------- | -------------- | ----------------------------------------------------- |
| `num_of_prev_attempts` | CORE           | Retake history — directly indicates academic struggle |
| `studied_credits`      | CORE           | Workload context — overloaded vs. disengaged          |
| `highest_education`    | CORE           | Ordinal-encoded entry qualification                   |
| `age_band`             | CORE           | Ordinal-encoded age bracket                           |
| `imd_band`             | COVARIATE      | Socioeconomic proxy — fairness audit                  |
| `disability`           | COVARIATE      | Fairness audit — accommodation check                  |
| **`final_result`**     | **VALIDATION** | **NEVER in X. Post-hoc external validation only.**    |

### Category B — VLE Behavioral Data (`studentVle.csv` + `vle.csv`)

| Attribute           | Table      | Usage    | Reason                                      |
| ------------------- | ---------- | -------- | ------------------------------------------- |
| `date`              | studentVle | CORE     | Day since module start — temporal backbone  |
| `sum_click`         | studentVle | CORE     | Click count per material per day            |
| `id_site`           | studentVle | JOIN_KEY | Links to vle.csv for activity_type          |
| `activity_type`     | vle        | CORE     | Distinguishes active vs. passive engagement |
| `week_from/week_to` | vle        | CORE     | Planned usage window per material           |

### Category C — Registration (`studentRegistration.csv`)

| Attribute             | Usage | Reason                                                       |
| --------------------- | ----- | ------------------------------------------------------------ |
| `date_registration`   | CORE  | Negative = enrolled before module start (proactivity signal) |
| `date_unregistration` | CORE  | Non-null = strongest dropout signal                          |

### Category D — Assessments (`studentAssessment.csv` + `assessments.csv`)

| Attribute         | Table             | Usage     | Reason                         |
| ----------------- | ----------------- | --------- | ------------------------------ |
| `date_submitted`  | studentAssessment | CORE      | For computing submission_delay |
| `score`           | studentAssessment | CORE      | Grade 0–100; <40 = Fail        |
| `is_banked`       | studentAssessment | COVARIATE | Filter out for repeat students |
| `assessment_type` | assessments       | CORE      | TMA / CMA / Exam distinction   |
| `date` (deadline) | assessments       | CORE      | For computing submission_delay |
| `weight`          | assessments       | CORE      | For weighted_avg_score         |

### Excluded Attributes — With Justification

| Attribute                           | Reason Excluded                                                                                         |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `gender`                            | Not behavioral. Creates demographic clusters, not learning behavior clusters. Protected characteristic. |
| `region`                            | No behavioral information. Correlates with imd_band already included as covariate.                      |
| `code_module` / `code_presentation` | Would partition students by course, not behavior. Defeats the purpose.                                  |
| `courses.csv` (all)                 | Module length only — property of course, not student.                                                   |
| `id_student` (raw)                  | Merge key only. Zero behavioral information.                                                            |

---

## 8. The Core Engineering Problem

**OULAD contains raw event logs. The project requires behavioral features. The bridge is feature engineering.**

```
RAW (what OULAD has)              →  BEHAVIORAL CONSTRUCT (what we derive)
─────────────────────────────────────────────────────────────────────────────
Student clicked material on day 18     → Was this early, mid, or late in module?
Sum of clicks per day                  → Is engagement declining over weeks?
Submission day vs. deadline            → Does this student submit early or late?
No row in studentAssessment            → This student did NOT submit (missing rate)
date_unregistration is not null        → Student withdrew (is_withdrawn = 1)
Activity type = 'quiz'                 → Student actively self-tests (quiz_click_ratio)
```

Every behavioral claim must be traceable to a specific computation on raw OULAD columns. There are no shortcuts.

### The Zero-VLE Problem — Critical Rule

Some students have **zero rows** in `studentVle.csv`. This is **not missing data** — it means they never logged in. Their behavior is the most extreme signal of disengagement.

**Rule:** Fill all VLE-derived features with `0` for these students — **never with the column mean or median.** A student who never logged in is fundamentally different from the average student. Mean-filling would hide them in the center of feature space and prevent the clustering algorithm from detecting them.

---

## 9. Data Merge Strategy

### Step-by-Step Merge Sequence

```
Step 1: Load studentInfo, filter to MODULE='BBB', PRES='2013J'
        → This is your master student list (~7,000 rows)

Step 2: Load studentVle, filter to same module/presentation
        Join vle.csv on id_site to add activity_type to every click row

Step 3: Aggregate studentVle per student:
        - total_clicks = SUM(sum_click)
        - active_days = COUNT(DISTINCT date)
        - first_access_day = MIN(date)
        - last_access_day = MAX(date)
        - weekly totals: assign week = date // 7, then groupby (student, week)
        - quiz_clicks, forum_clicks, resource_clicks (by activity_type)

Step 4: Load assessments, filter to BBB
        Load studentAssessment, filter to students in our cohort
        Merge on id_assessment to attach deadline and weight to each submission
        Compute: submission_delay = date_submitted − deadline

Step 5: Aggregate assessment data per student:
        - weighted_avg_score = SUM(score × weight) / SUM(weight)
        - score_variance = STD(scores)
        - late_submission_count, submitted_count, missing_count
        - avg_submission_delay = MEAN(submission_delay)

Step 6: Load studentRegistration, filter to module
        Extract date_registration and date_unregistration per student

Step 7: LEFT JOIN everything onto studentInfo master list using id_student
        Left join ensures every student in the cohort has exactly one row
        Students with no VLE rows get NaN → fill with 0 (not mean)
        final_result column stays but is masked from X
```

### Master Table Schema — Expected Output of Step 7

After the full merge, `master_raw.csv` should have these columns:

```
IDENTIFIERS (remove before clustering):
  id_student, code_module, code_presentation, final_result

VLE RAW AGGREGATIONS:
  total_clicks, active_days, first_access_day, last_access_day
  week_0_clicks, week_1_clicks, ... week_N_clicks  (one per week)
  quiz_clicks, forum_clicks, resource_clicks, oucontent_clicks

ASSESSMENT RAW AGGREGATIONS:
  weighted_avg_score, score_variance
  submitted_count, missing_count, late_submission_count
  avg_submission_delay

REGISTRATION:
  date_registration, date_unregistration

BACKGROUND (from studentInfo):
  num_of_prev_attempts, studied_credits
  highest_education, age_band, imd_band, disability
```

---

## 10. Feature Engineering — All 20 Features

These 20 features are the **only** inputs to the clustering algorithm. None exist in raw OULAD — all are derived.

### Group A — Overall Engagement (4 features)

| Feature              | Formula                                           | Profile Signal            |
| -------------------- | ------------------------------------------------- | ------------------------- |
| `total_clicks`       | `SUM(sum_click)` per student                      | Overall engagement volume |
| `active_days`        | `COUNT(DISTINCT date)` per student                | Attendance equivalent     |
| `avg_daily_clicks`   | `total_clicks / active_days` (0 if active_days=0) | Session intensity         |
| `first_activity_day` | `MIN(date)` — negative if before module start     | Proactivity signal        |

### Group B — Temporal Pattern (6 features)

| Feature                     | Formula                                   | Profile Signal                           |
| --------------------------- | ----------------------------------------- | ---------------------------------------- |
| `late_click_ratio`          | Clicks in final third / total_clicks      | Core Last-Minute Learner detector        |
| `early_click_ratio`         | Clicks in first third / total_clicks      | Proactivity / front-loading              |
| `click_in_final_week_ratio` | Clicks in last 7 days / total_clicks      | Extreme last-minute indicator            |
| `weekly_click_std`          | STD of the week_N_clicks columns          | High = bursty / cramming pattern         |
| `click_trend_slope`         | Slope of linear fit through weekly totals | Negative = disengaging → dropout warning |
| `max_daily_clicks`          | MAX(sum_click) in any single day          | Binge session detector                   |

**Computing `late_click_ratio` — exact steps:**

```python
module_length = vle_filtered['date'].max()   # e.g., 269 days for BBB
third = module_length // 3                    # 89 days per third
# Flag each VLE row as 'late' if date falls in final third
vle_filtered['is_late'] = vle_filtered['date'] > (2 * third)
late_clicks = vle_filtered[vle_filtered['is_late']].groupby('id_student')['sum_click'].sum()
total_clicks = vle_filtered.groupby('id_student')['sum_click'].sum()
late_click_ratio = (late_clicks / total_clicks).fillna(0)
```

**Computing `click_trend_slope` — exact steps:**

```python
# Build weekly click totals per student
vle_filtered['week'] = vle_filtered['date'] // 7
weekly = vle_filtered.groupby(['id_student', 'week'])['sum_click'].sum().reset_index()

# Fit linear trend per student using scipy.stats.linregress
from scipy import stats

def compute_slope(group):
    if len(group) < 2:
        return 0.0
    slope, _, _, _, _ = stats.linregress(group['week'], group['sum_click'])
    return slope

slopes = weekly.groupby('id_student').apply(compute_slope).rename('click_trend_slope')
# Negative slope = declining engagement (dropout early warning)
```

### Group C — Activity Type (4 features)

| Feature                   | Formula                              | Profile Signal               |
| ------------------------- | ------------------------------------ | ---------------------------- |
| `quiz_click_ratio`        | quiz_clicks / total_clicks           | Active self-testing behavior |
| `forum_click_ratio`       | forum_clicks / total_clicks          | Collaborative engagement     |
| `resource_click_ratio`    | resource_clicks / total_clicks       | Passive content consumption  |
| `active_vs_passive_ratio` | (quiz + forum) clicks / total_clicks | Deep vs. surface learning    |

Activity type mapping from `vle.csv`:

- **Active types:** `quiz`, `forumng`, `ouwiki`, `dataplus`
- **Passive types:** `oucontent`, `resource`, `page`, `url`, `folder`

### Group D — Assessment Behavior (6 features)

| Feature                   | Formula                                         | Profile Signal                  |
| ------------------------- | ----------------------------------------------- | ------------------------------- |
| `weighted_avg_score`      | SUM(score × weight) / SUM(weight)               | Core academic performance       |
| `score_variance`          | STD of chronological scores                     | High = inconsistency / cramming |
| `score_trend_slope`       | Slope of linear fit through time-ordered scores | Improving vs. declining         |
| `avg_submission_delay`    | MEAN(date_submitted − deadline)                 | Positive = habitually late      |
| `missing_submission_rate` | missing_count / total_assessments_due           | **Strongest at-risk predictor** |
| `early_submission_rate`   | COUNT(delay < −3 days) / total_submitted        | High = highly organised         |

**Computing `missing_submission_rate` — exact steps:**

```python
# Get all assessments for this module (excluding Final Exam if desired)
all_assessments = assessments_filtered['id_assessment'].tolist()
total_due = len(all_assessments)

# Count actual submissions per student
submitted_counts = student_assessment_filtered.groupby('id_student')['id_assessment'].count()

# For ALL students in cohort (including those who submitted nothing)
missing_rate = 1 - (submitted_counts.reindex(info['id_student']).fillna(0) / total_due)
```

### Group E — Background (3 features)

| Feature                  | Source / Formula                             | Profile Signal       |
| ------------------------ | -------------------------------------------- | -------------------- |
| `num_prev_attempts`      | Direct from studentInfo                      | Retake history       |
| `registration_lead_days` | ABS(date_registration) if negative, else 0   | Proactive enrollment |
| `is_withdrawn`           | 1 if date_unregistration is not null, else 0 | Binary dropout flag  |

---

## 11. Preprocessing Pipeline

Execute these steps in strict order before any clustering.

### Step 1 — Separate labels from features

```python
LABEL_COLS = ['id_student', 'final_result', 'code_module', 'code_presentation']
labels_df = master[LABEL_COLS].copy()
X_raw = master[FEATURE_COLS].copy()   # FEATURE_COLS = the 20 features only
```

### Step 2 — Log-transform right-skewed features

```python
# total_clicks and max_daily_clicks are extremely right-skewed
# log1p handles zeros gracefully
import numpy as np
for col in ['total_clicks', 'max_daily_clicks', 'active_days']:
    X_raw[f'log_{col}'] = np.log1p(X_raw[col])
    X_raw.drop(col, axis=1, inplace=True)
```

### Step 3 — Ordinal encode categorical features

```python
edu_map = {
    'No Formal quals': 0,
    'Lower Than A Level': 1,
    'A Level or Equivalent': 2,
    'HE Qualification': 3,
    'Post Graduate Qualification': 4
}
age_map = {'0-35': 0, '35-55': 1, '55<=': 2}
imd_map = {f'{i*10}-{(i+1)*10}%': i+1 for i in range(10)}

X_raw['highest_education'] = X_raw['highest_education'].map(edu_map).fillna(2)
X_raw['age_band'] = X_raw['age_band'].map(age_map).fillna(0)
X_raw['imd_band'] = X_raw['imd_band'].map(imd_map).fillna(5)
```

### Step 4 — StandardScaler (mandatory for K-Means)

```python
from sklearn.preprocessing import StandardScaler
import joblib

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)

# Save for centroid inverse-transform later (M4 will need this)
joblib.dump(scaler, '../models/scaler.pkl')
np.save('../data/processed/X_scaled.npy', X_scaled)
```

### Step 5 — PCA (visualization only — do NOT cluster on this)

```python
from sklearn.decomposition import PCA

# Find components for ≥85% explained variance
pca_full = PCA().fit(X_scaled)
cumvar = np.cumsum(pca_full.explained_variance_ratio_)
n_components = np.argmax(cumvar >= 0.85) + 1
print(f'Components for 85% variance: {n_components}')

# Fit final PCA
pca = PCA(n_components=n_components, random_state=42)
X_pca = pca.fit_transform(X_scaled)
joblib.dump(pca, '../models/pca_model.pkl')
np.save('../data/processed/X_pca.npy', X_pca)

# Always keep 2D version for scatter plot
pca_2d = PCA(n_components=2, random_state=42).fit_transform(X_scaled)
master['PC1'] = pca_2d[:, 0]
master['PC2'] = pca_2d[:, 1]
```

> **Rule:** Cluster on `X_scaled` (full features). Use `X_pca` only for 2D scatter visualization. Running K-Means on PCA-reduced data can distort distances if dropped components carry discriminative behavioral information.

---

## 12. Exploratory Data Analysis

M2 must produce exactly these 7 plots before any feature engineering.

### Required EDA Plots

| #   | Plot                                                              | What to Look For                                                        |
| --- | ----------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 1   | Bar chart of `final_result` distribution                          | Expect ~26% Withdrawn — your largest at-risk group                      |
| 2   | Histogram of `total_clicks` (log scale)                           | Heavy right skew — confirms log transform is needed                     |
| 3   | Histogram of `active_days`                                        | Check for bimodal distribution — two humps hint at two natural clusters |
| 4   | Scatter: `avg_score` vs `total_clicks`, colored by `final_result` | Do failing students cluster in low-clicks + low-score corner?           |
| 5   | Heatmap of missing values across all columns                      | Identify any column with >20% missing — decide impute or drop           |
| 6   | Correlation matrix of all numeric raw columns                     | Flag pairs with >0.85 correlation — you may not need both               |
| 7   | Box plots of `total_clicks` split by `final_result`               | Do Withdrawn students have lower click medians? (expected: yes)         |

### EDA Key Findings to Document

After plotting, document these specific findings in the notebook:

- **Percentage of students by final_result** (exact counts)
- **Percentage of zero-VLE students** (students with total_clicks = 0)
- **Correlation between total_clicks and final_result** (Withdrawn should be lowest)
- **Any highly correlated feature pairs** (>0.85) to consider dropping
- **Skewness values** for total_clicks and max_daily_clicks (expect >3.0 — justifies log transform)

---

## 13. Clustering Models

The repository implements four clustering approaches and one comparison notebook.

- `03_kmeans_clustering.ipynb` is the main clustering notebook.
- `04_hierarchical_clustering.ipynb` provides the Ward linkage baseline.
- `05_dbscan_clustering.ipynb` covers density-based clustering and noise points.
- `06_gmm_clustering.ipynb` covers probabilistic clustering.
- `07_model_comparison.ipynb` compares the model outputs.

### K-Means results

The K-Means sweep recorded the highest silhouette score at `k = 3` among the tested values.

| k   | Silhouette | Davies-Bouldin | Calinski-Harabasz | Min cluster % | Max cluster % |
| --- | ---------- | -------------- | ----------------- | ------------- | ------------- |
| 2   | 0.2557     | 1.6764         | 10060.8           | 36.15         | 63.85         |
| 3   | 0.2687     | 1.6744         | 8963.3            | 20.34         | 55.32         |
| 4   | 0.2018     | 1.9022         | 7179.3            | 14.88         | 41.83         |
| 5   | 0.1984     | 1.8592         | 6211.4            | 13.32         | 30.96         |

The main comparison table also records the two final K-Means variants:

| Model                       | Silhouette | DBI    | CHI    |
| --------------------------- | ---------- | ------ | ------ |
| Euclidean K-Means (sklearn) | 0.2687     | 1.6744 | 8963.3 |
| Manhattan K-Means (Lloyd)   | 0.2612     | 1.7200 | 8721.9 |

### GMM results

The GMM search notebook selected a 4-component model with high posterior confidence and clear outcome separation.

| Components | Covariance | Silhouette | CHI    | DBI    | Mean max posterior |
| ---------- | ---------- | ---------- | ------ | ------ | ------------------ |
| 4          | full       | 0.2202     | 5668.3 | 2.5337 | 0.9974             |

The output plot shows one cluster dominated by Withdrawn students, two clusters dominated by Pass students, and one mixed cluster with a larger Fail share.

### Cluster interpretation from the saved table

The interpretation table in `reports/results/cluster_interpretation_ensia.csv` contains the final project labels:

| Cluster | Label                                          | Risk         | Students | Main pattern                                                   |
| ------- | ---------------------------------------------- | ------------ | -------- | -------------------------------------------------------------- |
| 0       | Engaged Last-Minute Learners (Mostly On-Track) | Low-moderate | 17,830   | High engagement with late activity and mostly passing outcomes |
| 1       | Struggling Students (High Missing Work)        | High         | 7,185    | Low activity and very high fail/withdrawn share                |
| 2       | Disengaged / Withdrawn (Minimal VLE Use)       | Very high    | 7,578    | Minimal platform use and the highest withdrawn share           |

---

## 14. Evaluation Protocol

### Internal metrics used in the repo

| Metric                  | Use                                  |
| ----------------------- | ------------------------------------ |
| Silhouette score        | Cluster separation and cohesion      |
| Davies-Bouldin index    | Compactness vs overlap               |
| Calinski-Harabasz index | Between-cluster separation           |
| Adjusted Rand Index     | Agreement between clustering methods |

### Actual outputs captured in the project tables

| Notebook / table                                   | Result                                                                       |
| -------------------------------------------------- | ---------------------------------------------------------------------------- |
| `reports/results/kmeans_k_sweep.csv`               | Best K-Means silhouette at `k = 3`                                           |
| `reports/results/kmeans_evaluation_summary.csv`    | Euclidean K-Means silhouette `0.2687`; Manhattan K-Means silhouette `0.2612` |
| `reports/results/distance_metric_k_sweep.csv`      | Euclidean slightly ahead of Manhattan and Mahalanobis on silhouette          |
| `reports/results/cluster_interpretation_ensia.csv` | 3 final behavioral clusters with the labels shown above                      |
| `models/gmm_search.csv`                            | Best GMM result at `4` components with high posterior confidence             |

### External validation that was actually run

- Cluster vs. `final_result` cross-tabs were used for post-hoc interpretation.
- Outcome plots show one cluster dominated by Withdrawn students, one mixed struggling cluster, and one mostly passing engaged cluster.
- The notebooks use these outputs for interpretation rather than a prewritten expected cluster profile.

---

## 15. Team Structure and Timeline

### Responsibilities

| Person         | Main work                              | Notebook / folder                                                                                              |
| -------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Afaf Khadraoui | Data merge, EDA, feature engineering   | `00_data_engineering.ipynb`, `01_eda.ipynb`, `02_feature_engineering.ipynb`                                    |
| Serine Hacene  | K-Means and frontend                   | `03_kmeans_clustering.ipynb`, `web/frontend/`                                                                  |
| Khalem Lydia   | Hierarchical clustering and DBSCAN     | `04_hierarchical_clustering.ipynb`, `05_dbscan_clustering.ipynb`                                               |
| Amel Saidouni  | GMM, comparison, backend, DTW notebook | `06_gmm_clustering.ipynb`, `07_model_comparison.ipynb`, `08_research_paper_dtw_pure_raw.ipynb`, `web/backend/` |

### Timeline

| Stage     | Owner                         | Result                            |
| --------- | ----------------------------- | --------------------------------- |
| 00 to 02  | Afaf Khadraoui                | Master tables and feature matrix  |
| 03        | Serine Hacene                 | K-Means clustering notebook       |
| 04 and 05 | Khalem Lydia                  | Hierarchical and DBSCAN notebooks |
| 06 and 07 | Amel Saidouni                 | GMM and comparison notebook       |
| 08        | Amel Saidouni                 | DTW raw time-series notebook      |
| Web layer | Serine Hacene + Amel Saidouni | Frontend and backend linking      |

There is no separate `notebook 09` file in the repository. The final integration work is handled in `web/` and `reports/`.

---

## 16. References

### [1] Primary Citation

Peach R.L., Yaliraki S.N., Lefevre D., Barahona M. (2019).
_Data-driven unsupervised clustering of online learner behaviour._
npj Science of Learning, 4, Article 14.
https://doi.org/10.1038/s41539-019-0054-0

### [2] Dataset Citation

Kuzilek J., Hlosta M., Zdrahal Z. (2017).
_Open University Learning Analytics dataset._
Scientific Data, 4:170171.
https://doi.org/10.1038/sdata.2017.171

### [3] Systematic Review

Jin L., Wang Y., Song H., So H-J. (2024).
_Predictive Modelling with the Open University Learning Analytics Dataset (OULAD): A Systematic Literature Review._
AIED 2024, CCIS vol. 2150.

---

_Document maintained by: Afaf Khadraoui, Serine Hacene, Lydia Khalem, Amel Saidouni — ENSIA ML Project Team, Spring 2025–2026_  
_Last updated: 2026_
