"""Analytics endpoints."""

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.core.database import async_session_factory
from app.schemas.analytics import AnalyticsOverview
from app.services.analytics_service import AnalyticsService


router = APIRouter()


@router.get("/overview", response_model=AnalyticsOverview, summary="Get analytics overview")
async def analytics_overview(current_user: dict = Depends(get_current_user)) -> dict:
    async with async_session_factory() as session:
        service = AnalyticsService(session)
        return await service.get_overview()

