# Unsupervised Clustering of Student Behavioral Profiles in OULAD

**Authors:** Afaf, Serine, Lydia, Amel — ENSIA Machine Learning Project  
**Date:** Spring 2025–2026  
**Dataset:** Open University Learning Analytics Dataset (OULAD), cohort BBB-2013J  
**License:** CC-BY 4.0

---

## Abstract

<!-- 150–250 words: research question, method (4 algorithms), key finding, at-risk precision -->

Can unsupervised clustering of behavioral signals recover educationally meaningful learning profiles and support early at-risk identification? We engineered 20 behavioral features from VLE clicks and assessment records, applied K-Means, Hierarchical, DBSCAN, and GMM on standardized features, and validated clusters post-hoc against `final_result`. *[Fill after experiments.]*

---

## 1. Introduction

### 1.1 Motivation
- Online learning scale; need for early intervention
- Peach et al. (2019) benchmark on OULAD

### 1.2 Research question
> Can unsupervised clustering recover meaningful learning profiles and identify at-risk students before failure or withdrawal?

### 1.3 Contributions
- [ ] 20-feature behavioral model
- [ ] Four-algorithm comparison with internal + external metrics
- [ ] At-risk scoring system with reported precision
- [ ] Interactive web dashboard (`web/`)

---

## 2. Related work

| Reference | Relevance |
|-----------|-----------|
| Kuzilek et al. (2017) | OULAD dataset |
| Peach et al. (2019) | Temporal clustering benchmark; 86% at-risk recall |
| Jin et al. (2024) | Systematic review |

---

## 3. Data

### 3.1 OULAD sources
<!-- Table: 7 CSV files, row counts -->

### 3.2 Cohort selection
- Module: `BBB`, Presentation: `2013J`
- Approx. N = *[fill]* students

### 3.3 Ethical note
`final_result` used **only** for post-hoc validation, never as a clustering input.

---

## 4. Methods

### 4.1 Data engineering (M1)
<!-- Merge strategy — see README Section 9 -->

### 4.2 Feature engineering (M2)
<!-- List 20 features in 5 groups -->

### 4.3 Preprocessing
- log1p on skewed counts
- StandardScaler (mandatory)
- PCA for visualization only

### 4.4 Clustering algorithms

| Algorithm | Notebook | Optimal hyperparameters |
|-----------|----------|-------------------------|
| K-Means | `03_kmeans_clustering.ipynb` | K = *[from elbow]* |
| Hierarchical (Ward) | `04_hierarchical_clustering.ipynb` | K = *[same or justified]* |
| DBSCAN | `05_dbscan_clustering.ipynb` | eps = *, min_samples = * |
| GMM | `06_gmm_clustering.ipynb` | components = * |

### 4.5 Evaluation
- Internal: Silhouette, Davies-Bouldin, Calinski-Harabasz (on `X_scaled`)
- External: ARI between models; cluster × `final_result` crosstabs
- At-risk: risk_score ≥ 4 → precision vs Fail/Withdrawn

---

## 5. Results

### 5.1 K-Means
<!-- Paste table / figure refs from notebook 03 -->
![Elbow + Silhouette](../figures/elbow_silhouette.png)

**Cluster profiles:**
| Cluster | Label | Size | % Fail/Withdrawn |
|---------|-------|------|------------------|
| 0 | *[fill]* | | |

### 5.2 Hierarchical
<!-- Dendrogram, ARI with K-Means -->

### 5.3 DBSCAN
<!-- Noise %, noise student outcomes -->

### 5.4 GMM
<!-- Soft assignment insights -->

### 5.5 Model comparison
<!-- Table from 07_model_comparison.ipynb — export to reports/results/evaluation_table.csv -->

| Model | Silhouette | DBI | CHI | Notes |
|-------|------------|-----|-----|-------|
| K-Means | | | | Primary |
| Hierarchical | | | | ARI vs KM: |
| DBSCAN | | | | Noise: % |
| GMM | | | | |

### 5.6 At-risk detection
- Flagged students: *[N]*
- Precision: *[%]* actually Failed or Withdrew

---

## 6. Discussion

### 6.1 Comparison to Peach et al. (2019)
<!-- Distributed vs massed learners, etc. -->

### 6.2 Limitations
- Single cohort primary analysis
- Behavioral proxies, not causal claims
- DBSCAN parameter sensitivity

### 6.3 Future work
- Multi-cohort stratification
- Web dashboard deployment
- Temporal sequence models

---

## 7. Conclusion

*[3–5 sentences summarizing answer to research question.]*

---

## References

1. Kuzilek J., Hlosta M., Zdrahal Z. (2017). *Open University Learning Analytics dataset.* Scientific Data, 4:170171.
2. Peach R.L. et al. (2019). *Data-driven unsupervised clustering of online learner behaviour.* npj Science of Learning, 4:14.
3. Jin L. et al. (2024). *Predictive Modelling with OULAD: A Systematic Literature Review.* AIED 2024.

---

## Appendix

- **A.** Full feature formulas → `README.md` Section 10
- **B.** Evaluation table CSV → `reports/results/evaluation_table.csv`
- **C.** Student profiles → `reports/results/student_profiles.csv`
- **D.** Reproducibility → `requirements.txt`, `RANDOM_STATE=42`
