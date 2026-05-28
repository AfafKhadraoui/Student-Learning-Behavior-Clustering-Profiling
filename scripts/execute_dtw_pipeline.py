"""
Execute the Peach et al. (2019) DTW clustering pipeline.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

from src.features import FEATURE_COLS
from src.clustering.train_dtw import DTWClusteringPipeline
from src.clustering.evaluate import compute_clustering_metrics

def main():
    print("Loading master features...")
    df = pd.read_csv("data/processed/master_features.csv")
    
    # Filter for the specific cohort
    print("Filtering for BBB 2013J cohort...")
    cohort_mask = (df["code_module"] == "BBB") & (df["code_presentation"] == "2013J")
    df_cohort = df[cohort_mask].copy()
    
    # Subsample to N=300 to make pairwise DTW computationally feasible
    if len(df_cohort) > 300:
        print(f"Subsampling cohort from {len(df_cohort)} to 300 students...")
        df_cohort = df_cohort.sample(n=300, random_state=42).copy()
    
    X_raw = df_cohort[FEATURE_COLS].copy()
    X_raw = X_raw.apply(pd.to_numeric, errors='coerce')
    if X_raw.isna().any().any():
        X_raw = X_raw.fillna(X_raw.median())
        
    print("Scaling features...")
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X_raw)
    
    print("Running DTW clustering pipeline...")
    # relaxation is typically tuned, using 0.8 as seen in notebook
    pipeline = DTWClusteringPipeline(sigma_quantile=0.5, relaxation=0.8, random_state=42)
    labels = pipeline.fit_predict(X_scaled)
    
    print("Evaluating clusters...")
    metrics = compute_clustering_metrics(X_scaled, labels)
    print("Clustering Metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v:.4f}")
        
    # Save the resulting assignments
    df_cohort["cluster_dtw"] = labels
    out_path = Path("data/processed/dtw_clusters.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_cohort.to_csv(out_path, index=False)
    print(f"\nSaved cluster assignments to {out_path}")
    
    print("\nCluster Statistics:")
    # Print size and pass rate
    if "final_result" in df_cohort.columns:
        # Create a boolean column for pass rate
        df_cohort["passed"] = df_cohort["final_result"].isin(["Pass", "Distinction"]).astype(int)
        stats = df_cohort.groupby("cluster_dtw").agg(
            size=("id_student", "count"),
            pass_rate=("passed", "mean")
        )
        print(stats)
    else:
        sizes = df_cohort["cluster_dtw"].value_counts().sort_index()
        print(sizes)

    # Save the evaluation summary
    summary_path = Path("reports/results/dtw_evaluation_summary.csv")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    best_res = pipeline.best_resolution_
    best_res_stats = pipeline.multiscale_results_[best_res]
    summary_df = pd.DataFrame([{
        "algorithm": "DTW-RMST-Louvain",
        "n_clusters": int(best_res_stats["n_clusters"]),
        "n_samples": len(df_cohort),
        "modularity": float(best_res_stats["modularity"]),
        "silhouette": float(metrics["silhouette"]),
        "davies_bouldin": float(metrics["davies_bouldin"]),
        "calinski_harabasz": float(metrics["calinski_harabasz"]),
        "best_resolution": float(best_res)
    }])
    summary_df.to_csv(summary_path, index=False)
    print(f"Saved evaluation summary to {summary_path}")

    # Generate and save plots
    figures_dir = Path("figures")
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Multiscale resolution plot
    resolutions = sorted(pipeline.multiscale_results_.keys())
    n_clusters_list = [pipeline.multiscale_results_[r]['n_clusters'] for r in resolutions]
    modularities = [pipeline.multiscale_results_[r]['modularity'] for r in resolutions]
    stabilities = [pipeline.multiscale_results_[r]['stability'] for r in resolutions]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    axes[0].plot(resolutions, n_clusters_list, 'o-', color='#2196F3', linewidth=2, markersize=8)
    axes[0].set_xlabel('Resolution (gamma)', fontsize=11)
    axes[0].set_ylabel('Number of Clusters', fontsize=11)
    axes[0].set_title('Cluster Count vs. Resolution', fontweight='bold')
    axes[0].grid(alpha=0.3)
    
    axes[1].plot(resolutions, modularities, 's-', color='#4CAF50', linewidth=2, markersize=8)
    axes[1].set_xlabel('Resolution (gamma)', fontsize=11)
    axes[1].set_ylabel('Modularity Q', fontsize=11)
    axes[1].set_title('Modularity vs. Resolution', fontweight='bold')
    axes[1].grid(alpha=0.3)
    
    axes[2].plot(resolutions, stabilities, '^-', color='#FF5722', linewidth=2, markersize=8)
    axes[2].set_xlabel('Resolution (gamma)', fontsize=11)
    axes[2].set_ylabel('Partition Stability', fontsize=11)
    axes[2].set_title('Stability vs. Resolution\n(fraction of runs agreeing on k)', fontweight='bold')
    axes[2].set_ylim(0, 1.1)
    axes[2].grid(alpha=0.3)
    
    plt.suptitle('Multiscale Louvain Analysis (Markov Stability Approximation)', fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plot1_path = figures_dir / "dtw_multiscale_resolution.png"
    plt.savefig(plot1_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved multiscale resolution plot to {plot1_path}")
    
    # 2. RMST graph plot
    fig, ax = plt.subplots(figsize=(12, 9))
    G = pipeline.graph_
    node_list = list(G.nodes())
    pos = nx.spring_layout(G, seed=42, k=2/np.sqrt(len(G)))
    
    CLUSTER_COLORS = ['#2196F3', '#4CAF50', '#FF5722', '#9C27B0', '#FF9800', '#00BCD4', '#E91E63', '#795548']
    node_colors_cluster = [CLUSTER_COLORS[labels[n] % len(CLUSTER_COLORS)] for n in node_list]
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.12,
                           width=[w * 1.5 for w in edge_weights],
                           edge_color='#BBDEFB')
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors_cluster,
                           node_size=80, alpha=0.9)
    
    n_clusters = len(np.unique(labels))
    legend_patches = [mpatches.Patch(color=CLUSTER_COLORS[c % len(CLUSTER_COLORS)], label=f'Cluster {c}')
                      for c in range(n_clusters)]
    ax.legend(handles=legend_patches, loc='upper left', title='Cluster', fontsize=9)
    ax.set_title('Student Similarity Graph - Colored by DTW Cluster', fontweight='bold', fontsize=12)
    ax.axis('off')
    plt.tight_layout()
    plot2_path = figures_dir / "dtw_rmst_graph.png"
    plt.savefig(plot2_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved RMST graph plot to {plot2_path}")

if __name__ == "__main__":
    main()
