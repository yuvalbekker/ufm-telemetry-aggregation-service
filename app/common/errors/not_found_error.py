from starlette import status
from app.common.errors.base_error import BaseError

class NotFoundError(BaseError):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, resource_name: str):
        self.message = f"Resource '{resource_name}' was not found."
