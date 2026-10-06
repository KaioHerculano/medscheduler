from typing import Dict

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=Dict[str, str])
async def check_health() -> Dict[str, str]:
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
    }
