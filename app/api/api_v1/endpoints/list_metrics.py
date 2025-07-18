from fastapi import APIRouter, Query
from typing import Any, Optional
from app.schemas.error_responses import SINGLE_RESOURCE_ERROR_RESPONSES
from app.schemas.list_metrics import ListMetricsResponse
import app.db.utils as db_utils
from app.core.config import settings

router = APIRouter()

@router.get(
    "/{metric_name}",
    response_model=ListMetricsResponse,
    responses=SINGLE_RESOURCE_ERROR_RESPONSES,
)
def list_metrics(
    metric_name: str,
    limit: Optional[int] = Query(10, ge=1, le=100, description="Max results per page"),
    offset: Optional[int] = Query(0, ge=0, description="Number of items to skip"),
) -> Any:
    """
    List latest metric values for all switches (paginated).
    """
    engine = db_utils.get_engine(settings.DB_URL)
    SessionLocal = db_utils.get_session_maker(engine)
    db_utils.ensure_tables(engine)
    with SessionLocal() as session:
        metrics, total = db_utils.fetch_metrics(session, metric_name, limit, offset)
        return ListMetricsResponse(items=metrics, total=total, limit=limit, offset=offset)