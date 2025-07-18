from typing import List
from pydantic import BaseModel
from datetime import datetime

class MetricValueResponse(BaseModel):
    switch_id: str
    value: float
    timestamp: datetime

class ListMetricsResponse(BaseModel):
    items: List[MetricValueResponse]
    total: int
    limit: int
    offset: int