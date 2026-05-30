"""Execute notebooks/07_model_comparison.ipynb headless."""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "07_model_comparison.ipynb"
OUTPUT = ROOT / "notebooks" / "07_model_comparison_executed.ipynb"


def main() -> None:
    import matplotlib

    matplotlib.use("Agg")

    sys.path.insert(0, str(ROOT))
    from nbclient import NotebookClient
    from nbformat import read, write

    if not NOTEBOOK.exists():
        raise FileNotFoundError(NOTEBOOK)

    print(f"Executing {NOTEBOOK.relative_to(ROOT)} ...")
    nb = read(NOTEBOOK, as_version=4)
    client = NotebookClient(
        nb,
        timeout=3600,
        kernel_name="python3",
        resources={"metadata": {"path": str(ROOT / "notebooks")}},
    )
    client.execute()
    write(nb, OUTPUT)
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")

    comparisons = ROOT / "figures" / "comparisons"
    expected = [
        "at_risk_concentration_all_methods.png",
        "at_risk_precision_recall_scatter.png",
        "bootstrap_stability_boxplots.png",
        "cluster_purity_all_methods.png",
        "cluster_sizes_all_methods.png",
        "cross_method_ari.png",
        "external_metrics_grouped_bar.png",
        "gmm_posterior_histogram.png",
        "metric_heatmap.png",
        "outcome_heatmap_all_methods.png",
        "pca_all_methods.png",
        "radar_comparison.png",
        "tsne_all_methods.png",
    ]
    missing = [f for f in expected if not (comparisons / f).exists()]
    csv_path = ROOT / "reports" / "results" / "model_comparison_summary.csv"
    if missing:
        print("MISSING figures:", missing)
        sys.exit(1)
    if not csv_path.exists():
        print("MISSING", csv_path)
        sys.exit(1)
    print("All expected outputs present.")


if __name__ == "__main__":
    main()
