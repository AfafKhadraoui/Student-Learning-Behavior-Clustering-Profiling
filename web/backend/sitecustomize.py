"""Ensure the repository root is importable when running from web/backend.

This lets commands like `uvicorn web.backend.app.main:app` work even when the
current working directory is `web/backend`.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))