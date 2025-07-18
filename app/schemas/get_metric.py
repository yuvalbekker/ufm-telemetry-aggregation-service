from pydantic import BaseModel

# Properties to return to client
class GetMetric(BaseModel):
    service: str
    status: str
    version: str
