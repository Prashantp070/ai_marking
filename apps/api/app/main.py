"""FastAPI application entrypoint."""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, auth, batch, feedback, process, results, uploads
from app.api.routes import submissions
from app.api.routes.health import router as health_router
from app.core.config import settings
from app.core.database import init_db


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="AI Handwritten Answer Evaluation Platform API",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=3600,
    )

    app.include_router(health_router, tags=["health"])
    app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
    app.include_router(uploads.router, prefix=settings.API_V1_STR, tags=["uploads"])
    app.include_router(submissions.router, prefix=settings.API_V1_STR, tags=["submissions"])
    app.include_router(process.router, prefix=settings.API_V1_STR, tags=["process"])
    app.include_router(results.router, prefix=settings.API_V1_STR, tags=["results"])
    app.include_router(feedback.router, prefix=settings.API_V1_STR, tags=["feedback"])
    app.include_router(analytics.router, prefix=settings.API_V1_STR, tags=["analytics"])
    app.include_router(batch.router, prefix=settings.API_V1_STR, tags=["batch"])

    @app.on_event("startup")
    async def startup_event() -> None:
        await init_db()

    return app


app = create_app()



