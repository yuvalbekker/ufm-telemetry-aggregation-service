from typing import Any

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.error_responses import ERROR_RESPONSES
from app.schemas.list_metrics import ListMetrics

router = APIRouter()

@router.get("", response_model=ListMetrics, responses=ERROR_RESPONSES)
def list_metrics() -> Any:
    """
    health.
    """
    return {
        "service": settings.SERVICE_NAME,
        "status": settings.HEALTHY_STATUS,
        "version": settings.SERVICE_VERSION,
    }
