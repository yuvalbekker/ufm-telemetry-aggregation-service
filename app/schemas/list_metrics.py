from pydantic import BaseModel

# Properties to return to client
class ListMetrics(BaseModel):
    service: str
    status: str
    version: str
