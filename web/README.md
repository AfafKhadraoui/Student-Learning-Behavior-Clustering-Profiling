# Web Application — OULAD Cluster Dashboard

Optional deliverable for demo day: visualize clusters and at-risk students without re-running notebooks.

## Layout

```
web/
├── backend/     # Python API — loads models/*.pkl + processed CSVs
└── frontend/    # React/Vue/static UI — calls the API
```

## Data flow

1. **Notebooks + `src/`** train models and write `data/processed/master_with_clusters.csv`
2. **`models/scaler.pkl`** + **`models/kmeans.pkl`** (or chosen primary model) are loaded by the API
3. **Frontend** requests cluster stats, PCA scatter data, and at-risk list via REST

## Suggested stack

| Layer | Technology | Why |
|-------|------------|-----|
| Backend | FastAPI + uvicorn | Lightweight, auto OpenAPI docs, easy `src/` imports |
| Frontend | React + Vite (or Streamlit for faster MVP) | Interactive charts for jury demo |

## Development

```bash
# Backend (from repo root)
cd web/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd web/frontend
npm install
npm run dev
```

## API endpoints (planned)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Service status |
| GET | `/clusters/summary` | Cluster sizes and labels |
| GET | `/clusters/{id_student}` | Cluster + risk for one student |
| GET | `/visualization/pca` | PC1/PC2 points for scatter plot |
| GET | `/at-risk` | List of flagged students |

Implement handlers in `web/backend/app/main.py` using artifacts from `models/` and `data/processed/`.
