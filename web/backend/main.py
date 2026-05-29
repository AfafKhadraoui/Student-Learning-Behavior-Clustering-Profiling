"""ASGI entrypoint shim for local development.

This lets `uvicorn main:app --reload --port 8000` work when run from
`web/backend`.
"""

from app.main import app
