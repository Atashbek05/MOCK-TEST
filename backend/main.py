"""
main.py — Entry point for the ScamShield FastAPI application.

Responsibilities:
  - Creates and configures the FastAPI app instance
  - Registers API routers (added later as features are built)
  - Configures middleware (CORS, logging, etc.)
  - Starts the Uvicorn server when run directly
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from loguru import logger

# ─── App Instance ─────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered scam detection API",
    version=settings.APP_VERSION,
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc UI
)

# ─── CORS Middleware ──────────────────────────────────────────────────────────
# Allows the frontend (React/Next.js) to call this API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Startup / Shutdown Events ────────────────────────────────────────────────
@app.on_event("startup")
async def on_startup():
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    # Future: load AI models into memory here

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down ScamShield backend")
    # Future: release model resources here

# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    """Simple liveness probe — returns 200 if the server is running."""
    return {"status": "ok", "app": settings.APP_NAME}

# ─── Routers ──────────────────────────────────────────────────────────────────
# API routes will be registered here as they are implemented
# Example (uncomment when ready):
# from app.api.v1.routes import detection
# app.include_router(detection.router, prefix="/api/v1")


# ─── Dev Server ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
