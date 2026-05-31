# K-Means Pipeline

This document describes the K-Means workflow implemented in `notebooks/03_kmeans_clustering.ipynb` and the supporting helpers in `src/clustering/`.

## Inputs

- `data/processed/master_features.csv` for the feature table.
- `data/processed/X_scaled.npy` for the standardised feature matrix.
- `data/processed/X_pca_2d.npy` for 2D visualisations.
- `data/processed/master_features_with_clusters.csv` for the final labeled table.

## Pipeline steps

1. Load the processed feature table and the saved scaled matrix.
2. Inspect feature balance, outliers, and distance behavior.
3. Sweep candidate values of `k` to compare inertia, silhouette score, Davies-Bouldin index, and Calinski-Harabasz score.
4. Train the final K-Means model on the selected feature space.
5. Save the fitted model and the cluster labels to `models/` and `data/processed/`.
6. Generate plots and interpretation tables in `figures/` and `reports/results/`.

## Outputs

- `models/kmeans.pkl` and related model files.
- `reports/results/kmeans_k_sweep.csv`.
- `reports/results/kmeans_evaluation_summary.csv`.
- `reports/results/cluster_interpretation_ensia.csv`.
- Figures saved under `figures/clustering/`.

## Notebook sections

The notebook is organized in the same order as the implementation:

1. imports and configuration
2. data loading
3. preprocessing and scaling checks
4. distance metric analysis
5. K selection
6. model training
7. stability checks
8. cluster visualisation
9. profile interpretation
10. validation against academic outcomes
11. summary and export

## Notes

- `final_result` is used only after clustering for validation and reporting.
- The clustering step should run on the full scaled feature space, not on the label columns.
- The notebook is the narrative record of the method; `src/` keeps only reusable code.
