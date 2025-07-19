from typing import Any

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.error_responses import HEALTH_ERROR_RESPONSES
from app.schemas.health import Health

router = APIRouter()


@router.get("", response_model=Health, responses=HEALTH_ERROR_RESPONSES)
def health() -> Any:
    return {
        "service": settings.SERVICE_NAME,
        "status": settings.HEALTHY_STATUS,
        "version": settings.SERVICE_VERSION,
    }
