# Web Dashboard

This folder contains the optional dashboard for the student clustering project.

## Structure

```text
web/
├── backend/   # FastAPI service that reads saved models and processed tables
└── frontend/  # Vite + React UI for cluster views and student lookup
```

## Data flow

1. The notebooks and `src/` modules generate `data/processed/` and `models/` artifacts.
2. The backend loads those artifacts and exposes cluster and student endpoints.
3. The frontend consumes the API and renders charts, summaries, and lookup views.

## Backend

The backend uses FastAPI and Uvicorn. Its dependencies are listed in `web/backend/requirements.txt`.

Typical run commands from the repository root:

```bash
cd web/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Frontend

The frontend uses React, TypeScript, and Vite.

```bash
cd web/frontend
npm install
npm run dev
```

## Intended scope

The dashboard is a view layer over the pipeline output. It should not rebuild the clustering workflow or re-run the notebooks.
