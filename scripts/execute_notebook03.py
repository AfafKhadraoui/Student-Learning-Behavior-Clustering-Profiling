"""
Execute notebooks/03_kmeans_clustering.ipynb headless and save outputs in-place.

Usage (from repo root):
    python scripts/execute_notebook03.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NB_PATH = ROOT / "notebooks" / "03_kmeans_clustering.ipynb"
NOTEBOOK_DIR = NB_PATH.parent

# Avoid sklearn KMeans memory warning on Windows/MKL
os.environ.setdefault("OMP_NUM_THREADS", "1")


def main() -> None:
    try:
        import nbformat
        from nbclient import NotebookClient
    except ImportError as exc:
        raise SystemExit(
            "nbformat and nbclient are required. pip install nbformat nbclient"
        ) from exc

    if not NB_PATH.is_file():
        raise SystemExit(f"Notebook not found: {NB_PATH}")

    print(f"Executing {NB_PATH.relative_to(ROOT)} (timeout 45 min per cell)...")
    nb = nbformat.read(NB_PATH, as_version=4)
    client = NotebookClient(
        nb,
        timeout=2700,
        kernel_name="python3",
        resources={"metadata": {"path": str(NOTEBOOK_DIR)}},
    )
    # Run with cwd = notebooks/ so Path('..') resolves to repo root
    orig_cwd = Path.cwd()
    os.chdir(NOTEBOOK_DIR)
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    try:
        client.execute()
    finally:
        os.chdir(orig_cwd)

    nbformat.write(nb, NB_PATH)
    fig_dir = ROOT / "reports" / "figures" / "clustering"
    n_figs = len(list(fig_dir.glob("*.png"))) if fig_dir.is_dir() else 0
    print(f"Done. Figures in reports/figures/clustering/: {n_figs} PNG files")


if __name__ == "__main__":
    main()
