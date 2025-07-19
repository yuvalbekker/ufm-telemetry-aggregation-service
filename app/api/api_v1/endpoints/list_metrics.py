from fastapi import APIRouter, Query
from typing import Any, Optional
from app.schemas.error_responses import SINGLE_RESOURCE_ERROR_RESPONSES
from app.schemas.list_metrics import ListMetricsResponse
import app.db.utils as db_utils
from app.common.types.valid_metrics import MetricName
from app.common.errors.error_handling import db_error_handling
from app.db.session_handling import get_session
from fastapi import Depends

router = APIRouter()


@router.get(
    "/{metric_name}",
    response_model=ListMetricsResponse,
    responses=SINGLE_RESOURCE_ERROR_RESPONSES,
)
@db_error_handling
def list_metrics(
        metric_name: MetricName,
        limit: Optional[int] = Query(10, ge=1, le=100, description="Max results per page"),
        offset: Optional[int] = Query(0, ge=0, description="Number of items to skip"),
        session=Depends(get_session),
) -> Any:
    metrics, total = db_utils.fetch_metrics(session, metric_name, limit, offset)
    return ListMetricsResponse(items=metrics, total=total, limit=limit, offset=offset)
