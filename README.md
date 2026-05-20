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
15. [Expected Cluster Profiles](#15-expected-cluster-profiles)
16. [At-Risk Detection System](#16-at-risk-detection-system)
17. [Required Visualizations](#17-required-visualizations)
18. [Team Structure and Timeline](#18-team-structure-and-timeline)
19. [LLM Working Instructions](#19-llm-working-instructions)
20. [Common Pitfalls](#20-common-pitfalls)
21. [References](#21-references)

---

## 1. Project Overview

This project builds an end-to-end machine learning system that applies **unsupervised clustering** to student behavioral data from the Open University Learning Analytics Dataset (OULAD). The system automatically groups students into meaningful learning profiles — High Performer, Consistent Learner, Last-Minute Learner, Struggling Student, and Disengaged/At-Risk — using only behavioral signals derived from their interaction logs, assessment submissions, and academic records.

The system is designed to support academic decision-making by identifying at-risk students **before** they fail or withdraw, enabling targeted early intervention.

### Key Facts

| Property | Value |
|---|---|
| Dataset | OULAD (Kuzilek et al., 2017) |
| License | CC-BY 4.0 (no ethics approval needed) |
| Total students | 32,593 |
| Working cohort | BBB-2013J (~7,000 students) |
| VLE interaction logs | 10,655,280 rows |
| Engineered features | 20 behavioral constructs |
| ML task | Unsupervised clustering |
| Primary algorithm | K-Means |
| Validation benchmark | Peach et al. (2019) — 86% at-risk recall |

---

## 2. Research Question

> **Can unsupervised clustering of students' behavioral signals in OULAD recover educationally meaningful learning profiles — and can those profiles be used to identify at-risk students before they fail or withdraw?**

The answer is **yes** — Peach et al. (2019, *npj Science of Learning*) demonstrated exactly this on the same dataset using unsupervised temporal clustering on VLE click data, recovering a robust 3-cluster partition where 6/7 low-performing students concentrated in a single "massed learning" cluster. This project replicates, extends, and explains that finding with a richer 20-feature behavioral model.

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

| File | Rows | Git Status | Role in Project |
|---|---|---|---|
| `studentInfo.csv` | 32,593 | ignored | Primary table. Demographics + `final_result` for post-hoc validation |
| `studentVle.csv` | 10,655,280 | ignored | Core behavioral data. Every click, every day, every material |
| `studentAssessment.csv` | 173,912 | ignored | Submission dates and scores |
| `assessments.csv` | 206 | ignored | Assessment deadlines and weights — join key |
| `vle.csv` | 6,364 | ignored | Activity type per material — join key |
| `studentRegistration.csv` | 32,593 | ignored | Registration + withdrawal dates |
| `courses.csv` | 22 | ignored | Module lengths only — not used |

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

| Attribute | Usage | Reason |
|---|---|---|
| `num_of_prev_attempts` | CORE | Retake history — directly indicates academic struggle |
| `studied_credits` | CORE | Workload context — overloaded vs. disengaged |
| `highest_education` | CORE | Ordinal-encoded entry qualification |
| `age_band` | CORE | Ordinal-encoded age bracket |
| `imd_band` | COVARIATE | Socioeconomic proxy — fairness audit |
| `disability` | COVARIATE | Fairness audit — accommodation check |
| **`final_result`** | **VALIDATION** | **NEVER in X. Post-hoc external validation only.** |

### Category B — VLE Behavioral Data (`studentVle.csv` + `vle.csv`)

| Attribute | Table | Usage | Reason |
|---|---|---|---|
| `date` | studentVle | CORE | Day since module start — temporal backbone |
| `sum_click` | studentVle | CORE | Click count per material per day |
| `id_site` | studentVle | JOIN_KEY | Links to vle.csv for activity_type |
| `activity_type` | vle | CORE | Distinguishes active vs. passive engagement |
| `week_from/week_to` | vle | CORE | Planned usage window per material |

### Category C — Registration (`studentRegistration.csv`)

| Attribute | Usage | Reason |
|---|---|---|
| `date_registration` | CORE | Negative = enrolled before module start (proactivity signal) |
| `date_unregistration` | CORE | Non-null = strongest dropout signal |

### Category D — Assessments (`studentAssessment.csv` + `assessments.csv`)

| Attribute | Table | Usage | Reason |
|---|---|---|---|
| `date_submitted` | studentAssessment | CORE | For computing submission_delay |
| `score` | studentAssessment | CORE | Grade 0–100; <40 = Fail |
| `is_banked` | studentAssessment | COVARIATE | Filter out for repeat students |
| `assessment_type` | assessments | CORE | TMA / CMA / Exam distinction |
| `date` (deadline) | assessments | CORE | For computing submission_delay |
| `weight` | assessments | CORE | For weighted_avg_score |

### Excluded Attributes — With Justification

| Attribute | Reason Excluded |
|---|---|
| `gender` | Not behavioral. Creates demographic clusters, not learning behavior clusters. Protected characteristic. |
| `region` | No behavioral information. Correlates with imd_band already included as covariate. |
| `code_module` / `code_presentation` | Would partition students by course, not behavior. Defeats the purpose. |
| `courses.csv` (all) | Module length only — property of course, not student. |
| `id_student` (raw) | Merge key only. Zero behavioral information. |

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

| Feature | Formula | Profile Signal |
|---|---|---|
| `total_clicks` | `SUM(sum_click)` per student | Overall engagement volume |
| `active_days` | `COUNT(DISTINCT date)` per student | Attendance equivalent |
| `avg_daily_clicks` | `total_clicks / active_days` (0 if active_days=0) | Session intensity |
| `first_activity_day` | `MIN(date)` — negative if before module start | Proactivity signal |

### Group B — Temporal Pattern (6 features)

| Feature | Formula | Profile Signal |
|---|---|---|
| `late_click_ratio` | Clicks in final third / total_clicks | Core Last-Minute Learner detector |
| `early_click_ratio` | Clicks in first third / total_clicks | Proactivity / front-loading |
| `click_in_final_week_ratio` | Clicks in last 7 days / total_clicks | Extreme last-minute indicator |
| `weekly_click_std` | STD of the week_N_clicks columns | High = bursty / cramming pattern |
| `click_trend_slope` | Slope of linear fit through weekly totals | Negative = disengaging → dropout warning |
| `max_daily_clicks` | MAX(sum_click) in any single day | Binge session detector |

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

| Feature | Formula | Profile Signal |
|---|---|---|
| `quiz_click_ratio` | quiz_clicks / total_clicks | Active self-testing behavior |
| `forum_click_ratio` | forum_clicks / total_clicks | Collaborative engagement |
| `resource_click_ratio` | resource_clicks / total_clicks | Passive content consumption |
| `active_vs_passive_ratio` | (quiz + forum) clicks / total_clicks | Deep vs. surface learning |

Activity type mapping from `vle.csv`:
- **Active types:** `quiz`, `forumng`, `ouwiki`, `dataplus`
- **Passive types:** `oucontent`, `resource`, `page`, `url`, `folder`

### Group D — Assessment Behavior (6 features)

| Feature | Formula | Profile Signal |
|---|---|---|
| `weighted_avg_score` | SUM(score × weight) / SUM(weight) | Core academic performance |
| `score_variance` | STD of chronological scores | High = inconsistency / cramming |
| `score_trend_slope` | Slope of linear fit through time-ordered scores | Improving vs. declining |
| `avg_submission_delay` | MEAN(date_submitted − deadline) | Positive = habitually late |
| `missing_submission_rate` | missing_count / total_assessments_due | **Strongest at-risk predictor** |
| `early_submission_rate` | COUNT(delay < −3 days) / total_submitted | High = highly organised |

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

| Feature | Source / Formula | Profile Signal |
|---|---|---|
| `num_prev_attempts` | Direct from studentInfo | Retake history |
| `registration_lead_days` | ABS(date_registration) if negative, else 0 | Proactive enrollment |
| `is_withdrawn` | 1 if date_unregistration is not null, else 0 | Binary dropout flag |

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

| # | Plot | What to Look For |
|---|---|---|
| 1 | Bar chart of `final_result` distribution | Expect ~26% Withdrawn — your largest at-risk group |
| 2 | Histogram of `total_clicks` (log scale) | Heavy right skew — confirms log transform is needed |
| 3 | Histogram of `active_days` | Check for bimodal distribution — two humps hint at two natural clusters |
| 4 | Scatter: `avg_score` vs `total_clicks`, colored by `final_result` | Do failing students cluster in low-clicks + low-score corner? |
| 5 | Heatmap of missing values across all columns | Identify any column with >20% missing — decide impute or drop |
| 6 | Correlation matrix of all numeric raw columns | Flag pairs with >0.85 correlation — you may not need both |
| 7 | Box plots of `total_clicks` split by `final_result` | Do Withdrawn students have lower click medians? (expected: yes) |

### EDA Key Findings to Document

After plotting, document these specific findings in the notebook:

- **Percentage of students by final_result** (exact counts)
- **Percentage of zero-VLE students** (students with total_clicks = 0)
- **Correlation between total_clicks and final_result** (Withdrawn should be lowest)
- **Any highly correlated feature pairs** (>0.85) to consider dropping
- **Skewness values** for total_clicks and max_daily_clicks (expect >3.0 — justifies log transform)

---

## 13. Clustering Models

### Model 1 — K-Means (Primary)

**Purpose:** Main clustering solution. Produces the final named profiles.

**Configuration:**
```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.metrics import calinski_harabasz_score

# Always use these settings
KMeans(
    n_clusters=K,
    init='k-means++',      # better initialization than random
    n_init=10,             # run 10 times with different seeds
    max_iter=500,
    random_state=42
)
```

**K Selection Process:**
1. Run K-Means for K = 2, 3, 4, 5, 6, 7, 8
2. Record inertia, Silhouette Score, DBI, CHI for each K
3. Plot Elbow (inertia vs K) + Silhouette vs K side by side
4. Choose K where elbow bends **AND** Silhouette peaks
5. For OULAD BBB-2013J data, expect optimal K = 4 or 5

**After training final model:**
```python
# Inverse-transform centroids to original scale for human-readable interpretation
centroids_original = scaler.inverse_transform(kmeans.cluster_centers_)
centroid_df = pd.DataFrame(centroids_original, columns=FEATURE_COLS)
print(centroid_df.round(2))
# This table tells you what the "average student" in each cluster looks like
```

### Model 2 — Hierarchical Clustering (Validation)

**Purpose:** Independently confirms K-Means result. If ARI > 0.6, clusters are robust.

```python
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score

# Run on full dataset with same K as K-Means
hc = AgglomerativeClustering(n_clusters=BEST_K, linkage='ward')
hc_labels = hc.fit_predict(X_scaled)

# Compute ARI — key validation metric
ari = adjusted_rand_score(kmeans_labels, hc_labels)
print(f'ARI (K-Means vs Hierarchical): {ari:.4f}')
# ARI > 0.6 = strong agreement = clusters are not algorithm artifacts
```

**Dendrogram:** Run on 200–300 student sample only (full dataset is unreadable).

### Model 3 — DBSCAN (Outlier Detection)

**Purpose:** Identifies students who fit no cluster — label = -1. These are the most severely at-risk.

**Eps Tuning (mandatory before running):**
```python
from sklearn.neighbors import NearestNeighbors
import numpy as np

# 5th nearest neighbor distance plot
k = 5
nbrs = NearestNeighbors(n_neighbors=k).fit(X_scaled)
distances, _ = nbrs.kneighbors(X_scaled)
dist_sorted = np.sort(distances[:, k-1])[::-1]

# Plot and find the elbow — that value is your eps
plt.plot(dist_sorted)
plt.title('k-NN Distance Plot — elbow = good eps value')
plt.ylabel('5th nearest neighbor distance')
plt.savefig('../figures/knn_distance.png', dpi=150)
```

**Starting parameters:** `eps=1.5`, `min_samples=10` — adjust based on knn plot.

**After running:**
```python
# Students labeled -1 are the most extreme outliers
noise_students = master[master['cluster_dbscan'] == -1]
print(f'Noise students: {len(noise_students)}')
print(noise_students['final_result'].value_counts())
# Expected: Fail and Withdrawn dominate noise students
```

### Model 4 — Gaussian Mixture Models (Bonus)

**Purpose:** Probabilistic soft assignments. BIC selects K automatically. Identifies borderline students.

```python
from sklearn.mixture import GaussianMixture

# Run for K = 2 to 8, select K with lowest BIC
bics = []
for k in range(2, 9):
    gmm = GaussianMixture(n_components=k, covariance_type='full', random_state=42)
    gmm.fit(X_pca)
    bics.append(gmm.bic(X_pca))

best_k_gmm = np.argmin(bics) + 2
gmm_final = GaussianMixture(n_components=best_k_gmm, random_state=42)
gmm_final.fit(X_pca)

# Soft assignments — probability matrix (n_students × n_clusters)
proba_matrix = gmm_final.predict_proba(X_pca)
master['cluster_gmm'] = gmm_final.predict(X_pca)
master['gmm_max_prob'] = proba_matrix.max(axis=1)

# Borderline students (below 60% confidence) — between profiles
borderline = master[master['gmm_max_prob'] < 0.6]
print(f'Borderline students: {len(borderline)} ({len(borderline)/len(master)*100:.1f}%)')
```

---

## 14. Evaluation Protocol

### Internal Metrics

| Metric | Formula (conceptual) | Target | Direction |
|---|---|---|---|
| Silhouette Score | (b − a) / max(a, b) | > 0.5 strong > 0.7 | Higher is better |
| Davies-Bouldin Index | (1/k) Σ max(within/between) | < 1.0 | Lower is better |
| Calinski-Harabasz Index | (between / within) × scale | Maximize | Higher is better |
| Adjusted Rand Index | Corrected agreement between two clusterings | > 0.6 for robustness | Higher is better |

### Evaluation Summary Table — Fill In After Running

| Algorithm | Silhouette ↑ | DBI ↓ | CHI ↑ | ARI vs K-Means | Notes |
|---|---|---|---|---|---|
| K-Means (K=4) | — compute — | — compute — | — compute — | 1.0 (reference) | Primary model |
| K-Means (K=5) | — compute — | — compute — | — compute — | — | Compare to K=4 |
| Hierarchical (Ward) | — compute — | — compute — | — compute — | — compute — | ARI >0.6 = robust |
| DBSCAN | — compute (excl. noise) — | — | — | — compute — | N noise = ? |
| GMM (BIC-optimal) | — compute — | — | — | — compute — | Optimal K = ? |

### External Validation — Three Required Layers

```python
# Cross-tabulate cluster labels vs. actual final_result
crosstab = pd.crosstab(
    master['cluster_label'],     # named labels (High Performer, etc.)
    master['final_result'],
    normalize='index'
) * 100
print(crosstab.round(1))

# Target: Struggling + Disengaged clusters should contain 70-85% Fail/Withdrawn
# Peach et al. benchmark: 86% at-risk recall
```

**Three validation layers — all must appear in the final report:**
1. **Quantitative:** Silhouette > 0.5 confirms statistical separation
2. **Cross-algorithm:** ARI > 0.6 confirms K-Means and Hierarchical independently found same structure
3. **Post-hoc external:** Fail/Withdrawn students concentrate in at-risk clusters

---

## 15. Expected Cluster Profiles

After clustering, interpret each cluster by reading its **inverse-transformed centroid values**. The label is determined by the combination of distinguishing features.

### Profile 1 — High Performer / Early Bird
- **first_activity_day:** negative (started before module)
- **early_submission_rate:** high (submits 3+ days before deadlines)
- **weighted_avg_score:** high (typically > 65)
- **active_vs_passive_ratio:** high (uses forums and quizzes)
- **score_variance:** low (consistent, not erratic)
- **Risk level:** Low. No intervention needed.

### Profile 2 — Consistent / On-Track Learner
- **active_days:** high (steady weekly presence)
- **weekly_click_std:** low (no dramatic spikes)
- **avg_submission_delay:** small (mostly on time)
- **score_trend_slope:** flat or slightly positive (stable or improving)
- **weighted_avg_score:** moderate (typically 50–70)
- **Risk level:** Low–Moderate. Candidate for personalized recommendations.

### Profile 3 — Last-Minute Learner / Crammer
- **click_in_final_week_ratio:** high (majority of activity in final days)
- **max_daily_clicks:** very high (extreme single-day binges)
- **weekly_click_std:** high (silence then frenzy near deadlines)
- **late_submission_rate:** high (regularly misses deadlines)
- **score_variance:** high (inconsistent performance)
- **Risk level:** Moderate. Peach et al. found most low performers here.

### Profile 4 — Struggling Student
- **missing_submission_rate:** high (skips many assignments)
- **weighted_avg_score:** low (multiple below-40 scores)
- **num_prev_attempts:** often > 0 (retake student)
- **active_days:** low (rarely logs in)
- **Risk level:** High. Primary intervention target before module midpoint.

### Profile 5 — Disengaged / Withdrawn
- **total_clicks:** ≈ 0 (essentially never used the platform)
- **is_withdrawn:** 1 (confirmed or imminent dropout)
- **submission_rate:** < 50% (skips most work entirely)
- **click_trend_slope:** strongly negative (stopped engaging early)
- **last_access_day:** very early relative to module length
- **Risk level:** Maximum. Intervention possible in weeks 1–3 only.

### Labeling Process

```python
# After clustering, compute cluster profile table
profile_table = master.groupby('cluster_kmeans')[FEATURE_COLS].mean().round(2)
print(profile_table)

# Manually assign labels based on centroid values
# The label is YOUR scientific interpretation — document your reasoning
cluster_labels = {
    0: 'High Performer',
    1: 'Consistent Learner',
    2: 'Last-Minute Learner',
    3: 'Struggling Student',
    # Add cluster 4 if K=5
}
master['cluster_label'] = master['cluster_kmeans'].map(cluster_labels)
```

---

## 16. At-Risk Detection System

Three-layer composite risk scoring system.

### Layer 1 — Base Cluster Risk Score

| Cluster Label | Base Score |
|---|---|
| High Performer | 0 |
| Consistent Learner | 1 |
| Last-Minute Learner | 2 |
| Struggling Student | 3 |
| DBSCAN Noise Point (-1) | 4 |

### Layer 2 — Individual Threshold Flags (each +1)

```python
master['flag_missing']     = (master['missing_submission_rate'] > 0.5).astype(int)
master['flag_low_score']   = (master['weighted_avg_score'] < 40).astype(int)
master['flag_declining']   = (master['click_trend_slope'] < -0.5).astype(int)
master['flag_inactive']    = (master['last_access_day'] < module_length * 0.5).astype(int)
```

### Layer 3 — Final Risk Score and Action Threshold

```python
base_scores = {'High Performer': 0, 'Consistent Learner': 1,
               'Last-Minute Learner': 2, 'Struggling Student': 3}
master['base_risk'] = master['cluster_label'].map(base_scores).fillna(4)

flag_cols = ['flag_missing', 'flag_low_score', 'flag_declining', 'flag_inactive']
master['risk_score'] = master['base_risk'] + master[flag_cols].sum(axis=1)

# Students with risk_score ≥ 4 → immediate academic advisor contact
master['at_risk'] = (master['risk_score'] >= 4).astype(int)

# Compute and report at-risk precision metric
at_risk_students = master[master['at_risk'] == 1]
actual_fail_withdraw = at_risk_students['final_result'].isin(['Fail', 'Withdrawn']).mean()
print(f"At-risk students flagged: {master['at_risk'].sum()}")
print(f"At-risk precision: {actual_fail_withdraw:.1%} of flagged students actually Failed/Withdrew")
```

---

## 17. Required Visualizations

All 6 must be publication-quality with titles, axis labels, and captions.

| # | Plot | File | How to Make |
|---|---|---|---|
| 1 | Elbow + Silhouette (2-panel) | `figures/elbow_silhouette.png` | Inertia vs K + Silhouette vs K, vertical line at chosen K |
| 2 | PCA 2D Scatter | `figures/pca_clusters.png` | PC1 vs PC2, colored by K-Means cluster label, alpha=0.6 |
| 3 | Cluster Feature Heatmap | `figures/cluster_heatmap.png` | seaborn heatmap, normalized 0–1, clusters as rows |
| 4 | Stacked Bar: Cluster × final_result | `figures/cluster_outcome_bar.png` | pd.crosstab normalized by row, stacked bar |
| 5 | Hierarchical Dendrogram | `figures/dendrogram.png` | 200–300 student sample, Ward linkage, truncate_mode='lastp' |
| 6 | Radar / Spider Chart | `figures/radar_chart.png` | matplotlib polar axes or plotly, 5–6 features, one polygon per cluster |

---

## 18. Team Structure and Timeline

### Roles

| Member | Title | Primary Deliverable |
|---|---|---|
| M1 | Data Engineer | `data/processed/master_raw.csv` |
| M2 | Feature Engineer | `data/processed/master_features.csv` + `X_scaled.npy` + EDA section |
| M3 | Modeling Specialist | `data/processed/master_with_clusters.csv` + eval table + `.pkl` models |
| M4 | Analyst & Presenter | `outputs/student_profiles.csv` + all 6 figures + polished notebook + slides |

### 8-Week Timeline

| Week | Owner | Milestone | Integration Point |
|---|---|---|---|
| 1–2 | M1 | Load OULAD, filter BBB-2013J, all aggregations, master_raw.csv | ⚑ Integration Day 1 |
| 3–4 | M2 | EDA (7 plots), all 20 features, scaling, PCA, master_features.csv | ⚑ Integration Day 2 |
| 5–6 | M3 | All 4 clustering models, evaluation table, models saved | ⚑ Integration Day 3 |
| 7 | M4 | Cluster labeling, at-risk system, all 6 visualizations, notebook polish | — |
| 8 | All | Dry run (Restart & Run All), slides, demo day | ⚑ Demo Day |

### Per-Member Checklists

**M1 — Before handoff to M2:**
- [ ] Row count matches BBB-2013J cohort (~7,000 rows)
- [ ] No NaN in any VLE feature column (all replaced with 0)
- [ ] `final_result` column present and populated
- [ ] Weekly click columns sum to `total_clicks` per student
- [ ] `master_raw.csv` saved to `data/processed/`

**M2 — Before handoff to M3:**
- [ ] All 7 EDA plots completed and in notebook
- [ ] 20 engineered features computed and documented
- [ ] `click_trend_slope` computed using `scipy.stats.linregress`
- [ ] `score_trend_slope` computed using `scipy.stats.linregress`
- [ ] `X_scaled.npy` shape = (n_students, 20), no NaN, all standardized
- [ ] `scaler.pkl` saved to `models/` for M4's centroid inverse-transform
- [ ] `master_features.csv` saved to `data/processed/`

**M3 — Before handoff to M4:**
- [ ] Elbow + Silhouette plot saved to `figures/`
- [ ] All 4 models trained and saved as `.pkl` files
- [ ] `master_with_clusters.csv` has columns: `cluster_kmeans`, `cluster_hc`, `cluster_dbscan`, `cluster_gmm`, `gmm_max_prob`
- [ ] ARI between K-Means and Hierarchical computed and documented
- [ ] Evaluation table complete with real numbers (no "— compute —" left)
- [ ] DBSCAN noise students identified and their `final_result` distribution noted

**M4 — Before demo:**
- [ ] Every cluster has a written label with 2–3 sentence scientific justification
- [ ] At-risk precision metric stated (e.g., "78% of flagged students Failed/Withdrew")
- [ ] All 6 figures saved as high-resolution PNG in `figures/`
- [ ] `student_profiles.csv` contains: `id_student`, `cluster_label`, `risk_score`, `final_result`
- [ ] Notebook runs clean with **Kernel → Restart & Run All** — zero errors
- [ ] Slides cover: dataset intro, feature rationale, model comparison, cluster profiles, at-risk system

---

## 19. LLM Working Instructions

**This section is specifically for AI assistants (Claude, GPT, Copilot, etc.) helping with this project. Read this before generating any code.**

### Project Identity
This is the OULAD student clustering project at ENSIA (École Nationale Supérieure d'Informatique d'Alger), Spring 2025–2026. The task is unsupervised machine learning — clustering, not classification or regression.

### Non-Negotiable Rules

1. **`final_result` NEVER enters the feature matrix X.** It is kept in the DataFrame as a separate column and used only for post-hoc external validation after clustering is complete. Any code that includes `final_result` as a clustering input is wrong.

2. **Zero-VLE students get 0, not the column mean.** Students with no rows in `studentVle.csv` never logged in. Their VLE-derived features must be filled with `0`. Using `.fillna(df.mean())` for these features is wrong.

3. **Cluster on `X_scaled`, not `X_pca`.** PCA is for visualization only (2D scatter plot). All clustering algorithms (K-Means, Hierarchical, DBSCAN) run on the full standardized 20-feature matrix.

4. **`StandardScaler` is mandatory before K-Means.** K-Means uses Euclidean distance. Without scaling, features with large ranges dominate completely.

5. **`random_state=42` everywhere.** Every stochastic operation must use `random_state=42` for reproducibility.

6. **Never pre-commit to K.** The optimal K is determined empirically from Elbow + Silhouette plots. Do not hardcode K=4 as a magic number — it must be justified from the data.

7. **`scipy.stats.linregress` for slopes.** Both `click_trend_slope` and `score_trend_slope` must be computed using `scipy.stats.linregress`, not `numpy.polyfit`, for consistency.

8. **Module scope: BBB-2013J only** for primary analysis. Never mix students from different modules without stratification.

9. **All file paths must be relative** to the repo root using `pathlib.Path`. No hardcoded absolute paths.

10. **Save every trained object.** Scaler, PCA, K-Means, and all other models must be saved with `joblib.dump()` to the `models/` directory.

### Code Style Requirements

```python
# ─── Always import from pathlib ───────────────────────────────────────────────
from pathlib import Path

# ─── Always define paths relative to root ────────────────────────────────────
ROOT     = Path('../')
RAW_DIR  = ROOT / 'data/raw'
PROC_DIR = ROOT / 'data/processed'
MOD_DIR  = ROOT / 'models'
FIG_DIR  = ROOT / 'figures'

# ─── Always use RANDOM_STATE constant ────────────────────────────────────────
RANDOM_STATE = 42
MODULE = 'BBB'
PRES   = '2013J'

# ─── Always add section comments ─────────────────────────────────────────────
# ─── Section name ─────────────────────────────────────────────────────────────

# ─── Always save figures with bbox_inches='tight' ────────────────────────────
plt.savefig(FIG_DIR / 'figure_name.png', dpi=150, bbox_inches='tight')
plt.close()  # always close to free memory
```

### Feature Computation Checklist for LLMs

When generating feature engineering code, verify:
- [ ] `late_click_ratio` uses module's actual max date, not a hardcoded value
- [ ] `click_trend_slope` uses `scipy.stats.linregress`, handles students with < 2 data points (return 0.0)
- [ ] `missing_submission_rate` counts non-submission as a real signal (no row = missing)
- [ ] `avg_daily_clicks` handles division by zero when `active_days = 0`
- [ ] All ratios are clipped to [0, 1] range
- [ ] Students with zero VLE activity receive 0 for all VLE features, not NaN

### Evaluation Code Checklist for LLMs

When generating evaluation code, verify:
- [ ] Silhouette Score computed on `X_scaled`, not `X_pca`
- [ ] DBI computed on `X_scaled`
- [ ] CHI (Calinski-Harabasz) computed on `X_scaled`
- [ ] ARI computed between two label arrays (not between features)
- [ ] DBSCAN evaluation excludes noise points (label = -1) from Silhouette calculation
- [ ] Centroids are inverse-transformed before printing/displaying

### Notebook Section Headers

Every notebook section must start with a markdown cell using this format:

```markdown
## Section X.Y — Section Title
**Owner:** MX  
**Input:** description of input  
**Output:** description of output  
**Key decisions:** bullet list of design choices made in this section
```

---

## 20. Common Pitfalls

| Pitfall | Consequence | Correct Approach |
|---|---|---|
| Including `final_result` in X | Makes task supervised, trivially perfect "validation" | Keep in separate labels_df. Never in X. |
| Filling zero-VLE with mean | Hides most at-risk students in center of feature space | Fill with 0. Zero engagement IS the signal. |
| No StandardScaler before K-Means | Large-range features dominate distance metric entirely | Always scale. No exceptions. |
| Clustering on X_pca | May discard discriminative information | Cluster on X_scaled. Use X_pca for viz only. |
| Mixing all modules | Module length differences create artifactual clusters | Filter to BBB-2013J first. Expand only after validation. |
| Hardcoding K=4 | No scientific justification for K choice | Let Elbow + Silhouette determine K empirically. |
| Notebook hidden state | Errors in front of jury | Kernel → Restart & Run All before every demo. |
| Over-claiming prediction | "We predict failure" is wrong — you cluster behavior | "Our behavioral clusters correlate with outcomes." |
| Reverse-engineering K | Choosing K=4 because you expect 4 profiles | Let data choose K. Adapt labels to whatever K emerges. |
| Not saving scaler.pkl | Cannot inverse-transform centroids for interpretation | Always joblib.dump(scaler, 'models/scaler.pkl') |

---

## 21. References

### [1] Primary Citation
Peach R.L., Yaliraki S.N., Lefevre D., Barahona M. (2019).
*Data-driven unsupervised clustering of online learner behaviour.*
npj Science of Learning, 4, Article 14.
https://doi.org/10.1038/s41539-019-0054-0

### [2] Dataset Citation
Kuzilek J., Hlosta M., Zdrahal Z. (2017).
*Open University Learning Analytics dataset.*
Scientific Data, 4:170171.
https://doi.org/10.1038/sdata.2017.171

### [3] Systematic Review
Jin L., Wang Y., Song H., So H-J. (2024).
*Predictive Modelling with the Open University Learning Analytics Dataset (OULAD): A Systematic Literature Review.*
AIED 2024, CCIS vol. 2150.

---

*Document maintained by: Afaf, Serine, Lydia, Amel — ENSIA ML Project Team, Spring 2025–2026*  
*Last updated: 2025*