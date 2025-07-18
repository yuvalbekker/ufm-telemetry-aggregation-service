from fastapi import APIRouter

from counters.api.api_v1.endpoints import (health, counters)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(counters.router, prefix="/counters", tags=["counters"])
