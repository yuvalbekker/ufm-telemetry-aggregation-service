from typing import Any

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.error_responses import ERROR_RESPONSES
from app.schemas.get_metric import GetMetric

router = APIRouter()


@router.get("", response_model=GetMetric, responses=ERROR_RESPONSES)
def get_metric() -> Any:
    """
    health.
    """
    return {
        "service": settings.SERVICE_NAME,
        "status": settings.HEALTHY_STATUS,
        "version": settings.SERVICE_VERSION,
    }
