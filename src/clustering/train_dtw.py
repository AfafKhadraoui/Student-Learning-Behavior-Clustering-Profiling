"""
DTW and Graph-based Clustering Pipeline (Peach et al. 2019).
"""

from __future__ import annotations

import numpy as np
import networkx as nx
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.sparse import csr_matrix
from dtaidistance import dtw


try:
    import community as community_louvain  # provided by python-louvain
except ImportError as exc:
    raise ImportError(
        "Missing Louvain dependency. Install with: pip install python-louvain"
    ) from exc

if not hasattr(community_louvain, "best_partition"):
    raise ImportError(
        "Detected the wrong 'community' package. Uninstall it and install python-louvain:\n"
        "  pip uninstall -y community\n"
        "  pip install python-louvain"
    )


class DTWClusteringPipeline:
    """
    Encapsulates the DTW -> RMST -> Louvain clustering pipeline.
    """
    
    def __init__(
        self, 
        sigma_quantile: float = 0.5, 
        relaxation: float = 1.0, 
        resolutions: list[float] | None = None,
        n_runs: int = 50,
        random_state: int = 42
    ):
        self.sigma_quantile = sigma_quantile
        self.relaxation = relaxation
        self.resolutions = resolutions if resolutions is not None else [0.3, 0.5, 0.7, 1.0, 1.3, 1.6, 2.0]
        self.n_runs = n_runs
        self.random_state = random_state
        
        self.similarity_matrix_ = None
        self.graph_ = None
        self.multiscale_results_ = None
        self.best_resolution_ = None
        self.labels_ = None
        self.input_matrices_ = None
        self.input_weights_ = None
        
    def _compute_dtw_similarity_matrix(self, X_list: list[np.ndarray], weights: list[float]) -> tuple[np.ndarray, np.ndarray, float]:
        if len(X_list) == 0:
            raise ValueError("X_list must contain at least one input matrix.")
        if len(X_list) != len(weights):
            raise ValueError("X_list and weights must have the same length.")

        X_list = [np.ascontiguousarray(X, dtype=np.float64) for X in X_list]
        N = len(X_list[0])
        if any(len(X) != N for X in X_list):
            raise ValueError("All input matrices must have the same number of students in the same row order.")

        for idx, X in enumerate(X_list):
            print(f"Input {idx + 1}: {N} students x {X.shape[1]} features (weight={weights[idx]:.2f})")

        print(f"Computing weighted DTW distances for {N} students across {len(X_list)} temporal signals...")
        
        dtw_distances = np.zeros((N, N), dtype=np.float64)
        for i in range(N):
            for j in range(i + 1, N):
                d_combined = 0.0
                for X, w in zip(X_list, weights):
                    d = dtw.distance_fast(X[i], X[j])
                    if not np.isfinite(d):
                        d = float(np.sqrt(np.sum((X[i] - X[j]) ** 2)))
                    d_combined += w * d

                dtw_distances[i, j] = d_combined
                dtw_distances[j, i] = d_combined
            
            if i % 50 == 0:
                print(f"  Progress: {i}/{N} ({100*i/N:.0f}%)")
        print(f"  Progress: {N}/{N} (100%)")
        upper_tri = dtw_distances[np.triu_indices(N, k=1)]
        sigma2 = np.quantile(upper_tri, self.sigma_quantile) ** 2
        if sigma2 == 0:
            sigma2 = 1e-6
            
        print("\nDTW distance stats:")
        print(f"  min={upper_tri.min():.4f}, median={np.median(upper_tri):.4f}, max={upper_tri.max():.4f}")
        print(f"  sigma^2 = {sigma2:.4f}")
        
        similarity_matrix = np.exp(-dtw_distances / sigma2)
        np.fill_diagonal(similarity_matrix, 1.0)
        
        return similarity_matrix, dtw_distances, sigma2
        
    def _build_rmst_graph(self, similarity_matrix: np.ndarray) -> nx.Graph:
        N = similarity_matrix.shape[0]
        
        neg_sim = -similarity_matrix.copy()
        np.fill_diagonal(neg_sim, 0)
        mst = minimum_spanning_tree(csr_matrix(neg_sim)).toarray()
        mst_sym = (mst + mst.T) != 0
        
        G = nx.Graph()
        G.add_nodes_from(range(N))
        
        for i, j in zip(*np.where(mst_sym)):
            if i < j:
                G.add_edge(i, j, weight=similarity_matrix[i, j])
                
        mst_weights = [d['weight'] for _, _, d in G.edges(data=True)]
        threshold = self.relaxation * np.median(mst_weights) if mst_weights else 0.5
        
        for i in range(N):
            for j in range(i + 1, N):
                if not G.has_edge(i, j) and similarity_matrix[i, j] > threshold:
                    G.add_edge(i, j, weight=similarity_matrix[i, j])
                    
        print("Graph built:")
        print(f"  Nodes: {G.number_of_nodes()}")
        print(f"  Edges: {G.number_of_edges()} (from {N*(N-1)//2} total possible)")
        print(f"  Sparsity: {G.number_of_edges() / (N*(N-1)//2) * 100:.1f}% of edges retained")
        print(f"  Connected: {nx.is_connected(G)}")
        
        return G
        
    def _run_louvain_multiscale(self, G: nx.Graph) -> dict:
        results = {}
        node_list = list(G.nodes())
        
        print(f"Running Louvain at {len(self.resolutions)} resolution levels ({self.n_runs} runs each)...")
        print(f"{'Resolution':>12} | {'# Clusters':>12} | {'Modularity':>12} | {'Stability':>12}")
        print("-" * 55)
        
        for res in self.resolutions:
            partitions = []
            modularities = []
            
            for seed in range(self.n_runs):
                partition = community_louvain.best_partition(
                    G, resolution=res, weight='weight', random_state=self.random_state + seed
                )
                labels = np.array([partition[n] for n in node_list])
                mod = community_louvain.modularity(partition, G, weight='weight')
                partitions.append(labels)
                modularities.append(mod)
                
            best_labels = partitions[np.argmax(modularities)]
            n_clusters = len(np.unique(best_labels))
            
            unique_labels = np.unique(best_labels)
            remap = {old: new for new, old in enumerate(unique_labels)}
            best_labels = np.array([remap[l] for l in best_labels])
            
            cluster_counts = [len(np.unique(p)) for p in partitions]
            stability = cluster_counts.count(n_clusters) / self.n_runs
            
            results[res] = {
                'labels': best_labels,
                'n_clusters': n_clusters,
                'modularity': np.max(modularities),
                'stability': stability,
            }
            print(f"{res:>12.1f} | {n_clusters:>12d} | {np.max(modularities):>12.4f} | {stability:>11.0%}")
            
        return results

    def fit_predict(self, X_list: list[np.ndarray], weights: list[float]) -> np.ndarray:
        """
        Run the full DTW clustering pipeline on the input feature matrix X.
        
        Returns:
            np.ndarray: Cluster labels for each sample in X.
        """
        self.input_matrices_ = X_list
        self.input_weights_ = weights
        self.similarity_matrix_, _, _ = self._compute_dtw_similarity_matrix(X_list, weights)
        self.graph_ = self._build_rmst_graph(self.similarity_matrix_)
        self.multiscale_results_ = self._run_louvain_multiscale(self.graph_)
        
        # Select the best resolution using the weighted stability/modularity score.
        self.best_resolution_ = max(
            self.multiscale_results_,
            key=lambda r: (
                self.multiscale_results_[r]['stability'] * 0.6 +
                self.multiscale_results_[r]['modularity'] * 0.4
            ) if 2 <= self.multiscale_results_[r]['n_clusters'] <= 12 else -1
        )
            
        self.labels_ = self.multiscale_results_[self.best_resolution_]['labels']
        print(f"\nSelected optimal resolution: {self.best_resolution_} with {self.multiscale_results_[self.best_resolution_]['n_clusters']} clusters.")
        
        return self.labels_
