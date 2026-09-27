"""
FastAPI Application Entry Point
Configures CORS, middleware, and registers API routers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Academic Mental Wellness Assessment System based on Indian Psychology (IKS)",
    version=settings.PROJECT_VERSION,
)

# Configure Cross-Origin Resource Sharing (CORS) for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router under the configured prefix
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    """
    Root landing endpoint directing to documentation and health check.
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health",
        "disclaimer": settings.DISCLAIMER_TEXT,
    }
