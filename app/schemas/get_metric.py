from pydantic import BaseModel
from datetime import datetime

class GetMetricResponse(BaseModel):
    switch_id: str
    metric_name: str
    value: float
    timestamp: datetime
