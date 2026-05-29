"""
Central configuration — all paths and toggles in one place.
"""
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── Paths ────────────────────────────────────────────────────────────────
    # Adjust ROOT to point at your project root (the folder that contains
    # data/, models/, notebooks/, etc.)
    ROOT: Path = Path(__file__).resolve().parents[4]

    @property
    def PROCESSED_DIR(self) -> Path:
        return self.ROOT / "data" / "processed"

    @property
    def RAW_DIR(self) -> Path:
        return self.ROOT / "data" / "raw"

    @property
    def MODELS_DIR(self) -> Path:
        return self.ROOT / "models"

    @property
    def RESULTS_DIR(self) -> Path:
        return self.ROOT / "reports" / "results"

    # ── CORS ─────────────────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",   # CRA / Next dev server
        "http://localhost:4173",   # Vite preview
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()