from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class SwitchMetric(BaseModel):
    switch_id: str = Field()
    bandwidth_usage: float = Field()
    latency: float = Field()
    packet_errors: int = Field()
    collection_time: datetime = Field()
    timestamp: Optional[datetime] = Field(default=None)

class SwitchMetrics(BaseModel):
    items: Optional[List[SwitchMetric]] = Field(
        default=None,
        description="A list of switch metric events."
    )
