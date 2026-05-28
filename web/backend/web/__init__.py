"""Import shim so `web.backend...` works when the cwd is `web/backend`.

When Python starts from `web/backend`, the repository root is not on `sys.path`,
so the real top-level `web` package is not discoverable. This shim redirects the
package search path to the repository's actual `web/` directory.
"""

from __future__ import annotations

from pathlib import Path


_repo_web = Path(__file__).resolve().parents[3] / "web"
__path__ = [str(_repo_web)]