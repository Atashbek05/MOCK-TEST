"""
config.py — Centralized application configuration.

Loads all environment variables from .env and exposes them
as typed settings via Pydantic BaseSettings.
All other modules import from here — never read os.environ directly.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # ── Application ────────────────────────────────────────────────────────
    APP_NAME: str = "ScamShield"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # ── Server ─────────────────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── CORS ───────────────────────────────────────────────────────────────
    # Comma-separated list in .env: ALLOWED_ORIGINS=http://localhost:3000,...
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # ── AI Model ───────────────────────────────────────────────────────────
    MODEL_DIR: str = "app/models/weights"       # Where trained weights are stored
    DEFAULT_MODEL: str = "scam_classifier_v1"   # Model to load on startup

    # ── Database (future) ──────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./scamshield.db"  # Switch to PostgreSQL in prod

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton — import this everywhere
settings = Settings()
