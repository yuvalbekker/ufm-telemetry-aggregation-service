from typing import Any

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.error_responses import SINGLE_RESOURCE_ERROR_RESPONSES
from app.schemas.get_metric import GetMetricResponse
import app.db.utils as db_utils

router = APIRouter()

@router.get(
    "/{metric_name}/{switch_id}",
    response_model=GetMetricResponse,
    responses=SINGLE_RESOURCE_ERROR_RESPONSES,
)
def get_metric(
        metric_name: str,
        switch_id: str) -> Any:
    """
    Retrieve a metric value for a specific switch.
    """
    engine = db_utils.get_engine(settings.DB_URL)
    SessionLocal = db_utils.get_session_maker(engine)
    db_utils.ensure_tables(engine)
    with SessionLocal() as session:
        value, timestamp = db_utils.fetch_metric_value(session, switch_id, metric_name)
        return GetMetricResponse(
            switch_id=switch_id,
            metric_name=metric_name,
            value=value,
            timestamp=timestamp
        )
