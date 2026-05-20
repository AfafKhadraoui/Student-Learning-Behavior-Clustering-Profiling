"""
OULAD Student Clustering — reusable Python modules.

ENSIA Machine Learning Project · Spring 2025–2026
See README.md for full specification.
"""

__version__ = "0.1.0"

from pathlib import Path

# Repo root (parent of src/)
ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROC_DIR = ROOT / "data" / "processed"
MOD_DIR = ROOT / "models"
FIG_DIR = ROOT / "figures"
REPORT_DIR = ROOT / "reports"

RANDOM_STATE = 42
MODULE = "BBB"
PRES = "2013J"
