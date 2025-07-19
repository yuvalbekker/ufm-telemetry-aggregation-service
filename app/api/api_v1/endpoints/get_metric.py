from typing import Any
from fastapi import APIRouter

from app.schemas.error_responses import SINGLE_RESOURCE_ERROR_RESPONSES
from app.schemas.get_metric import GetMetricResponse
import app.db.utils as db_utils
from app.common.types.valid_metrics import MetricName
from app.common.errors.error_handling import db_error_handling
from app.db.session_handling import get_session
from fastapi import Depends

router = APIRouter()


@router.get(
    "/{metric_name}/{switch_id}",
    response_model=GetMetricResponse,
    responses=SINGLE_RESOURCE_ERROR_RESPONSES,
)
@db_error_handling
def get_metric(
        metric_name: MetricName,
        switch_id: str,
        session=Depends(get_session),
) -> Any:
    value, timestamp = db_utils.fetch_metric_value(session, switch_id, metric_name)
    return GetMetricResponse(
        switch_id=switch_id,
        metric_name=metric_name,
        value=value,
        timestamp=timestamp
    )
