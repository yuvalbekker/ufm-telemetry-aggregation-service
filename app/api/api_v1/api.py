from fastapi import APIRouter

from app.api.api_v1.endpoints import (health, get_metric, list_metrics)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(get_metric.router, prefix="/GetMetric", tags=["get_metric"])
api_router.include_router(list_metrics.router, prefix="/ListMetrics", tags=["list_metrics"])
