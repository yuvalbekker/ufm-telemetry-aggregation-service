from pydantic import BaseModel

# Properties to return to client
class Health(BaseModel):
    service: str
    status: str
    version: str
